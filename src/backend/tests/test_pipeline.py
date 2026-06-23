"""
Tests for TalkToDataPipeline.

All LLM calls and DB execution are mocked. Tests verify that:
- A question answered by safe SQL returns an answer with a trace.
- A question classified as not answerable is refused at intent stage.
- SQL that fails validation is refused before execution.
- SQL generation returning empty string is refused.
- The trace captures stage-level artefacts at every failure point.
"""
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.intent as intent_module
import backend.app.stages.sql_generation as sql_gen_module
import backend.app.stages.answer as answer_module
import backend.app.stages.view_selection as vs_module
import backend.app.services.talk_to_data_pipeline as pipeline_module
import backend.app.stages.metadata as metadata_stage_module
import backend.app.stages.execution as execution_stage_module
from backend.app.models.talk_to_data import AskRequest
from backend.app.stages.intent import IntentResult
from backend.app.stages.sql_generation import SQLGenResult
from backend.app.stages.answer import AnswerResult


SAFE_SQL = (
    "SELECT TOP 10 article_id, title, comment_count "
    "FROM analytics.vw_article_engagement ORDER BY comment_count DESC"
)
UNSAFE_SQL = "DROP TABLE analytics.vw_article_engagement"

MOCK_METADATA = {
    "analytics.vw_article_engagement": {
        "purpose": "Article engagement",
        "columns": [{"name": "article_id"}, {"name": "comment_count"}],
        "limitations": ["Sentiment is averaged"],
    }
}

MOCK_ROWS = [
    {"article_id": 1, "title": "A", "comment_count": 42},
    {"article_id": 2, "title": "B", "comment_count": 30},
]


def _make_intent(answerable: bool, domain: str = "article_engagement") -> IntentResult:
    return IntentResult(
        answerable=answerable,
        reason="test" if answerable else "Out of scope",
        domain=domain,
        suggested_metrics=[],
        prompt_version="intent_v1",
        model_deployment="test-deploy",
        latency_ms=1.0,
    )


def _make_sql_result(sql: str) -> SQLGenResult:
    return SQLGenResult(
        sql=sql,
        prompt_version="sql_gen_v1",
        model_deployment="test-deploy",
        latency_ms=1.0,
    )


def _make_answer_result() -> AnswerResult:
    return AnswerResult(
        answer="Article A has 42 comments.",
        caveats=["Sentiment is averaged"],
        prompt_version="answer_gen_v1",
        model_deployment="test-deploy",
        latency_ms=1.0,
    )


def _build_pipeline(monkeypatch):
    """Build a pipeline with all LLM services mocked out."""
    # Prevent real LLM construction in each service
    for mod in [intent_module, sql_gen_module, answer_module, vs_module]:
        monkeypatch.setattr(mod, "LLMService", MagicMock(side_effect=ValueError("no config")))
    return pipeline_module.TalkToDataPipeline()


async def test_pipeline_happy_path(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.95,
        "reason": "matches article domain",
    })
    monkeypatch.setattr(metadata_stage_module, "get_context_for_views", AsyncMock(return_value=MOCK_METADATA))
    pipeline.sql_generation_service.generate = AsyncMock(return_value=_make_sql_result(SAFE_SQL))
    monkeypatch.setattr(execution_stage_module, "execute_query", AsyncMock(return_value=MOCK_ROWS))
    pipeline.answer_service.generate = AsyncMock(return_value=_make_answer_result())

    response = await pipeline.run(AskRequest(question="Which articles have the most comments?"))

    assert response.refused is False
    assert response.answer == "Article A has 42 comments."
    assert "Sentiment" in response.caveats[0]

    trace = response.trace
    assert trace.question == "Which articles have the most comments?"
    assert trace.answerable is True
    assert trace.selected_views == ["analytics.vw_article_engagement"]
    assert trace.generated_sql == SAFE_SQL
    assert trace.validation_result is not None
    assert trace.validation_result.passed is True
    assert trace.executed_sql == SAFE_SQL
    assert trace.execution_status == "success"
    assert trace.row_count == 2
    assert trace.answer == "Article A has 42 comments."
    assert trace.latency_ms.total_ms is not None
    assert trace.prompt_versions.get("intent") == "intent_v1"
    assert trace.prompt_versions.get("sql_generation") == "sql_gen_v1"
    assert trace.prompt_versions.get("answer_generation") == "answer_gen_v1"
    assert "Access context is captured" in trace.access_enforcement_note


