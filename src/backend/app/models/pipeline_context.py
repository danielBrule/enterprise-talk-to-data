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

    # Populated progressively — None until the responsible stage completes
    selected_views: list[str] | None = None
    metadata_context: dict | None = None
    sql: str | None = None
    rows: list | None = None
