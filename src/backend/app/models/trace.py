import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class StageLatency(BaseModel):
    intent_ms: float | None = None
    view_selection_ms: float | None = None
    metadata_ms: float | None = None
    sql_generation_ms: float | None = None
    sql_validation_ms: float | None = None
    execution_ms: float | None = None
    answer_generation_ms: float | None = None
    total_ms: float | None = None


class ValidationResult(BaseModel):
    passed: bool
    reason: str | None = None


class TraceRecord(BaseModel):
    """
    Full observability record for one pipeline run. Designed as the persistence
    contract for Phase 5 (trace store): trace_id is the primary key, all fields
    are JSON-serialisable, timestamp is UTC ISO 8601.
    """
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    # Conversation threading — links all turns of one session; client-generated
    session_id: str | None = None

    # Input
    question: str
    user_context: str | None = None

    # Intent classification
    intent: str | None = None
    answerable: bool | None = None
    refusal_reason: str | None = None

    # View selection
    selected_views: list[str] = Field(default_factory=list)
    view_selection_confidence: float | None = None
    view_selection_reason: str | None = None

    # Metadata
    metadata_used: list[str] = Field(default_factory=list)

    # Prompt and model versioning
    prompt_versions: dict[str, str] = Field(default_factory=dict)
    model_deployments: dict[str, str] = Field(default_factory=dict)

    # SQL
    generated_sql: str | None = None  # final accepted SQL (last attempt)
    sql_attempts: list[str] = Field(default_factory=list)  # all attempts including failed ones
    validation_result: ValidationResult | None = None
    executed_sql: str | None = None
    # Number of SQL generation retries triggered by validation failures (0 = first attempt succeeded)
    sql_retries: int = 0

    # Execution
    execution_status: str | None = None  # "success" | "failed" | "refused" | "skipped"
    row_count: int | None = None
    result_sample: list[dict[str, Any]] | None = None

    # Answer
    caveats: list[str] = Field(default_factory=list)
    answer: str | None = None

    # Token usage per LLM stage (prompt_tokens, completion_tokens, total_tokens)
    token_usage: dict[str, dict[str, int]] = Field(default_factory=dict)

    # Latency (per stage, in milliseconds)
    latency_ms: StageLatency = Field(default_factory=StageLatency)

    # Error detail
    error: str | None = None

    access_enforcement_note: str = "Access enforced at execution stage."


class RecentTraceItem(BaseModel):
    """Compact trace summary returned by GET /traces/recent — one item per pipeline run."""
    trace_id: str
    timestamp: str
    question: str
    execution_status: str | None
    intent: str | None
    selected_views: list[str]
    answer: str | None          # truncated to 200 chars for UI display
    refusal_reason: str | None
    latency_total_ms: float | None
    user_context: str | None
    session_id: str | None = None
