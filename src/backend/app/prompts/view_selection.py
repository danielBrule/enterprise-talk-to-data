import json

PROMPT_VERSION = "view_selection_v1"


def build_view_selection_prompt(question: str, views_context: list[dict]) -> list[dict]:
    user = f"""Given the question: "{question}"

And the available views with their metadata:

{json.dumps(views_context, indent=2)}

Please select the most relevant view(s) that would help answer this question. Consider:
- The purpose and business meaning of each view
- The columns available in each view
- The example questions that are similar to the given question

Select 1-3 views maximum. If no views are relevant, select the closest match.

Respond with exactly this JSON:
{{
  "selected_views": ["<view_name>"],
  "confidence": "<float between 0.0 and 1.0>",
  "reason": "<brief explanation of why these views were selected>"
}}"""

    return [
        {
            "role": "system",
            "content": (
                "You select the most relevant database views to answer analytics questions. "
                "Respond only with valid JSON — no markdown, no explanation outside the JSON."
            ),
        },
        {"role": "user", "content": user},
    ]
