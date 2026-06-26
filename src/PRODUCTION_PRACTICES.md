# Production Practices — Reference Implementation

This document maps every production-readiness mechanism implemented in the pipeline to the file
that implements it and the environment variable that controls it. It is written for a reader who
wants to understand _what_ the system does to be safe, resilient and governable — and _where_ to
look to verify it.

✅ = implemented · 🔜 = planned (see task board)

---

## Input safety

Checks run before the question touches any LLM prompt or database.

| # | Practice | Status | File | Env var |
|---|---|---|---|---|
| 1 | **SQL comment injection blocked** — `--`, `/*`, `*/` in user input are refused (not stripped), with a log entry | ✅ | `app/core/input_safety.py` | — |
| 2 | **Prompt injection refused** — instruction-override phrases (`ignore previous instructions`, `you are now…`, `system:`, LLM token markers) trigger an immediate refusal | ✅ | `app/core/input_safety.py` | — |
| 3 | **Control character rejection** — null bytes and ESC sequences are refused | ✅ | `app/core/input_safety.py` | — |
| 4 | **Question length cap** — questions exceeding the limit are refused before any LLM call | ✅ | `app/core/input_safety.py` | `MAX_QUESTION_LENGTH` (default 1 000) |
| 5 | **Refuse, don't strip** — all input safety failures are refused with a user-facing message and a structured log entry (`security.injection_attempt`) for observability | ✅ | `app/core/input_safety.py` | — |

---

## Query safety (deterministic, pre-execution)

Validated by a pure-Python rule engine in stage 5. No LLM involved. The query is rejected _before_ reaching the database.

| # | Practice | Status | File |
|---|---|---|---|
| 6 | **SELECT only** — any statement that does not start with SELECT is rejected | ✅ | `app/core/sql_safety.py` |
| 7 | **Approved views only** — the FROM clause and any JOINs must reference `analytics.*` views exclusively; `dbo.*` and any other schema are rejected | ✅ | `app/core/sql_safety.py` |
| 8 | **No DDL / DML** — DROP, INSERT, UPDATE, DELETE, MERGE, TRUNCATE, EXECUTE, GRANT are blocked as dangerous keywords | ✅ | `app/core/sql_safety.py` |
| 9 | **No multi-statement** — semicolons inside the query body are rejected | ✅ | `app/core/sql_safety.py` |
| 10 | **Row limit required** — TOP / LIMIT clause is mandatory; max 500 rows enforced | ✅ | `app/core/sql_safety.py` |
| 11 | **JOIN allowlist** — cross-view JOINs validated against an approved join register. Scans the full SQL string (not just JOIN clauses) so subquery and CTE references are caught. Blocked when any view pair is not in `approved_joins.yml`; skips check when no policy is loaded (backward compat). Currently all cross-view pairs are forbidden. | ✅ | `app/core/sql_safety.py`, `app/stages/sql_validation.py` |
| 12 | **Column and filter validation** — generated SQL checked against view column lists (unknown columns rejected with a list of valid ones); mandatory filters declared in view YAML enforced per-view, scoped to views actually referenced in the query | ✅ | `app/core/sql_safety.py` |

---

## Resilience — timeout enforcement

Three independent layers, each targeting a different failure mode.

| Layer | Covers | Status | File | Env var |
|---|---|---|---|---|
| **DB query timeout** | Slow or locked SQL query | ✅ | `app/db/connection.py` | `SQL_QUERY_TIMEOUT_SECONDS` (default 30) |
| **LLM call timeout** | Slow or hung Azure OpenAI request | ✅ | `app/services/llm_service.py` | `LLM_TIMEOUT_SECONDS` (default 60) |
| **Pipeline timeout** | End-to-end wall-clock limit across all stages | ✅ | `app/services/talk_to_data_pipeline.py` | `PIPELINE_TIMEOUT_SECONDS` (default 120) |

All three timeout types return a user-facing refusal with a clear message (no bare 500 errors).
Both `asyncio.TimeoutError` (Python-level) and `openai.APITimeoutError` (SDK-level) are caught and
handled uniformly.

---

## Cost control

