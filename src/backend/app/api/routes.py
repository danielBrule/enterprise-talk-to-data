from typing import Annotated

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from ..core.auth import AuthError, DemoAuthService, ResolvedUser
from ..core.config import API_PREFIX, API_VERSION
from ..core.feedback_store import FeedbackStore
from ..db.analytics_store import AnalyticsStore
from ..models.feedback import FeedbackRecord, FeedbackRequest
from ..models.talk_to_data import AskRequest, AskResponse
from ..models.trace import RecentTraceItem
from ..services.article_service import get_article, list_articles
from ..services.contributor_service import get_contributor, list_contributors
from ..services.ingestion_error_service import list_ingestion_errors
from ..services.keyword_service import get_keyword, list_keywords
from ..services.data_quality_service import DataQualityService
from ..services.metadata_service import (
    get_views_metadata,
    get_metrics_metadata,
    get_glossary_metadata,
)
from ..services.talk_to_data_pipeline import TalkToDataPipeline
from ..validators import (
    ArticleResponse,
    ContributorResponse,
    IngestionErrorResponse,
    KeywordResponse,
)

router = APIRouter(prefix=API_PREFIX, tags=["analytics"])
metadata_router = APIRouter(prefix=f"{API_PREFIX}/metadata", tags=["metadata"])
data_quality_router = APIRouter(prefix=f"{API_PREFIX}/data-quality", tags=["data-quality"])

_auth_service = DemoAuthService()


async def get_current_user(
    x_user_role: Annotated[str | None, Header(alias="X-User-Role")] = None,
) -> ResolvedUser:
    """
    FastAPI dependency that resolves the caller's role from the X-User-Role header.

    DEMO ONLY — see app/core/auth.py for the production replacement pattern.
    In production this dependency would validate a Bearer token (Azure AD / OIDC)
    and extract role claims from the verified JWT, never from a plain header.
    """
    try:
        return _auth_service.resolve(x_user_role)
    except AuthError as exc:
        raise HTTPException(status_code=401, detail=str(exc))


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


@router.post("/ask", response_model=AskResponse, tags=["talk-to-data"])
async def ask(
    request: AskRequest,
    user: Annotated[ResolvedUser, Depends(get_current_user)],
) -> AskResponse:
    """
    Answer a natural language analytics question.

    Returns a grounded answer, caveats, and a full trace of every pipeline
    stage. When the question is out of scope, unsafe, or unanswerable,
    the response is refused with an explicit reason — never a silent failure.

    Requires an X-User-Role header (analyst / editor / admin). Missing header
    defaults to analyst. Unknown role returns 401.
    """
    pipeline = TalkToDataPipeline()
    return await pipeline.run(request, user)


@router.get("/traces/recent", response_model=list[RecentTraceItem], tags=["talk-to-data"])
async def get_recent_traces(
    user: Annotated[ResolvedUser, Depends(get_current_user)],
    limit: int = Query(20, ge=1, le=100),
) -> list[RecentTraceItem]:
    """
    Return the N most recent pipeline runs, newest first.

    Used by the UI recent-questions panel. Each item is a compact summary —
    full trace detail (SQL, token usage, per-stage latency) is omitted.
    """
    raw_records = AnalyticsStore().get_recent_traces(limit=limit)
    return [_to_recent_item(r) for r in raw_records]


@router.post("/feedback", status_code=201, tags=["talk-to-data"])
async def submit_feedback(
    request: FeedbackRequest,
    user: Annotated[ResolvedUser, Depends(get_current_user)],
) -> dict:
    """
    Submit thumbs-up (1) or thumbs-down (-1) feedback on a pipeline answer.

    Stored in data/analytics/feedback.jsonl (raw log) and data/analytics/analytics.db
    (queryable, JOIN-able with the traces table via trace_id).
    """
    record = FeedbackRecord(
        trace_id=request.trace_id,
        rating=request.rating,
        comment=request.comment,
        user_role=user.role,
    )
    FeedbackStore(analytics_store=AnalyticsStore()).append(record)
    return {"feedback_id": record.feedback_id}


def _to_recent_item(raw: dict) -> RecentTraceItem:
    import json as _json
    # selected_views is stored as a JSON string in SQLite
    selected_views = raw.get("selected_views") or []
    if isinstance(selected_views, str):
        selected_views = _json.loads(selected_views)
    # latency_total_ms is a direct float column in SQLite (not a nested dict)
    latency_total_ms = raw.get("latency_total_ms")
    if latency_total_ms is None:
        latency = raw.get("latency_ms") or {}
        latency_total_ms = latency.get("total_ms") if isinstance(latency, dict) else None
    answer = raw.get("answer")
    if answer and len(answer) > 200:
        answer = answer[:200] + "…"
    return RecentTraceItem(
        trace_id=raw.get("trace_id", ""),
        timestamp=raw.get("timestamp", ""),
        question=raw.get("question", ""),
        execution_status=raw.get("execution_status"),
        intent=raw.get("intent"),
        selected_views=selected_views,
        answer=answer,
        refusal_reason=raw.get("refusal_reason"),
        latency_total_ms=latency_total_ms,
        user_context=raw.get("user_context"),
        session_id=raw.get("session_id"),
    )


@router.get("/version", tags=["analytics"])
async def read_version():
    return {"version": API_VERSION}


@data_quality_router.post("/refresh")
async def refresh_data_quality():
    """
    Run health checks for all analytics views and persist results to local SQLite.

    Intended to be called once daily (manually or via an external scheduler).
    Returns the full quality report immediately so callers can inspect results
    without a separate GET call.
    """
    service = DataQualityService()
    results = await service.refresh_all()
    return {
        "checked_at": results[0].checked_at if results else None,
        "views": [
            {
                "view_name": r.view_name,
                "row_count": r.row_count,
                "freshness_days": r.freshness_days,
                "null_rates": r.null_rates,
                "sanity_issues": r.sanity_issues,
                "error": r.error,
            }
            for r in results
        ],
    }


@data_quality_router.get("")
async def get_data_quality():
    """
    Return the most recent data quality report from local SQLite.

    Returns an empty views list if no refresh has been run yet.
    Call POST /data-quality/refresh to populate.
    """
    service = DataQualityService()
    results = await service.get_latest()
    checked_at = results[0].checked_at if results else None
    return {
        "checked_at": checked_at,
        "views": [
            {
                "view_name": r.view_name,
                "row_count": r.row_count,
                "freshness_days": r.freshness_days,
                "null_rates": r.null_rates,
                "sanity_issues": r.sanity_issues,
                "error": r.error,
            }
            for r in results
        ],
    }
