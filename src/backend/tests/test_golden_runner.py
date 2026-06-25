"""
Tests for GoldenRunner.

All LLM calls are mocked. The metadata loader reads real YAML files from
the repository (they are not mocked â€” we want to verify the actual metadata
loads correctly). validate_query is the real deterministic implementation.
"""
import pytest
from unittest.mock import AsyncMock, MagicMock


import backend.app.stages.intent as intent_module
import backend.app.stages.sql_generation as sql_gen_module
import backend.app.stages.view_selection as vs_module
from backend.app.evaluation.golden_runner import (
    ACCESS_TEST_CASES,
    GoldenRunner,
    NEGATIVE_SQL_PATTERNS,
)
from backend.app.stages.execution import ExecutionStage
from backend.app.stages.intent import IntentResult
from backend.app.stages.sql_generation import SQLGenResult


SAFE_SQL = (
    "SELECT TOP 10 article_id, title, comment_count "
    "FROM analytics.vw_article_engagement ORDER BY comment_count DESC"
)


def _make_intent(answerable: bool = True) -> IntentResult:
    return IntentResult(
        answerable=answerable,
        reason="test" if answerable else "out of scope",
        domain="article_engagement" if answerable else "unknown",
        suggested_metrics=[],
        prompt_version="intent_v1",
        model_deployment="test",
        latency_ms=1.0,
    )


def _make_sql(sql: str = SAFE_SQL) -> SQLGenResult:
    return SQLGenResult(
        sql=sql,
        prompt_version="sql_gen_v1",
        model_deployment="test",
        latency_ms=1.0,
    )


def _build_runner(monkeypatch) -> GoldenRunner:
    for mod in [intent_module, sql_gen_module, vs_module]:
        monkeypatch.setattr(mod, "LLMService", MagicMock(side_effect=ValueError("no config")))
    return GoldenRunner()


async def test_run_question_pass(monkeypatch):
    runner = _build_runner(monkeypatch)

    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    runner.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.9,
        "reason": "ok",
    })
    runner.sql_generation_service.generate = AsyncMock(return_value=_make_sql(SAFE_SQL))

    q = {
        "natural_language_question": "Which articles have the most comments?",
        "expected_view": "analytics.vw_article_engagement",
        "expected_sql": (
            "SELECT TOP 10 article_id, title, comment_count, avg_comment_sentiment\n"
            "FROM analytics.vw_article_engagement\n"
            "ORDER BY comment_count DESC"
        ),
    }
    record = await runner.run_question(q)

    assert record.intent_answerable is True
    assert record.view_match is True
    assert record.view_in_sql is True
    assert record.validation_pass is True
    assert record.trace is not None
    assert record.trace.trace_id is not None
    assert record.trace.generated_sql == SAFE_SQL
    assert record.trace.execution_status == "skipped"  # fast mode
    assert record.trace.latency_ms.total_ms is not None
    assert record.latency_ms is not None
    assert "Access enforced" in record.trace.access_enforcement_note


async def test_run_question_wrong_view(monkeypatch):
    runner = _build_runner(monkeypatch)

    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    runner.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_keyword_engagement"],  # wrong view
        "confidence": 0.5,
        "reason": "keyword match",
    })
    runner.sql_generation_service.generate = AsyncMock(return_value=_make_sql(
        "SELECT TOP 10 full_keyword FROM analytics.vw_keyword_engagement ORDER BY article_count DESC"
    ))

    q = {
        "natural_language_question": "Which articles have the most comments?",
        "expected_view": "analytics.vw_article_engagement",
        "expected_sql": "SELECT TOP 10 article_id FROM analytics.vw_article_engagement",
    }
    record = await runner.run_question(q)

    assert record.view_match is False
    assert record.status in ("fail", "partial")
    assert any("View" in r for r in record.failure_reasons)
    # Trace still exists with all artefacts
    assert record.trace is not None
    assert record.trace.selected_views == ["analytics.vw_keyword_engagement"]


