import json

PROMPT_VERSION = "answer_gen_v1"


def build_answer_generation_prompt(
    question: str,
    sql: str,
    results: list[dict],
    caveats: list[str],
) -> list[dict]:
    system = (
        "You interpret database query results and write a concise, factual answer to the "
        "user's question. Ground your answer entirely in the data provided. "
        "Do not speculate, forecast, or infer causation. "
        "If the result set is empty, say so clearly. "
        "Respond with valid JSON only — no markdown outside the JSON."
    )
    results_preview = results[:5]
    row_count = len(results)
    user = f"""Question: "{question}"

SQL executed:
{sql}

Result ({row_count} row(s) total, showing up to 5):
{json.dumps(results_preview, indent=2, default=str)}

Caveats from metadata:
{json.dumps(caveats)}

Respond with exactly this JSON:
{{
  "answer": "A concise factual answer grounded in the result above (under 100 words).",
  "caveats": ["include all metadata caveats plus any you observe from the result"]
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