| # | Practice | Status | File | Env var |
|---|---|---|---|---|
| 13 | **Per-request token budget** — accumulated `total_tokens` across all LLM stages is checked after each LLM call; the pipeline refuses early if the budget is exceeded. Token usage is accumulated across SQL generation retries so the budget correctly reflects total cost. Set to 0 to disable. | ✅ | `app/services/talk_to_data_pipeline.py` | `MAX_TOKENS_PER_REQUEST` (default 10 000) |
| 13b | **SQL self-correction retry loop** — when SQL validation fails (any rule: missing column, forbidden join, missing TOP, etc.) the error is fed back to the SQL generation stage as a correction hint and the query is regenerated. Up to `MAX_SQL_RETRIES` retries before refusing to the user with the last error. Retry count is tracked in the trace (`sql_retries`) and logged to MLflow (`questions_with_sql_retries`, `total_sql_retries`). Token usage and latency are accumulated across all attempts. | ✅ | `app/services/talk_to_data_pipeline.py`, `app/stages/sql_generation.py`, `app/prompts/sql_generation.py` | `MAX_SQL_RETRIES` (default 2) |

---

## Observability

| # | Practice | Status | File |
|---|---|---|---|
| 14 | **Full trace on every response** — latency per stage, token usage per stage, model names, generated SQL, row count, prompt versions, refusal reasons | ✅ | `app/models/trace.py` |
| 14b | **Enrichment fields on AskResponse** — `source_view`, `metric_definitions[]` (name + description + allowed aggregations), `filters_applied[]` (LLM self-reported WHERE conditions), `sql`, `row_count`, `confidence`, `latency_ms` (per stage), `token_usage` (per stage) surfaced at the top level of every response. Designed for UI: main display (`source_view`, `filters_applied`, `row_count`), expandable panels (`metric_definitions`, `sql`), and debug view (`confidence`, `latency_ms`, `token_usage`). Enrichment fields default to null/empty on early refusals (intent, input safety, timeout) where the pipeline never reaches metadata or SQL stages. | ✅ | `app/models/talk_to_data.py`, `app/services/talk_to_data_pipeline.py` |
| 15 | **Model name captured from API response** — the actual model version (e.g. `gpt-4.1-mini-2025-04-14`) is stored, not the deployment alias | ✅ | `app/services/llm_service.py` |
| 16 | **MLflow experiment tracking** — every golden eval run logs pass/fail per question, token usage per stage, model names and pipeline latency | ✅ | `evaluation_runner.py` |
| 17 | **Structured logging** — security events (`security.injection_attempt`), timeout events (`llm.timeout`), budget events (`cost.budget_exceeded`) use structured key=value format | ✅ | `app/core/input_safety.py`, `llm_service.py`, `talk_to_data_pipeline.py` |
| 18 | **Dual-write trace store** — every pipeline run (answered or refused) is written to two backends in a single `append()` call: (1) `data/analytics/traces.jsonl` — append-only raw log, human-readable, replay source; (2) `data/analytics/analytics.db` — SQLite `traces` table, queryable and JOIN-able with `feedback` via `trace_id`. Writes are independent: a SQLite failure never prevents the JSONL write, and vice versa. Every record is stamped with `pipeline_env` so eval/dev traces can be filtered out of production dashboards. **DEMO ONLY** — SQLite is used for zero-setup local observability. In production, both `analytics.db` and `data_quality.db` would be tables in the same Azure SQL database as the analytics views, so traces, feedback and quality checks are all JOIN-able with source data in one place. `AnalyticsStore` uses standard SQL with no SQLite-specific extensions — swap `_get_conn()` for the Azure SQL pool and no other code changes are needed. | ✅ | `app/core/trace_store.py`, `app/db/analytics_store.py` | `TRACE_FILE`, `ANALYTICS_DB`, `PIPELINE_ENV` |
| 19 | **PII filter on trace writes** — `PiiFilter` runs before every trace write: when enabled, SHA-256-hashes the question (non-reversible, but stable for duplicate detection) and drops `user_context`. Disabled by default (internal analytics domain, no personal data in questions). In a domain with PII in queries (HR, finance), extend `PiiFilter.apply()` with Microsoft Presidio or Azure AI Language before the hash step. | ✅ | `app/core/pii_filter.py` | `TRACE_ANONYMIZE` (default `false`) |
| 20 | **Trace viewer endpoint** — `GET /traces/recent?limit=N` returns the N most recent pipeline runs (newest first) from `data/analytics/analytics.db`. Each record is a compact `RecentTraceItem` — answer truncated to 200 chars, full trace detail omitted. Used by the UI recent-questions panel. Requires `X-User-Role` header (same auth as `/ask`). | ✅ | `app/api/routes.py`, `app/db/analytics_store.py` |
| 20b | **Feedback endpoint** — `POST /feedback` accepts `{trace_id, rating: -1\|1, comment?}` and dual-writes to `data/analytics/feedback.jsonl` and the `feedback` table in `data/analytics/analytics.db`. The `feedback` table is JOIN-able with `traces` on `trace_id`, making it possible to navigate: bug → trace (SQL + answer) → user feedback in one query. `rating` is validated by Pydantic as `Literal[-1, 1]` so any other integer returns HTTP 422. | ✅ | `app/api/routes.py`, `app/core/feedback_store.py`, `app/db/analytics_store.py` |
| 21 | **Health check endpoint** — `GET /health` probes Azure SQL (live `SELECT 1`), LLM config (all 5 env vars present), and metadata YAML files. Returns `"ok"` / `"degraded"` / `"error"` with per-check detail. HTTP 503 on `"error"` so load balancers can route around a broken instance; 200 on `"degraded"` (core up, metadata missing). | ✅ | `app/services/health_service.py`, `app/main.py` |

