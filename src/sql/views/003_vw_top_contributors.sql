IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
EXEC('CREATE SCHEMA analytics');
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW analytics.vw_top_contributors AS
SELECT
    contributor_id,
    COUNT(*) AS comment_count,
    COALESCE(AVG(CAST(sentiment AS FLOAT)), 0.0) AS avg_sentiment,
    SUM(replies_count) AS total_replies,
    COUNT(DISTINCT article_id) AS distinct_article_count
FROM dbo.core_comments
GROUP BY contributor_id;
