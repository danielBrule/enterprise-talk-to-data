"""
Golden-question evaluation runner.

Fast mode (default): runs stages 1-5 (intent → view selection → metadata →
SQL generation → SQL validation) for every golden question. No database
execution required. Produces a full TraceRecord per question.

Reuses the same Stage implementations as TalkToDataPipeline. The runner
diverges only in how it handles stage failures: intent refusal stops evaluation
for that question (a positive question must be answerable), but failures in
later stages are recorded as eval failures and execution continues so all
checks can be accumulated.

Checks per positive question:
  - intent classified as answerable
  - expected view appears in selected_views
  - expected view referenced in generated SQL
  - required metric / measure columns present in generated SQL
  - required GROUP BY columns present when expected SQL has GROUP BY
  - required filter / date terms present when expected SQL has WHERE
  - SQL validation passes

Negative cases:
  - Out-of-scope questions must be refused (intent not answerable)
  - Synthetic unsafe SQL patterns must fail validate_query
"""

import asyncio
import re
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from ..core.auth import ResolvedUser
from ..core.logger import logger
from ..core.sql_safety import SQLSafetyError, validate_query
from ..models.pipeline_context import PipelineContext
from ..models.trace import TraceRecord, ValidationResult
from ..stages.intent import IntentService, IntentStage
from ..stages.view_selection import ViewSelectionService, ViewSelectionStage
from ..stages.metadata import MetadataStage
from ..stages.sql_generation import SQLGenerationService, SQLGenerationStage
from ..stages.sql_validation import SQLValidationStage
from ..stages.execution import ExecutionStage
from ..stages.answer import AnswerService, AnswerStage
from ..stages.base import build_latency, Refusal

_GOLDEN_QUESTIONS_PATH = (
    Path(__file__).resolve().parents[3] / "metadata" / "example_questions" / "golden_questions.yml"
)

# Questions that must be refused — not answerable from the approved views
NEGATIVE_QUESTIONS = [
    {
        "question": "What will article engagement look like next quarter?",
        "expect": "refused",
        "reason": "Requires forecasting — not supported",
    },
    {
        "question": "Why do some articles generate more comments than others?",
        "expect": "refused",
        "reason": "Requires causal explanation — not supported",
    },
    {
        "question": "Show me the stock price for articles published today",
        "expect": "refused",
        "reason": "Requires external financial data — not in approved views",
    },
]

# SQL patterns that must fail validate_query — confirms the validator blocks them
NEGATIVE_SQL_PATTERNS = [
    ("INSERT INTO analytics.vw_article_engagement VALUES (1)", "INSERT not allowed"),
    ("DROP TABLE analytics.vw_article_engagement", "DDL not allowed"),
    ("SELECT * FROM dbo.core_articles", "Raw dbo.* table access not allowed"),
    ("SELECT * FROM analytics.vw_article_engagement", "Missing TOP/LIMIT clause"),
    ("UPDATE analytics.vw_article_engagement SET comment_count = 0", "DML not allowed"),
    ("SELECT TOP 501 * FROM analytics.vw_article_engagement", "Exceeds row limit"),
    (
        "SELECT TOP 10 article_id FROM analytics.vw_article_engagement; SELECT TOP 5 keyword_id FROM analytics.vw_keyword_engagement",
        "Multi-statement query not allowed",
    ),
]

