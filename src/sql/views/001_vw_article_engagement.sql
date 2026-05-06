IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
EXEC('CREATE SCHEMA analytics');
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW analytics.vw_article_engagement AS
SELECT
    a.id AS article_id,
    a.title,
    a.publication_date,
    a.insert_date,
    COUNT(c.id) AS comment_count,
    AVG(CAST(c.sentiment AS FLOAT)) AS avg_comment_sentiment,
    SUM(c.replies_count) AS total_replies,
    COUNT(DISTINCT ak.keyword_id) AS keyword_count
FROM dbo.core_articles AS a
LEFT JOIN dbo.core_comments AS c ON c.article_id = a.id
LEFT JOIN dbo.core_article_keywords AS ak ON ak.article_id = a.id
GROUP BY
    a.id,
    a.title,
    a.publication_date,
    a.insert_date;
