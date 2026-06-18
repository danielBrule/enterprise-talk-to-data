import json
import re
import time
from dataclasses import dataclass

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


class SQLGenerationService:
    def __init__(self):
        try:
            self.llm = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm = None
            self.llm_available = False

    def _build_views_context(self, metadata_context: dict) -> str:
        """
        Format metadata_context into a plain-text block for the SQL generation prompt.

        Produces one section per view:
            View: analytics.vw_name
              Purpose: ...
              Available columns: col1, col2, ...
              Limitations: ...  (omitted when empty)
        """
        parts = []
        for view_name, view_data in metadata_context.items():
            columns = view_data.get("columns", [])
            col_list = ", ".join(c["name"] for c in columns if "name" in c)
            purpose = view_data.get("purpose", view_data.get("description", ""))
            limitations = view_data.get("limitations", [])

            part = f"View: {view_name}\n"
            part += f"  Purpose: {purpose}\n"
            part += f"  Available columns: {col_list}\n"
            if limitations:
                part += f"  Limitations: {'; '.join(limitations)}\n"
            parts.append(part)
        return "\n".join(parts)

    async def generate(self, question: str, metadata_context: dict) -> SQLGenResult:
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

        views_context = self._build_views_context(metadata_context)
        messages = build_sql_generation_prompt(question, views_context)

        try:
            raw = await self.llm.generate_sql_generation(messages, temperature=0)
            clean = re.sub(r"```(?:json|sql)?", "", raw).strip().strip("`").strip()
            result = json.loads(clean)
            sql = result.get("sql", "").strip()
            logger.info(
                "sql_generation.complete question=%s sql_preview=%s",
                question[:60],
                sql[:80],
            )
            return SQLGenResult(
                sql=sql,
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
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
        result = await self.sql_generation_service.generate(
            ctx.question, ctx.metadata_context or {}
        )
        ctx.latency["sql_generation_ms"] = (time.perf_counter() - t0) * 1000

        ctx.trace.generated_sql = result.sql
        ctx.trace.prompt_versions["sql_generation"] = result.prompt_version
        ctx.trace.model_deployments["sql_generation"] = result.model_deployment
        ctx.sql = result.sql

        if not result.sql:
            return refuse(ctx, "SQL generation produced no query — cannot answer this question.")
        return None
