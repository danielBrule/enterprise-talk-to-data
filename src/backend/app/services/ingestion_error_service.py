from sqlalchemy import text

from ..db.connection import execute_query


async def list_ingestion_errors(limit: int = 50) -> list[dict]:
    query = text(
        "SELECT TOP (:limit) * "
        "FROM analytics.vw_ingestion_errors "
        "ORDER BY attempted_at DESC"
    )
    return await execute_query(query, {"limit": limit})
