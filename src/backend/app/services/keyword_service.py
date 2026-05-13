from sqlalchemy import text

from ..db.connection import execute_query


async def list_keywords(limit: int = 50) -> list[dict]:
    query = text(
        "SELECT TOP (:limit) * "
        "FROM analytics.vw_keyword_engagement "
        "ORDER BY article_count DESC"
    )
    return await execute_query(query, {"limit": limit})


async def get_keyword(keyword_id: str) -> dict | None:
    query = text(
        "SELECT TOP (1) * FROM analytics.vw_keyword_engagement "
        "WHERE keyword_id = :keyword_id"
    )
    result = await execute_query(query, {"keyword_id": keyword_id})
    return result[0] if result else None
