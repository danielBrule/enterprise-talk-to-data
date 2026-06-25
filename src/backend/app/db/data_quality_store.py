import asyncio
import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

from ..core.logger import logger

_DEFAULT_DB_PATH = Path("data_quality.db")


@dataclass
class ViewHealthResult:
    view_name: str
    checked_at: str          # ISO-8601 UTC datetime string
    row_count: int | None
    freshness_days: int | None
    null_rates: dict[str, float] = field(default_factory=dict)
    sanity_issues: list[str] = field(default_factory=list)
    error: str | None = None


_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS view_quality_checks (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    view_name     TEXT    NOT NULL,
    checked_at    TEXT    NOT NULL,
    row_count     INTEGER,
    freshness_days INTEGER,
    null_rates    TEXT,
    sanity_issues TEXT,
    error         TEXT
)
"""


class DataQualityStore:
    def __init__(self, db_path: Path = _DEFAULT_DB_PATH):
        self._db_path = db_path
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(_CREATE_TABLE)
        except Exception as e:
            logger.warning("data_quality_store.schema_init_failed error=%s", e)

    async def save_results(self, results: list[ViewHealthResult]) -> None:
        def _sync() -> None:
            with sqlite3.connect(self._db_path) as conn:
                conn.executemany(
                    """INSERT INTO view_quality_checks
                       (view_name, checked_at, row_count, freshness_days,
                        null_rates, sanity_issues, error)
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    [
                        (
                            r.view_name,
                            r.checked_at,
                            r.row_count,
                            r.freshness_days,
                            json.dumps(r.null_rates),
                            json.dumps(r.sanity_issues),
                            r.error,
                        )
                        for r in results
                    ],
                )
        try:
            await asyncio.to_thread(_sync)
        except Exception as e:
            logger.warning("data_quality_store.save_failed error=%s", e)

    async def get_latest_results(self) -> list[ViewHealthResult]:
        def _sync() -> list[tuple]:
            with sqlite3.connect(self._db_path) as conn:
                return conn.execute(
                    """SELECT view_name, checked_at, row_count, freshness_days,
                              null_rates, sanity_issues, error
                       FROM view_quality_checks
                       WHERE id IN (
                           SELECT MAX(id) FROM view_quality_checks GROUP BY view_name
                       )
                       ORDER BY view_name"""
                ).fetchall()
        try:
            rows = await asyncio.to_thread(_sync)
        except Exception as e:
            logger.warning("data_quality_store.read_failed error=%s", e)
            return []
        return [
            ViewHealthResult(
                view_name=r[0],
                checked_at=r[1],
                row_count=r[2],
                freshness_days=r[3],
                null_rates=json.loads(r[4]) if r[4] else {},
                sanity_issues=json.loads(r[5]) if r[5] else [],
                error=r[6],
            )
            for r in rows
        ]
