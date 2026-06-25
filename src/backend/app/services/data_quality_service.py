"""
Data quality service — runs per-view health checks against Azure SQL and stores
results in a local SQLite database for fast reads at answer time.

DEMO NOTE: This implementation runs a focused subset of checks (row count,
freshness, NULL rate on sentiment columns, sanity bounds). In a production data
layer these checks would be managed by purpose-built tooling — dbt tests,
Great Expectations, Azure Purview Data Quality, or Databricks Quality Monitoring
— running at ingestion time with full column coverage and historical comparison.

NULL rate is monitored only on sentiment columns (avg_comment_sentiment,
avg_sentiment) because they are derived/scored and most likely to have gaps.
In a production context every meaningful non-nullable column would be monitored
and per-column thresholds would be set from observed baselines.
"""
import asyncio
from datetime import datetime, timezone

from sqlalchemy import text

from ..core.logger import logger
from ..db.connection import get_connection
from ..db.data_quality_store import DataQualityStore, ViewHealthResult
from ..services.metadata_service import get_metrics_metadata


def _build_check_sql(view_name: str, config: dict) -> str:
    """
    Build a single T-SQL query that collects all health metrics for a view in
    one round-trip: row count, freshness, NULL rates, and sanity checks.
    """
    freshness_col = config.get("freshness_column")
    null_cols = config.get("monitor_null_rate") or []
    neg_cols = config.get("sanity_non_negative") or []
    sent_cols = config.get("sanity_sentiment_range") or []

    parts = ["SELECT TOP 1", "  COUNT(*) AS row_count"]

    if freshness_col:
        parts.append(
            f"  ,DATEDIFF(day, MAX({freshness_col}), GETDATE()) AS freshness_days"
        )
    else:
        parts.append("  ,NULL AS freshness_days")

    for col in null_cols:
        alias = f"null_pct_{col}"
        parts.append(
            f"  ,SUM(CASE WHEN {col} IS NULL THEN 1.0 ELSE 0 END)"
            f" * 100.0 / NULLIF(COUNT(*), 0) AS {alias}"
        )

    for col in neg_cols:
        parts.append(
            f"  ,SUM(CASE WHEN {col} < 0 THEN 1 ELSE 0 END) AS neg_{col}"
        )

    for col in sent_cols:
        parts.append(
            f"  ,SUM(CASE WHEN {col} < -1 OR {col} > 1 THEN 1 ELSE 0 END)"
            f" AS oor_{col}"
        )

    parts.append(f"FROM {view_name}")
    return "\n".join(parts)


async def _run_check_query(view_name: str, sql: str) -> dict:
    def _sync() -> dict:
        with get_connection() as conn:
            result = conn.execute(text(sql))
            row = result.mappings().first()
            return dict(row) if row else {}

    return await asyncio.to_thread(_sync)


async def check_view(view_name: str, config: dict) -> ViewHealthResult:
    """Run all health checks for a single view. Never raises — errors are captured."""
    checked_at = datetime.now(timezone.utc).isoformat()
    null_cols = config.get("monitor_null_rate") or []
    neg_cols = config.get("sanity_non_negative") or []
    sent_cols = config.get("sanity_sentiment_range") or []

    try:
        sql = _build_check_sql(view_name, config)
        row = await _run_check_query(view_name, sql)

        row_count = row.get("row_count")
        freshness_days = row.get("freshness_days")

        null_rates: dict[str, float] = {}
        for col in null_cols:
            val = row.get(f"null_pct_{col}")
            if val is not None:
                null_rates[col] = round(float(val), 1)

        sanity_issues: list[str] = []
        for col in neg_cols:
            count = row.get(f"neg_{col}") or 0
            if count > 0:
                sanity_issues.append(f"{count} row(s) with negative {col}")
        for col in sent_cols:
            count = row.get(f"oor_{col}") or 0
            if count > 0:
                sanity_issues.append(f"{count} row(s) with {col} outside [-1, 1]")

        logger.info(
            "data_quality.check_complete view=%s rows=%s freshness_days=%s",
            view_name,
            row_count,
            freshness_days,
        )
        return ViewHealthResult(
            view_name=view_name,
            checked_at=checked_at,
            row_count=row_count,
            freshness_days=int(freshness_days) if freshness_days is not None else None,
            null_rates=null_rates,
            sanity_issues=sanity_issues,
        )
    except Exception as e:
        logger.error("data_quality.check_failed view=%s error=%s", view_name, e)
        return ViewHealthResult(
            view_name=view_name,
            checked_at=checked_at,
            row_count=None,
            freshness_days=None,
            error=str(e),
        )


class DataQualityService:
    def __init__(self, store: DataQualityStore | None = None):
        self._store = store or DataQualityStore()

    async def refresh_all(self) -> list[ViewHealthResult]:
        """Run health checks for all views sequentially and persist results.

        Sequential rather than parallel to avoid overwhelming the Azure SQL
        connection pool when multiple views are checked at once.
        """
        metrics_list = await get_metrics_metadata()
        results: list[ViewHealthResult] = []
        for m in metrics_list:
            if m.get("view_name") and m.get("health_checks"):
                result = await check_view(m["view_name"], m.get("health_checks") or {})
                results.append(result)
        await self._store.save_results(results)
        logger.info("data_quality.refresh_complete views=%s", len(results))
        return results

    async def get_latest(self) -> list[ViewHealthResult]:
        return await self._store.get_latest_results()
