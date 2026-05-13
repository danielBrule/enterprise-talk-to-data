import asyncio
import time
from sqlalchemy import create_engine
from sqlalchemy.sql import Executable

from ..core.config import settings
from ..core.logger import logger
from ..core.sql_safety import validate_query, SQLSafetyError

_engine = None


def _get_engine():
    global _engine
    if _engine is None:
        if not settings.database_url:
            raise RuntimeError(
                "Database connection is not configured. Set AZURE_SQL_SERVER, AZURE_SQL_DATABASE, "
                "AZURE_SQL_USERNAME, and AZURE_SQL_PASSWORD."
            )
        _engine = create_engine(settings.database_url, future=True)
    return _engine


def get_connection():
    return _get_engine().connect()


async def execute_query(query: Executable, params: dict | None = None) -> list[dict]:
    start_time = time.perf_counter()
    params = params or {}

    # Validate query for safety
    try:
        validate_query(str(query), params)
    except SQLSafetyError as e:
        logger.warning("sql.query.blocked query=%s reason=%s", str(query), str(e))
        raise

    logger.info("sql.query.start sql=%s params=%s", str(query), params)
    try:

        def _sync_execute():
            with get_connection() as conn:
                result = conn.execute(query, params)
                return [dict(row._mapping) for row in result]

        rows = await asyncio.to_thread(_sync_execute)
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.info(
            "sql.query.complete sql=%s params=%s duration_ms=%s rows=%s",
            str(query),
            params,
            round(duration_ms, 2),
            len(rows),
        )
        return rows
    except Exception:
        duration_ms = (time.perf_counter() - start_time) * 1000
        logger.exception(
            "sql.query.failed sql=%s params=%s duration_ms=%s",
            str(query),
            params,
            round(duration_ms, 2),
        )
        raise