# Access enforcement test cases — SQL + role pairs verified against ExecutionStage.
# No LLM or DB required: denied cases are blocked before the DB call; allowed cases
# confirm access enforcement did not fire (DB errors are treated as "not denied").
ACCESS_TEST_CASES = [
    {
        "description": "Editor denied: analytics.vw_ingestion_errors not in editor's allowed_views",
        "sql": "SELECT TOP 10 stage, error_type, error_count FROM analytics.vw_ingestion_errors ORDER BY error_count DESC",
        "role": "editor",
        "allowed_views": ["analytics.vw_article_engagement", "analytics.vw_top_contributors"],
        "expect": "denied",
    },
    {
        "description": "Editor denied: analytics.vw_keyword_engagement not in editor's allowed_views",
        "sql": "SELECT TOP 10 full_keyword, article_count FROM analytics.vw_keyword_engagement ORDER BY article_count DESC",
        "role": "editor",
        "allowed_views": ["analytics.vw_article_engagement", "analytics.vw_top_contributors"],
        "expect": "denied",
    },
    {
        "description": "Analyst allowed: analytics.vw_ingestion_errors is in analyst's allowed_views",
        "sql": "SELECT TOP 10 stage, error_type, error_count FROM analytics.vw_ingestion_errors ORDER BY error_count DESC",
        "role": "analyst",
        "allowed_views": [
            "analytics.vw_article_engagement",
            "analytics.vw_keyword_engagement",
            "analytics.vw_top_contributors",
            "analytics.vw_ingestion_errors",
        ],
        "expect": "allowed",
    },
    {
        "description": "Editor allowed: analytics.vw_article_engagement is in editor's allowed_views",
        "sql": "SELECT TOP 10 article_id, title, comment_count FROM analytics.vw_article_engagement ORDER BY comment_count DESC",
        "role": "editor",
        "allowed_views": ["analytics.vw_article_engagement", "analytics.vw_top_contributors"],
        "expect": "allowed",
    },
]


@dataclass
class GoldenEvalRecord:
    question: str
    expected_view: str
    expected_sql: str
    expected_expressions: list[str] = field(default_factory=list)
    case_type: str = "positive"  # "positive" | "negative_question" | "negative_sql" | "access" | "conversation" | "system_info"

    # Per-check results (None = not applicable)
    intent_answerable: bool | None = None
    view_match: bool | None = None
    view_in_sql: bool | None = None
    metric_present: bool | None = None
    grouping_present: bool | None = None
    filter_present: bool | None = None
    validation_pass: bool | None = None

    # Outcome
    status: str = "pending"  # "pass" | "partial" | "fail" | "error"
    failure_reasons: list[str] = field(default_factory=list)
    # Primary failure category for failing/partial records: semantic | retrieval | sql | access | answer | other
    failure_category: str | None = None

    # Artefacts
    generated_sql: str | None = None
    execution_status: str | None = None  # "success" | "failed" | "skipped" (full mode only)
    answer: str | None = None
    answer_quality_pass: bool | None = None
    trace: TraceRecord | None = None
    latency_ms: float | None = None


_FAILURE_CATEGORIES = ("semantic", "retrieval", "sql", "access", "answer", "other")


def _categorize_failure(record: GoldenEvalRecord) -> str | None:
    """Return the primary failure category for a failing/partial record.

    Priority order mirrors pipeline stage order: semantic (intent) → retrieval
    (view selection) → sql (generation/validation) → access → answer.
    """
    if record.status not in ("fail", "partial"):
        return None

    # semantic — intent classified the question wrong
    if record.intent_answerable is False:
        return "semantic"
    if record.case_type == "system_info" and record.status in ("fail", "partial"):
        return "semantic"
    # negative question not refused → semantic misclassification
    if record.case_type == "negative_question" and record.status == "fail":
        return "semantic"

    # retrieval — correct intent but wrong view selected or not referenced in SQL
    if record.view_match is False or record.view_in_sql is False:
        return "retrieval"

    # sql — view right but SQL generation or validation broke
    if record.validation_pass is False:
        return "sql"
    if record.metric_present is False or record.grouping_present is False or record.filter_present is False:
        return "sql"

    # access — execution blocked by role enforcement
    if record.case_type == "access" and record.status == "fail":
        return "access"
    if record.execution_status == "failed" and any(
        "denied" in r.lower() or "access" in r.lower() for r in record.failure_reasons
    ):
        return "access"

    # answer — SQL executed fine but answer quality check failed (full mode)
    if record.answer_quality_pass is False:
        return "answer"

    return "other"


