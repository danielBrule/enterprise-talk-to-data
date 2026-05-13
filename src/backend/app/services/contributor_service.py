from sqlalchemy import text

from ..db.connection import execute_query


async def list_contributors(limit: int = 50) -> list[dict]:
    query = text(
        "SELECT TOP (:limit) * "
        "FROM analytics.vw_top_contributors "
        "ORDER BY comment_count DESC"
    )
    return await execute_query(query, {"limit": limit})


async def get_contributor(contributor_id: str) -> dict | None:
    query = text(
        "SELECT TOP (1) * FROM analytics.vw_top_contributors "
        "WHERE contributor_id = :contributor_id"
    )
    result = await execute_query(query, {"contributor_id": contributor_id})
    return result[0] if result else None
