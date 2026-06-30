# Production Practices

Maps the safety, governance, resilience and observability mechanisms in this pipeline to the files that implement them.

✅ = implemented · [demo] = intentionally simplified for a self-contained build; the production equivalent is noted inline.

---

## Input safety

Runs before any LLM call or database access.

| Practice | File |
|---|---|
| **Injection attempts refused, not stripped** — SQL comments (`--`, `/*`), prompt-override phrases (`ignore previous instructions`, `you are now…`, LLM token markers), control characters and questions over `MAX_QUESTION_LENGTH` (default 1 000) all trigger an immediate refusal with a structured `security.injection_attempt` log entry | `app/core/input_safety.py` | `MAX_QUESTION_LENGTH` |
| **Refuse, don't sanitise** — stripping injection attempts silently allows the question through and hides the signal; refusing and logging is the correct call for an enterprise system | `app/core/input_safety.py` |

**Coarse pre-filter, not the safety boundary.** Regex/keyword matching only catches phrasings someone thought to list; it is trivially bypassed by paraphrase, translation or encoding (base64, unicode homoglyphs). It is not relied on as the actual control — that's [query safety](#query-safety) below, which allow-lists what SQL can ever execute regardless of what the LLM was tricked into generating. A stronger input-side filter — e.g. Azure AI Content Safety's **Prompt Shields**, a classifier rather than a pattern list, already available since this runs on Azure OpenAI — would catch more attempts (paraphrase, obfuscation) at the cost of added latency and a per-call charge. Not implemented here; the deterministic downstream control was judged sufficient for this build's scope.

---

## Query safety

Stage 5 validation runs before the query touches the database. No LLM involved — fully deterministic.

| Practice | File |
|---|---|
| **AST-based validation (sqlglot)** — parses in tsql dialect before rule checks; handles string literals, CTEs and subqueries correctly where regex cannot | `app/core/sql_safety.py` |
| **SELECT only, approved views only** — non-SELECT statements and references outside `analytics.*` are rejected | `app/core/sql_safety.py` |
| **No DDL / DML** — DROP, INSERT, UPDATE, DELETE, MERGE, TRUNCATE, EXECUTE, GRANT blocked | `app/core/sql_safety.py` |
| **Row limit required** — TOP / LIMIT mandatory; max 500 rows enforced | `app/core/sql_safety.py` |
| **Join allowlist** — cross-view joins validated against `approved_joins.yml`; forbidden pairs include reason and alternative. Currently all cross-view pairs are forbidden (different grains, no shared key) | `app/core/sql_safety.py`, `app/stages/sql_validation.py` |
| **Column and filter validation** — SQL checked against view column lists; mandatory filters declared in view YAML enforced for views referenced in the query | `app/core/sql_safety.py` |

---

## Resilience

Three timeout layers, each targeting a different failure mode. The first two are independent; the pipeline timeout is the outer boundary that contains them — see the retry-loop note below.

| Layer | Covers | Env var |
|---|---|---|
| DB query timeout | Slow or locked SQL query | `SQL_QUERY_TIMEOUT_SECONDS` (default 30) |
| LLM call timeout | Slow or hung Azure OpenAI request | `LLM_TIMEOUT_SECONDS` (default 60) |
| Pipeline timeout | End-to-end wall-clock limit across all stages | `PIPELINE_TIMEOUT_SECONDS` (default 120) |

All three return a user-facing refusal with a clear message. Both `asyncio.TimeoutError` and `openai.APITimeoutError` are caught and handled uniformly — no bare 500s.

**SQL self-correction retry loop** — when SQL validation fails, the error is fed back to the SQL generation stage as a correction hint and the query is regenerated. Up to `MAX_SQL_RETRIES` retries (default 2) before refusing. Token usage and latency accumulate across all attempts so the budget check is accurate. | `app/services/talk_to_data_pipeline.py` | `MAX_SQL_RETRIES`