@dataclass
class EvaluationReport:
    total: int
    passed: int
    partial: int
    failed: int
    errors: int
    records: list[GoldenEvalRecord]
    access_enforcement_note: str = "Access enforced at execution stage."
    access_tests_passed: int = 0
    access_tests_total: int = 0
    conversation_tests_passed: int = 0
    conversation_tests_total: int = 0
    system_info_tests_passed: int = 0
    system_info_tests_total: int = 0
    failure_distribution: dict[str, int] = field(default_factory=dict)

    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0

    def summary_lines(self) -> list[str]:
        lines = [
            f"Evaluation complete — {self.total} cases",
            f"  Pass:    {self.passed}",
            f"  Partial: {self.partial}",
            f"  Fail:    {self.failed}",
            f"  Error:   {self.errors}",
            f"  Pass rate: {self.pass_rate:.0%}",
        ]
        if self.failure_distribution:
            dist_parts = "  |  ".join(
                f"{cat}: {self.failure_distribution.get(cat, 0)}"
                for cat in _FAILURE_CATEGORIES
                if self.failure_distribution.get(cat, 0) > 0
            )
            lines.append(f"  Failure breakdown: {dist_parts}")
        if self.access_tests_total:
            lines.append(f"  Access:       {self.access_tests_passed}/{self.access_tests_total} passed")
        if self.conversation_tests_total:
            lines.append(f"  Conversation: {self.conversation_tests_passed}/{self.conversation_tests_total} passed")
        if self.system_info_tests_total:
            lines.append(f"  System-info:  {self.system_info_tests_passed}/{self.system_info_tests_total} passed")
        lines.append(f"  Note: {self.access_enforcement_note}")
        return lines

    def print_summary(self) -> None:
        for line in self.summary_lines():
            print(line)

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "partial": self.partial,
            "failed": self.failed,
            "errors": self.errors,
            "pass_rate": self.pass_rate,
            "access_enforcement_note": self.access_enforcement_note,
            "access_tests_passed": self.access_tests_passed,
            "access_tests_total": self.access_tests_total,
            "conversation_tests_passed": self.conversation_tests_passed,
            "conversation_tests_total": self.conversation_tests_total,
            "system_info_tests_passed": self.system_info_tests_passed,
            "system_info_tests_total": self.system_info_tests_total,
            "failure_distribution": self.failure_distribution,
            "records": [
                {
                    "question": r.question,
                    "case_type": r.case_type,
                    "status": r.status,
                    "failure_category": r.failure_category,
                    "expected_view": r.expected_view,
                    "generated_sql": r.generated_sql,
                    "expected_sql": r.expected_sql,
                    "checks": {
                        "intent_answerable": r.intent_answerable,
                        "view_match": r.view_match,
                        "view_in_sql": r.view_in_sql,
                        "metric_present": r.metric_present,
                        "grouping_present": r.grouping_present,
                        "filter_present": r.filter_present,
                        "validation_pass": r.validation_pass,
                        "execution_status": r.execution_status,
                        "answer_quality": r.answer_quality_pass,
                    },
                    "answer": r.answer,
                    "failure_reasons": r.failure_reasons,
                    "latency_ms": r.latency_ms,
                    "trace_id": r.trace.trace_id if r.trace else None,
                }
                for r in self.records
            ],
        }



def _extract_group_by_columns(sql_upper: str) -> list[str]:
    match = re.search(r"\bGROUP\s+BY\s+(.*?)(?:\bORDER\b|\bHAVING\b|\bFETCH\b|$)", sql_upper, re.DOTALL)
    if not match:
        return []
    return [c.strip() for c in match.group(1).split(",") if c.strip()]


def _extract_filter_terms(sql_upper: str) -> list[str]:
    """Return significant tokens from the WHERE clause."""
    match = re.search(r"\bWHERE\b(.*?)(?:\bGROUP\b|\bORDER\b|\bFETCH\b|$)", sql_upper, re.DOTALL)
    if not match:
        return []
    where_text = match.group(1)
    tokens = re.findall(r"'[^']*'|\b[A-Z_][A-Z0-9_]{2,}\b|-?\d+(?:\.\d+)?", where_text)
    _SQL_WORDS = {"AND", "OR", "NOT", "NULL", "BETWEEN", "LIKE", "IS", "IN", "EXISTS"}
    return [t for t in tokens if t not in _SQL_WORDS]


_NO_RESULT_PHRASES = ("no ", "none", "zero", "empty", "0 ")


def _check_answer_quality(answer: str, rows: list[dict]) -> bool:
    """Return True if the answer reflects the query result.

    Empty result sets pass when the answer conveys "no results."
    Non-empty sets pass when at least one row value appears in the answer
    (numbers normalized to strip comma/period formatting).
    """
    if not answer:
        return False
    answer_lower = answer.lower()
    if not rows:
        return any(phrase in answer_lower for phrase in _NO_RESULT_PHRASES)
    # Strip formatting characters so "2,666,366" matches value 2666366
    answer_stripped = answer_lower.replace(",", "").replace(".", "")
    for row in rows:
        for value in row.values():
            if value is None:
                continue
            raw = str(value).lower()
            if raw in answer_lower:
                return True
            normalized = raw.replace(",", "").replace(".", "")
            if normalized and normalized in answer_stripped:
                return True
    return False


