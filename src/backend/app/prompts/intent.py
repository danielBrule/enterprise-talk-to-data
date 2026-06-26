from datetime import date
import json

PROMPT_VERSION = "intent_v13"


_KNOWN_DOMAINS = (
    "article_engagement (article_id, title, publication_date, insert_date, comment_count, avg_comment_sentiment, total_replies, "
    "keyword_count [= number of keywords associated with the article — use this to answer 'how many keywords are linked to articles']), "
    "keyword_engagement (keyword_id, full_keyword, article_count, comment_count, avg_comment_sentiment, contributor_count), "
    "contributor_behaviour [= vw_top_contributors; 'top' is the view name not a filter — covers ALL contributors] "
    "(contributor_id, comment_count, avg_sentiment, distinct_article_count, total_replies), "
    "ingestion_errors (error_id, stage, data_id, error_type, error_message, attempted_at)"
)

_KNOWN_VIEWS = (
    "analytics.vw_article_engagement, "
    "analytics.vw_keyword_engagement, "
    "analytics.vw_top_contributors, "
    "analytics.vw_ingestion_errors"
)

# Few-shot exchange injected before the real question so temperature=0 doesn't
# override the injected date context with the model's training-set priors.
_EXAMPLE_USER = """Classify this question: "What is the average sentiment for articles published in 2025?"

Available analytics domains: {domains}
Available views: {views}

Rules:
- answerable is true only if the question can be answered from the available views above.
- If the question requires forecasting future values, causal explanation ("why", "what causes"), external data, or data not covered by the views above, set answerable to false.
- Date filtering on publication_date or insert_date is supported and should be classified as answerable.
- Today's date is 2026-06-24. The current year is 2026. Years before 2026 (e.g. 2025, 2024, 2023) are in the past — historical data exists for them and questions about them are answerable. Only dates strictly after today require forecasting.
- domain must be one of: article_engagement, keyword_engagement, contributor_behaviour, ingestion_errors, or unknown.
- suggested_metrics should be column names or aggregate expressions from the available views.

Respond with exactly this JSON:
{{
  "answerable": "<boolean>",
  "reason": "<brief explanation>",
  "domain": "<article_engagement | keyword_engagement | contributor_behaviour | ingestion_errors | unknown>",
  "suggested_metrics": ["<column_name_or_aggregate_expression>"]
}}""".format(domains=_KNOWN_DOMAINS, views=_KNOWN_VIEWS)

_EXAMPLE_ASSISTANT = json.dumps({
    "answerable": True,
    "reason": "2025 is a past year (current year is 2026) — historical sentiment data for articles published in 2025 is available in vw_article_engagement.",
    "domain": "article_engagement",
    "suggested_metrics": ["avg_comment_sentiment"],
})


def _format_history(conversation_history: list) -> str:
    if not conversation_history:
        return ""
    from ..core.config import settings
    turns = conversation_history[-settings.max_history_turns:]
    prior = [
        f'"{getattr(t, "question", "") or ""}"'
        for t in reversed(turns)
    ]
    return (
        "Prior conversation (this question may be a follow-up — use for context):\n"
        + "\n".join(f"- {q}" for q in prior)
        + "\n\n"
    )


def build_intent_prompt(question: str, aliases: dict[str, list[str]] | None = None, conversation_history: list | None = None) -> list[dict]:
    today = date.today().isoformat()
    current_year = date.today().year
    system = (
        "You classify whether an analytics question can be answered from a specific set of "
        "database views. Reply only with valid JSON — no markdown, no explanation outside the JSON."
    )

    alias_lines = ""
    if aliases:
        parts = []
        for view_name, terms in aliases.items():
            quoted = ", ".join(f'"{t}"' for t in terms)
            parts.append(f"{quoted} → {view_name}")
        alias_lines = "\n- Domain vocabulary: " + "; ".join(parts) + "."

    history_section = _format_history(conversation_history or [])
    user = f"""{history_section}Classify this question: "{question}"

Available analytics domains: {_KNOWN_DOMAINS}
Available views: {_KNOWN_VIEWS}

Rules:
- answerable is true only if the question can be answered from the available views above.
- If the question requires forecasting future values, causal explanation ("why", "what causes"), \
external data, or data not covered by the views above, set answerable to false.
- Date filtering on publication_date or insert_date is supported and should be classified as answerable.
- Today's date is {today}. The current year is {current_year}. Years before {current_year} \
(e.g. {current_year - 1}, {current_year - 2}, {current_year - 3}) are in the past — historical \
data exists for them and questions about them are answerable. Only dates strictly after today \
require forecasting.
- domain must be one of: article_engagement, keyword_engagement, contributor_behaviour, \
ingestion_errors, or unknown.
- suggested_metrics should be column names or aggregate expressions from the available views.
- Any question mentioning "top contributors" refers to the contributor_behaviour domain \
(vw_top_contributors). The word "top" is part of the view name — not a filter. This view covers \
ALL contributors and provides: total_replies, comment_count, avg_sentiment, distinct_article_count.{alias_lines}

Respond with exactly this JSON:
{{
  "answerable": "<boolean>",
  "reason": "<brief explanation of why the question is or is not answerable>",
  "domain": "<article_engagement | keyword_engagement | contributor_behaviour | ingestion_errors | unknown>",
  "suggested_metrics": ["<column_name_or_aggregate_expression>"]
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": _EXAMPLE_USER},
        {"role": "assistant", "content": _EXAMPLE_ASSISTANT},
        {"role": "user", "content": user},
    ]