---

## Governance — scope and access

| # | Practice | Status | File |
|---|---|---|---|
| 22 | **Intent classification** — question classified as in-scope / out-of-scope against the domain vocabulary before any data access. The domain listing in the prompt includes both identifier columns (article_id, full_keyword, contributor_id, error_id) and metric columns so the classifier can correctly resolve questions that filter by identifier (e.g. "which articles have no comments?"). | ✅ | `app/stages/intent.py` |
| 23 | **View selection with confidence threshold** — questions with view-selection confidence < 0.4 are refused rather than guessed | ✅ | `app/stages/view_selection.py` |
| 24 | **Metadata grounding** — SQL is generated from approved view definitions (column names, types, grain, limitations), not inferred from the user's wording | ✅ | `app/stages/metadata.py`, `app/stages/sql_generation.py` |
| 24b | **Grain and aggregation contracts in view metadata** — each metric YAML declares `grain` (what one row represents), `allowed_aggregations` (permitted SQL aggregate functions per column — e.g. no SUM on pre-averaged sentiment), `dimensions` (valid GROUP BY targets), and `mandatory_filters`. These are injected into the SQL generation prompt to prevent double-counting and semantically invalid aggregations. | ✅ | `src/metadata/metrics/`, `app/stages/sql_generation.py`, `app/prompts/sql_generation.py` |
| 25 | **Domain vocabulary aliases** — alternative names for metrics are loaded from view metadata so intent classification understands synonyms | ✅ | `app/stages/intent.py`, `src/metadata/metrics/` |
| 26 | **Answer caveats from metadata** — answer stage injects the `limitations` declared in view YAML as explicit caveats | ✅ | `app/stages/answer.py` |
| 27 | **Data quality caveats** — per-view health checks (row count, freshness, NULL rate on sentiment columns, sanity bounds) stored in local SQLite via `POST /api/v0/data-quality/refresh`; latest report read at answer time and injected as caveats including the last-check date and a stale-data nudge. **DEMO ONLY** — SQLite storage is used for zero-setup local operation; in production this would be a table in Azure SQL (see row 18). **Demo scope**: checks run a focused subset of what a production data layer would cover. In real life these checks would be managed by dbt tests, Great Expectations, Azure Purview Data Quality, or Databricks Quality Monitoring — running at ingestion time with full column coverage, per-column thresholds based on observed baselines, and historical drift comparison (e.g. via Power BI). NULL rate is monitored only on sentiment columns (most likely to have gaps); a production implementation would check every meaningful non-nullable column. | ✅ | `app/services/data_quality_service.py`, `app/db/data_quality_store.py`, `app/stages/answer.py` |
| 28 | **Persona-based access control** — `DemoAuthService` resolves `X-User-Role` header to one of three personas (analyst / editor / admin), each with an explicit allowed-views list. Role is stamped on the trace. **DEMO ONLY** — in production replace with Azure AD / OIDC JWT validation; never resolve permissions from a plain header. See `app/core/auth.py` module docstring for the production replacement pattern. | ✅ | `app/core/auth.py`, `app/api/routes.py` |
| 29 | **Access enforcement at execution** — before running the query, `ExecutionStage` extracts every view referenced in the SQL (via `extract_views()` on the sqlglot AST) and refuses with `security.access_denied` log if any view is outside the caller's `allowed_views`. Skipped when no user context is present (eval runner). | ✅ | `app/stages/execution.py`, `app/core/sql_safety.py` |
| 30 | **Approved join register** — `approved_joins.yml` declares which view pairs may be JOINed and which are forbidden, with reason and alternative for each forbidden pair. Loaded by `metadata_service.get_approved_joins()` and injected into the SQL generation prompt so the LLM never attempts a cross-view JOIN unless it is explicitly approved. Currently no cross-view JOINs are approved (all four views aggregate to different grains with no shared key). SQL validation enforcement is Task 9. | ✅ | `src/metadata/joins/approved_joins.yml`, `app/services/metadata_service.py`, `app/stages/sql_generation.py` |
| 31 | **Clarification stage** — ambiguous questions returned with a clarifying question rather than a low-confidence guess | 🔜 | planned |
| 32 | **Multi-turn conversation context** — `AskRequest` accepts a `conversation_history: list[ConversationTurn]` field (each turn carries the prior question, generated SQL, and a truncated answer). The client owns the full history and sends it on every call (stateless server). The SQL generation and intent stages inject the last 3 turns verbatim so follow-up questions ("what about last month?", "show me the top 5 instead") resolve correctly without re-stating the full context. Answers are truncated to 300 chars in the prompt (SQL is injected in full — it is the structurally critical part). `session_id` is server-generated (UUID v4) if the client omits it, and echoed back in every `AskResponse` so clients can link turns into a session. Window size and answer truncation are env-configurable (`MAX_HISTORY_TURNS`, `MAX_HISTORY_ANSWER_CHARS`). **Architecture decision**: a sliding window of the last 3 turns was chosen over LLM-based summarisation or SLM-based context selection. Summarisation is lossy for SQL (column names and filters are dropped); SLM selection is the right production direction but requires a model that understands SQL structural relevance, not just semantic similarity. **If user testing shows the 3-turn window is insufficient** (users regularly reference older context that drops off), the recommended production upgrade is an SLM relevance ranker: the client sends the full history, a small model scores each turn for structural relevance to the current question, and only the top-K turns are injected verbatim. The API contract (`conversation_history` list on the request) is already compatible with this upgrade — no client changes needed. | ✅ | `app/models/talk_to_data.py`, `app/prompts/sql_generation.py`, `app/stages/intent.py` |

