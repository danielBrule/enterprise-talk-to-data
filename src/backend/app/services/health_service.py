"""
Health check service — probes each system dependency and returns a structured report.

Three checks:
- database   : executes SELECT 1 against Azure SQL; catches config-missing and connection errors
- llm_config : verifies all required Azure OpenAI env vars are set (no API call — avoids token cost)
- metadata   : loads view + metric YAML files and counts them

Overall status:
  "ok"       — all checks passed
  "degraded" — metadata files failed but core services are up (answers may lack context)
  "error"    — database or LLM config is missing/unreachable (pipeline cannot function)
"""
import asyncio
import time
from datetime import datetime, timezone

from sqlalchemy import text

from ..core.config import settings
from ..core.logger import logger
from ..services.metadata_service import get_views_metadata, get_metrics_metadata


async def _check_database() -> dict:
    if not settings.database_url:
        return {
            "status": "error",
            "detail": "Not configured — set AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD",
        }
    t0 = time.perf_counter()
    try:
        from ..db.connection import get_connection

        def _ping():
            with get_connection() as conn:
                conn.execute(text("SELECT 1"))

        await asyncio.to_thread(_ping)
        elapsed_ms = round((time.perf_counter() - t0) * 1000)
        return {"status": "ok", "detail": f"Connected — SELECT 1 in {elapsed_ms}ms"}
    except Exception as exc:
        logger.warning("health.database_failed error=%s", str(exc))
        return {"status": "error", "detail": str(exc)}


def _check_llm_config() -> dict:
    missing = [
        name
        for name, val in [
            ("AZURE_OPENAI_ENDPOINT", settings.azure_openai_endpoint),
            ("AZURE_OPENAI_API_KEY", settings.azure_openai_api_key),
            ("AZURE_OPENAI_SCHEMA_RETRIEVAL_DEPLOYMENT", settings.azure_openai_schema_retrieval_deployment),
            ("AZURE_OPENAI_SQL_GENERATION_DEPLOYMENT", settings.azure_openai_sql_generation_deployment),
            ("AZURE_OPENAI_SUMMARY_DEPLOYMENT", settings.azure_openai_summary_deployment),
        ]
        if not val
    ]
    if missing:
        return {"status": "error", "detail": f"Missing env vars: {', '.join(missing)}"}
    return {"status": "ok", "detail": "All 3 task deployments configured"}


async def _check_metadata() -> dict:
    try:
        views, metrics = await asyncio.gather(get_views_metadata(), get_metrics_metadata())
        return {
            "status": "ok",
            "detail": f"{len(views)} view schema(s), {len(metrics)} metric definition(s) loaded",
        }
    except Exception as exc:
        logger.warning("health.metadata_failed error=%s", str(exc))
        return {"status": "error", "detail": str(exc)}


async def run_health_checks() -> dict:
    db_result, meta_result = await asyncio.gather(_check_database(), _check_metadata())
    llm_result = _check_llm_config()

    checks = {
        "database": db_result,
        "llm_config": llm_result,
        "metadata": meta_result,
    }

    critical_failed = db_result["status"] == "error" or llm_result["status"] == "error"
    any_failed = any(c["status"] == "error" for c in checks.values())

    if critical_failed:
        overall = "error"
    elif any_failed:
        overall = "degraded"
    else:
        overall = "ok"

    logger.info("health.check status=%s", overall)
    return {
        "status": overall,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "checks": checks,
    }
