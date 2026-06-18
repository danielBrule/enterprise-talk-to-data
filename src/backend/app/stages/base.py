import time
from dataclasses import dataclass
from typing import Protocol

from ..models.pipeline_context import PipelineContext
from ..models.trace import StageLatency, TraceRecord
from ..core.logger import logger


def build_latency(ctx: PipelineContext) -> StageLatency:
    return StageLatency(
        intent_ms=ctx.latency.get("intent_ms"),
        view_selection_ms=ctx.latency.get("view_selection_ms"),
        metadata_ms=ctx.latency.get("metadata_ms"),
        sql_generation_ms=ctx.latency.get("sql_generation_ms"),
        sql_validation_ms=ctx.latency.get("sql_validation_ms"),
        execution_ms=ctx.latency.get("execution_ms"),
        answer_generation_ms=ctx.latency.get("answer_generation_ms"),
        total_ms=(time.perf_counter() - ctx.pipeline_start) * 1000,
    )


@dataclass
class Refusal:
    reason: str
    trace: TraceRecord


@dataclass
class Success:
    answer: str
    caveats: list[str]
    trace: TraceRecord


StageOutcome = Refusal | Success | None


def refuse(ctx: PipelineContext, reason: str) -> Refusal:
    ctx.trace.refusal_reason = reason
    ctx.trace.execution_status = "refused"
    ctx.trace.latency_ms = build_latency(ctx)
    logger.info("pipeline.refused trace_id=%s reason=%s", ctx.trace.trace_id, reason[:120])
    return Refusal(reason=reason, trace=ctx.trace)


class Stage(Protocol):
    async def run(self, ctx: PipelineContext) -> StageOutcome: ...
