import json
import pytest
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.sql_generation as sql_gen_module
from backend.app.prompts.sql_generation import PROMPT_VERSION

SAMPLE_METADATA = {
    "analytics.vw_article_engagement": {
        "purpose": "Article engagement metrics",
        "description": "Article engagement",
        "columns": [
            {"name": "article_id", "description": "Primary identifier"},
            {"name": "title", "description": "Article title"},
            {"name": "comment_count", "description": "Total comments"},
            {"name": "avg_comment_sentiment", "description": "Average sentiment"},
        ],
        "limitations": ["Sentiment averaged at comment level"],
    }
}

SAFE_SQL = (
    "SELECT TOP 10 article_id, title, comment_count "
    "FROM analytics.vw_article_engagement ORDER BY comment_count DESC"
)


@pytest.mark.asyncio
async def test_generate_returns_sql(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value=json.dumps({"sql": SAFE_SQL}))
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate(
        question="Which articles have the most comments?",
        metadata_context=SAMPLE_METADATA,
    )

    assert result.sql == SAFE_SQL
    assert result.prompt_version == PROMPT_VERSION
    assert result.latency_ms >= 0


@pytest.mark.asyncio
async def test_generate_metadata_included_in_prompt(monkeypatch):
    """Verify that view name and column names are sent to the LLM."""
    mock_llm = MagicMock()
    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL})

    mock_llm.generate_sql_generation = capture_messages
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    await service.generate(
        question="Show articles by comment count",
        metadata_context=SAMPLE_METADATA,
    )

    assert captured, "LLM was never called"
    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "analytics.vw_article_engagement" in prompt_text
    assert "comment_count" in prompt_text


@pytest.mark.asyncio
async def test_generate_strips_markdown_fences(monkeypatch):
    raw_response = "```json\n" + json.dumps({"sql": SAFE_SQL}) + "\n```"
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value=raw_response)
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("q", SAMPLE_METADATA)

    assert result.sql == SAFE_SQL


@pytest.mark.asyncio
async def test_generate_bad_json_returns_empty(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value="not json")
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("question", SAMPLE_METADATA)

    assert result.sql == ""
    assert result.prompt_version == PROMPT_VERSION


@pytest.mark.asyncio
async def test_generate_llm_unavailable_returns_empty(monkeypatch):
    monkeypatch.setattr(
        sql_gen_module, "LLMService", MagicMock(side_effect=ValueError("no config"))
    )

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("question", {})

    assert result.sql == ""
    assert result.model_deployment == "none"
