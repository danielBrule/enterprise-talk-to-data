import pytest
from fastapi.testclient import TestClient

from backend.app.main import app

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
