-- Performance indexes for analytics views.
--
-- Root cause of slow view queries: the three heavy views (article_engagement,
-- keyword_engagement, top_contributors) do full-table aggregations with JOINs.
-- Without indexes on the join and group keys, every query is a full scan.
--
-- Apply with: make apply-sql-indexes
-- Safe to re-run: CREATE INDEX ... IF NOT EXISTS is idempotent.

-- vw_article_engagement: JOINs core_comments and core_article_keywords on article_id
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_comments_article_id' AND object_id = OBJECT_ID('dbo.core_comments'))
    CREATE INDEX idx_comments_article_id ON dbo.core_comments(article_id);

IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_article_keywords_article_id' AND object_id = OBJECT_ID('dbo.core_article_keywords'))
    CREATE INDEX idx_article_keywords_article_id ON dbo.core_article_keywords(article_id);

-- vw_keyword_engagement: JOINs core_article_keywords on keyword_id
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_article_keywords_keyword_id' AND object_id = OBJECT_ID('dbo.core_article_keywords'))
    CREATE INDEX idx_article_keywords_keyword_id ON dbo.core_article_keywords(keyword_id);

-- vw_top_contributors: GROUP BY contributor_id on core_comments (317s without index)
IF NOT EXISTS (SELECT 1 FROM sys.indexes WHERE name = 'idx_comments_contributor_id' AND object_id = OBJECT_ID('dbo.core_comments'))
    CREATE INDEX idx_comments_contributor_id ON dbo.core_comments(contributor_id, article_id);
