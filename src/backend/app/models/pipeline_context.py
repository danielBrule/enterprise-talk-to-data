from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .trace import TraceRecord

if TYPE_CHECKING:
    from ..core.auth import ResolvedUser


@dataclass
class PipelineContext:
    """
    Mutable state threaded through pipeline stages.

    Each stage reads what prior stages have set and writes its own outputs.
    The invariants are additive: selected_views is None until ViewSelectionStage
    completes, metadata_context until MetadataStage, and so on.
    """
    question: str
    user_context: str | None
    trace: TraceRecord
    latency: dict[str, float]
    pipeline_start: float

    # Resolved at the API layer and carried through for access enforcement
    # (Task 11). None when the pipeline is called outside the HTTP context
    # (e.g. evaluation runner, tests).
    user: ResolvedUser | None = None

    # Prior turns sent by the client. The pipeline injects the last 3 into the
    # SQL generation and intent prompts so follow-up questions resolve correctly.
    # The client owns the full history — the server never accumulates it.
    conversation_history: list = field(default_factory=list)  # list[ConversationTurn]

    # Populated progressively — None until the responsible stage completes
    selected_views: list[str] | None = None
    metadata_context: dict | None = None
    sql: str | None = None
    rows: list | None = None

    # Set by SQLValidationStage when the generated SQL fails any safety or metadata check.
    # Read by SQLGenerationStage on retry to inject the error as a correction hint into
    # the prompt. Cleared to None when validation passes.
    sql_validation_error: str | None = None

    # Pre-fetched once by the pipeline before the SQL retry loop and shared with both
    # SQLGenerationStage (prompt) and SQLValidationStage (enforcement) to avoid
    # reloading approved_joins.yml on every retry attempt.
    joins_config: dict | None = None
