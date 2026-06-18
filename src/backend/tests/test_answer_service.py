import json
import pytest
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.answer as answer_service_module
from backend.app.prompts.answer_generation import PROMPT_VERSION

SAMPLE_RESULTS = [
    {"article_id": 1, "title": "Article One", "comment_count": 100},
    {"article_id": 2, "title": "Article Two", "comment_count": 80},
]

SAMPLE_METADATA = {
    "analytics.vw_article_engagement": {
        "limitations": [
            "Sentiment is averaged at the comment level.",
            "Articles without comments appear with zero counts.",
        ]
    }
}


@pytest.mark.asyncio
async def test_generate_answer(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_summary = AsyncMock(
        return_value=json.dumps({
            "answer": "Article One has the most comments with 100.",
            "caveats": ["Sentiment is averaged at the comment level."],
        })
    )
    monkeypatch.setattr(answer_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = answer_service_module.AnswerService()
    result = await service.generate(
        question="Which articles have the most comments?",
        sql="SELECT TOP 10 article_id FROM analytics.vw_article_engagement",
        results=SAMPLE_RESULTS,
        metadata_context=SAMPLE_METADATA,
    )

    assert "Article One" in result.answer
    assert result.caveats
    assert result.prompt_version == PROMPT_VERSION
    assert result.latency_ms >= 0


@pytest.mark.asyncio
async def test_generate_empty_results(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_summary = AsyncMock(
        return_value=json.dumps({
            "answer": "No results found for this query.",
            "caveats": [],
        })
    )
    monkeypatch.setattr(answer_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = answer_service_module.AnswerService()
    result = await service.generate("q", "sql", [], SAMPLE_METADATA)

    assert "No results" in result.answer


@pytest.mark.asyncio
async def test_generate_collects_metadata_caveats(monkeypatch):
    """Metadata limitations must appear in the prompt even if LLM omits them."""
    mock_llm = MagicMock()
    mock_llm.generate_summary = AsyncMock(
        return_value=json.dumps({
            "answer": "Some answer.",
            "caveats": ["Sentiment is averaged at the comment level."],
        })
    )
    monkeypatch.setattr(answer_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = answer_service_module.AnswerService()
    result = await service.generate("q", "sql", SAMPLE_RESULTS, SAMPLE_METADATA)

    assert result.caveats  # at least one caveat returned


@pytest.mark.asyncio
async def test_generate_bad_json_falls_back(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_summary = AsyncMock(return_value="not valid json")
    monkeypatch.setattr(answer_service_module, "LLMService", MagicMock(return_value=mock_llm))

    service = answer_service_module.AnswerService()
    result = await service.generate("q", "sql", SAMPLE_RESULTS, SAMPLE_METADATA)

    # Fallback answer mentions row count
    assert "2 row" in result.answer
    assert result.prompt_version == PROMPT_VERSION


@pytest.mark.asyncio
async def test_generate_llm_unavailable(monkeypatch):
    monkeypatch.setattr(
        answer_service_module, "LLMService", MagicMock(side_effect=ValueError("no config"))
    )

    service = answer_service_module.AnswerService()
    result = await service.generate("q", "sql", SAMPLE_RESULTS, SAMPLE_METADATA)

    assert "2 row" in result.answer
    assert result.model_deployment == "none"
    # Metadata caveats should still be surfaced
    assert result.caveats
