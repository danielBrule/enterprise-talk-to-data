PROMPT_VERSION = "intent_v1"

_KNOWN_DOMAINS = (
    "article_engagement (comment volume, sentiment, replies, keyword coverage), "
    "keyword_engagement (keyword article count, comment count, contributor reach), "
    "contributor_behaviour (comment count, sentiment, article breadth, reply count), "
    "ingestion_errors (pipeline stage failures, error types, timing)"
)

_KNOWN_VIEWS = (
    "analytics.vw_article_engagement, "
    "analytics.vw_keyword_engagement, "
    "analytics.vw_top_contributors, "
    "analytics.vw_ingestion_errors"
)


def build_intent_prompt(question: str) -> list[dict]:
    system = (
        "You classify whether an analytics question can be answered from a specific set of "
        "database views. Reply only with valid JSON — no markdown, no explanation outside the JSON."
    )
    user = f"""Classify this question: "{question}"

Available analytics domains: {_KNOWN_DOMAINS}
Available views: {_KNOWN_VIEWS}

Rules:
- answerable is true only if the question can be answered from the available views above.
- If the question requires forecasting, causal explanation, external data, or data not covered \
by the views above, set answerable to false.
- domain must be one of: article_engagement, keyword_engagement, contributor_behaviour, \
ingestion_errors, or unknown.
- suggested_metrics should be column names or aggregate expressions from the available views.

Respond with exactly this JSON:
{{
  "answerable": true,
  "reason": "brief explanation",
  "domain": "article_engagement",
  "suggested_metrics": ["comment_count", "avg_comment_sentiment"]
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
