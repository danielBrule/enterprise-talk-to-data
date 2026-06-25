"""
SQL safety validation using sqlglot AST parsing.

All checks operate on the parsed AST rather than regex so they are correct for
CTEs, subqueries, aliases, and string literals containing SQL keywords. On any
parse failure the query is rejected (fail closed).

Dialect: tsql — matches Azure SQL Server. sqlglot normalises SELECT TOP N to the
same Limit node as LIMIT N, so a single _check_row_limit covers both forms.
"""
from itertools import combinations

import sqlglot
import sqlglot.expressions as exp

from .config import settings
from .logger import logger


class SQLSafetyError(Exception):
    """Raised when a query violates SQL safety rules."""
    pass


MAX_LIMIT = 500
QUERY_TIMEOUT_SECONDS: int = settings.sql_query_timeout_seconds

_DIALECT = "tsql"

_FORBIDDEN_NODE_TYPES = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Create,
    exp.Alter,
    exp.TruncateTable,
    exp.Merge,
    exp.Execute,   # EXEC / EXECUTE
    exp.Grant,
)


# ── Parsing ────────────────────────────────────────────────────────────────────

def _parse(query: str) -> tuple[exp.Expression, list]:
    """Parse with tsql dialect. Raises SQLSafetyError on failure (fail closed)."""
    try:
        statements = sqlglot.parse(query, dialect=_DIALECT, error_level=sqlglot.ErrorLevel.RAISE)
    except sqlglot.errors.ParseError as e:
        raise SQLSafetyError(f"Query could not be parsed: {e}") from e
    if not statements or statements[0] is None:
        raise SQLSafetyError("Only SELECT statements are allowed")
    return statements[0], statements


# ── Rules ──────────────────────────────────────────────────────────────────────

def _check_single_select(statements: list) -> None:
    if len(statements) > 1:
        raise SQLSafetyError("Multi-statement queries are not allowed")
    if not isinstance(statements[0], exp.Select):
        raise SQLSafetyError("Only SELECT statements are allowed")


def _check_no_dangerous_nodes(tree: exp.Expression) -> None:
    for node_type in _FORBIDDEN_NODE_TYPES:
        if tree.find(node_type):
            raise SQLSafetyError(f"Statement type '{node_type.__name__}' is not allowed")


def _check_no_dbo_access(tree: exp.Expression) -> None:
    for table in tree.find_all(exp.Table):
        db = (table.args.get("db") or exp.Identifier(this="")).name.lower()
        if db == "dbo":
            raise SQLSafetyError(
                "Direct table access (dbo.*) is not allowed. Only analytics.* views are permitted."
            )


def _check_row_limit(tree: exp.Expression, params: dict | None) -> None:
    """Require TOP or LIMIT with a value in (0, MAX_LIMIT]. sqlglot normalises
    SELECT TOP N to the same Limit node as LIMIT N in tsql dialect."""
    limit = tree.find(exp.Limit)

    if not limit:
        raise SQLSafetyError(f"Query must include a LIMIT or TOP clause (max {MAX_LIMIT})")

    value_expr = limit.args.get("expression")
    if value_expr is None:
        raise SQLSafetyError("LIMIT/TOP clause has no value")

    # Negative literal: LIMIT -10 parses as Neg(Literal(10))
    if isinstance(value_expr, exp.Neg):
        raise SQLSafetyError("LIMIT/TOP value must be greater than 0")

    # Parameter placeholder (e.g. :row_limit)
    if isinstance(value_expr, (exp.Parameter, exp.Var)):
        param_name = str(value_expr).lstrip(":").lower()
        if not params or param_name not in params:
            raise SQLSafetyError(f"Missing parameter for LIMIT/TOP: :{param_name}")
        try:
            value = int(params[param_name])
        except (TypeError, ValueError):
            raise SQLSafetyError(f"LIMIT/TOP parameter :{param_name} must be an integer")
    else:
        try:
            value = int(value_expr.name)
        except (TypeError, ValueError, AttributeError):
            raise SQLSafetyError("LIMIT/TOP value could not be resolved to an integer")

    if value <= 0:
        raise SQLSafetyError("LIMIT/TOP value must be greater than 0")
    if value > MAX_LIMIT:
        raise SQLSafetyError(f"LIMIT/TOP value {value} exceeds maximum of {MAX_LIMIT}")


def _check_no_forbidden_joins(
    tree: exp.Expression, approved_pairs: set[frozenset]
) -> None:
    """
    Block any SQL that references more than one analytics view unless every
    view pair it touches is listed in the approved join register.

    Operates on the AST so CTE aliases and subquery references resolve to their
    source tables — regex scanning of the raw SQL string cannot do this.
    """
    views = {
        f"analytics.{table.name.lower()}"
        for table in tree.find_all(exp.Table)
        if (table.args.get("db") or exp.Identifier(this="")).name.lower() == "analytics"
    }
    if len(views) < 2:
        return
    for a, b in combinations(sorted(views), 2):
        if frozenset({a, b}) not in approved_pairs:
            raise SQLSafetyError(
                f"Cross-view query not allowed: {a} and {b} cannot be used together. "
                "Query each view independently."
            )


# ── Public API ─────────────────────────────────────────────────────────────────

def validate_query(
    query: str,
    params: dict | None = None,
    approved_pairs: set[frozenset] | None = None,
) -> None:
    """
    Validate that a SQL query is safe to execute against the analytics views.

    Raises SQLSafetyError if any rule is violated:
    - Rule 1  : Must be a single SELECT statement (no DDL/DML, no multi-statement)
    - Rule 2  : No dangerous statement types inside the tree (Insert, Drop, Merge …)
    - Rule 3  : No direct dbo.* table access (analytics.* views only)
    - Rule 4/5: Must include SELECT TOP or LIMIT; value must be 1–MAX_LIMIT
    - Rule 6  : Cross-view references only allowed for approved pairs (skipped if
                approved_pairs is None — backward compat for callers without a policy)

    Fails closed: any parse error rejects the query.
    """
    if not query or not isinstance(query, str):
        raise SQLSafetyError("Query must be a non-empty string")

    tree, statements = _parse(query)

    _check_single_select(statements)
    _check_no_dangerous_nodes(tree)
    _check_no_dbo_access(tree)
    _check_row_limit(tree, params)
    if approved_pairs is not None:
        _check_no_forbidden_joins(tree, approved_pairs)

    logger.debug("sql_safety.passed query_preview=%s", query[:80])
