import json
import time
from typing import Dict, Any

from ..services.llm_service import LLMService
from ..services.metadata_service import get_metrics_metadata
from ..prompts.view_selection import build_view_selection_prompt
from ..core.logger import logger
from ..models.pipeline_context import PipelineContext
from .base import Stage, Refusal, refuse


class ViewSelectionService:
    def __init__(self):
        try:
            self.llm_service = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm_service = None
            self.llm_available = False

    async def select_views(self, question: str) -> Dict[str, Any]:
        metrics = await get_metrics_metadata()

        if not self.llm_available or not metrics:
            logger.warning("view_selection.llm_unavailable question=%s", question[:80])
            fallback_view = metrics[0]["view_name"] if metrics else ""
            return {
                "question": question,
                "selected_views": [fallback_view] if fallback_view else [],
                "confidence": 0.0,
                "reason": "LLM not configured or no metadata available",
            }

        views_context = [
            {
                "view_name": m.get("view_name"),
                "category": m.get("category"),
                "purpose": m.get("purpose"),
                "business_meaning": m.get("business_meaning"),
                "columns": [
                    {"name": col["name"], "description": col["description"]}
                    for col in m.get("columns", [])
                ],
                "example_questions": [
                    eq["natural_language_question"]
                    for eq in m.get("example_questions", [])
                ],
            }
            for m in metrics
        ]

        messages = build_view_selection_prompt(question, views_context)

        logger.debug("view_selection.request question=%s", question[:80])
        response = await self.llm_service.generate_schema_retrieval(messages)
        logger.debug("view_selection.response preview=%s", (response or "")[:120])

        try:
            result = json.loads(response.strip())
            return {
                "question": question,
                "selected_views": result.get("selected_views", []),
                "confidence": result.get("confidence", 0.0),
                "reason": result.get("reason", ""),
            }
        except json.JSONDecodeError as e:
            logger.error("view_selection.parse_failed error=%s", str(e))
            return {
                "question": question,
                "selected_views": [],
                "confidence": 0.0,
                "reason": "Failed to parse LLM response",
            }


class ViewSelectionStage(Stage):
    def __init__(self, view_selection_service: ViewSelectionService | None = None):
        self.view_selection_service = view_selection_service or ViewSelectionService()

    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()
        result = await self.view_selection_service.select_views(ctx.question)
        ctx.latency["view_selection_ms"] = (time.perf_counter() - t0) * 1000

        selected_views: list[str] = result.get("selected_views", [])
        confidence: float = result.get("confidence") or 0.0

        ctx.trace.selected_views = selected_views
        ctx.trace.view_selection_confidence = confidence
        ctx.trace.view_selection_reason = result.get("reason")
        ctx.selected_views = selected_views

        if confidence < 0.4:
            return refuse(
                ctx,
                f"View selection confidence is too low ({confidence:.2f}) — "
                "the question may be ambiguous or out of scope.",
            )
        if not selected_views:
            return refuse(ctx, "No relevant views could be identified for this question.")
        return None
