import time

from ..core.sql_safety import validate_query, SQLSafetyError
from ..models.pipeline_context import PipelineContext
from ..models.trace import ValidationResult
from .base import Stage, Refusal, refuse


class SQLValidationStage(Stage):
    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()
        try:
            validate_query(ctx.sql or "")
            passed, reason = True, None
        except SQLSafetyError as e:
            passed, reason = False, str(e)
        ctx.latency["sql_validation_ms"] = (time.perf_counter() - t0) * 1000

        ctx.trace.validation_result = ValidationResult(passed=passed, reason=reason)

        if not passed:
            return refuse(ctx, f"SQL validation failed: {reason}")
        return None
