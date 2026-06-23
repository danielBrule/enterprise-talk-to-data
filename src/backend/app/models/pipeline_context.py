from dataclasses import dataclass

from .trace import TraceRecord


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

    # Populated progressively — None until the responsible stage completes
    selected_views: list[str] | None = None
    metadata_context: dict | None = None
    sql: str | None = None
    rows: list | None = None
