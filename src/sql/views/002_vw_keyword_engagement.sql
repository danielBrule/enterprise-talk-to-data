IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
EXEC('CREATE SCHEMA analytics');
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW analytics.vw_keyword_engagement AS
SELECT
    k.id AS keyword_id,
    k.full_keyword,
    COUNT(DISTINCT ak.article_id) AS article_count,
    COUNT(c.id) AS comment_count,
    COALESCE(AVG(CAST(c.sentiment AS FLOAT)), 0.0) AS avg_comment_sentiment,
    COUNT(DISTINCT c.contributor_id) AS contributor_count
FROM dbo.core_keywords AS k
LEFT JOIN dbo.core_article_keywords AS ak ON ak.keyword_id = k.id
LEFT JOIN dbo.core_comments AS c ON c.article_id = ak.article_id
GROUP BY
    k.id,
    k.full_keyword;
