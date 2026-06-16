from fastapi import APIRouter, HTTPException, Query

from ..core.config import API_PREFIX, API_VERSION
from ..services.article_service import get_article, list_articles
from ..services.contributor_service import get_contributor, list_contributors
from ..services.ingestion_error_service import list_ingestion_errors
from ..services.keyword_service import get_keyword, list_keywords
from ..services.metadata_service import (
    get_views_metadata,
    get_metrics_metadata,
    get_glossary_metadata,
)
from ..services.view_selection_service import ViewSelectionService
from ..validators import (
    ArticleResponse,
    ContributorResponse,
    IngestionErrorResponse,
    KeywordResponse,
)

router = APIRouter(prefix=API_PREFIX, tags=["analytics"])
metadata_router = APIRouter(prefix=f"{API_PREFIX}/metadata", tags=["metadata"])


@router.get("/articles", response_model=list[ArticleResponse])
async def read_articles(limit: int = Query(50, ge=1, le=500)):
    return await list_articles(limit=limit)


@router.get("/articles/{article_id}", response_model=ArticleResponse)
async def read_article(article_id: str):
    article = await get_article(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article


@router.get("/keywords", response_model=list[KeywordResponse])
async def read_keywords(limit: int = Query(50, ge=1, le=500)):
    return await list_keywords(limit=limit)


@router.get("/keywords/{keyword_id}", response_model=KeywordResponse)
async def read_keyword(keyword_id: str):
    keyword = await get_keyword(keyword_id)
    if not keyword:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return keyword


@router.get("/contributors", response_model=list[ContributorResponse])
async def read_contributors(limit: int = Query(50, ge=1, le=500)):
    return await list_contributors(limit=limit)


@router.get("/contributors/{contributor_id}", response_model=ContributorResponse)
async def read_contributor(contributor_id: str):
    contributor = await get_contributor(contributor_id)
    if not contributor:
        raise HTTPException(status_code=404, detail="Contributor not found")
    return contributor


@router.get("/errors", response_model=list[IngestionErrorResponse])
async def read_ingestion_errors(limit: int = Query(50, ge=1, le=500)):
    return await list_ingestion_errors(limit=limit)


# Metadata endpoints
@metadata_router.get("/views", response_model=list[dict])
async def get_views():
    """Get metadata for all analytics views."""
    return await get_views_metadata()


@metadata_router.get("/metrics", response_model=list[dict])
async def get_metrics():
    """Get metadata for all metrics."""
    return await get_metrics_metadata()


@metadata_router.get("/glossary", response_model=list[dict])
async def get_glossary():
    """Get metadata for all glossary terms."""
    return await get_glossary_metadata()


@metadata_router.post("/select-views")
async def select_views(question: str = Query(...)):
    """Select relevant views for a given question."""
    service = ViewSelectionService()
    return await service.select_views(question)


@router.get("/version", tags=["analytics"])
async def read_version():
    return {"version": API_VERSION}
