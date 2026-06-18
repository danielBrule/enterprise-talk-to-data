import time

from ..services.metadata_service import get_context_for_views
from ..models.pipeline_context import PipelineContext
from .base import Stage, Refusal, refuse


class MetadataStage(Stage):
    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()
        metadata_context = await get_context_for_views(ctx.selected_views or [])
        ctx.latency["metadata_ms"] = (time.perf_counter() - t0) * 1000

        ctx.trace.metadata_used = list(metadata_context.keys())
        ctx.metadata_context = metadata_context

        if not metadata_context:
            return refuse(ctx, f"No metadata found for selected views: {ctx.selected_views}")
        return None