---

## CI / CD

| # | Practice | Status | Where |
|---|---|---|---|
| 35 | **GitHub Actions CI on every push and PR** — runs on `push` to `main` and on all pull requests targeting `main` | ✅ | `.github/workflows/ci.yml` |
| 36 | **Lint gate (ruff)** — CI fails if any Python file under `src/` has a lint error; runs before tests | ✅ | `.github/workflows/ci.yml` |
| 37 | **Full unit test suite in CI** — all 212+ tests run in CI with no external dependencies (LLM and DB are fully mocked) | ✅ | `.github/workflows/ci.yml` |
| 38 | **PYTHONPATH set in CI** — `PYTHONPATH: src` is exported explicitly in the workflow so the import paths match local development | ✅ | `.github/workflows/ci.yml` |
| 39 | **Standardised task runner (Makefile)** — `make tests`, `make eval`, `make start-backend`, `make infra-apply` give consistent entry points across environments | ✅ | `Makefile` |

---

## Evaluation and model monitoring

| # | Practice | Status | Where |
|---|---|---|---|
| 40 | **Golden question set** — curated questions with expected answerability, domain and SQL intent, covering in-scope, out-of-scope and safe-failure cases | ✅ | `src/metadata/example_questions/golden_questions.yml` |
| 41 | **Automated evaluation runner** — replays golden questions through the live pipeline; reports pass/fail, latency and token usage per question | ✅ | `evaluation_runner.py` (`make eval`) |
| 42 | **MLflow experiment tracking** — every eval run logged as an MLflow experiment: per-question pass/fail, per-stage token usage, model names, overall pass rate | ✅ | `evaluation_runner.py` |
| 43 | **Model name tracking per stage** — actual model version (e.g. `gpt-4.1-mini-2025-04-14`) captured from the API response and logged to MLflow, enabling model comparison across eval runs | ✅ | `app/services/llm_service.py`, `evaluation_runner.py` |
| 44 | **Evaluation results committed to git** — `evaluation_results/` JSON snapshots committed alongside code so regressions are visible in diff without a running server | ✅ | `evaluation_results/` |
| 45 | **MLflow UI available locally** — `make mlflow-ui` launches MLflow at `localhost:5000` with no additional setup; `mlflow.db` and `mlruns/` are committed so the UI works immediately after `git clone`. Note: `data/data_quality/data_quality.db` is intentionally gitignored — unlike MLflow eval snapshots (generated offline, no credentials needed), data quality results require a live Azure SQL connection to produce and would be misleading if committed. Run `POST /api/v1/data-quality/refresh` once connected. | ✅ | `Makefile`, `mlflow.db`, `mlruns/` |
| 46e | **Access enforcement eval tests** — `ACCESS_TEST_CASES` in the golden runner injects SQL + role pairs directly into `ExecutionStage` (no LLM or DB required): denied cases confirm `security.access_denied` fires; allowed cases confirm access enforcement does not block legitimate queries. Pass rate logged to MLflow as `access_tests_pass_rate`. | ✅ | `app/evaluation/golden_runner.py`, `evaluation_runner.py` |