**Retries share the pipeline timeout — they don't get their own budget.** The loop itself has no timeout; only each individual SQL-generation call inside it is bounded by `LLM_TIMEOUT_SECONDS`. The loop as a whole draws down the same `PIPELINE_TIMEOUT_SECONDS` clock as every other stage (intent, view selection, execution, answer generation). Worst case — `MAX_SQL_RETRIES + 1` slow attempts — can exhaust the pipeline timeout before the loop's own "retries exhausted" refusal fires, in which case the caller gets the generic timeout message instead of the more diagnostic retry-exhaustion one.

**Per-request token budget** — accumulated `total_tokens` across all LLM stages is checked after each call; the pipeline refuses early if the budget is exceeded. Set to 0 to disable. | `app/services/talk_to_data_pipeline.py` | `MAX_TOKENS_PER_REQUEST` (default 10 000)

---

## Observability

| Practice | File |
|---|---|
| **Full trace on every response** — latency per stage, token usage per stage, actual model version (not deployment alias), generated SQL, row count, prompt versions, refusal reasons | `app/models/trace.py`, `app/services/llm_service.py` |
| **Enrichment fields on AskResponse** — `source_view`, `metric_definitions`, `filters_applied`, `sql`, `row_count`, `confidence`, `latency_ms`, `token_usage` surfaced as top-level fields on every response; defaults to null/empty on early refusals where the pipeline never reaches metadata or SQL | `app/models/talk_to_data.py` |
| **Dual-write trace store** — every pipeline run written to both `data/analytics/traces.jsonl` (append-only, replay source) and `data/analytics/analytics.db` (SQLite, queryable, JOIN-able with feedback on `trace_id`). Writes are independent — a SQLite failure never prevents the JSONL write. [demo: SQLite; production would use the Azure SQL analytics database] | `app/db/analytics_store.py` | `TRACE_FILE`, `ANALYTICS_DB`, `PIPELINE_ENV` |
| **Feedback endpoint** — `POST /feedback` accepts `{trace_id, rating: -1\|1, comment?}`, dual-writes to JSONL and SQLite. Feedback table is JOIN-able with traces so you can navigate: failed question → SQL → user rating in one query | `app/api/routes.py`, `app/core/feedback_store.py` |
| **Structured logging** — security, timeout and budget events use structured key=value format (`security.injection_attempt`, `llm.timeout`, `cost.budget_exceeded`) for log aggregation | `app/core/input_safety.py`, `app/services/llm_service.py` |
| **Health check** — `GET /health` probes Azure SQL (live `SELECT 1`), LLM config (all 5 env vars present) and metadata YAML files. HTTP 503 on error so load balancers can route around a broken instance; 200 on degraded (core up, metadata missing) | `app/services/health_service.py` |
| **PII filter** — SHA-256-hashes the question and drops `user_context` before trace writes when enabled. Disabled by default (analytics domain, no personal data in questions). Extend with Microsoft Presidio before the hash step for HR or finance domains | `app/core/pii_filter.py` | `TRACE_ANONYMIZE` |

---

## Governance

