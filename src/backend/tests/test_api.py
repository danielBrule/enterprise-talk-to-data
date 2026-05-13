from fastapi.testclient import TestClient

from backend.app.api import routes
from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


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
                    {"name": "comment_count", "description": "Comment count"}
                ]
            }
        ]

    monkeypatch.setattr(routes, "get_views_metadata", mock_get_views_metadata)
    response = client.get("/api/v0/metadata/views")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["view_name"] == "analytics.vw_article_engagement"


def test_select_views_endpoint(monkeypatch):
    """Test the view selection endpoint."""
    from backend.app.services.view_selection_service import ViewSelectionService

    async def mock_select_views(self, question):
        return {
            "question": question,
            "selected_views": ["analytics.vw_article_engagement"],
            "reason": "Question refers to articles and comment volume."
        }

    monkeypatch.setattr(ViewSelectionService, "select_views", mock_select_views)
    response = client.post("/api/v0/metadata/select-views?question=Which+articles+have+the+most+comments")

    assert response.status_code == 200
    data = response.json()
    assert data["question"] == "Which articles have the most comments"
    assert "analytics.vw_article_engagement" in data["selected_views"]
    assert len(data["reason"]) > 0