def _make_ctx(question: str, conversation_history: list | None = None) -> PipelineContext:
    return PipelineContext(
        question=question,
        user_context=None,
        trace=TraceRecord(question=question),
        latency={},
        pipeline_start=time.perf_counter(),
        conversation_history=conversation_history or [],
    )


class GoldenRunner:
    def __init__(
        self,
        intent_service: IntentService | None = None,
        view_selection_service: ViewSelectionService | None = None,
        sql_generation_service: SQLGenerationService | None = None,
        answer_service: AnswerService | None = None,
        golden_questions_path: Path | None = None,
    ):
        # Exposed as attributes so tests can inject mocks via runner.<service>.method = AsyncMock(...)
        self.intent_service = intent_service or IntentService()
        self.view_selection_service = view_selection_service or ViewSelectionService()
        self.sql_generation_service = sql_generation_service or SQLGenerationService()
        self.answer_service = answer_service or AnswerService()
        self.golden_questions_path = golden_questions_path or _GOLDEN_QUESTIONS_PATH

        self._intent_stage = IntentStage(self.intent_service)
        self._view_selection_stage = ViewSelectionStage(self.view_selection_service)
        self._metadata_stage = MetadataStage()
        self._sql_generation_stage = SQLGenerationStage(self.sql_generation_service)
        self._validation_stage = SQLValidationStage()
        self._execution_stage = ExecutionStage()
        self._answer_stage = AnswerStage(self.answer_service)

    def _load_golden_questions(self) -> list[dict]:
        with open(self.golden_questions_path, "r") as f:
            return yaml.safe_load(f) or []

    async def run_question(self, q: dict, mode: str = "fast", conversation_history: list | None = None) -> GoldenEvalRecord:
        """Run one positive golden question. Fast mode: stages 1-5 (no DB). Full mode: all 7 stages."""
        record = GoldenEvalRecord(
            question=q["natural_language_question"],
            expected_view=q.get("expected_view", ""),
            expected_sql=q.get("expected_sql", ""),
            expected_expressions=q.get("expected_result_shape", {}).get("columns", []),
            case_type="positive",
        )
        ctx = _make_ctx(record.question, conversation_history=conversation_history)

        # Stage 1 — stop if refused; positive questions must be answerable
        outcome = await self._intent_stage.run(ctx)
        record.intent_answerable = ctx.trace.answerable
        if isinstance(outcome, Refusal):
            record.failure_reasons.append(f"Intent: {outcome.reason}")
            record.status = "fail"
            record.trace = ctx.trace
            record.latency_ms = ctx.trace.latency_ms.total_ms
            return record

        # Stages 2-5 — run all, accumulate eval failures rather than stopping
        await self._view_selection_stage.run(ctx)
        await self._metadata_stage.run(ctx)
        await self._sql_generation_stage.run(ctx)
        await self._validation_stage.run(ctx)

        # ── Checks ────────────────────────────────────────────────────────────

        record.view_match = record.expected_view in (ctx.selected_views or [])
        if not record.view_match:
            record.failure_reasons.append(
                f"View: expected '{record.expected_view}', got {ctx.selected_views}"
            )

        record.generated_sql = ctx.sql

        if ctx.trace.validation_result:
            record.validation_pass = ctx.trace.validation_result.passed
            if not record.validation_pass:
                record.failure_reasons.append(f"Validation: {ctx.trace.validation_result.reason}")
        else:
            record.validation_pass = False
            record.failure_reasons.append("Validation: no result produced")

        gen_upper = (ctx.sql or "").upper()
        exp_upper = record.expected_sql.upper()

        view_token = record.expected_view.split(".")[-1].upper()
        record.view_in_sql = view_token in gen_upper or record.expected_view.upper() in gen_upper
        if not record.view_in_sql:
            record.failure_reasons.append(
                f"SQL: '{record.expected_view}' not referenced in generated SQL"
            )

        if record.expected_expressions:
            exprs_upper = [e.upper() for e in record.expected_expressions]
            missing = [e for e in exprs_upper if e not in gen_upper]
            record.metric_present = len(missing) == 0
            if not record.metric_present:
                record.failure_reasons.append(f"Metrics: missing {missing}")
        else:
            record.metric_present = None

        expected_groups = _extract_group_by_columns(exp_upper)
        if expected_groups:
            record.grouping_present = any(g in gen_upper for g in expected_groups)
            if not record.grouping_present:
                record.failure_reasons.append(f"Grouping: expected GROUP BY {expected_groups}, not found")
        else:
            record.grouping_present = None

        expected_filters = _extract_filter_terms(exp_upper)
        if expected_filters:
            record.filter_present = any(f in gen_upper for f in expected_filters)
            if not record.filter_present:
                record.failure_reasons.append(f"Filters: expected terms {expected_filters[:4]} not found")
        else:
            record.filter_present = None

        # ── Full mode: stages 6-7 ─────────────────────────────────────────────
        if mode == "full" and record.validation_pass and ctx.sql:
            exec_outcome = await self._execution_stage.run(ctx)
            if isinstance(exec_outcome, Refusal):
                record.execution_status = "failed"
                record.failure_reasons.append(f"Execution: {exec_outcome.reason}")
            else:
                record.execution_status = "success"
                answer_outcome = await self._answer_stage.run(ctx)
                record.answer = answer_outcome.answer
                record.answer_quality_pass = _check_answer_quality(answer_outcome.answer, ctx.rows or [])
                if not record.answer_quality_pass:
                    record.failure_reasons.append("Answer: no result values found in answer text")
        elif mode == "full":
            record.execution_status = "skipped"

        # ── Status determination ──────────────────────────────────────────────
        if mode == "full" and record.execution_status == "failed":
            record.status = "fail"
        else:
            mandatory = [record.view_match, record.view_in_sql, record.validation_pass]
            optional = [c for c in [record.metric_present, record.grouping_present, record.filter_present, record.answer_quality_pass] if c is not None]
            all_checks = [c for c in mandatory if c is not None] + optional

            if all(all_checks):
                record.status = "pass"
            elif any(all_checks):
                record.status = "partial"
            else:
                record.status = "fail"

        if mode == "fast":
            ctx.trace.execution_status = "skipped"
        ctx.trace.latency_ms = build_latency(ctx)
        record.trace = ctx.trace
        record.latency_ms = ctx.trace.latency_ms.total_ms
        return record

    async def run_negative_question(self, neg: dict) -> GoldenEvalRecord:
        """Run one negative question — it must be refused at intent stage."""
        record = GoldenEvalRecord(
            question=neg["question"],
            expected_view="none",
            expected_sql="",
            case_type="negative_question",
        )
        ctx = _make_ctx(record.question)

        outcome = await self._intent_stage.run(ctx)
        record.intent_answerable = ctx.trace.answerable

        if isinstance(outcome, Refusal):  # refused — correct for a negative question
            record.status = "pass"
        else:
            record.status = "fail"
            record.failure_reasons.append(
                "System should have refused this question but classified it as answerable."
            )
            ctx.trace.execution_status = "skipped"
            ctx.trace.latency_ms = build_latency(ctx)

        record.trace = ctx.trace
        record.latency_ms = ctx.trace.latency_ms.total_ms
        return record

    def run_negative_sql_checks(self) -> list[GoldenEvalRecord]:
        """Validate that known-unsafe SQL patterns are blocked by validate_query."""
        records = []
        for sql, description in NEGATIVE_SQL_PATTERNS:
            record = GoldenEvalRecord(
                question=description,
                expected_view="none",
                expected_sql=sql,
                case_type="negative_sql",
            )
            try:
                validate_query(sql)
                record.validation_pass = False
                record.status = "fail"
                record.failure_reasons.append(f"Validator should have blocked: {sql[:80]}")
            except SQLSafetyError:
                record.validation_pass = True
                record.status = "pass"

            record.trace = TraceRecord(
                question=description,
                generated_sql=sql,
                validation_result=ValidationResult(
                    passed=not record.validation_pass,
                    reason=f"Negative SQL check: {description}",
                ),
                execution_status="refused",
            )
            records.append(record)
        return records

    async def _run_one_access_check(self, case: dict) -> GoldenEvalRecord:
        """Run one access test case — ExecutionStage only, no LLM or DB required for denied cases."""
        record = GoldenEvalRecord(
            question=case["description"],
            expected_view="",
            expected_sql=case["sql"],
            case_type="access",
        )
        ctx = _make_ctx(case["description"])
        ctx.user = ResolvedUser(role=case["role"], allowed_views=case["allowed_views"])
        ctx.sql = case["sql"]

        try:
            await self._execution_stage.run(ctx)
        except Exception as exc:
            record.status = "error"
            record.failure_reasons.append(str(exc))
            record.trace = ctx.trace
            record.latency_ms = 0.0
            return record

        # "refused" means the access check fired; "failed" means the DB was unreachable after access passed.
        execution_status = ctx.trace.execution_status or ""
        if case["expect"] == "denied":
            if execution_status == "refused":
                record.status = "pass"
            else:
                record.status = "fail"
                record.failure_reasons.append(
                    f"Expected access denied for role '{case['role']}' but execution_status was '{execution_status}'"
                )
        else:  # "allowed"
            if execution_status == "refused":
                record.status = "fail"
                record.failure_reasons.append(
                    f"Role '{case['role']}' was incorrectly denied: {ctx.trace.refusal_reason}"
                )
            else:
                record.status = "pass"

        ctx.trace.latency_ms = build_latency(ctx)
        record.trace = ctx.trace
        record.latency_ms = ctx.trace.latency_ms.total_ms
        return record

    async def run_access_checks(self) -> list[GoldenEvalRecord]:
        """Verify access enforcement using hardcoded SQL + role pairs. No LLM or DB required."""
        records = []
        for case in ACCESS_TEST_CASES:
            records.append(await self._run_one_access_check(case))
        return records

    def _load_conversation_cases(self) -> list[dict]:
        path = (
            Path(__file__).resolve().parents[3]
            / "metadata" / "example_questions" / "golden_conversations.yml"
        )
        if not path.exists():
            return []
        with open(path, "r") as f:
            return yaml.safe_load(f) or []

    async def run_conversation_check(self, case: dict, mode: str = "fast") -> GoldenEvalRecord:
        """Run a 2-turn conversation test: stage turn 1 to build history, then evaluate turn 2 with it."""
        from ..models.talk_to_data import ConversationTurn

        # Turn 1: run normally to populate history
        turn1_dict = case["turn_1"]
        turn1_result = await self.run_question(turn1_dict, mode=mode)

        history = [ConversationTurn(
            question=turn1_dict["natural_language_question"],
            sql=turn1_result.generated_sql,
            answer=turn1_result.answer,
        )]

        # Turn 2: run with history injected
        turn2_dict = case["turn_2"]
        record = GoldenEvalRecord(
            question=f"[conv] {turn2_dict['natural_language_question']}",
            expected_view=turn2_dict.get("expected_view", ""),
            expected_sql="",
            expected_expressions=turn2_dict.get("expected_sql_contains", []),
            case_type="conversation",
        )
        ctx = _make_ctx(turn2_dict["natural_language_question"], conversation_history=history)

        outcome = await self._intent_stage.run(ctx)
        record.intent_answerable = ctx.trace.answerable
        if isinstance(outcome, Refusal):
            record.status = "fail"
            record.failure_reasons.append(f"Turn 2 intent refused: {outcome.reason}")
            ctx.trace.execution_status = "skipped"
            ctx.trace.latency_ms = build_latency(ctx)
            record.trace = ctx.trace
            record.latency_ms = ctx.trace.latency_ms.total_ms
            return record

        await self._view_selection_stage.run(ctx)
        await self._metadata_stage.run(ctx)
        await self._sql_generation_stage.run(ctx)
        await self._validation_stage.run(ctx)

        record.generated_sql = ctx.sql

        record.view_match = record.expected_view in (ctx.selected_views or [])
        if not record.view_match:
            record.failure_reasons.append(
                f"View: expected '{record.expected_view}', got {ctx.selected_views}"
            )

        if ctx.trace.validation_result:
            record.validation_pass = ctx.trace.validation_result.passed
            if not record.validation_pass:
                record.failure_reasons.append(f"Validation: {ctx.trace.validation_result.reason}")
        else:
            record.validation_pass = False
            record.failure_reasons.append("Validation: no result")

        gen_upper = (ctx.sql or "").upper()
        view_token = record.expected_view.split(".")[-1].upper()
        record.view_in_sql = view_token in gen_upper or record.expected_view.upper() in gen_upper
        if not record.view_in_sql:
            record.failure_reasons.append(f"SQL: '{record.expected_view}' not referenced in generated SQL")

        if record.expected_expressions:
            exprs_upper = [e.upper() for e in record.expected_expressions]
            missing = [e for e in exprs_upper if e not in gen_upper]
            record.metric_present = len(missing) == 0
            if not record.metric_present:
                record.failure_reasons.append(f"Expected terms missing from SQL: {missing}")

        mandatory = [record.view_match, record.view_in_sql, record.validation_pass]
        optional = [c for c in [record.metric_present] if c is not None]
        all_checks = [c for c in mandatory if c is not None] + optional

        if all(all_checks):
            record.status = "pass"
        elif any(all_checks):
            record.status = "partial"
        else:
            record.status = "fail"

        ctx.trace.execution_status = "skipped"
        ctx.trace.latency_ms = build_latency(ctx)
        record.trace = ctx.trace
        record.latency_ms = ctx.trace.latency_ms.total_ms
        return record

    async def run_system_info_question(self, q: dict) -> GoldenEvalRecord:
        """Run a system_info question — intent stage only; no SQL pipeline."""
        record = GoldenEvalRecord(
            question=q["natural_language_question"],
            expected_view="",
            expected_sql="",
            case_type="system_info",
        )
        ctx = _make_ctx(record.question)

        outcome = await self._intent_stage.run(ctx)
        record.intent_answerable = ctx.trace.answerable

        domain_ok = ctx.trace.intent == "system_info"
        answerable_ok = ctx.trace.answerable is True

        if answerable_ok and domain_ok:
            record.status = "pass"
        elif answerable_ok:
            record.status = "partial"
            record.failure_reasons.append(
                f"Answerable but domain={ctx.trace.intent!r} (expected 'system_info')"
            )
        else:
            reason = outcome.reason if isinstance(outcome, Refusal) else "not answerable"
            record.status = "fail"
            record.failure_reasons.append(f"system_info question refused: {reason}")

        ctx.trace.execution_status = "skipped"
        ctx.trace.latency_ms = build_latency(ctx)
        record.trace = ctx.trace
        record.latency_ms = ctx.trace.latency_ms.total_ms
        return record

    async def run_system_info_checks(self, questions: list[dict]) -> list[GoldenEvalRecord]:
        records = []
        for q in questions:
            try:
                records.append(await self.run_system_info_question(q))
            except Exception as exc:
                logger.exception("golden_runner.system_info_error q=%s", q.get("natural_language_question", "?"))
                rec = GoldenEvalRecord(
                    question=q.get("natural_language_question", "unknown"),
                    expected_view="",
                    expected_sql="",
                    case_type="system_info",
                    status="error",
                )
                rec.failure_reasons.append(str(exc))
                records.append(rec)
        return records

    async def run_conversation_checks(self, mode: str = "fast") -> list[GoldenEvalRecord]:
        """Run all 2-turn conversation test cases from golden_conversations.yml."""
        cases = self._load_conversation_cases()
        if not cases:
            return []
        records = []
        for case in cases:
            try:
                records.append(await self.run_conversation_check(case, mode=mode))
            except Exception as exc:
                logger.exception("golden_runner.conversation_error desc=%s", case.get("description", "?"))
                rec = GoldenEvalRecord(
                    question=f"[conv] {case.get('turn_2', {}).get('natural_language_question', 'unknown')}",
                    expected_view="",
                    expected_sql="",
                    case_type="conversation",
                    status="error",
                )
                rec.failure_reasons.append(str(exc))
                records.append(rec)
        return records

    async def _run_question_safe(self, q: dict, mode: str, sem: asyncio.Semaphore) -> GoldenEvalRecord:
        async with sem:
            try:
                return await self.run_question(q, mode=mode)
            except Exception as exc:
                if "429" in str(exc) or "too_many_requests" in str(exc).lower():
                    logger.warning("golden_runner.rate_limited q=%s — sleeping 60s", q.get("natural_language_question", "?")[:60])
                    await asyncio.sleep(60)
                    try:
                        return await self.run_question(q, mode=mode)
                    except Exception as retry_exc:
                        logger.exception("golden_runner.question_error q=%s", q.get("natural_language_question", "?"))
                        rec = GoldenEvalRecord(
                            question=q.get("natural_language_question", "unknown"),
                            expected_view=q.get("expected_view", ""),
                            expected_sql=q.get("expected_sql", ""),
                            status="error",
                        )
                        rec.failure_reasons.append(str(retry_exc))
                        return rec
                logger.exception("golden_runner.question_error q=%s", q.get("natural_language_question", "?"))
                rec = GoldenEvalRecord(
                    question=q.get("natural_language_question", "unknown"),
                    expected_view=q.get("expected_view", ""),
                    expected_sql=q.get("expected_sql", ""),
                    status="error",
                )
                rec.failure_reasons.append(str(exc))
                return rec

    async def _run_negative_safe(self, neg: dict, sem: asyncio.Semaphore) -> GoldenEvalRecord:
        async with sem:
            try:
                return await self.run_negative_question(neg)
            except Exception as exc:
                logger.exception("golden_runner.negative_error q=%s", neg["question"])
                rec = GoldenEvalRecord(
                    question=neg["question"],
                    expected_view="none",
                    expected_sql="",
                    case_type="negative_question",
                    status="error",
                )
                rec.failure_reasons.append(str(exc))
                return rec

    async def run_all(self, mode: str = "fast", limit: int | None = None, concurrency: int = 5) -> EvaluationReport:
        all_questions = self._load_golden_questions()

        # Split: system_info questions use intent-only path; all others go through the SQL pipeline
        system_info_questions = [q for q in all_questions if q.get("expected_intent") == "system_info"]
        sql_questions = [q for q in all_questions if q.get("expected_intent") != "system_info"]

        if limit is not None:
            sql_questions = sql_questions[:limit]

        logger.info(
            "golden_runner.start mode=%s total_sql=%d total_system_info=%d concurrency=%d",
            mode, len(sql_questions), len(system_info_questions), concurrency,
        )

        sem = asyncio.Semaphore(concurrency)
        positive_records = await asyncio.gather(
            *[self._run_question_safe(q, mode, sem) for q in sql_questions]
        )
        negative_records = await asyncio.gather(
            *[self._run_negative_safe(neg, sem) for neg in NEGATIVE_QUESTIONS]
        )
        access_records = await self.run_access_checks()
        conversation_records = await self.run_conversation_checks(mode=mode)
        system_info_records = await self.run_system_info_checks(system_info_questions)

        records: list[GoldenEvalRecord] = [*positive_records, *negative_records]
        records.extend(self.run_negative_sql_checks())
        records.extend(access_records)
        records.extend(conversation_records)
        records.extend(system_info_records)

        # Assign failure categories to all failing/partial records
        for r in records:
            r.failure_category = _categorize_failure(r)

        counts: dict[str, int] = {"pass": 0, "partial": 0, "fail": 0, "error": 0}
        for r in records:
            counts[r.status] = counts.get(r.status, 0) + 1

        failure_distribution: dict[str, int] = {cat: 0 for cat in _FAILURE_CATEGORIES}
        for r in records:
            if r.failure_category:
                failure_distribution[r.failure_category] = failure_distribution.get(r.failure_category, 0) + 1

        access_passed = sum(1 for r in access_records if r.status == "pass")
        conversation_passed = sum(1 for r in conversation_records if r.status == "pass")
        system_info_passed = sum(1 for r in system_info_records if r.status == "pass")

        report = EvaluationReport(
            total=len(records),
            passed=counts["pass"],
            partial=counts["partial"],
            failed=counts["fail"],
            errors=counts["error"],
            records=records,
            access_tests_passed=access_passed,
            access_tests_total=len(access_records),
            conversation_tests_passed=conversation_passed,
            conversation_tests_total=len(conversation_records),
            system_info_tests_passed=system_info_passed,
            system_info_tests_total=len(system_info_records),
            failure_distribution=failure_distribution,
        )
        logger.info(
            "golden_runner.complete total=%d pass=%d partial=%d fail=%d error=%d "
            "access=%d/%d conv=%d/%d sysinfo=%d/%d",
            report.total, report.passed, report.partial, report.failed, report.errors,
            access_passed, len(access_records),
            conversation_passed, len(conversation_records),
            system_info_passed, len(system_info_records),
        )
        return report
