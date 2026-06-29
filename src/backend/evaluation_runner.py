"""
Entry point for the golden question evaluation runner.

Usage:
    make eval                                          # fast mode, print summary
    make eval MODE=full OUTPUT=report.json             # full mode, save JSON report
    make eval LIMIT=10                                 # only first 10 positive questions
    make mlflow-ui                                     # open MLflow UI
    poetry run python -m backend.evaluation_runner --mode fast
    poetry run python -m backend.evaluation_runner --mode fast --limit 10
    poetry run python -m backend.evaluation_runner --mode full --output report.json

Modes:
    fast (default)  Stages 1-5 only. No database required.
                    Checks intent classification, view selection, SQL generation,
                    and SQL validation against golden questions.

    full            All 7 stages. Requires live Azure SQL and Azure OpenAI credentials.
                    Adds database execution and answer quality checks on top of fast mode.

Exit code: 0 if pass rate >= 80%, 1 otherwise.
"""
import argparse
import asyncio
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path

import mlflow

from backend.app.evaluation.golden_runner import GoldenRunner, _GOLDEN_QUESTIONS_PATH
from backend.app.prompts.intent import PROMPT_VERSION as INTENT_VERSION
from backend.app.prompts.sql_generation import PROMPT_VERSION as SQL_GEN_VERSION
from backend.app.prompts.answer_generation import PROMPT_VERSION as ANSWER_GEN_VERSION

MLFLOW_EXPERIMENT = "talk-to-data-eval"
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"


def _golden_questions_hash() -> str:
    content = _GOLDEN_QUESTIONS_PATH.read_bytes()
    return hashlib.md5(content).hexdigest()[:8]


def _extract_model_names(report) -> dict[str, str]:
    """Return per-stage model name from the first record that has each stage populated."""
    stage_models: dict[str, str] = {}
    for r in report.records:
        if not r.trace:
            continue
        for stage, usage in r.trace.token_usage.items():
            if stage not in stage_models and usage.get("model_name"):
                stage_models[stage] = usage["model_name"]
        if len(stage_models) >= 4:
            break
    return stage_models


def _aggregate_token_usage(report) -> dict[str, dict[str, int]]:
    """Sum token usage across all records, broken down by stage."""
    stage_totals: dict[str, dict[str, int]] = {}
    for r in report.records:
        if not r.trace:
            continue
        for stage, counts in r.trace.token_usage.items():
            if stage not in stage_totals:
                stage_totals[stage] = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
            for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
                stage_totals[stage][k] += counts.get(k, 0)
    return stage_totals


