import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .api.routes import router, metadata_router
from .core.config import API_VERSION
from .core.logger import logger

app = FastAPI(
    title="Newspaper Talk to Data API",
    description="Backend API skeleton for newspaper analytics and SQL view access.",
    version=API_VERSION,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()
    logger.info(
        "request.start method=%s path=%s query=%s",
        request.method,
        str(request.url.path),
        str(request.url.query),
    )
    try:
        response = await call_next(request)
        return response
    except Exception as exc:
        logger.exception(
            "request.error method=%s path=%s error=%s",
            request.method,
            str(request.url.path),
            str(exc),
        )
        raise
    finally:
        duration_ms = (time.perf_counter() - start_time) * 1000
        status_code = response.status_code if "response" in locals() else 500
        logger.info(
            "request.complete method=%s path=%s status_code=%s duration_ms=%s",
            request.method,
            str(request.url.path),
            status_code,
            round(duration_ms, 2),
        )


@app.get("/health", tags=["health"])
async def health():
    return {"status": "ok"}


@app.get("/version", tags=["health"])
async def version():
    return {"version": API_VERSION}


app.include_router(router)
app.include_router(metadata_router)
