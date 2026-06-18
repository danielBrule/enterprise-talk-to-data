import pytest
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.prompts.intent import _KNOWN_VIEWS
from backend.app.services.metadata_service import get_metrics_metadata

client = TestClient(app)


def test_metadata_views_endpoint():
    """Test GET /api/v0/metadata/views"""
    response = client.get("/api/v0/metadata/views")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_metadata_metrics_endpoint():
    """Test GET /api/v0/metadata/metrics"""
    response = client.get("/api/v0/metadata/metrics")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_metadata_glossary_endpoint():
    """Test GET /api/v0/metadata/glossary"""
    response = client.get("/api/v0/metadata/glossary")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_intent_prompt_views_match_metadata():
    """Catch drift between _KNOWN_VIEWS in the intent prompt and the metrics metadata files."""
    prompt_views = {v.strip() for v in _KNOWN_VIEWS.split(",")}
    metadata = await get_metrics_metadata()
    metadata_views = {m["view_name"] for m in metadata if "view_name" in m}

    assert prompt_views == metadata_views, (
        f"Intent prompt _KNOWN_VIEWS is out of sync with metrics metadata.\n"
        f"In prompt only: {prompt_views - metadata_views}\n"
        f"In metadata only: {metadata_views - prompt_views}"
    )