async def test_pipeline_refused_at_intent(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)
    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(False))

    response = await pipeline.run(AskRequest(question="What will engagement be next year?"))

    assert response.refused is True
    assert response.refusal_reason == "Out of scope"
    trace = response.trace
    assert trace.answerable is False
    assert trace.execution_status == "refused"
    # Pipeline must not have proceeded beyond intent
    assert trace.selected_views == []
    assert trace.generated_sql is None
    assert trace.latency_ms.total_ms is not None


async def test_pipeline_refused_at_sql_validation(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.9,
        "reason": "ok",
    })
    monkeypatch.setattr(metadata_stage_module, "get_context_for_views", AsyncMock(return_value=MOCK_METADATA))
    pipeline.sql_generation_service.generate = AsyncMock(return_value=_make_sql_result(UNSAFE_SQL))
    # execute_query should never be called
    mock_exec = AsyncMock(return_value=[])
    monkeypatch.setattr(execution_stage_module, "execute_query", mock_exec)

    response = await pipeline.run(AskRequest(question="Drop all articles"))

    assert response.refused is True
    assert "SQL validation failed" in response.refusal_reason
    trace = response.trace
    assert trace.validation_result is not None
    assert trace.validation_result.passed is False
    assert trace.execution_status == "refused"
    assert trace.executed_sql is None
    mock_exec.assert_not_awaited()


async def test_pipeline_refused_when_no_sql_generated(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.5,
        "reason": "ok",
    })
    monkeypatch.setattr(metadata_stage_module, "get_context_for_views", AsyncMock(return_value=MOCK_METADATA))
    pipeline.sql_generation_service.generate = AsyncMock(return_value=_make_sql_result(""))

    response = await pipeline.run(AskRequest(question="some question"))

    assert response.refused is True
    assert "no query" in response.refusal_reason.lower()


async def test_pipeline_refused_when_no_views_selected(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": [],
        "confidence": 0.5,
        "reason": "nothing matched",
    })

    response = await pipeline.run(AskRequest(question="some question"))

    assert response.refused is True
    assert "views" in response.refusal_reason.lower()


async def test_pipeline_trace_has_user_context(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(False))

    response = await pipeline.run(
        AskRequest(question="test", user_context="role=analyst; team=editorial")
    )

    assert response.trace.user_context == "role=analyst; team=editorial"


async def test_pipeline_refused_when_low_confidence(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.3,
        "reason": "ambiguous question",
    })

    response = await pipeline.run(AskRequest(question="tell me something interesting"))

    assert response.refused is True
    assert "confidence" in response.refusal_reason.lower()
    assert response.trace.execution_status == "refused"


async def test_pipeline_execution_failure_refuses(monkeypatch):
    pipeline = _build_pipeline(monkeypatch)

    pipeline.intent_service.classify = AsyncMock(return_value=_make_intent(True))
    pipeline.view_selection_service.select_views = AsyncMock(return_value={
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.9,
        "reason": "ok",
    })
    monkeypatch.setattr(metadata_stage_module, "get_context_for_views", AsyncMock(return_value=MOCK_METADATA))
    pipeline.sql_generation_service.generate = AsyncMock(return_value=_make_sql_result(SAFE_SQL))
    monkeypatch.setattr(execution_stage_module, "execute_query", AsyncMock(side_effect=RuntimeError("DB down")))

    response = await pipeline.run(AskRequest(question="top articles"))

    assert response.refused is True
    assert "execution failed" in response.refusal_reason.lower()
    assert response.trace.execution_status == "failed"
    assert "DB down" in response.trace.error
