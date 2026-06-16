import pytest
import asyncio
from sqlalchemy import text
from unittest.mock import MagicMock, AsyncMock

import backend.app.db.connection as connection


def test_get_connection_raises_without_database_url(monkeypatch):
    monkeypatch.setattr(connection.settings, "database_url", "")
    connection._engine = None

    with pytest.raises(RuntimeError):
        connection.get_connection()


@pytest.mark.asyncio
async def test_execute_query_logs_success(monkeypatch):
    # Mock Row class that has ._mapping attribute
    class MockRow:
        def __init__(self, data):
            self._mapping = data

    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute = MagicMock(return_value=[MockRow({"article_id": 1})])

    monkeypatch.setattr(connection, "get_connection", lambda: mock_conn)

    # Execute query and verify it returns correct data
    result = await connection.execute_query(
        text("SELECT * FROM analytics.vw_article_engagement LIMIT 1"), {"limit": 1}
    )

    assert result == [{"article_id": 1}]


@pytest.mark.asyncio
async def test_execute_query_logs_failure(monkeypatch):
    mock_conn = MagicMock()
    mock_conn.__enter__.return_value = mock_conn
    mock_conn.execute = MagicMock(side_effect=ValueError("boom"))

    monkeypatch.setattr(connection, "get_connection", lambda: mock_conn)

    with pytest.raises(ValueError, match="boom"):
        await connection.execute_query(
            text("SELECT * FROM analytics.vw_article_engagement LIMIT 1"), {"limit": 1}
        )
