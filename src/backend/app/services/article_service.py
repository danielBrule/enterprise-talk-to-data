from sqlalchemy import text

from ..db.connection import execute_query


async def list_articles(limit: int = 50) -> list[dict]:
    query = text(
        "SELECT TOP (:limit) * "
        "FROM analytics.vw_article_engagement "
        "ORDER BY comment_count DESC"
    )
    return await execute_query(query, {"limit": limit})


async def get_article(article_id: str) -> dict | None:
    query = text(
        "SELECT TOP (1) * FROM analytics.vw_article_engagement "
        "WHERE article_id = :article_id"
    )
    result = await execute_query(query, {"article_id": article_id})
    return result[0] if result else None