---

## Docker

| # | Practice | Status | Where |
|---|---|---|---|
| 46 | **Minimal base image** — `python:3.12-slim` (Debian bookworm slim); no unnecessary OS packages | ✅ | `Dockerfile` |
| 47 | **Dependency layer caching** — `pyproject.toml` and `poetry.lock` are copied and installed before source code, so the heavy dependency layer is rebuilt only when deps change | ✅ | `Dockerfile` |
| 48 | **Production-only install** — `poetry install --without dev` excludes test and linting tools from the image | ✅ | `Dockerfile` |
| 49 | **No venv inside container** — `poetry config virtualenvs.create false` installs into the system Python, keeping the image lean and avoiding PATH issues | ✅ | `Dockerfile` |
| 50 | **ODBC Driver 18 baked in** — Microsoft ODBC Driver 18 for SQL Server installed at build time; no runtime dependency fetching | ✅ | `Dockerfile` |
| 51 | **Explicit PYTHONPATH** — `ENV PYTHONPATH=src` set in the image so imports resolve identically to local development | ✅ | `Dockerfile` |

---

## Infrastructure as code (Terraform)

| # | Practice | Status | Where |
|---|---|---|---|
| 52 | **Module-based structure** — resources split into `modules/resource_group` and `modules/openai`; root module composes them | ✅ | `src/infra/terraform/` |
| 53 | **Three task-specific deployments provisioned** — `schema-retrieval`, `sql-generation`, `summary` deployed as separate Azure OpenAI deployments so model tier can be changed per task via Terraform variables | ✅ | `src/infra/terraform/main.tf` |
| 54 | **Model configurable per deployment** — `schema_retrieval_model`, `sql_generation_model`, `summary_model` variables allow different models per task without touching module code | ✅ | `src/infra/terraform/variables.tf` |
| 55 | **Environment-specific tfvars** — `envs/dev/` and `envs/prod/` directories hold separate variable files; `make infra-apply ENV=dev\|prod` targets the correct file | ✅ | `src/infra/terraform/envs/` |
| 56 | **Resource tagging** — all resources tagged with `environment` and `project` for cost attribution and resource management | ✅ | `src/infra/terraform/main.tf` |
| 57 | **Terraform outputs for `.env` population** — endpoint and deployment names are exported as Terraform outputs so `.env` can be filled without navigating the Azure portal | ✅ | `src/infra/terraform/outputs.tf` |

---

## Configuration hygiene

| # | Practice | Status |
|---|---|---|
| 31 | **Secrets have no default** — `AZURE_OPENAI_API_KEY`, `AZURE_SQL_PASSWORD` etc. fail loudly if missing | ✅ |
| 32 | **Tuning knobs have sensible defaults** — all timeout, safety and cost limits default to reasonable values so the system works out of the box | ✅ |
| 33 | **All env vars documented in `.env.example`** — with inline comments explaining the trade-off for each value | ✅ |
| 34 | **Three task-specific LLM deployments** — intent/view selection, SQL generation, and answer generation use separate deployments so model tier can be tuned per task | ✅ |
