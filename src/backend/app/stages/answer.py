import json
import re
import time
from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from ..services.llm_service import LLMService
from ..prompts.answer_generation import PROMPT_VERSION, build_answer_generation_prompt
from ..core.config import settings
from ..core.logger import logger
from ..db.data_quality_store import DataQualityStore, ViewHealthResult
from ..models.pipeline_context import PipelineContext
from .base import Stage, build_latency, Success


@dataclass
class AnswerResult:
    answer: str
    caveats: list[str]
    prompt_version: str
    model_deployment: str
    latency_ms: float
    token_usage: dict = field(default_factory=dict)


class AnswerService:
    def __init__(self):
        try:
            self.llm = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm = None
            self.llm_available = False

    def _collect_caveats(self, metadata_context: dict) -> list[str]:
        caveats = []
        for view_data in metadata_context.values():
            caveats.extend(view_data.get("limitations", []))
        return caveats

    def _collect_quality_caveats(
        self,
        metadata_context: dict,
        quality_results: list[ViewHealthResult],
    ) -> list[str]:
        caveats: list[str] = []
        today = date.today().isoformat()

        if not quality_results:
            caveats.append(
                "Data quality has not been checked yet — consider calling"
                " POST /api/v1/data-quality/refresh."
            )
            return caveats

        # Stamp with last check date (always shown)
        latest_checked_at = max(r.checked_at for r in quality_results)
        checked_date = latest_checked_at[:10]
        days_since = (date.today() - date.fromisoformat(checked_date)).days
        if days_since == 0:
            caveats.append(f"Data quality last checked: today ({checked_date}).")
        elif days_since == 1:
            caveats.append(
                f"Data quality last checked: yesterday ({checked_date})"
                " — consider running a fresh check."
            )
        else:
            caveats.append(
                f"Data quality last checked: {days_since} days ago ({checked_date})"
                " — consider running a fresh check."
            )

        selected_views = set(metadata_context.keys())
        quality_by_view = {r.view_name: r for r in quality_results}

        for view_name in selected_views:
            result = quality_by_view.get(view_name)
            if not result or result.error:
                continue

            high_row_count_is_bad = "ingestion_errors" in view_name

            if result.row_count == 0 and not high_row_count_is_bad:
                caveats.append(f"{view_name}: view currently contains no data.")
            elif result.row_count and result.row_count > 0 and high_row_count_is_bad:
                caveats.append(
                    f"{view_name}: {result.row_count} ingestion error(s) on record"
                    " — review pipeline health."
                )

            if result.freshness_days is not None and result.freshness_days > 7:
                caveats.append(
                    f"{view_name}: data is {result.freshness_days} day(s) old"
                    " — figures may not reflect current state."
                )

            for col, pct in result.null_rates.items():
                if pct > 20:
                    caveats.append(
                        f"{view_name}: {pct:.0f}% of records are missing {col}"
                        " — aggregates may be understated."
                    )

            for issue in result.sanity_issues:
                caveats.append(f"{view_name}: {issue}.")

        return caveats

    async def generate(
        self,
        question: str,
        sql: str,
        results: list[dict],
        metadata_context: dict,
        quality_results: list[ViewHealthResult] | None = None,
    ) -> AnswerResult:
        start = time.perf_counter()
        deployment = settings.get_azure_openai_deployment("summary")
        metadata_caveats = self._collect_caveats(metadata_context)
        quality_caveats = self._collect_quality_caveats(
            metadata_context, quality_results or []
        )
        all_caveats = metadata_caveats + quality_caveats

        if not self.llm_available:
            logger.warning("answer_service.llm_unavailable question=%s", question[:80])
            row_count = len(results)
            return AnswerResult(
                answer=f"Query returned {row_count} row(s). LLM not configured for answer generation.",
                caveats=all_caveats,
                prompt_version=PROMPT_VERSION,
                model_deployment="none",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        messages = build_answer_generation_prompt(question, sql, results, all_caveats)

        try:
            raw, usage = await self.llm.generate_summary(messages, temperature=0)
            clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
            result = json.loads(clean)
            return AnswerResult(
                answer=result.get("answer", ""),
                caveats=result.get("caveats", metadata_caveats),
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
                token_usage=usage,
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("answer_service.parse_failed error=%s", str(e))
            row_count = len(results)
            return AnswerResult(
                answer=f"Query returned {row_count} row(s). Answer generation failed.",
                caveats=all_caveats,
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
            )


class AnswerStage(Stage):
    def __init__(
        self,
        answer_service: AnswerService | None = None,
        quality_store: DataQualityStore | None = None,
    ):
        self.answer_service = answer_service or AnswerService()
        self._quality_store = quality_store or DataQualityStore()

    async def run(self, ctx: PipelineContext) -> Success:
        t0 = time.perf_counter()
        quality_results = await self._quality_store.get_latest_results()
        result = await self.answer_service.generate(
            ctx.question,
            ctx.sql or "",
            ctx.rows or [],
            ctx.metadata_context or {},
            quality_results=quality_results,
        )
        ctx.latency["answer_generation_ms"] = (time.perf_counter() - t0) * 1000

        ctx.trace.answer = result.answer
        ctx.trace.caveats = result.caveats
        ctx.trace.prompt_versions["answer_generation"] = result.prompt_version
        ctx.trace.model_deployments["answer_generation"] = result.model_deployment
        ctx.trace.token_usage["answer_generation"] = result.token_usage
        ctx.trace.latency_ms = build_latency(ctx)

        logger.info(
            "pipeline.complete trace_id=%s rows=%s total_ms=%.0f",
            ctx.trace.trace_id,
            ctx.trace.row_count,
            ctx.trace.latency_ms.total_ms or 0,
        )
        return Success(
            answer=result.answer,
            caveats=result.caveats,
            trace=ctx.trace,
        )
