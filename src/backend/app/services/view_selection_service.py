import json
from typing import List, Dict, Any

from .llm_service import LLMService
from .metadata_service import get_metrics_metadata


class ViewSelectionService:
    def __init__(self):
        try:
            self.llm_service = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm_service = None
            self.llm_available = False

    async def select_views(self, question: str) -> Dict[str, Any]:
        """
        Select the most relevant views for a given question using LLM.

        Args:
            question: The natural language question

        Returns:
            Dict with question, selected_views, and reason
        """
        # Get all metrics metadata which includes view information and example questions
        metrics = await get_metrics_metadata()

        if not self.llm_available or not metrics:
            # Fallback: return first view or empty
            fallback_view = metrics[0]["view_name"] if metrics else ""
            return {
                "question": question,
                "selected_views": [fallback_view] if fallback_view else [],
                "reason": "LLM not configured or no metadata available",
            }

        # Prepare the context for the LLM
        views_context = []
        for metric in metrics:
            view_info = {
                "view_name": metric.get("view_name"),
                "category": metric.get("category"),
                "purpose": metric.get("purpose"),
                "business_meaning": metric.get("business_meaning"),
                "columns": [
                    {"name": col["name"], "description": col["description"]}
                    for col in metric.get("columns", [])
                ],
                "example_questions": [
                    eq["natural_language_question"]
                    for eq in metric.get("example_questions", [])
                ],
            }
            views_context.append(view_info)
        # Create the prompt
        prompt = f"""
You are an expert at selecting the most relevant database views for natural language questions about analytics data.

Given the question: "{question}"

And the available views with their metadata:

{json.dumps(views_context, indent=2)}

Please select the most relevant view(s) that would help answer this question. Consider:
- The purpose and business meaning of each view
- The columns available in each view
- The example questions that are similar to the given question

Return your response as a JSON object with the following structure:
{{
  "selected_views": ["view_name1", "view_name2"],
  "reason": "Brief explanation of why these views were selected"
}}

Select 1-3 views maximum. If no views are relevant, select the closest match.
"""

        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant that selects database views for analytics questions. Always respond with valid JSON.",
            },
            {"role": "user", "content": prompt},
        ]

        # Get LLM response
        print("Sending prompt to LLM for view selection...")
        response = await self.llm_service.generate_response(
            messages, task="schema_retrieval"
        )
        print(f"Received response from LLM: {response}")
        try:
            # Parse the JSON response
            result = json.loads(response.strip())
            selected_views = result.get("selected_views", [])
            reason = result.get("reason", "")

            return {
                "question": question,
                "selected_views": selected_views,
                "reason": reason,
            }
        except json.JSONDecodeError:
            # Fallback if LLM doesn't return valid JSON
            return {
                "question": question,
                "selected_views": [],
                "reason": "Failed to parse LLM response",
            }
