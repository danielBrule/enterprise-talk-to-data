PROMPT_VERSION = "sql_gen_v8"


def _format_history(conversation_history: list) -> str:
    """Format the last N turns for prompt injection. Answer truncated, SQL verbatim."""
    if not conversation_history:
        return ""
    from ..core.config import settings
    max_turns = settings.max_history_turns
    max_answer_chars = settings.max_history_answer_chars
    turns = conversation_history[-max_turns:]
    lines = ["Prior conversation (use to resolve follow-up references — 'that', 'same', 'instead', 'last month', etc.):"]
    for i, turn in enumerate(reversed(turns)):
        label = "Most recent turn" if i == 0 else f"Turn -{i + 1}"
        q = getattr(turn, "question", "") or ""
        sql = getattr(turn, "sql", None) or ""
        ans = getattr(turn, "answer", None) or ""
        if ans and len(ans) > max_answer_chars:
            ans = ans[:max_answer_chars] + "…"
        lines.append(f"[{label}]")
        lines.append(f"  Q: \"{q}\"")
        if sql:
            lines.append(f"  SQL: {sql}")
        if ans:
            lines.append(f"  A: {ans}")
    return "\n".join(lines) + "\n\n"


def build_sql_generation_prompt(
    question: str,
    views_context: str,
    correction: str | None = None,
    conversation_history: list | None = None,
) -> list[dict]:
    """
    Build the SQL generation prompt.

    Expects:
        question:      the user's natural language question
        views_context: pre-formatted string produced by _build_views_context —
                       one block per view with purpose, available columns, and limitations
        correction:    validation error from a previous attempt (optional). When provided,
                       a simulated assistant turn + correction request is appended so the
                       model understands exactly what went wrong and how to fix it.

    Returns a message list (system + user [+ assistant + correction user]) instructing
    the model to produce a single JSON object {"sql": "<T-SQL SELECT TOP N statement>"}.
    """
    system = (
        "You generate T-SQL SELECT statements for Azure SQL Server. "
        "You must only query the analytics views provided. "
        "Every query must use SELECT TOP N where N is between 1 and 500. "
        "Never use LIMIT, FETCH FIRST, or OFFSET — this is T-SQL, not standard SQL. "
        "Never query any table outside the analytics schema. "
        "Respond only with valid JSON containing keys 'sql' and 'filters'. "
        "No markdown fences, no explanation outside the JSON."
    )
    history_section = _format_history(conversation_history or [])
    user = f"""{history_section}Generate a T-SQL SELECT statement to answer this question:
"{question}"

Approved views and columns:
{views_context}

Rules:
- Query only analytics.* views listed above.
- Use SELECT TOP N (1 <= N <= 500). Do not use LIMIT or FETCH FIRST.
- No DDL, DML, EXEC, subqueries outside analytics schema, or multi-statement queries.
- Include only columns that exist in the view definitions above.
- For ranking questions, use ORDER BY with SELECT TOP 10 (or another appropriate N).
- For scalar aggregate questions (a single SUM/AVG/COUNT/MAX/MIN with no GROUP BY), \
use SELECT TOP 1 — the result is always one row.
- For grouped aggregate questions (aggregate + GROUP BY), use SELECT TOP 10 for \
"top N by metric" questions, or SELECT TOP 500 when all groups are needed.
- For filter-only questions where all matching rows are needed, use SELECT TOP 500.
- When returning multiple rows, always include the primary identifier column of the view \
(article_id for vw_article_engagement, keyword_id for vw_keyword_engagement, \
contributor_id for vw_top_contributors, error_id for vw_ingestion_errors).
- Use descriptive aliases for aggregate results that reflect the metric, \
e.g. total_comment_count, avg_sentiment, max_comment_count, error_count.
- Respect grain: each view already has one row per its stated unit (article, keyword, contributor, error). \
Do not re-aggregate a column if the grain context shows rows are already atomic.
- Respect allowed aggregations: only apply the aggregate functions listed for each column. \
Never SUM a column listed as [AVG, MIN, MAX] only (e.g. avg_comment_sentiment, avg_sentiment).
- GROUP BY only columns listed as valid dimensions for the view. \
If no dimensions are listed, the view is already at grain level — do not add GROUP BY.
- Do not JOIN analytics views unless the pair is listed as APPROVED in the cross-view join \
policy above. If no approved joins are listed, every cross-view JOIN is forbidden — \
query the single most relevant view instead.

Respond with exactly this JSON:
{{
  "sql": "<SELECT TOP N col1, col2 FROM analytics.vw_name [WHERE ...] [ORDER BY ...]>",
  "filters": ["<short description of each WHERE condition, e.g. 'publication_date >= 2025'>"]
}}

If no WHERE conditions are applied, return an empty list for "filters"."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]

    if correction:
        messages.append({"role": "assistant", "content": '{"sql": "<invalid — see correction>"}'})
        messages.append({
            "role": "user",
            "content": (
                "CORRECTION REQUIRED — your previous query failed validation:\n\n"
                f"ERROR: {correction}\n\n"
                "Generate a corrected SQL query that fixes this exact error. "
                "Do not repeat the same mistake. "
                "Follow all original rules above. "
                "Respond with only the JSON object."
            ),
        })

    return messages
