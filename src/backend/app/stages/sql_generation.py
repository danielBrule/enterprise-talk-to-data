import json
import re
import time
from dataclasses import dataclass, field

from ..services.llm_service import LLMService
from ..prompts.sql_generation import PROMPT_VERSION, build_sql_generation_prompt
from ..core.config import settings
from ..core.logger import logger
from ..models.pipeline_context import PipelineContext
from .base import Stage, Refusal, refuse


@dataclass
class SQLGenResult:
    sql: str
    prompt_version: str
    model_deployment: str
    latency_ms: float
    token_usage: dict = field(default_factory=dict)
    filters: list = field(default_factory=list)


class SQLGenerationService:
    def __init__(self):
        try:
            self.llm = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm = None
            self.llm_available = False

    def _build_views_context(self, metadata_context: dict, joins: dict | None = None) -> str:
        """
        Format metadata_context into a plain-text block for the SQL generation prompt.

        Produces one section per view with purpose, grain, columns, allowed aggregations,
        valid GROUP BY dimensions, and limitations. Appends a cross-view join policy
        section when joins data is provided.
        """
        parts = []
        for view_name, view_data in metadata_context.items():
            columns = view_data.get("columns", [])
            col_list = ", ".join(c["name"] for c in columns if "name" in c)
            purpose = view_data.get("purpose", view_data.get("description", ""))
            grain = view_data.get("grain", "")
            allowed_aggs = view_data.get("allowed_aggregations", {})
            dimensions = view_data.get("dimensions", [])
            limitations = view_data.get("limitations", [])

            part = f"View: {view_name}\n"
            part += f"  Purpose: {purpose}\n"
            if grain:
                part += f"  Grain: {grain}\n"
            part += f"  Available columns: {col_list}\n"
            if allowed_aggs:
                agg_lines = "; ".join(
                    f"{col}: {', '.join(funcs)}" for col, funcs in allowed_aggs.items()
                )
                part += f"  Allowed aggregations: {agg_lines}\n"
            if dimensions:
                part += f"  Valid GROUP BY dimensions: {', '.join(dimensions)}\n"
            else:
                part += "  Valid GROUP BY dimensions: (none — this view is already at grain level)\n"
            if limitations:
                part += f"  Limitations: {'; '.join(limitations)}\n"
            parts.append(part)

        if joins is not None:
            approved = joins.get("approved_joins") or []
            join_lines = ["Cross-view join policy:"]
            if approved:
                for j in approved:
                    views = " + ".join(j.get("views", []))
                    key = j.get("join_key", "")
                    join_lines.append(f"  APPROVED: {views} ON {key}")
            else:
                join_lines.append(
                    "  No cross-view JOINs approved — query each view independently."
                )
            parts.append("\n".join(join_lines))

        return "\n".join(parts)

    async def generate(self, question: str, metadata_context: dict, joins: dict | None = None, correction: str | None = None, conversation_history: list | None = None) -> SQLGenResult:
        start = time.perf_counter()
        deployment = settings.get_azure_openai_deployment("sql_generation")

        if not self.llm_available:
            logger.warning("sql_generation.llm_unavailable question=%s", question[:80])
            return SQLGenResult(
                sql="",
                prompt_version=PROMPT_VERSION,
                model_deployment="none",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        views_context = self._build_views_context(metadata_context, joins)
        messages = build_sql_generation_prompt(question, views_context, correction=correction, conversation_history=conversation_history)

        try:
            raw, usage = await self.llm.generate_sql_generation(messages, temperature=0)
            clean = re.sub(r"```(?:json|sql)?", "", raw).strip().strip("`").strip()
            result = json.loads(clean)
            sql = result.get("sql", "").strip()
            filters = [str(f) for f in result.get("filters", []) if f]
            logger.info(
                "sql_generation.generated question=%s sql_preview=%s filters=%s",
                question[:60],
                sql[:80],
                filters,
            )
            return SQLGenResult(
                sql=sql,
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
                token_usage=usage,
                filters=filters,
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(
                "sql_generation.parse_failed error=%s raw_preview=%s",
                str(e),
                (raw or "")[:200],
            )
            return SQLGenResult(
                sql="",
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
            )


class SQLGenerationStage(Stage):
    def __init__(self, sql_generation_service: SQLGenerationService | None = None):
        self.sql_generation_service = sql_generation_service or SQLGenerationService()

    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()

        is_retry = ctx.sql_validation_error is not None
        if is_retry:
            ctx.trace.sql_retries += 1
        attempt_num = ctx.trace.sql_retries + 1  # 1-based; sql_retries=0 on first attempt
        logger.info(
            "sql_generation.attempt attempt=%d is_retry=%s question=%s",
            attempt_num, is_retry, ctx.question[:60],
        )

        result = await self.sql_generation_service.generate(
            ctx.question,
            ctx.metadata_context or {},
            joins=ctx.joins_config,
            correction=ctx.sql_validation_error,
            conversation_history=ctx.conversation_history or None,
        )

        # Accumulate latency and tokens across attempts so totals are accurate
        elapsed_ms = (time.perf_counter() - t0) * 1000
        ctx.latency["sql_generation_ms"] = ctx.latency.get("sql_generation_ms", 0) + elapsed_ms

        prev = ctx.trace.token_usage.get("sql_generation", {})
        ctx.trace.token_usage["sql_generation"] = {
            "prompt_tokens": prev.get("prompt_tokens", 0) + result.token_usage.get("prompt_tokens", 0),
            "completion_tokens": prev.get("completion_tokens", 0) + result.token_usage.get("completion_tokens", 0),
            "total_tokens": prev.get("total_tokens", 0) + result.token_usage.get("total_tokens", 0),
        }

        ctx.trace.sql_attempts.append(result.sql)  # always recorded — empty string included for debug
        ctx.trace.generated_sql = result.sql  # overwritten each attempt; final value = last attempt
        ctx.trace.filters_applied = result.filters  # overwritten on retry; final value = last attempt
        ctx.trace.prompt_versions["sql_generation"] = result.prompt_version
        ctx.trace.model_deployments["sql_generation"] = result.model_deployment
        ctx.sql = result.sql

        if not result.sql:
            return refuse(ctx, "SQL generation produced no query — cannot answer this question.")
        return None
