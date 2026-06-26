import json
import time
from dataclasses import dataclass, field

from ..services.llm_service import LLMService
from ..services.metadata_service import get_view_aliases
from ..prompts.intent import PROMPT_VERSION, build_intent_prompt
from ..core.config import settings
from ..core.logger import logger
from ..models.pipeline_context import PipelineContext
from .base import Stage, Refusal, refuse


@dataclass
class IntentResult:
    answerable: bool
    reason: str
    domain: str
    suggested_metrics: list[str]
    prompt_version: str
    model_deployment: str
    latency_ms: float
    token_usage: dict = field(default_factory=dict)


class IntentService:
    def __init__(self):
        try:
            self.llm = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm = None
            self.llm_available = False

    async def classify(self, question: str, conversation_history: list | None = None) -> IntentResult:
        start = time.perf_counter()
        deployment = settings.get_azure_openai_deployment("schema_retrieval")

        if not self.llm_available:
            logger.warning("intent.llm_unavailable question=%s", question[:80])
            return IntentResult(
                answerable=False,
                reason="LLM not configured — cannot classify intent",
                domain="unknown",
                suggested_metrics=[],
                prompt_version=PROMPT_VERSION,
                model_deployment="none",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        aliases = await get_view_aliases()
        messages = build_intent_prompt(question, aliases=aliases, conversation_history=conversation_history)
        try:
            raw, usage = await self.llm.generate_schema_retrieval(messages, temperature=0)
            result = json.loads(raw.strip())
            logger.info(
                "intent.classified question=%s answerable=%s domain=%s",
                question[:80],
                result.get("answerable"),
                result.get("domain"),
            )
            return IntentResult(
                answerable=bool(result.get("answerable", False)),
                reason=result.get("reason", ""),
                domain=result.get("domain", "unknown"),
                suggested_metrics=result.get("suggested_metrics", []),
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
                token_usage=usage,
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.error("intent.parse_failed error=%s", str(e))
            return IntentResult(
                answerable=False,
                reason=f"Intent parse failed ({e}) — cannot determine answerability",
                domain="unknown",
                suggested_metrics=[],
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
            )


class IntentStage(Stage):
    def __init__(self, intent_service: IntentService | None = None):
        self.intent_service = intent_service or IntentService()

    async def run(self, ctx: PipelineContext) -> Refusal | None:
        t0 = time.perf_counter()
        result = await self.intent_service.classify(ctx.question, conversation_history=ctx.conversation_history)
        ctx.latency["intent_ms"] = (time.perf_counter() - t0) * 1000

        ctx.trace.intent = result.domain
        ctx.trace.answerable = result.answerable
        ctx.trace.prompt_versions["intent"] = result.prompt_version
        ctx.trace.model_deployments["intent"] = result.model_deployment
        ctx.trace.token_usage["intent"] = result.token_usage

        if not result.answerable:
            return refuse(ctx, result.reason)
        return None
