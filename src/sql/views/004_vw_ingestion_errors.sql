IF NOT EXISTS (SELECT * FROM sys.schemas WHERE name = 'analytics')
EXEC('CREATE SCHEMA analytics');
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE OR ALTER VIEW analytics.vw_ingestion_errors AS
SELECT
    id AS error_id,
    stage,
    data_id,
    error_type,
    error_message,
    attempted_at
FROM dbo.ops_pipeline_errors;
