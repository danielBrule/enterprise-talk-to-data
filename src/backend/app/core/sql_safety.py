import re
from typing import Tuple


class SQLSafetyError(Exception):
    """Raised when a query violates SQL safety rules."""
    pass


# Dangerous SQL keywords that should never appear in user queries
DANGEROUS_KEYWORDS = [
    r'\bINSERT\b',
    r'\bUPDATE\b',
    r'\bDELETE\b',
    r'\bDROP\b',
    r'\bCREATE\b',
    r'\bALTER\b',
    r'\bTRUNCATE\b',
    r'\bEXEC\b',
    r'\bEXECUTE\b',
    r'\bGRANT\b',
    r'\bREVOKE\b',
    r'\bDENY\b',
]

# Max number of rows that can be returned
MAX_LIMIT = 500

# Query timeout in seconds
QUERY_TIMEOUT_SECONDS = 30


def validate_query(query: str) -> None:
    """
    Validate that a SQL query is safe to execute.
    
    Rules:
    - Must be a SELECT statement
    - Can only reference analytics.* views (no raw dbo.* tables)
    - Cannot contain dangerous keywords (INSERT, UPDATE, DELETE, DROP, etc.)
    - Must include a LIMIT clause
    - LIMIT value must not exceed MAX_LIMIT
    
    Args:
        query: SQL query string to validate
        
    Raises:
        SQLSafetyError: If query violates any safety rules
    """
    if not query or not isinstance(query, str):
        raise SQLSafetyError("Query must be a non-empty string")
    
    # Normalize whitespace and convert to uppercase for analysis
    normalized = re.sub(r'\s+', ' ', query.strip()).upper()
    
    # Rule 1: Must be a SELECT statement
    if not normalized.startswith('SELECT'):
        raise SQLSafetyError("Only SELECT statements are allowed")
    
    # Rule 2: Check for dangerous keywords
    for keyword_pattern in DANGEROUS_KEYWORDS:
        if re.search(keyword_pattern, normalized, re.IGNORECASE):
            keyword = re.search(keyword_pattern, normalized, re.IGNORECASE).group(0)
            raise SQLSafetyError(f"Keyword '{keyword}' is not allowed")
    
    # Rule 3: Verify no direct dbo.* table access (only analytics.* views allowed)
    # Look for FROM or JOIN clauses referencing dbo.*
    dbo_pattern = r'\b(FROM|JOIN)\s+dbo\.'
    if re.search(dbo_pattern, normalized, re.IGNORECASE):
        raise SQLSafetyError("Direct table access (dbo.*) is not allowed. Only analytics.* views are permitted.")
    
    # Rule 4 & 5: Check for LIMIT clause and validate value
    # Allow negative numbers to catch them with proper error message
    limit_match = re.search(r'\bLIMIT\s+(-?\d+)\b', normalized, re.IGNORECASE)
    if not limit_match:
        raise SQLSafetyError(f"Query must include a LIMIT clause (max {MAX_LIMIT})")
    
    limit_value = int(limit_match.group(1))
    if limit_value <= 0:
        raise SQLSafetyError(f"LIMIT value must be greater than 0")
    
    if limit_value > MAX_LIMIT:
        raise SQLSafetyError(f"LIMIT value {limit_value} exceeds maximum of {MAX_LIMIT}")


def add_query_timeout(timeout_seconds: int = QUERY_TIMEOUT_SECONDS) -> str:
    """
    Get the SQL Server command to set query timeout.
    
    Args:
        timeout_seconds: Timeout in seconds
        
    Returns:
        SQL command string for setting timeout
    """
    # SQL Server uses milliseconds for timeout (from context manager perspective)
    # The timeout is typically enforced at connection level in asyncio.to_thread
    return f"SET STATEMENT_TIMEOUT {timeout_seconds * 1000}"
