import json
import re
import time
from dataclasses import dataclass, field

from .llm_service import LLMService
from ..prompts.answer_generation import PROMPT_VERSION, build_answer_generation_prompt
from ..core.config import settings
from ..core.logger import logger


@dataclass
class AnswerResult:
    answer: str
    caveats: list[str]
    prompt_version: str
    model_deployment: str
    latency_ms: float


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

    async def generate(
        self,
        question: str,
        sql: str,
        results: list[dict],
        metadata_context: dict,
    ) -> AnswerResult:
        start = time.perf_counter()
        deployment = settings.get_azure_openai_deployment("summary")
        metadata_caveats = self._collect_caveats(metadata_context)

        if not self.llm_available:
            logger.warning("answer_service.llm_unavailable question=%s", question[:80])
            row_count = len(results)
            return AnswerResult(
                answer=f"Query returned {row_count} row(s). LLM not configured for answer generation.",
                caveats=metadata_caveats,
                prompt_version=PROMPT_VERSION,
                model_deployment="none",
                latency_ms=(time.perf_counter() - start) * 1000,
            )

        messages = build_answer_generation_prompt(question, sql, results, metadata_caveats)

        try:
            raw = await self.llm.generate_summary(messages, temperature=0)
            clean = re.sub(r"```(?:json)?", "", raw).strip().strip("`").strip()
            result = json.loads(clean)
            return AnswerResult(
                answer=result.get("answer", ""),
                caveats=result.get("caveats", metadata_caveats),
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
            )
        except (json.JSONDecodeError, KeyError) as e:
            logger.warning("answer_service.parse_failed error=%s", str(e))
            row_count = len(results)
            return AnswerResult(
                answer=f"Query returned {row_count} row(s). Answer generation failed.",
                caveats=metadata_caveats,
                prompt_version=PROMPT_VERSION,
                model_deployment=deployment,
                latency_ms=(time.perf_counter() - start) * 1000,
            )