def _log_to_mlflow(report, mode: str, commit: str, eval_run: str, duration_s: float) -> None:
    from backend.app.core.config import settings
    from backend.app.prompts.intent import build_intent_prompt
    from backend.app.prompts.sql_generation import build_sql_generation_prompt

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT)
    with mlflow.start_run(run_name=f"{eval_run}-{mode}-{commit[:8]}"):
        stage_models = _extract_model_names(report)
        mlflow.log_params({
            "mode": mode,
            "git_commit": commit[:8],
            "intent_version": INTENT_VERSION,
            "sql_gen_version": SQL_GEN_VERSION,
            "answer_gen_version": ANSWER_GEN_VERSION,
            "golden_questions_hash": _golden_questions_hash(),
            "eval_run": eval_run,
            "model_intent": stage_models.get("intent", "unknown"),
            "model_view_selection": stage_models.get("view_selection", "unknown"),
            "model_sql_gen": stage_models.get("sql_generation", "unknown"),
            "model_answer": stage_models.get("answer_generation", "unknown"),
            # Pipeline tuning parameters — logged so each eval run is fully reproducible
            "max_history_turns": settings.max_history_turns,
            "max_history_answer_chars": settings.max_history_answer_chars,
            "max_sql_retries": settings.max_sql_retries,
            "max_tokens_per_request": settings.max_tokens_per_request,
            "pipeline_timeout_s": settings.pipeline_timeout_seconds,
        })

        # Aggregate token usage across all records
        stage_totals = _aggregate_token_usage(report)
        total_tokens = sum(s.get("total_tokens", 0) for s in stage_totals.values())
        total_prompt = sum(s.get("prompt_tokens", 0) for s in stage_totals.values())
        total_completion = sum(s.get("completion_tokens", 0) for s in stage_totals.values())
        questions_with_usage = sum(
            1 for r in report.records if r.trace and r.trace.token_usage
        )

        token_metrics: dict[str, float] = {
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "total_tokens": total_tokens,
            "avg_tokens_per_question": round(total_tokens / questions_with_usage, 1) if questions_with_usage else 0,
        }
        for stage, counts in stage_totals.items():
            token_metrics[f"prompt_tokens_{stage}"] = counts.get("prompt_tokens", 0)
            token_metrics[f"completion_tokens_{stage}"] = counts.get("completion_tokens", 0)

        questions_with_retries = sum(
            1 for r in report.records if r.trace and r.trace.sql_retries > 0
        )
        total_sql_retries = sum(
            r.trace.sql_retries for r in report.records if r.trace
        )
        access_pass_rate = (
            round(report.access_tests_passed / report.access_tests_total, 4)
            if report.access_tests_total else 0.0
        )
        conversation_pass_rate = (
            round(report.conversation_tests_passed / report.conversation_tests_total, 4)
            if report.conversation_tests_total else 0.0
        )
        mlflow.log_metrics({
            "pass_rate": round(report.pass_rate, 4),
            "passed": report.passed,
            "partial": report.partial,
            "failed": report.failed,
            "total": report.total,
            "partial_rate": round(report.partial / report.total, 4) if report.total else 0,
            "eval_duration_s": round(duration_s, 1),
            "questions_with_sql_retries": questions_with_retries,
            "total_sql_retries": total_sql_retries,
            "access_tests_passed": report.access_tests_passed,
            "access_tests_total": report.access_tests_total,
            "access_tests_pass_rate": access_pass_rate,
            "conversation_tests_passed": report.conversation_tests_passed,
            "conversation_tests_total": report.conversation_tests_total,
            "conversation_tests_pass_rate": conversation_pass_rate,
            **token_metrics,
        })

        # Per-question trace: full details for every question
        traces = []
        for r in report.records:
            stage_usage = r.trace.token_usage if r.trace else {}
            q_total = {
                "prompt_tokens": sum(v.get("prompt_tokens", 0) for v in stage_usage.values()),
                "completion_tokens": sum(v.get("completion_tokens", 0) for v in stage_usage.values()),
                "total_tokens": sum(v.get("total_tokens", 0) for v in stage_usage.values()),
            }
            traces.append({
                "question": r.question,
                "case_type": r.case_type,
                "status": r.status,
                "expected_view": r.expected_view,
                "generated_sql": r.generated_sql,
                "expected_sql": r.expected_sql,
                "view_match": r.view_match,
                "validation_pass": r.validation_pass,
                "metric_present": r.metric_present,
                "execution_status": r.execution_status,
                "failure_reasons": r.failure_reasons,
                "latency_ms": r.latency_ms,
                "trace_id": r.trace.trace_id if r.trace else None,
                "sql_retries": r.trace.sql_retries if r.trace else 0,
                "token_usage": {**stage_usage, "total": q_total},
            })
        mlflow.log_text(json.dumps(traces, indent=2, default=str), "traces.json")

        # Prompt system messages — static per version, useful for diffing across runs
        from backend.app.prompts.answer_generation import build_answer_generation_prompt
        intent_system = build_intent_prompt("__placeholder__")[0]["content"]
        sql_gen_system = build_sql_generation_prompt("__placeholder__", "__views__")[0]["content"]
        answer_system = build_answer_generation_prompt("__placeholder__", "__sql__", [], [])[0]["content"]
        mlflow.log_text(intent_system, "prompts/intent_system.txt")
        mlflow.log_text(sql_gen_system, "prompts/sql_gen_system.txt")
        mlflow.log_text(answer_system, "prompts/answer_system.txt")


async def _run(mode: str, output: Path | None, limit: int | None, eval_run: str, concurrency: int) -> int:
    t0 = time.monotonic()
    runner = GoldenRunner()
    report = await runner.run_all(mode=mode, limit=limit, concurrency=concurrency)
    duration_s = time.monotonic() - t0
    report.print_summary()

    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL
        ).decode().strip()
    except Exception:
        commit = "unknown"

    if output:
        data = {"git_commit": commit, "eval_run": eval_run, **report.to_dict()}
        output.write_text(json.dumps(data, indent=2, default=str))
        print(f"\nReport written to {output} (commit {commit[:8]})")

    _log_to_mlflow(report, mode, commit, eval_run, duration_s)
    print(f"MLflow run logged to experiment '{MLFLOW_EXPERIMENT}' — run: mlflow ui")

    return 0 if report.pass_rate >= 0.8 else 1


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run golden question evaluation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--mode",
        choices=["fast", "full"],
        default="fast",
        help="fast: stages 1-5, no DB (default); full: all 7 stages with DB and LLM",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        metavar="FILE",
        help="Write JSON report to FILE",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        metavar="N",
        help="Run only the first N positive questions (useful when rate-limited)",
    )
    parser.add_argument(
        "--eval-run",
        default="",
        metavar="LABEL",
        help="Short label for this run logged to MLflow (e.g. v12, post-prompt-fix)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        metavar="N",
        help="Number of questions to evaluate in parallel (default 5; use 3-5 for full mode to avoid DB contention)",
    )
    args = parser.parse_args()
    sys.exit(asyncio.run(_run(args.mode, args.output, args.limit, args.eval_run, args.concurrency)))


if __name__ == "__main__":
    main()
