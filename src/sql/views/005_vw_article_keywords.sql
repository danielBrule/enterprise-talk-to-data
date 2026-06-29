IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
EXEC('CREATE SCHEMA analytics');
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW analytics.vw_article_keywords AS
SELECT
    a.id          AS article_id,
    a.title,
    a.publication_date,
    au.url,
    k.id          AS keyword_id,
    k.full_keyword
FROM dbo.core_articles AS a
LEFT JOIN dbo.core_articles_urls AS au ON au.id = a.id
JOIN dbo.core_article_keywords   AS ak ON ak.article_id = a.id
JOIN dbo.core_keywords           AS k  ON k.id = ak.keyword_id;
