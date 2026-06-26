import asyncio
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..stages.base import Stage

from ..models.pipeline_context import PipelineContext
from ..stages.base import Refusal, Success
from ..models.talk_to_data import AskRequest, AskResponse
from ..models.trace import TraceRecord
from ..stages.intent import IntentService, IntentStage
from ..stages.view_selection import ViewSelectionService, ViewSelectionStage
from ..stages.metadata import MetadataStage
from ..stages.sql_generation import SQLGenerationService, SQLGenerationStage
from ..stages.sql_validation import SQLValidationStage
from ..stages.execution import ExecutionStage
from ..core.auth import ResolvedUser
from ..core.config import settings
from ..core.input_safety import validate_user_input, InputSafetyError
from ..core.logger import logger
from ..core.trace_store import TraceStore
from ..services.llm_service import APITimeoutError
from ..services.metadata_service import get_approved_joins
from ..db.analytics_store import AnalyticsStore
from ..db.data_quality_store import DataQualityStore
from ..stages.answer import AnswerService, AnswerStage


class TalkToDataPipeline:
    """
    Orchestrates the 7-stage question-to-answer pipeline.

    Each stage receives the shared PipelineContext and returns a StageOutcome:
      - None     → stage passed, continue to the next stage
      - Refusal  → pipeline stops, reason surfaced to the caller
      - Success  → pipeline complete (only AnswerStage returns this)

    Stages in order
    ---------------
    1. IntentStage          [LLM: schema_retrieval]
       Classifies whether the question is answerable from the available analytics views.
       Refuses if: question is out of scope, LLM unavailable, or JSON parse fails.

    2. ViewSelectionStage   [LLM: schema_retrieval]
       Selects which analytics.* views are relevant to the question.
       Refuses if: selection confidence < 0.4, or no views could be identified.

    3. MetadataStage        [no LLM]
       Loads full schema + metrics metadata for the selected views from YAML files.
       Refuses if: no metadata is found for the selected views.

    4. SQLGenerationStage   [LLM: sql_generation]
       Generates a SQL SELECT query from the question and view metadata.
       Refuses if: LLM unavailable, LLM returns no query, or JSON parse fails.

    5. SQLValidationStage   [no LLM]
       Validates the generated SQL: SELECT only, analytics.* views only, no DDL/DML,
       no multi-statement, LIMIT required, columns exist in metadata, mandatory filters
       present. Does NOT refuse directly — stores the error in ctx.sql_validation_error
       so the pipeline can retry SQL generation (up to MAX_SQL_RETRIES times) with the
       error as a correction hint before surfacing a refusal to the user.

    6. ExecutionStage       [no LLM]
       Executes the validated SQL against Azure SQL.
       Returns Refusal with status "failed" (not "refused") on database errors.

    7. AnswerStage          [LLM: summary]
       Translates query result rows into a natural-language answer with caveats
       sourced from view metadata limitations.
       Always returns Success — falls back to a row-count summary if LLM is unavailable.
    """

    def __init__(
        self,
        intent_service: IntentService | None = None,
        view_selection_service: ViewSelectionService | None = None,
        sql_generation_service: SQLGenerationService | None = None,
        answer_service: AnswerService | None = None,
        trace_store: TraceStore | None = None,
        quality_store: DataQualityStore | None = None,
    ):
        # Exposed as attributes so tests can inject mocks via pipeline.<service>.method = AsyncMock(...)
        self.intent_service = intent_service or IntentService()
        self.view_selection_service = view_selection_service or ViewSelectionService()
        self.sql_generation_service = sql_generation_service or SQLGenerationService()
        self.answer_service = answer_service or AnswerService()
        # Injectable so tests can pass a MagicMock() and avoid writing to disk.
        self._trace_store = trace_store or TraceStore(analytics_store=AnalyticsStore())
        self._quality_store = quality_store or DataQualityStore()

        # Named references for the SQL retry sub-loop — avoids brittle positional indexing
        self._pre_sql_stages: "list[Stage]" = [
            IntentStage(self.intent_service),
            ViewSelectionStage(self.view_selection_service),
            MetadataStage(),
        ]
        self._sql_gen_stage = SQLGenerationStage(self.sql_generation_service)
        self._sql_val_stage = SQLValidationStage()
        self._post_sql_stages: "list[Stage]" = [
            ExecutionStage(),
            AnswerStage(self.answer_service, self._quality_store),
        ]
        # Kept for test introspection (monkeypatch.setattr targets this attribute)
        self.stages = (
            self._pre_sql_stages
            + [self._sql_gen_stage, self._sql_val_stage]
            + self._post_sql_stages
        )

    async def run(self, request: AskRequest, user: ResolvedUser) -> AskResponse:
        ctx = PipelineContext(
            question=request.question,
            user_context=request.user_context,
            trace=TraceRecord(
                question=request.question,
                user_context=request.user_context,
                session_id=request.session_id,
            ),
            latency={},
            pipeline_start=time.perf_counter(),
            user=user,
            conversation_history=request.conversation_history,
        )
        # Record resolved identity in the trace so every response is self-documenting.
        # "Enforcement planned (Task 11)" is intentional — the note tracks what IS
        # enforced, not what will be. Update this string when enforcement is wired in.
        ctx.trace.access_enforcement_note = (
            f"Role '{user.role}' resolved via X-User-Role header. "
            f"Allowed views: {user.allowed_views}. "
            f"Access enforced at execution stage."
        )

        try:
            try:
                validate_user_input(request.question)
            except InputSafetyError as e:
                reason = str(e)
                ctx.trace.refusal_reason = reason
                ctx.trace.execution_status = "refused"
                return AskResponse(refused=True, refusal_reason=reason, trace=ctx.trace)

            timeout = settings.pipeline_timeout_seconds
            try:
                return await asyncio.wait_for(self._run_stages(ctx), timeout=timeout)
            except (asyncio.TimeoutError, APITimeoutError):
                reason = f"Request timed out after {timeout}s — please try a simpler question."
                ctx.trace.refusal_reason = reason
                ctx.trace.execution_status = "failed"
                return AskResponse(refused=True, refusal_reason=reason, trace=ctx.trace)
        finally:
            # Append the trace on every code path: answered, refused, and timed out.
            # Python's finally guarantee fires this even when the try block contains
            # a return statement, so a single call here covers all exit points.
            self._trace_store.append(ctx.trace)

    async def _run_stages(self, ctx: PipelineContext) -> AskResponse:
        budget = settings.max_tokens_per_request
        max_sql_retries = settings.max_sql_retries

        def _to_response(outcome) -> AskResponse | None:
            if isinstance(outcome, Refusal):
                return AskResponse(refused=True, refusal_reason=outcome.reason, trace=outcome.trace)
            if isinstance(outcome, Success):
                return AskResponse(answer=outcome.answer, caveats=outcome.caveats, refused=False, trace=outcome.trace)
            return None

        def _budget_response() -> AskResponse | None:
            if budget > 0:
                used = sum(u.get("total_tokens", 0) for u in ctx.trace.token_usage.values())
                if used > budget:
                    reason = f"Request exceeded the {budget}-token budget ({used} tokens used)."
                    logger.warning("cost.budget_exceeded total_tokens=%s limit=%s", used, budget)
                    ctx.trace.refusal_reason = reason
                    ctx.trace.execution_status = "refused"
                    return AskResponse(refused=True, refusal_reason=reason, trace=ctx.trace)
            return None

        # Stages 1–3: intent, view_selection, metadata (linear, no retry)
        for stage in self._pre_sql_stages:
            if r := _to_response(await stage.run(ctx)):
                return r
            if r := _budget_response():
                return r

        # Load join policy once — shared with both sql_gen (prompt) and sql_val (enforcement)
        # so approved_joins.yml is not re-read on every retry attempt.
        ctx.joins_config = await get_approved_joins()

        # Stages 4–5: SQL generation + validation with self-correction retry loop.
        # SQLValidationStage stores the error in ctx.sql_validation_error rather than
        # refusing directly, so the generation stage can receive it as a correction hint.
        for attempt in range(1, max_sql_retries + 2):
            if r := _to_response(await self._sql_gen_stage.run(ctx)):
                return r
            if r := _budget_response():
                return r

            await self._sql_val_stage.run(ctx)

            if ctx.sql_validation_error is None:
                break  # validation passed — proceed to execution

            if attempt > max_sql_retries:
                reason = (
                    f"The SQL query could not be generated correctly after "
                    f"{max_sql_retries + 1} attempts. "
                    f"Last error: {ctx.sql_validation_error}"
                )
                logger.warning(
                    "sql_generation.retry_exhausted attempts=%d error=%s",
                    attempt, ctx.sql_validation_error,
                )
                ctx.trace.refusal_reason = reason
                ctx.trace.execution_status = "refused"
                return AskResponse(refused=True, refusal_reason=reason, trace=ctx.trace)

            logger.info(
                "sql_generation.retrying attempt=%d error=%s",
                attempt, ctx.sql_validation_error,
            )

        # Stages 6–7: execution, answer (linear, no retry)
        for stage in self._post_sql_stages:
            if r := _to_response(await stage.run(ctx)):
                return r
            if r := _budget_response():
                return r

        raise RuntimeError("pipeline exited without a response — AnswerStage must always return Success")
