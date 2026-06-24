from unittest.mock import MagicMock, AsyncMock

import backend.app.services.article_service as article_service
import backend.app.services.contributor_service as contributor_service
import backend.app.services.ingestion_error_service as ingestion_error_service
import backend.app.services.keyword_service as keyword_service
import backend.app.stages.view_selection as view_selection_service


def make_conn_mock(result):
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute = AsyncMock(return_value=result)
    return mock_conn


async def test_list_articles_uses_connection(monkeypatch):
    mock_execute = AsyncMock(return_value=[{"article_id": 1}])
    monkeypatch.setattr(article_service, "execute_query", mock_execute)

    results = await article_service.list_articles(limit=5)

    assert results == [{"article_id": 1}]
    mock_execute.assert_awaited_once()


async def test_get_article_returns_none_when_not_found(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[])

    monkeypatch.setattr(
        article_service,
        "execute_query",
        mock_execute_query,
    )

    result = await article_service.get_article("missing")

    assert result is None
    mock_execute_query.assert_awaited_once()


async def test_list_keywords_uses_connection(monkeypatch):
    mock_execute = AsyncMock(return_value=[{"keyword_id": 1}])
    monkeypatch.setattr(keyword_service, "execute_query", mock_execute)

    results = await keyword_service.list_keywords(limit=5)

    assert results == [{"keyword_id": 1}]
    mock_execute.assert_awaited_once()


async def test_list_contributors_uses_connection(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[{"contributor_id": "c1"}])

    monkeypatch.setattr(
        contributor_service,
        "execute_query",
        mock_execute_query,
    )

    results = await contributor_service.list_contributors(limit=5)

    assert results == [{"contributor_id": "c1"}]
    mock_execute_query.assert_awaited_once()


async def test_list_ingestion_errors_uses_connection(monkeypatch):
    mock_execute_query = AsyncMock(return_value=[{"error_id": "e1"}])

    monkeypatch.setattr(
        ingestion_error_service,
        "execute_query",
        mock_execute_query,
    )

    results = await ingestion_error_service.list_ingestion_errors(limit=5)

    assert results == [{"error_id": "e1"}]
    mock_execute_query.assert_awaited_once()


async def test_view_selection_service(monkeypatch):
    # Mock the metadata service
    mock_metrics = [
        {
            "view_name": "analytics.vw_article_engagement",
            "category": "article engagement",
            "purpose": "Provides article-level engagement metrics",
            "columns": [
                {"name": "article_id", "description": "Primary article identifier"},
                {"name": "comment_count", "description": "Total number of comments"},
            ],
            "example_questions": [
                {
                    "natural_language_question": "Which articles have the most comments?",
                    "expected_view": "analytics.vw_article_engagement",
                }
            ],
        }
    ]
    monkeypatch.setattr(
        view_selection_service,
        "get_metrics_metadata",
        AsyncMock(return_value=mock_metrics),
    )

    # Mock the LLM service
    _mock_usage = {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "model_name": "gpt-4o"}
    mock_llm_response = '{"selected_views": ["analytics.vw_article_engagement"], "reason": "Question refers to articles and comment volume."}'
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(return_value=(mock_llm_response, _mock_usage))
    monkeypatch.setattr(
        view_selection_service, "LLMService", MagicMock(return_value=mock_llm)
    )

    service = view_selection_service.ViewSelectionService()
    result = await service.select_views(
        "Which articles had the most comments last week?"
    )

    expected = {
        "question": "Which articles had the most comments last week?",
        "selected_views": ["analytics.vw_article_engagement"],
        "confidence": 0.0,
        "reason": "Question refers to articles and comment volume.",
        "token_usage": _mock_usage,
    }
    assert result == expected


