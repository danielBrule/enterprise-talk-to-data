"""
Tests for GET /health.

All external dependencies (database, metadata files) are mocked so the test
suite runs without Azure credentials.
"""
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


# ── health_service unit tests ──────────────────────────────────────────────────

async def test_run_health_checks_all_ok(monkeypatch):
    import backend.app.services.health_service as svc

    monkeypatch.setattr(svc, "_check_database", AsyncMock(return_value={"status": "ok", "detail": "Connected — SELECT 1 in 5ms"}))
    monkeypatch.setattr(svc, "_check_metadata", AsyncMock(return_value={"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"}))
    monkeypatch.setattr(svc, "_check_llm_config", lambda: {"status": "ok", "detail": "All 3 task deployments configured"})

    result = await svc.run_health_checks()

    assert result["status"] == "ok"
    assert result["checks"]["database"]["status"] == "ok"
    assert result["checks"]["llm_config"]["status"] == "ok"
    assert result["checks"]["metadata"]["status"] == "ok"
    assert "timestamp" in result


async def test_run_health_checks_db_error_gives_error_status(monkeypatch):
    import backend.app.services.health_service as svc

    monkeypatch.setattr(svc, "_check_database", AsyncMock(return_value={"status": "error", "detail": "Connection refused"}))
    monkeypatch.setattr(svc, "_check_metadata", AsyncMock(return_value={"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"}))
    monkeypatch.setattr(svc, "_check_llm_config", lambda: {"status": "ok", "detail": "All 3 task deployments configured"})

    result = await svc.run_health_checks()

    assert result["status"] == "error"
    assert result["checks"]["database"]["status"] == "error"


async def test_run_health_checks_llm_config_error_gives_error_status(monkeypatch):
    import backend.app.services.health_service as svc

    monkeypatch.setattr(svc, "_check_database", AsyncMock(return_value={"status": "ok", "detail": "Connected — SELECT 1 in 5ms"}))
    monkeypatch.setattr(svc, "_check_metadata", AsyncMock(return_value={"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"}))
    monkeypatch.setattr(svc, "_check_llm_config", lambda: {"status": "error", "detail": "Missing env vars: AZURE_OPENAI_API_KEY"})

    result = await svc.run_health_checks()

    assert result["status"] == "error"
    assert result["checks"]["llm_config"]["status"] == "error"


async def test_run_health_checks_metadata_error_gives_degraded_status(monkeypatch):
    """Metadata failure is non-critical — overall status becomes 'degraded', not 'error'."""
    import backend.app.services.health_service as svc

    monkeypatch.setattr(svc, "_check_database", AsyncMock(return_value={"status": "ok", "detail": "Connected — SELECT 1 in 5ms"}))
    monkeypatch.setattr(svc, "_check_metadata", AsyncMock(return_value={"status": "error", "detail": "YAML directory not found"}))
    monkeypatch.setattr(svc, "_check_llm_config", lambda: {"status": "ok", "detail": "All 3 task deployments configured"})

    result = await svc.run_health_checks()

    assert result["status"] == "degraded"
    assert result["checks"]["metadata"]["status"] == "error"


# ── _check_llm_config unit tests ───────────────────────────────────────────────

def test_check_llm_config_all_present(monkeypatch):
    import backend.app.services.health_service as svc

    mock_settings = MagicMock()
    mock_settings.azure_openai_endpoint = "https://example.openai.azure.com"
    mock_settings.azure_openai_api_key = "key-abc"
    mock_settings.azure_openai_schema_retrieval_deployment = "schema-dep"
    mock_settings.azure_openai_sql_generation_deployment = "sql-dep"
    mock_settings.azure_openai_summary_deployment = "summary-dep"
    monkeypatch.setattr(svc, "settings", mock_settings)

    result = svc._check_llm_config()
    assert result["status"] == "ok"
    assert "3 task deployments" in result["detail"]


def test_check_llm_config_missing_key(monkeypatch):
    import backend.app.services.health_service as svc

    mock_settings = MagicMock()
    mock_settings.azure_openai_endpoint = "https://example.openai.azure.com"
    mock_settings.azure_openai_api_key = ""  # missing
    mock_settings.azure_openai_schema_retrieval_deployment = "schema-dep"
    mock_settings.azure_openai_sql_generation_deployment = "sql-dep"
    mock_settings.azure_openai_summary_deployment = "summary-dep"
    monkeypatch.setattr(svc, "settings", mock_settings)

    result = svc._check_llm_config()
    assert result["status"] == "error"
    assert "AZURE_OPENAI_API_KEY" in result["detail"]


# ── HTTP endpoint tests ────────────────────────────────────────────────────────

def test_health_endpoint_returns_200_when_ok(monkeypatch):
    import backend.app.main as main_module

    async def _mock_checks():
        return {
            "status": "ok",
            "timestamp": "2026-06-25T00:00:00+00:00",
            "checks": {
                "database": {"status": "ok", "detail": "Connected"},
                "llm_config": {"status": "ok", "detail": "All 3 task deployments configured"},
                "metadata": {"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"},
            },
        }

    monkeypatch.setattr(main_module, "run_health_checks", _mock_checks)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_health_endpoint_returns_503_when_error(monkeypatch):
    import backend.app.main as main_module

    async def _mock_checks():
        return {
            "status": "error",
            "timestamp": "2026-06-25T00:00:00+00:00",
            "checks": {
                "database": {"status": "error", "detail": "Connection refused"},
                "llm_config": {"status": "ok", "detail": "All 3 task deployments configured"},
                "metadata": {"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"},
            },
        }

    monkeypatch.setattr(main_module, "run_health_checks", _mock_checks)
    response = client.get("/health")
    assert response.status_code == 503
    assert response.json()["status"] == "error"


def test_health_endpoint_returns_200_when_degraded(monkeypatch):
    """Degraded = metadata down but core up; still 200 so load balancer keeps routing."""
    import backend.app.main as main_module

    async def _mock_checks():
        return {
            "status": "degraded",
            "timestamp": "2026-06-25T00:00:00+00:00",
            "checks": {
                "database": {"status": "ok", "detail": "Connected"},
                "llm_config": {"status": "ok", "detail": "All 3 task deployments configured"},
                "metadata": {"status": "error", "detail": "YAML directory not found"},
            },
        }

    monkeypatch.setattr(main_module, "run_health_checks", _mock_checks)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "degraded"


def test_health_response_shape(monkeypatch):
    """Verify the response always contains status, timestamp, and all three check keys."""
    import backend.app.main as main_module

    async def _mock_checks():
        return {
            "status": "ok",
            "timestamp": "2026-06-25T00:00:00+00:00",
            "checks": {
                "database": {"status": "ok", "detail": "Connected"},
                "llm_config": {"status": "ok", "detail": "All 3 task deployments configured"},
                "metadata": {"status": "ok", "detail": "4 view schema(s), 4 metric definition(s) loaded"},
            },
        }

    monkeypatch.setattr(main_module, "run_health_checks", _mock_checks)
    body = client.get("/health").json()
    assert "status" in body
    assert "timestamp" in body
    assert set(body["checks"].keys()) == {"database", "llm_config", "metadata"}
    for check in body["checks"].values():
        assert "status" in check
        assert "detail" in check
