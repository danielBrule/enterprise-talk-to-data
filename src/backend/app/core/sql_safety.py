import re

from .logger import logger


class SQLSafetyError(Exception):
    """Raised when a query violates SQL safety rules."""
    pass


DANGEROUS_KEYWORDS = [
    r"\bINSERT\b",
    r"\bUPDATE\b",
    r"\bDELETE\b",
    r"\bDROP\b",
    r"\bCREATE\b",
    r"\bALTER\b",
    r"\bTRUNCATE\b",
    r"\bEXEC\b",
    r"\bEXECUTE\b",
    r"\bGRANT\b",
    r"\bREVOKE\b",
    r"\bDENY\b",
]

MAX_LIMIT = 500
QUERY_TIMEOUT_SECONDS = 30


# ── Rules ──────────────────────────────────────────────────────────────────────

def _check_is_select(normalized: str) -> None:
    if not normalized.startswith("SELECT"):
        raise SQLSafetyError("Only SELECT statements are allowed")


def _check_no_multi_statement(query: str) -> None:
    if ";" in query.strip()[:-1]:
        raise SQLSafetyError("Multi-statement queries are not allowed")


def _check_no_dangerous_keywords(normalized: str) -> None:
    for pattern in DANGEROUS_KEYWORDS:
        match = re.search(pattern, normalized, re.IGNORECASE)
        if match:
            raise SQLSafetyError(f"Keyword '{match.group(0)}' is not allowed")


def _check_no_dbo_access(normalized: str) -> None:
    if re.search(r"\b(FROM|JOIN)\s+dbo\.", normalized, re.IGNORECASE):
        raise SQLSafetyError(
            "Direct table access (dbo.*) is not allowed. Only analytics.* views are permitted."
        )


def _check_row_limit(normalized: str, params: dict | None) -> None:
    limit_match = re.search(
        r"\bLIMIT\s+\(?\s*(:[A-Z_][A-Z0-9_]*|-?\d+)\s*\)?",
        normalized,
        re.IGNORECASE,
    )
    top_match = re.search(
        r"\bSELECT\s+TOP\s*\(?\s*(:[A-Z_][A-Z0-9_]*|-?\d+)\s*\)?",
        normalized,
        re.IGNORECASE,
    )
    row_limit_match = limit_match or top_match

    if not row_limit_match:
        raise SQLSafetyError(
            f"Query must include a LIMIT or TOP clause (max {MAX_LIMIT})"
        )

    clause = "LIMIT" if limit_match else "TOP"
    raw = row_limit_match.group(1)

    if raw.startswith(":"):
        param_name = raw[1:].lower()
        logger.debug("sql_safety.param_check param=%s params_keys=%s", raw, list((params or {}).keys()))
        if not params or param_name not in params:
            raise SQLSafetyError(f"Missing parameter for {clause}: {raw}")
        try:
            value = int(params[param_name])
        except (TypeError, ValueError):
            raise SQLSafetyError(f"{clause} parameter {raw} must be an integer")
    else:
        value = int(raw)

    if value <= 0:
        raise SQLSafetyError(f"{clause} value must be greater than 0")
    if value > MAX_LIMIT:
        raise SQLSafetyError(f"{clause} value {value} exceeds maximum of {MAX_LIMIT}")


# ── Public API ─────────────────────────────────────────────────────────────────

def validate_query(query: str, params: dict | None = None) -> None:
    """
    Validate that a SQL query is safe to execute against the analytics views.

    Raises SQLSafetyError if any rule is violated:
    - Rule 1  : Must be a SELECT statement
    - Rule 2a : No multi-statement queries (semicolon before final character)
    - Rule 2b : No dangerous keywords (INSERT, UPDATE, DELETE, DROP, …)
    - Rule 3  : No direct dbo.* table access (analytics.* views only)
    - Rule 4/5: Must include SELECT TOP or LIMIT; value must be 1–MAX_LIMIT
    """
    if not query or not isinstance(query, str):
        raise SQLSafetyError("Query must be a non-empty string")

    normalized = re.sub(r"\s+", " ", query.strip()).upper()

    _check_is_select(normalized)
    _check_no_multi_statement(query)
    _check_no_dangerous_keywords(normalized)
    _check_no_dbo_access(normalized)
    _check_row_limit(normalized, params)


def add_query_timeout(timeout_seconds: int = QUERY_TIMEOUT_SECONDS) -> str:
    return f"SET STATEMENT_TIMEOUT {timeout_seconds * 1000}"
