import pytest

from backend.app.core.sql_safety import validate_query, SQLSafetyError, MAX_LIMIT


# Valid queries
def test_validate_query_simple_select_with_limit():
    """Valid: Simple SELECT with LIMIT"""
    validate_query("SELECT * FROM analytics.vw_article_engagement LIMIT 50")


def test_validate_query_with_where_clause():
    """Valid: SELECT with WHERE and LIMIT"""
    validate_query(
        "SELECT id, title FROM analytics.vw_article_engagement WHERE article_id = 1 LIMIT 100"
    )


def test_validate_query_max_limit():
    """Valid: SELECT with max LIMIT"""
    validate_query(f"SELECT * FROM analytics.vw_keyword_engagement LIMIT {MAX_LIMIT}")


def test_validate_query_multiple_views():
    """Valid: JOIN across analytics views"""
    validate_query("""
        SELECT a.article_id, k.keyword_id 
        FROM analytics.vw_article_engagement a
        JOIN analytics.vw_keyword_engagement k ON a.article_id = k.article_id
        LIMIT 50
    """)


def test_validate_query_with_aggregation():
    """Valid: SELECT with GROUP BY and aggregation"""
    validate_query("""
        SELECT article_id, COUNT(*) as count
        FROM analytics.vw_article_engagement
        GROUP BY article_id
        LIMIT 10
    """)


# Invalid queries - wrong statement type
def test_validate_query_insert_rejected():
    """Invalid: INSERT is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("INSERT INTO analytics.vw_article_engagement VALUES (1)")


def test_validate_query_update_rejected():
    """Invalid: UPDATE is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("UPDATE analytics.vw_article_engagement SET title = 'foo'")


def test_validate_query_delete_rejected():
    """Invalid: DELETE is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("DELETE FROM analytics.vw_article_engagement")


def test_validate_query_drop_rejected():
    """Invalid: DROP is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("DROP TABLE analytics.vw_article_engagement")


def test_validate_query_create_rejected():
    """Invalid: CREATE is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query(
            "CREATE VIEW test AS SELECT * FROM analytics.vw_article_engagement"
        )


def test_validate_query_execute_rejected():
    """Invalid: EXECUTE is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("EXECUTE sp_test")


def test_validate_query_grant_rejected():
    """Invalid: GRANT is not allowed"""
    with pytest.raises(SQLSafetyError, match="Only SELECT statements"):
        validate_query("GRANT SELECT ON analytics.vw_article_engagement")


# Invalid queries - schema restrictions
def test_validate_query_dbo_table_rejected():
    """Invalid: Direct dbo.* table access is not allowed"""
    with pytest.raises(SQLSafetyError, match="Direct table access"):
        validate_query("SELECT * FROM dbo.articles LIMIT 50")


def test_validate_query_dbo_join_rejected():
    """Invalid: JOIN with dbo.* table is not allowed"""
    with pytest.raises(SQLSafetyError, match="Direct table access"):
        validate_query("""
            SELECT a.id, c.comment
            FROM analytics.vw_article_engagement a
            JOIN dbo.comments c ON a.article_id = c.article_id
            LIMIT 50
        """)


# Invalid queries - missing or invalid LIMIT
def test_validate_query_no_limit_rejected():
    """Invalid: Missing LIMIT clause"""
    with pytest.raises(SQLSafetyError, match="must include a LIMIT or TOP clause"):
        validate_query("SELECT * FROM analytics.vw_article_engagement")


def test_validate_query_limit_exceeds_max():
    """Invalid: LIMIT exceeds maximum"""
    with pytest.raises(SQLSafetyError, match="exceeds maximum"):
        validate_query(
            f"SELECT * FROM analytics.vw_article_engagement LIMIT {MAX_LIMIT + 1}"
        )


def test_validate_query_limit_zero():
    """Invalid: LIMIT is zero"""
    with pytest.raises(SQLSafetyError, match="must be greater than 0"):
        validate_query("SELECT * FROM analytics.vw_article_engagement LIMIT 0")


def test_validate_query_limit_negative():
    """Invalid: LIMIT is negative"""
    with pytest.raises(SQLSafetyError, match="must be greater than 0"):
        validate_query("SELECT * FROM analytics.vw_article_engagement LIMIT -10")


# Edge cases
def test_validate_query_empty_string():
    """Invalid: Empty query"""
    with pytest.raises(SQLSafetyError, match="non-empty string"):
        validate_query("")


def test_validate_query_none():
    """Invalid: None query"""
    with pytest.raises(SQLSafetyError, match="non-empty string"):
        validate_query(None)


def test_validate_query_whitespace_only():
    """Invalid: Whitespace only"""
    with pytest.raises(SQLSafetyError, match="Only SELECT"):
        validate_query("   \n\t   ")


def test_validate_query_case_insensitive_keywords():
    """Valid: Keywords are case-insensitive"""
    validate_query("select * from analytics.vw_article_engagement limit 50")
    validate_query("SeLeCt * FrOm analytics.vw_article_engagement LiMiT 50")


def test_validate_query_dangerous_keyword_in_string_literal():
    """Invalid: Dangerous keywords are detected even in string context (conservative approach)"""
    # This is a limitation but safer to reject potentially dangerous patterns
    with pytest.raises(SQLSafetyError, match="Keyword"):
        validate_query("SELECT 'INSERT' FROM analytics.vw_article_engagement LIMIT 50")
