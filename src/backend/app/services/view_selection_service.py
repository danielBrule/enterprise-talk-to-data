import json
from typing import Dict, Any

from .llm_service import LLMService
from .metadata_service import get_metrics_metadata
from ..prompts.view_selection import build_view_selection_prompt
from ..core.logger import logger


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
        response = await self.llm_service.generate_response(messages, task="schema_retrieval")
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
