import time

from sqlalchemy import text

from ..db.connection import execute_query
from ..core.logger import logger
from ..models.pipeline_context import PipelineContext
from .base import Stage, build_latency, Refusal


class ExecutionStage(Stage):
    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()
        try:
            rows = await execute_query(text(ctx.sql or ""))
            ctx.latency["execution_ms"] = (time.perf_counter() - t0) * 1000
            ctx.trace.executed_sql = ctx.sql
            ctx.trace.execution_status = "success"
            ctx.trace.row_count = len(rows)
            ctx.trace.result_sample = rows[:3]
            ctx.rows = rows
            return None
        except Exception as exc:
            ctx.latency["execution_ms"] = (time.perf_counter() - t0) * 1000
            ctx.trace.execution_status = "failed"
            ctx.trace.error = str(exc)
            reason = "Query execution failed — the database may be unavailable."
            ctx.trace.refusal_reason = reason
            ctx.trace.latency_ms = build_latency(ctx)
            logger.exception(
                "pipeline.execution_failed trace_id=%s sql=%s",
                ctx.trace.trace_id,
                (ctx.sql or "")[:80],
            )
            return Refusal(reason=reason, trace=ctx.trace)
