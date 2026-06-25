from fastapi.testclient import TestClient

from backend.app.api import routes
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint(monkeypatch):
    import backend.app.main as main_module

    async def _mock_ok():
        return {
            "status": "ok",
            "timestamp": "2026-06-25T00:00:00+00:00",
            "checks": {
                "database": {"status": "ok", "detail": "Connected"},
                "llm_config": {"status": "ok", "detail": "All 3 task deployments configured"},
                "metadata": {"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"},
            },
        }

    monkeypatch.setattr(main_module, "run_health_checks", _mock_ok)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert "checks" in response.json()


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_list_articles_endpoint(monkeypatch):
    from datetime import datetime

    async def mock_list_articles(limit):
        return [
            {
                "article_id": 1,
                "title": "Test Article",
                "publication_date": datetime.now(),
                "insert_date": datetime.now(),
                "comment_count": 10,
                "avg_comment_sentiment": 0.5,
                "total_replies": 5,
                "keyword_count": 3,
            }
        ]

    monkeypatch.setattr(routes, "list_articles", mock_list_articles)
    response = client.get("/api/v0/articles")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["article_id"] == 1
    assert data[0]["title"] == "Test Article"


def test_read_article_not_found(monkeypatch):
    async def mock_get_article(article_id):
        return None

    monkeypatch.setattr(routes, "get_article", mock_get_article)
    response = client.get("/api/v0/articles/999")

    assert response.status_code == 404
    # The actual error message from FastAPI's default 404 handler
    assert "not found" in response.text


def test_get_views_metadata_endpoint(monkeypatch):
    async def mock_get_views_metadata():
        return [
            {
                "view_name": "analytics.vw_article_engagement",
                "columns": [
                    {"name": "article_id", "description": "Article ID"},
                    {"name": "comment_count", "description": "Comment count"},
                ],
            }
        ]

    monkeypatch.setattr(routes, "get_views_metadata", mock_get_views_metadata)
    response = client.get("/api/v0/metadata/views")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["view_name"] == "analytics.vw_article_engagement"


# ── /ask endpoint tests ────────────────────────────────────────────────────────

def test_ask_endpoint_returns_answer(monkeypatch):
    """A well-formed answerable question returns an answer with a trace."""
    from backend.app.services.talk_to_data_pipeline import TalkToDataPipeline
    from backend.app.models.talk_to_data import AskRequest, AskResponse
    from backend.app.models.trace import TraceRecord

    async def mock_run(self, request: AskRequest, user) -> AskResponse:
        trace = TraceRecord(
            question=request.question,
            answerable=True,
            intent="article_engagement",
            selected_views=["analytics.vw_article_engagement"],
            generated_sql="SELECT TOP 10 article_id FROM analytics.vw_article_engagement",
            executed_sql="SELECT TOP 10 article_id FROM analytics.vw_article_engagement",
            execution_status="success",
            row_count=10,
            answer="Article A has the most comments.",
            caveats=["Sentiment is averaged"],
        )
        return AskResponse(
            answer="Article A has the most comments.",
            caveats=["Sentiment is averaged"],
            refused=False,
            trace=trace,
        )

    monkeypatch.setattr(TalkToDataPipeline, "run", mock_run)
    response = client.post(
        "/api/v0/ask",
        json={"question": "Which articles have the most comments?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["refused"] is False
    assert data["answer"] == "Article A has the most comments."
    assert data["caveats"]
    assert "trace" in data
    trace = data["trace"]
    assert trace["question"] == "Which articles have the most comments?"
    assert trace["execution_status"] == "success"
    assert trace["answerable"] is True
    assert trace["access_enforcement_note"]  # non-empty


def test_ask_endpoint_returns_refusal(monkeypatch):
    """An out-of-scope question returns refused=True with a refusal reason and trace."""
    from backend.app.services.talk_to_data_pipeline import TalkToDataPipeline
    from backend.app.models.talk_to_data import AskRequest, AskResponse
    from backend.app.models.trace import TraceRecord

    async def mock_run(self, request: AskRequest, user) -> AskResponse:
        trace = TraceRecord(
            question=request.question,
            answerable=False,
            intent="unknown",
            execution_status="refused",
            refusal_reason="This question requires forecasting, which is not supported.",
        )
        return AskResponse(
            refused=True,
            refusal_reason="This question requires forecasting, which is not supported.",
            trace=trace,
        )

    monkeypatch.setattr(TalkToDataPipeline, "run", mock_run)
    response = client.post(
        "/api/v0/ask",
        json={"question": "What will engagement look like next year?"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["refused"] is True
    assert "forecasting" in data["refusal_reason"]
    assert data["answer"] is None
    trace = data["trace"]
    assert trace["answerable"] is False
    assert trace["execution_status"] == "refused"


def test_ask_endpoint_with_user_context(monkeypatch):
    """user_context is captured in the trace."""
    from backend.app.services.talk_to_data_pipeline import TalkToDataPipeline
    from backend.app.models.talk_to_data import AskRequest, AskResponse
    from backend.app.models.trace import TraceRecord

    async def mock_run(self, request: AskRequest, user) -> AskResponse:
        trace = TraceRecord(
            question=request.question,
            user_context=request.user_context,
            answerable=False,
            execution_status="refused",
            refusal_reason="out of scope",
        )
        return AskResponse(refused=True, refusal_reason="out of scope", trace=trace)

    monkeypatch.setattr(TalkToDataPipeline, "run", mock_run)
    response = client.post(
        "/api/v0/ask",
        json={"question": "test", "user_context": "role=analyst"},
    )

    assert response.status_code == 200
    assert response.json()["trace"]["user_context"] == "role=analyst"


def test_ask_endpoint_missing_question_returns_422():
    """Request body without 'question' field should return HTTP 422."""
    response = client.post("/api/v0/ask", json={})
    assert response.status_code == 422
