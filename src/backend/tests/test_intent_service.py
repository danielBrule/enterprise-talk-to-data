import json
import pytest
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.intent as intent_service_module
from backend.app.stages.intent import IntentResult
from backend.app.prompts.intent import PROMPT_VERSION


@pytest.mark.asyncio
async def test_classify_answerable(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=json.dumps({
            "answerable": True,
            "reason": "Question is about article engagement",
            "domain": "article_engagement",
            "suggested_metrics": ["comment_count", "avg_comment_sentiment"],
        })
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Which articles have the most comments?")

    assert result.answerable is True
    assert result.domain == "article_engagement"
    assert "comment_count" in result.suggested_metrics
    assert result.prompt_version == PROMPT_VERSION
    assert result.latency_ms >= 0


@pytest.mark.asyncio
async def test_classify_not_answerable(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=json.dumps({
            "answerable": False,
            "reason": "Requires external stock data",
            "domain": "unknown",
            "suggested_metrics": [],
        })
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("What will the stock price be next week?")

    assert result.answerable is False
    assert result.domain == "unknown"
    assert result.reason == "Requires external stock data"


@pytest.mark.asyncio
async def test_classify_llm_unavailable(monkeypatch):
    monkeypatch.setattr(
        intent_service_module, "LLMService", MagicMock(side_effect=ValueError("no config"))
    )

    service = intent_service_module.IntentService()
    result = await service.classify("Any question")

    assert result.answerable is False
    assert result.model_deployment == "none"
    assert "LLM not configured" in result.reason


@pytest.mark.asyncio
async def test_classify_bad_json_falls_back(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(return_value="not valid json {{{")
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Any question")

    # Parse failure: refuse, no crash
    assert result.answerable is False
    assert "parse failed" in result.reason.lower()


@pytest.mark.asyncio
async def test_classify_prompt_version_in_result(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=json.dumps({
            "answerable": True,
            "reason": "ok",
            "domain": "ingestion_errors",
            "suggested_metrics": [],
        })
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("List recent ingestion errors")

    assert result.prompt_version == PROMPT_VERSION


@pytest.mark.asyncio
async def test_classify_contributor_domain(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=json.dumps({
            "answerable": True,
            "reason": "Top contributors by comment count",
            "domain": "contributor_behaviour",
            "suggested_metrics": ["comment_count", "distinct_article_count"],
        })
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Who are the most active contributors?")

    assert result.answerable is True
    assert result.domain == "contributor_behaviour"
