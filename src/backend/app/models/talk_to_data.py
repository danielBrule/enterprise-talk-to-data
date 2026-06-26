from typing import Any

from pydantic import BaseModel, Field

from .trace import TraceRecord, StageLatency


class ConversationTurn(BaseModel):
    """One prior question/answer pair sent by the client for multi-turn context."""
    question: str
    sql: str | None = None
    answer: str | None = None


class MetricDefinition(BaseModel):
    name: str
    description: str
    allowed_aggregations: list[str] = Field(default_factory=list)


class AskRequest(BaseModel):
    question: str
    user_context: str | None = None
    session_id: str | None = None
    conversation_history: list[ConversationTurn] = Field(default_factory=list)


class AskResponse(BaseModel):
    answer: str | None = None
    caveats: list[str] = Field(default_factory=list)
    refused: bool = False
    refusal_reason: str | None = None
    session_id: str | None = None  # echo back on every subsequent turn as AskRequest.session_id

    # Enrichment — populated from pipeline context, exposed for UI panels and debug
    source_view: str | None = None
    metric_definitions: list[MetricDefinition] = Field(default_factory=list)
    filters_applied: list[str] = Field(default_factory=list)
    sql: str | None = None
    row_count: int | None = None
    confidence: float | None = None
    latency_ms: StageLatency | None = None
    token_usage: dict[str, dict[str, Any]] = Field(default_factory=dict)

    trace: TraceRecord
