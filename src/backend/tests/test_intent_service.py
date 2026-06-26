import json
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.intent as intent_service_module
from backend.app.prompts.intent import PROMPT_VERSION

_MOCK_USAGE = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "model_name": "gpt-4o"}


async def test_classify_answerable(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=(json.dumps({
            "answerable": True,
            "reason": "Question is about article engagement",
            "domain": "article_engagement",
            "suggested_metrics": ["comment_count", "avg_comment_sentiment"],
        }), _MOCK_USAGE)
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Which articles have the most comments?")

    assert result.answerable is True
    assert result.domain == "article_engagement"
    assert "comment_count" in result.suggested_metrics
    assert result.prompt_version == PROMPT_VERSION
    assert result.latency_ms >= 0
    assert result.token_usage == _MOCK_USAGE


async def test_classify_not_answerable(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=(json.dumps({
            "answerable": False,
            "reason": "Requires external stock data",
            "domain": "unknown",
            "suggested_metrics": [],
        }), _MOCK_USAGE)
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("What will the stock price be next week?")

    assert result.answerable is False
    assert result.domain == "unknown"
    assert result.reason == "Requires external stock data"


async def test_classify_llm_unavailable(monkeypatch):
    monkeypatch.setattr(
        intent_service_module, "LLMService", MagicMock(side_effect=ValueError("no config"))
    )

    service = intent_service_module.IntentService()
    result = await service.classify("Any question")

    assert result.answerable is False
    assert result.model_deployment == "none"
    assert "LLM not configured" in result.reason


async def test_classify_bad_json_falls_back(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(return_value=("not valid json {{{", _MOCK_USAGE))
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Any question")

    # Parse failure: refuse, no crash
    assert result.answerable is False
    assert "parse failed" in result.reason.lower()


async def test_classify_prompt_version_in_result(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=(json.dumps({
            "answerable": True,
            "reason": "ok",
            "domain": "ingestion_errors",
            "suggested_metrics": [],
        }), _MOCK_USAGE)
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("List recent ingestion errors")

    assert result.prompt_version == PROMPT_VERSION


# ── conversation history ───────────────────────────────────────────────────────

async def test_classify_injects_conversation_history_into_prompt(monkeypatch):
    """Prior questions must appear in the prompt sent to the LLM."""
    from backend.app.models.talk_to_data import ConversationTurn

    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({
            "answerable": True, "reason": "follow-up", "domain": "article_engagement", "suggested_metrics": []
        }), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = capture_messages
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    history = [ConversationTurn(question="Which articles have the most comments?", sql=None, answer=None)]
    service = intent_service_module.IntentService()
    await service.classify("What about last month?", conversation_history=history)

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "Which articles have the most comments?" in prompt_text


async def test_classify_without_history_has_no_context_section(monkeypatch):
    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({
            "answerable": True, "reason": "ok", "domain": "article_engagement", "suggested_metrics": []
        }), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = capture_messages
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    await service.classify("Which articles have comments?")

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "Prior conversation" not in prompt_text


async def test_classify_contributor_domain(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(
        return_value=(json.dumps({
            "answerable": True,
            "reason": "Top contributors by comment count",
            "domain": "contributor_behaviour",
            "suggested_metrics": ["comment_count", "distinct_article_count"],
        }), _MOCK_USAGE)
    )
    monkeypatch.setattr(intent_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = intent_service_module.IntentService()
    result = await service.classify("Who are the most active contributors?")

    assert result.answerable is True
    assert result.domain == "contributor_behaviour"
