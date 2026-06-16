from pydantic import BaseModel, Field


class ContributorFilters(BaseModel):
    min_comments: int | None = Field(None, ge=0)
    min_articles: int | None = Field(None, ge=0)
    min_replies: int | None = Field(None, ge=0)


class ContributorResponse(BaseModel):
    contributor_id: str
    comment_count: int
    avg_sentiment: float | None = None
    total_replies: int
    distinct_article_count: int
