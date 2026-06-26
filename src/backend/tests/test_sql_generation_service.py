import json
from unittest.mock import AsyncMock, MagicMock

import backend.app.stages.sql_generation as sql_gen_module
from backend.app.prompts.sql_generation import PROMPT_VERSION

_MOCK_USAGE = {"prompt_tokens": 20, "completion_tokens": 10, "total_tokens": 30, "model_name": "gpt-4o"}

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


async def test_generate_returns_sql(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value=(json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE))
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate(
        question="Which articles have the most comments?",
        metadata_context=SAMPLE_METADATA,
    )

    assert result.sql == SAFE_SQL
    assert result.prompt_version == PROMPT_VERSION
    assert result.latency_ms >= 0
    assert result.token_usage == _MOCK_USAGE


async def test_generate_metadata_included_in_prompt(monkeypatch):
    """Verify that view name and column names are sent to the LLM."""
    mock_llm = MagicMock()
    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE

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


async def test_generate_strips_markdown_fences(monkeypatch):
    raw_response = "```json\n" + json.dumps({"sql": SAFE_SQL}) + "\n```"
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value=(raw_response, _MOCK_USAGE))
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("q", SAMPLE_METADATA)

    assert result.sql == SAFE_SQL


async def test_generate_bad_json_returns_empty(monkeypatch):
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(return_value=("not json", _MOCK_USAGE))
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("question", SAMPLE_METADATA)

    assert result.sql == ""
    assert result.prompt_version == PROMPT_VERSION


async def test_generate_llm_unavailable_returns_empty(monkeypatch):
    monkeypatch.setattr(
        sql_gen_module, "LLMService", MagicMock(side_effect=ValueError("no config"))
    )

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("question", {})

    assert result.sql == ""
    assert result.model_deployment == "none"


# ── conversation history ───────────────────────────────────────────────────────

async def test_generate_injects_conversation_history_into_prompt(monkeypatch):
    """Prior turns must appear in the prompt sent to the LLM."""
    from backend.app.models.talk_to_data import ConversationTurn

    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = capture_messages
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    history = [
        ConversationTurn(
            question="Which articles have the most comments?",
            sql="SELECT TOP 10 article_id FROM analytics.vw_article_engagement ORDER BY comment_count DESC",
            answer="Article A has the most comments.",
        )
    ]
    service = sql_gen_module.SQLGenerationService()
    await service.generate("What about last month?", SAMPLE_METADATA, conversation_history=history)

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "Which articles have the most comments?" in prompt_text
    assert "SELECT TOP 10 article_id" in prompt_text
    assert "Article A has the most comments" in prompt_text


async def test_generate_truncates_long_answers_in_history(monkeypatch):
    """Answers longer than MAX_HISTORY_ANSWER_CHARS (default 300) must be truncated in the prompt."""
    from backend.app.models.talk_to_data import ConversationTurn

    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = capture_messages
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    long_answer = "Article " + "X" * 400  # 408 chars — exceeds default 300-char limit
    history = [ConversationTurn(question="q", sql="SELECT TOP 1 article_id FROM analytics.vw_article_engagement", answer=long_answer)]
    service = sql_gen_module.SQLGenerationService()
    await service.generate("follow-up?", SAMPLE_METADATA, conversation_history=history)

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert long_answer not in prompt_text
    assert "…" in prompt_text


async def test_generate_caps_history_at_three_turns(monkeypatch):
    """Only the 3 most recent turns must appear; older turns must be dropped."""
    from backend.app.models.talk_to_data import ConversationTurn

    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = capture_messages
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    history = [ConversationTurn(question=f"question {i}", sql=None, answer=None) for i in range(5)]
    service = sql_gen_module.SQLGenerationService()
    await service.generate("current question", SAMPLE_METADATA, conversation_history=history)

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "question 4" in prompt_text  # most recent
    assert "question 3" in prompt_text
    assert "question 2" in prompt_text
    assert "question 1" not in prompt_text  # dropped (4th oldest)
    assert "question 0" not in prompt_text  # dropped (oldest)


async def test_generate_without_history_unchanged(monkeypatch):
    """No conversation_history must produce the same prompt as before (no history section)."""
    captured: list[list] = []

    async def capture_messages(messages, **kwargs):
        captured.append(messages)
        return json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE

    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = capture_messages
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    await service.generate("Which articles have comments?", SAMPLE_METADATA)

    prompt_text = " ".join(m["content"] for m in captured[0])
    assert "Prior conversation" not in prompt_text


# ── filters_applied ────────────────────────────────────────────────────────────

async def test_generate_returns_filters(monkeypatch):
    """Filters declared in the LLM response are surfaced in SQLGenResult.filters."""
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(
        return_value=(
            json.dumps({"sql": SAFE_SQL, "filters": ["publication_date >= 2025", "comment_count > 5"]}),
            _MOCK_USAGE,
        )
    )
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("Articles from 2025 with more than 5 comments?", SAMPLE_METADATA)

    assert result.filters == ["publication_date >= 2025", "comment_count > 5"]


async def test_generate_returns_empty_filters_when_no_where_clause(monkeypatch):
    """Empty filters list is returned when the LLM reports no WHERE conditions."""
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(
        return_value=(json.dumps({"sql": SAFE_SQL, "filters": []}), _MOCK_USAGE)
    )
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("Which articles have the most comments?", SAMPLE_METADATA)

    assert result.filters == []


async def test_generate_filters_defaults_to_empty_when_key_absent(monkeypatch):
    """If the LLM omits the 'filters' key (old response format), result.filters defaults to []."""
    mock_llm = MagicMock()
    mock_llm.generate_sql_generation = AsyncMock(
        return_value=(json.dumps({"sql": SAFE_SQL}), _MOCK_USAGE)
    )
    monkeypatch.setattr(sql_gen_module, "LLMService", MagicMock(return_value=mock_llm))

    service = sql_gen_module.SQLGenerationService()
    result = await service.generate("Which articles have the most comments?", SAMPLE_METADATA)

    assert result.filters == []