async def test_view_selection_fallback_when_llm_not_configured(monkeypatch):
    """Test that service gracefully handles missing LLM configuration."""
    mock_metrics = [
        {
            "view_name": "analytics.vw_article_engagement",
            "category": "article engagement",
            "purpose": "Provides article-level engagement metrics",
            "columns": [],
        }
    ]
    monkeypatch.setattr(
        view_selection_service,
        "get_metrics_metadata",
        AsyncMock(return_value=mock_metrics),
    )

    # Mock LLMService to raise ValueError (simulating missing config)
    def mock_llm_init_error():
        raise ValueError("Azure OpenAI configuration is incomplete")

    monkeypatch.setattr(
        view_selection_service, "LLMService", MagicMock(side_effect=mock_llm_init_error)
    )

    service = view_selection_service.ViewSelectionService()
    result = await service.select_views("What is the engagement?")

    # Should still return a result with fallback
    assert result["question"] == "What is the engagement?"
    assert result["selected_views"] == ["analytics.vw_article_engagement"]
    assert "LLM not configured" in result["reason"]


async def test_view_selection_with_multiple_views(monkeypatch):
    """Test that service can select multiple views."""
    mock_metrics = [
        {
            "view_name": "analytics.vw_article_engagement",
            "category": "article engagement",
            "purpose": "Article engagement metrics",
            "columns": [],
            "example_questions": [],
        },
        {
            "view_name": "analytics.vw_keyword_engagement",
            "category": "keyword engagement",
            "purpose": "Keyword engagement metrics",
            "columns": [],
            "example_questions": [],
        },
    ]
    monkeypatch.setattr(
        view_selection_service,
        "get_metrics_metadata",
        AsyncMock(return_value=mock_metrics),
    )

    # Mock LLM to select both views
    mock_llm_response = '{"selected_views": ["analytics.vw_article_engagement", "analytics.vw_keyword_engagement"], "reason": "Question requires both article and keyword data."}'
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(return_value=(mock_llm_response, {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "model_name": "gpt-4o"}))
    monkeypatch.setattr(
        view_selection_service, "LLMService", MagicMock(return_value=mock_llm)
    )

    service = view_selection_service.ViewSelectionService()
    result = await service.select_views("Show articles and keywords trending together")

    assert len(result["selected_views"]) == 2
    assert "analytics.vw_article_engagement" in result["selected_views"]
    assert "analytics.vw_keyword_engagement" in result["selected_views"]


async def test_view_selection_invalid_json_response(monkeypatch):
    """Test that service handles invalid JSON from LLM gracefully."""
    mock_metrics = [
        {
            "view_name": "analytics.vw_article_engagement",
            "category": "article engagement",
            "purpose": "Article engagement metrics",
            "columns": [],
            "example_questions": [],
        }
    ]
    monkeypatch.setattr(
        view_selection_service,
        "get_metrics_metadata",
        AsyncMock(return_value=mock_metrics),
    )

    # Mock LLM to return invalid JSON
    mock_llm = MagicMock()
    mock_llm.generate_schema_retrieval = AsyncMock(return_value=("This is not JSON", {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "model_name": "gpt-4o"}))
    monkeypatch.setattr(
        view_selection_service, "LLMService", MagicMock(return_value=mock_llm)
    )

    service = view_selection_service.ViewSelectionService()
    result = await service.select_views("What is the engagement?")

    assert result["question"] == "What is the engagement?"
    assert result["selected_views"] == []
    assert "Failed to parse" in result["reason"]


async def test_view_selection_no_metrics_available(monkeypatch):
    """Test that service handles missing metrics gracefully."""
    monkeypatch.setattr(
        view_selection_service, "get_metrics_metadata", AsyncMock(return_value=[])
    )

    # Mock LLMService
    mock_llm = MagicMock()
    monkeypatch.setattr(
        view_selection_service, "LLMService", MagicMock(return_value=mock_llm)
    )

    service = view_selection_service.ViewSelectionService()
    result = await service.select_views("What is the engagement?")

    assert result["question"] == "What is the engagement?"
    assert result["selected_views"] == []
    assert "LLM not configured or no metadata available" in result["reason"]
