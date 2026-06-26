"""
Analytics store — SQLite backend for pipeline observability.

Two tables:
  traces    one row per pipeline run; linked to feedback by trace_id
  feedback  user thumbs-up/down on individual answers

This is the authoritative source for GET /traces/recent and the join surface
that links a bug → trace → user feedback → raw SQL + answer.

Production replacement: swap _get_conn() for Azure SQL connection pool;
INSERT/SELECT statements are standard SQL and require no changes.
"""
import json
import sqlite3
from pathlib import Path
from typing import TYPE_CHECKING

from ..core.logger import logger

if TYPE_CHECKING:
    from ..models.feedback import FeedbackRecord


_SCHEMA = """
CREATE TABLE IF NOT EXISTS traces (
    trace_id        TEXT PRIMARY KEY,
    timestamp       TEXT NOT NULL,
    question        TEXT NOT NULL,
    intent          TEXT,
    execution_status TEXT,
    selected_views  TEXT,
    answer          TEXT,
    refusal_reason  TEXT,
    latency_total_ms REAL,
    user_context    TEXT,
    sql_retries     INTEGER DEFAULT 0,
    pipeline_env    TEXT,
    session_id      TEXT,
    raw_json        TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
    feedback_id TEXT PRIMARY KEY,
    trace_id    TEXT NOT NULL,
    timestamp   TEXT NOT NULL,
    rating      INTEGER NOT NULL,
    comment     TEXT,
    user_role   TEXT NOT NULL
);
"""


class AnalyticsStore:
    def __init__(self, db_path: str | None = None) -> None:
        from ..core.config import settings
        self._db_path = Path(db_path or settings.analytics_db)
        self._ensure_schema()

    def _ensure_schema(self) -> None:
        try:
            self._db_path.parent.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(self._db_path) as conn:
                conn.executescript(_SCHEMA)
                # Migration: add session_id column if not present (added in v2 schema)
                try:
                    conn.execute("ALTER TABLE traces ADD COLUMN session_id TEXT")
                except sqlite3.OperationalError:
                    pass  # column already exists
        except Exception as exc:
            logger.warning("analytics_store.schema_init_failed error=%s", exc)

    def insert_trace(self, raw: dict) -> None:
        latency = raw.get("latency_ms") or {}
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """INSERT OR IGNORE INTO traces
                       (trace_id, timestamp, question, intent, execution_status,
                        selected_views, answer, refusal_reason, latency_total_ms,
                        user_context, sql_retries, pipeline_env, session_id, raw_json)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        raw.get("trace_id"),
                        raw.get("timestamp"),
                        raw.get("question", ""),
                        raw.get("intent"),
                        raw.get("execution_status"),
                        json.dumps(raw.get("selected_views") or []),
                        raw.get("answer"),
                        raw.get("refusal_reason"),
                        latency.get("total_ms") if isinstance(latency, dict) else None,
                        raw.get("user_context"),
                        raw.get("sql_retries", 0),
                        raw.get("pipeline_env"),
                        raw.get("session_id"),
                        json.dumps(raw),
                    ),
                )
        except Exception as exc:
            logger.warning("analytics_store.insert_trace_failed error=%s", exc)

    def get_recent_traces(self, limit: int = 20) -> list[dict]:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    """SELECT trace_id, timestamp, question, intent, execution_status,
                              selected_views, answer, refusal_reason, latency_total_ms,
                              user_context, session_id
                       FROM traces
                       ORDER BY timestamp DESC
                       LIMIT ?""",
                    (limit,),
                ).fetchall()
            return [dict(row) for row in rows]
        except Exception as exc:
            logger.warning("analytics_store.get_recent_traces_failed error=%s", exc)
            return []

    def insert_feedback(self, record: "FeedbackRecord") -> None:
        try:
            with sqlite3.connect(self._db_path) as conn:
                conn.execute(
                    """INSERT INTO feedback
                       (feedback_id, trace_id, timestamp, rating, comment, user_role)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        record.feedback_id,
                        record.trace_id,
                        record.timestamp,
                        record.rating,
                        record.comment,
                        record.user_role,
                    ),
                )
        except Exception as exc:
            logger.warning("analytics_store.insert_feedback_failed error=%s", exc)
