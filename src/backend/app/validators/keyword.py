from pydantic import BaseModel, Field


class KeywordFilters(BaseModel):
    min_article_count: int | None = Field(None, ge=0)
    min_comment_count: int | None = Field(None, ge=0)
    min_contributor_count: int | None = Field(None, ge=0)


class KeywordResponse(BaseModel):
    keyword_id: int
    full_keyword: str
    article_count: int
    comment_count: int
    avg_comment_sentiment: float
    contributor_count: int
