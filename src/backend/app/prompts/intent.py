from datetime import date

PROMPT_VERSION = "intent_v4"


_KNOWN_DOMAINS = (
    "article_engagement (comment volume, avg_comment_sentiment, total_replies, keyword_count, publication_date, insert_date), "
    "keyword_engagement (keyword article count, comment count, contributor reach), "
    "contributor_behaviour (comment count, sentiment, distinct_article_count, article breadth, reply count), "
    "ingestion_errors (pipeline stage failures, error types, timing)"
)

_KNOWN_VIEWS = (
    "analytics.vw_article_engagement, "
    "analytics.vw_keyword_engagement, "
    "analytics.vw_top_contributors, "
    "analytics.vw_ingestion_errors"
)


def build_intent_prompt(question: str) -> list[dict]:
    today = date.today().isoformat()
    system = (
        "You classify whether an analytics question can be answered from a specific set of "
        "database views. Reply only with valid JSON — no markdown, no explanation outside the JSON."
    )
    user = f"""Classify this question: "{question}"

Available analytics domains: {_KNOWN_DOMAINS}
Available views: {_KNOWN_VIEWS}

Rules:
- answerable is true only if the question can be answered from the available views above.
- If the question requires forecasting future values, causal explanation ("why", "what causes"), \
external data, or data not covered by the views above, set answerable to false.
- Date filtering on publication_date or insert_date is supported and should be classified as answerable.
- Today's date is {today}. Any year or date before today is historical, not a future date.
- domain must be one of: article_engagement, keyword_engagement, contributor_behaviour, \
ingestion_errors, or unknown.
- suggested_metrics should be column names or aggregate expressions from the available views.

Respond with exactly this JSON:
{{
  "answerable": "<boolean>",
  "reason": "<brief explanation of why the question is or is not answerable>",
  "domain": "<article_engagement | keyword_engagement | contributor_behaviour | ingestion_errors | unknown>",
  "suggested_metrics": ["<column_name_or_aggregate_expression>"]
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
