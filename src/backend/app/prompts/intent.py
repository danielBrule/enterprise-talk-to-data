from datetime import date
import json

PROMPT_VERSION = "intent_v18"


_KNOWN_DOMAINS = (
    "article_engagement (article_id, title, publication_date, insert_date, url, comment_count, avg_comment_sentiment, total_replies, "
    "keyword_count [= number of keywords associated with the article — use this to answer 'how many keywords are linked to articles']), "
    "article_keywords [= vw_article_keywords; one row per article-keyword pair — use to LIST the specific keywords for a given article, "
    "or to LIST articles that have a specific keyword; do NOT use article_engagement for listing keyword names] "
    "(article_id, title, publication_date, url, keyword_id, full_keyword), "
    "keyword_engagement (keyword_id, full_keyword, article_count, comment_count, avg_comment_sentiment, contributor_count), "
    "contributor_behaviour [= vw_top_contributors; 'top' is the view name not a filter — covers ALL contributors] "
    "(contributor_id, comment_count, avg_sentiment, distinct_article_count, total_replies), "
    "ingestion_errors (error_id, stage, data_id, error_type, error_message, attempted_at)"
)

_KNOWN_VIEWS = (
    "analytics.vw_article_engagement, "
    "analytics.vw_article_keywords, "
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
- If the question is a follow-up (uses vague references like "top 10", "more", "same", "these", "it", "them" without an explicit subject), resolve the subject from the prior conversation and classify as answerable with the same domain as the prior question.
- If the question requires forecasting future values, causal explanation ("why", "what causes"), external data, or data not covered by the views above, set answerable to false.
- Date filtering on publication_date or insert_date is supported and should be classified as answerable.
- Today's date is 2026-06-24. The current year is 2026. Years before 2026 (e.g. 2025, 2024, 2023) are in the past — historical data exists for them and questions about them are answerable. Only dates strictly after today require forecasting.
- domain must be one of: article_engagement, article_keywords, keyword_engagement, contributor_behaviour, ingestion_errors, system_info, or unknown.
- Use domain=article_keywords when the question asks for the list of keywords associated with a specific article, or the list of articles tagged with a specific keyword.
- Use domain=article_engagement when the question asks for keyword COUNT on an article (keyword_count column) — NOT article_keywords.
- Use domain=system_info (and answerable=true) when the question asks about the system itself: what views or data are available, what topics can be queried, what questions can be asked, etc.
- suggested_metrics should be column names or aggregate expressions from the available views.

Respond with exactly this JSON:
{{
  "answerable": "<boolean>",
  "reason": "<brief explanation>",
  "domain": "<article_engagement | article_keywords | keyword_engagement | contributor_behaviour | ingestion_errors | system_info | unknown>",
  "suggested_metrics": ["<column_name_or_aggregate_expression>"],
  "clarifying_question": null
}}""".format(domains=_KNOWN_DOMAINS, views=_KNOWN_VIEWS)

_EXAMPLE_ASSISTANT = json.dumps({
    "answerable": True,
    "reason": "2025 is a past year (current year is 2026) — historical sentiment data for articles published in 2025 is available in vw_article_engagement.",
    "domain": "article_engagement",
    "suggested_metrics": ["avg_comment_sentiment"],
    "clarifying_question": None,
})


def _format_history(conversation_history: list) -> str:
    if not conversation_history:
        return ""
    from ..core.config import settings
    max_turns = settings.max_history_turns
    max_answer_chars = settings.max_history_answer_chars
    turns = conversation_history[-max_turns:]
    lines = ["Prior conversation (resolve follow-up references using this context):"]
    for i, turn in enumerate(reversed(turns)):
        label = "Most recent" if i == 0 else f"Turn -{i + 1}"
        q = getattr(turn, "question", "") or ""
        ans = getattr(turn, "answer", None) or ""
        if ans and len(ans) > max_answer_chars:
            ans = ans[:max_answer_chars] + "…"
        lines.append(f"[{label}] Q: \"{q}\"")
        if ans:
            lines.append(f"         A: {ans}")
    return "\n".join(lines) + "\n\n"


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
- If the question is a follow-up (uses pronouns or vague references like "top 10", "more", \
"same", "these", "it", "them" without an explicit subject), resolve the subject from the \
prior conversation and classify as answerable with the same domain as the prior question.
- If the question requires forecasting future values, causal explanation ("why", "what causes"), \
external data, or data not covered by the views above, set answerable to false.
- Date filtering on publication_date or insert_date is supported and should be classified as answerable.
- Today's date is {today}. The current year is {current_year}. Years before {current_year} \
(e.g. {current_year - 1}, {current_year - 2}, {current_year - 3}) are in the past — historical \
data exists for them and questions about them are answerable. Only dates strictly after today \
require forecasting.
- domain must be one of: article_engagement, article_keywords, keyword_engagement, \
contributor_behaviour, ingestion_errors, system_info, or unknown.
- Use domain=article_keywords when the question asks for the list of keywords for a specific \
article, or the list of articles tagged with a specific keyword.
- Use domain=article_engagement when the question asks for keyword COUNT on an article \
(keyword_count column) — NOT article_keywords.
- Use domain=system_info (and answerable=true) when the question asks about the system itself: \
what views or data are available, what topics can be queried, what questions can be asked, etc.
- suggested_metrics should be column names or aggregate expressions from the available views.
- Any question mentioning "top contributors" refers to the contributor_behaviour domain \
(vw_top_contributors). The word "top" is part of the view name — not a filter. This view covers \
ALL contributors and provides: total_replies, comment_count, avg_sentiment, distinct_article_count.
- If the question is vague but potentially answerable (e.g. could match multiple domains, or \
references a subject without saying what metric is wanted), set answerable=false, domain=unknown, \
and populate clarifying_question with a short, specific question that helps the user narrow their \
intent. Example: "Do you want engagement metrics for that keyword, or a list of articles tagged \
with it?"
- Only set clarifying_question when the question is ambiguous about which domain or metric to use. \
Leave it null when the question is clearly out of scope (forecasting, causal, external data) — \
those should be refused without a clarifying question.{alias_lines}

Respond with exactly this JSON:
{{
  "answerable": "<boolean>",
  "reason": "<brief explanation of why the question is or is not answerable>",
  "domain": "<article_engagement | article_keywords | keyword_engagement | contributor_behaviour | ingestion_errors | system_info | unknown>",
  "suggested_metrics": ["<column_name_or_aggregate_expression>"],
  "clarifying_question": "<short question to resolve ambiguity, or null if not ambiguous>"
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": _EXAMPLE_USER},
        {"role": "assistant", "content": _EXAMPLE_ASSISTANT},
        {"role": "user", "content": user},
    ]