async def test_run_question_validation_fail(monkeypatch):
    runner = _build_runner(monkeypatch)

    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    runner.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.8,
        "reason": "ok",
    })
    runner.sql_generation_service.generate = AsyncMock(return_value=_make_sql(
        "DELETE FROM analytics.vw_article_engagement"
    ))

    q = {
        "natural_language_question": "Delete all articles",
        "expected_view": "analytics.vw_article_engagement",
        "expected_sql": "",
    }
    record = await runner.run_question(q)

    assert record.validation_pass is False
    assert any("Validation" in r for r in record.failure_reasons)
    assert record.trace.validation_result is not None
    assert record.trace.validation_result.passed is False


async def test_run_negative_question_correctly_refused(monkeypatch):
    runner = _build_runner(monkeypatch)
    runner.intent_service.classify = AsyncMock(return_value=_make_intent(False))

    neg = {
        "question": "What will article engagement look like next quarter?",
        "expect": "refused",
        "reason": "Forecasting not supported",
    }
    record = await runner.run_negative_question(neg)

    assert record.status == "pass"
    assert record.intent_answerable is False
    assert record.trace is not None
    assert record.trace.execution_status == "refused"


async def test_run_negative_question_not_refused_fails(monkeypatch):
    runner = _build_runner(monkeypatch)
    # LLM incorrectly says it's answerable
    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))

    neg = {
        "question": "Forecast next quarter engagement",
        "expect": "refused",
        "reason": "should be refused",
    }
    record = await runner.run_negative_question(neg)

    assert record.status == "fail"
    assert record.intent_answerable is True
    assert record.failure_reasons


def test_negative_sql_checks_all_blocked():
    runner = GoldenRunner.__new__(GoldenRunner)
    records = runner.run_negative_sql_checks()

    assert len(records) == len(NEGATIVE_SQL_PATTERNS)
    for record in records:
        assert record.case_type == "negative_sql"
        assert record.status == "pass", (
            f"Validator should have blocked '{record.expected_sql}' but did not. "
            f"Reasons: {record.failure_reasons}"
        )
        assert record.validation_pass is True  # True means "correctly rejected"
        assert record.trace is not None


async def test_run_all_returns_report(monkeypatch):
    runner = _build_runner(monkeypatch)

    # Mock services to return consistent answers
    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    runner.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.9,
        "reason": "ok",
    })
    runner.sql_generation_service.generate = AsyncMock(return_value=_make_sql(SAFE_SQL))

    report = await runner.run_all()

    assert report.total > 0
    assert report.total == report.passed + report.partial + report.failed + report.errors
    assert 0.0 <= report.pass_rate <= 1.0
    assert report.records
    assert "Access enforced" in report.access_enforcement_note

    summary = report.summary_lines()
    assert any("Pass" in line for line in summary)

    as_dict = report.to_dict()
    assert "total" in as_dict
    assert "pass_rate" in as_dict
    assert "records" in as_dict
    assert as_dict["records"]
    first = as_dict["records"][0]
    assert "trace_id" in first
    assert "checks" in first


async def test_run_one_access_check_denied():
    """Editor requesting a denied view must produce status='pass' (correctly blocked)."""
    runner = GoldenRunner.__new__(GoldenRunner)
    runner._execution_stage = ExecutionStage()

    case = {
        "description": "Editor denied: analytics.vw_ingestion_errors not in editor's allowed_views",
        "sql": "SELECT TOP 10 stage, error_type FROM analytics.vw_ingestion_errors ORDER BY error_count DESC",
        "role": "editor",
        "allowed_views": ["analytics.vw_article_engagement", "analytics.vw_top_contributors"],
        "expect": "denied",
    }
    record = await runner._run_one_access_check(case)

    assert record.status == "pass"
    assert record.case_type == "access"
    assert record.trace is not None
    assert record.trace.execution_status == "refused"
    assert not record.failure_reasons