| Practice | File |
|---|---|
| **Intent classification before data access** — question classified against domain vocabulary before any LLM or database call. Includes identifier columns so questions like "which articles have no comments?" resolve correctly | `app/stages/intent.py`, `app/prompts/intent.py` |
| **Short-circuit intents** — `system_info`, `clarifying` and `data_quality` exit after stage 1 with no SQL or database access. Clarification signals the question is in scope but underspecified; data quality returns a markdown health report from `DataQualityStore` | `app/stages/intent.py`, `app/services/talk_to_data_pipeline.py` |
| **View selection with confidence threshold** — confidence < 0.4 is refused rather than guessed | `app/stages/view_selection.py` |
| **Metadata grounding** — SQL generated against approved view definitions (column names, grain, allowed aggregations, mandatory filters, limitations), not inferred from user wording. Grain and aggregation contracts prevent double-counting and semantically invalid aggregations | `app/stages/metadata.py`, `app/stages/sql_generation.py`, `src/metadata/` |
| **Data quality caveats** — per-view health checks (row count, freshness, NULL rate on sentiment columns, sanity bounds) injected as answer caveats at query time. [demo: SQLite; production would be a table in Azure SQL, managed by dbt or Great Expectations at ingestion time] | `app/services/data_quality_service.py`, `app/db/data_quality_store.py` |
| **Role-based access** — `X-User-Role` header maps to an allowed-views list; role stamped on trace. [demo: header-based; production requires Azure AD group membership + row-level security enforced in SQL — `auth.py` documents the replacement pattern] | `app/core/auth.py`, `app/api/routes.py` |
| **Access enforcement at execution** — before running the query, `ExecutionStage` extracts every view referenced in the SQL via the sqlglot AST and refuses with `security.access_denied` if any view is outside `allowed_views` | `app/stages/execution.py`, `app/core/sql_safety.py` |
| **Multi-turn conversation** — `AskRequest` accepts `conversation_history: list[ConversationTurn]`; server is stateless, client owns history. Last N turns injected into SQL generation and intent prompts so follow-ups resolve correctly. Window size and answer truncation are env-configurable | `app/models/talk_to_data.py`, `app/prompts/sql_generation.py` | `MAX_HISTORY_TURNS`, `MAX_HISTORY_ANSWER_CHARS` |

---

## Evaluation

| Practice | File |
|---|---|
| **Golden question set** — curated questions covering in-scope, out-of-scope, safe-failure, access enforcement and multi-turn conversation cases | `src/metadata/example_questions/golden_questions.yml` |
| **Automated eval runner** — fast mode (stages 1–5, no DB) or full mode (all 7 stages); reports pass/fail, latency and token usage per question. Exit code 1 if pass rate < 80% | `evaluation_runner.py` (`make eval`) |
| **Failure taxonomy** — failing and partial records tagged by category (semantic, retrieval, sql, access, answer, other) for targeted diagnosis | `app/evaluation/golden_runner.py` |
| **Access enforcement tests** — `ACCESS_TEST_CASES` injects SQL + role pairs directly into `ExecutionStage`, no LLM or DB required. Denied cases assert `security.access_denied`; allowed cases confirm legitimate queries are not blocked | `app/evaluation/golden_runner.py` |
| **MLflow tracking** — every run logged: pass rate, per-stage token usage, model versions, prompt versions, pipeline config. `mlflow.db` and `mlruns/` are committed so `make mlflow-ui` works immediately after clone | `evaluation_runner.py` |

---

## CI / CD

GitHub Actions runs on every push to `main` and on all pull requests: lint (ruff) then the full 225-test suite with `PYTHONPATH: src` exported so import paths match local development. `make tests` is the single entry point — it runs the syntax gate first so a broken import never silently skips a test.

---

## Docker

`src/Dockerfile`, build context at repo root (needed for `COPY pyproject.toml` and `COPY src/`). `python:3.12-slim` base; dependencies installed before source code so the heavy layer only rebuilds when `pyproject.toml` or `poetry.lock` change; `poetry install --without dev`; `poetry config virtualenvs.create false` (system Python, no venv PATH issues); ODBC Driver 18 baked in; `ENV PYTHONPATH=src`.

---

## Infrastructure

Terraform provisions Azure OpenAI resources in `src/infra/terraform/`. **Azure SQL is not managed by Terraform** and must be provisioned separately.

Three task-specific OpenAI deployments (`schema-retrieval`, `sql-generation`, `summary`) are provisioned as separate resources so model tier and token budget can be tuned per task via Terraform variables. `envs/dev/` and `envs/prod/` tfvars separate environments. Endpoint and deployment names are exported as Terraform outputs so `.env` can be filled without navigating the portal.

---

## Configuration

Secrets (`AZURE_OPENAI_API_KEY`, `AZURE_SQL_PASSWORD`) fail loudly if missing — no defaults. All timeout, safety and cost limits have sensible defaults so the system runs out of the box. Every env var is documented in `.env.example` with an inline comment explaining the trade-off.
