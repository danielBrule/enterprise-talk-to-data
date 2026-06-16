from pydantic import BaseModel, Field
from datetime import datetime


class ArticleFilters(BaseModel):
    min_comments: int | None = Field(None, ge=0)
    max_comments: int | None = Field(None, ge=0)
    min_sentiment: float | None = Field(None, ge=-1.0, le=1.0)
    max_sentiment: float | None = Field(None, ge=-1.0, le=1.0)


class ArticleResponse(BaseModel):
    article_id: int
    title: str
    publication_date: datetime
    insert_date: datetime
    comment_count: int
    avg_comment_sentiment: float
    total_replies: int
    keyword_count: int