async def test_run_one_access_check_allowed(monkeypatch):
    """Role with access must not be blocked — DB errors are treated as 'not denied'."""
    import backend.app.stages.execution as exec_module
    monkeypatch.setattr(exec_module, "execute_query", AsyncMock(return_value=[]))

    runner = GoldenRunner.__new__(GoldenRunner)
    runner._execution_stage = ExecutionStage()

    case = {
        "description": "Analyst allowed: analytics.vw_ingestion_errors is in analyst's allowed_views",
        "sql": "SELECT TOP 10 stage, error_type FROM analytics.vw_ingestion_errors ORDER BY error_count DESC",
        "role": "analyst",
        "allowed_views": [
            "analytics.vw_article_engagement",
            "analytics.vw_keyword_engagement",
            "analytics.vw_top_contributors",
            "analytics.vw_ingestion_errors",
        ],
        "expect": "allowed",
    }
    record = await runner._run_one_access_check(case)

    assert record.status == "pass"
    assert record.case_type == "access"
    assert record.trace is not None
    assert record.trace.execution_status != "refused"
    assert not record.failure_reasons


async def test_run_one_access_check_allowed_wrong_role_fails():
    """If an 'allowed' test unexpectedly gets refused, the record status is 'fail'."""
    runner = GoldenRunner.__new__(GoldenRunner)
    runner._execution_stage = ExecutionStage()

    case = {
        "description": "Editor incorrectly expected to be allowed on denied view",
        "sql": "SELECT TOP 10 stage, error_type FROM analytics.vw_ingestion_errors ORDER BY error_count DESC",
        "role": "editor",
        "allowed_views": ["analytics.vw_article_engagement"],
        "expect": "allowed",  # wrong — editor can't reach ingestion_errors
    }
    record = await runner._run_one_access_check(case)

    assert record.status == "fail"
    assert record.failure_reasons


async def test_run_access_checks_all_pass(monkeypatch):
    """All ACCESS_TEST_CASES pass: denied cases blocked, allowed cases pass-through."""
    import backend.app.stages.execution as exec_module
    monkeypatch.setattr(exec_module, "execute_query", AsyncMock(return_value=[]))

    runner = GoldenRunner.__new__(GoldenRunner)
    runner._execution_stage = ExecutionStage()

    records = await runner.run_access_checks()

    assert len(records) == len(ACCESS_TEST_CASES)
    for r in records:
        assert r.case_type == "access"
        assert r.status == "pass", f"Access check failed: {r.question} — {r.failure_reasons}"


async def test_run_all_includes_access_records(monkeypatch):
    """run_all() report includes access test counters."""
    runner = _build_runner(monkeypatch)
    runner.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    runner.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.9,
        "reason": "ok",
    })
    runner.sql_generation_service.generate = AsyncMock(return_value=_make_sql(SAFE_SQL))

    import backend.app.stages.execution as exec_module
    monkeypatch.setattr(exec_module, "execute_query", AsyncMock(return_value=[]))

    report = await runner.run_all()

    assert report.access_tests_total == len(ACCESS_TEST_CASES)
    assert report.access_tests_passed == len(ACCESS_TEST_CASES)
    access_recs = [r for r in report.records if r.case_type == "access"]
    assert len(access_recs) == len(ACCESS_TEST_CASES)
    assert "Access" in "\n".join(report.summary_lines())


@pytest.mark.integration
async def test_golden_runner_pass_rate_above_threshold():
    """Fast-mode pass rate must be >= 80%. Requires live Azure OpenAI credentials.

    Run with: poetry run pytest -m integration
    """
    runner = GoldenRunner()
    report = await runner.run_all(mode="fast")
    failing = [
        f"  [{r.status}] {r.question[:80]}: {r.failure_reasons}"
        for r in report.records
        if r.status in ("fail", "error")
    ]
    assert report.pass_rate >= 0.8, (
        f"Pass rate {report.pass_rate:.0%} is below the 80% threshold.\n"
        + "\n".join(failing)
    )
