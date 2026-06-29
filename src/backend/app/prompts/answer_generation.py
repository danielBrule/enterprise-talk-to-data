import json

PROMPT_VERSION = "answer_gen_v3"


def build_answer_generation_prompt(
    question: str,
    sql: str,
    results: list[dict],
    caveats: list[str],
) -> list[dict]:
    system = (
        "You interpret database query results and write a factual answer to the "
        "user's question. Ground your answer entirely in the data provided. "
        "Do not speculate, forecast, or infer causation. "
        "If the result set is empty, say so clearly. "
        "Honour any formatting request in the question: if the user asks for a table, "
        "respond with a markdown table; if they ask for a list, use a markdown list. "
        "The answer field must always be a plain string — never a JSON array or object. "
        "The answer field may contain markdown. "
        "Respond with valid JSON only — no markdown outside the JSON."
    )
    results_preview = results[:20]
    row_count = len(results)
    truncated = " (truncated)" if row_count > 20 else ""
    user = f"""Question: "{question}"

SQL executed:
{sql}

Result ({row_count} row(s) total, showing up to 20{truncated}):
{json.dumps(results_preview, indent=2, default=str)}

Caveats from metadata:
{json.dumps(caveats)}

Respond with exactly this JSON:
{{
  "answer": "<factual answer grounded in the result — use markdown table or list if the question requests it>",
  "caveats": ["<caveat from metadata or observed from the result>"]
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
