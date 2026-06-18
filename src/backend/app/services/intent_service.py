import json
import time
from dataclasses import dataclass, field

from .llm_service import LLMService
from ..prompts.intent import PROMPT_VERSION, build_intent_prompt
from ..core.config import settings
from ..core.logger import logger


@dataclass
class IntentResult:
    answerable: bool
    reason: str
    domain: str
    suggested_metrics: list[str]
    prompt_version: str
    model_deployment: str
    latency_ms: float


class IntentService:
    def __init__(self):
        try:
            self.llm = LLMService()
            self.llm_available = True
        except ValueError:
            self.llm = None
            self.llm_available = False

    async def classify(self, question: str) -> IntentResult:
        start = time.perf_counter()
        deployment = settings.get_azure_openai_deployment("schema_retrieval")

        if not self.llm_available:
            logger.warning("intent.llm_unavailable question=%s", question[:80])
            return IntentResult(
                answerable=True,
                reason="LLM not configured — assuming answerable",
                domain="unknown",
                suggested_metrics=[],
                prompt_version=PROMPT_VERSION,
                model_deployment="none",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        messages = build_intent_prompt(question)
        try:
            raw = await self.llm.generate_schema_retrieval(messages, temperature=0)
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
