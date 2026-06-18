PROMPT_VERSION = "sql_gen_v1"


def build_sql_generation_prompt(question: str, views_context: str) -> list[dict]:
    system = (
        "You generate T-SQL SELECT statements for Azure SQL Server. "
        "You must only query the analytics views provided. "
        "Every query must use SELECT TOP N where N is between 1 and 500. "
        "Never use LIMIT, FETCH FIRST, or OFFSET — this is T-SQL, not standard SQL. "
        "Never query any table outside the analytics schema. "
        "Respond only with valid JSON containing a single key 'sql'. "
        "No markdown fences, no explanation outside the JSON."
    )
    user = f"""Generate a T-SQL SELECT statement to answer this question:
"{question}"

Approved views and columns:
{views_context}

Rules:
- Query only analytics.* views listed above.
- Use SELECT TOP N (1 <= N <= 500). Do not use LIMIT or FETCH FIRST.
- No DDL, DML, EXEC, subqueries outside analytics schema, or multi-statement queries.
- Include only columns that exist in the view definitions above.
- For ranking questions, use ORDER BY with SELECT TOP 10 (or another appropriate N).
- For aggregate-only questions (SUM, AVG, COUNT, MAX, MIN with no natural row limit), \
use SELECT TOP 500.
- For filter-only questions where all matching rows are needed, use SELECT TOP 500.

Respond with exactly this JSON:
{{
  "sql": "SELECT TOP 10 col1, col2 FROM analytics.vw_... ORDER BY col1 DESC"
}}"""
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
