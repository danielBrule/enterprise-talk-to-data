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
| 11 | **JOIN allowlist** — cross-view JOINs validated against an approved join register | 🔜 | `app/core/sql_safety.py` |
| 12 | **Metric and filter validation** — generated SQL checked against mandatory filters declared in view metadata | 🔜 | planned |

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
| 13 | **Per-request token budget** — accumulated `total_tokens` across all LLM stages is checked after each LLM call; the pipeline refuses early if the budget is exceeded. Set to 0 to disable. | ✅ | `app/services/talk_to_data_pipeline.py` | `MAX_TOKENS_PER_REQUEST` (default 10 000) |

---

## Observability

| # | Practice | Status | File |
|---|---|---|---|
| 14 | **Full trace on every response** — latency per stage, token usage per stage, model names, generated SQL, row count, prompt versions, refusal reasons | ✅ | `app/models/trace.py` |
| 15 | **Model name captured from API response** — the actual model version (e.g. `gpt-4.1-mini-2025-04-14`) is stored, not the deployment alias | ✅ | `app/services/llm_service.py` |
| 16 | **MLflow experiment tracking** — every golden eval run logs pass/fail per question, token usage per stage, model names and pipeline latency | ✅ | `evaluation_runner.py` |
| 17 | **Structured logging** — security events (`security.injection_attempt`), timeout events (`llm.timeout`), budget events (`cost.budget_exceeded`) use structured key=value format | ✅ | `app/core/input_safety.py`, `llm_service.py`, `talk_to_data_pipeline.py` |
| 18 | **Trace store** — every pipeline run (answered or refused) appended to `traces/pipeline_traces.jsonl`. Interface is a single `_write()` method so the backend can be swapped for Azure SQL or Application Insights without touching the pipeline. In production: Azure SQL for queryable analytics; Application Insights for real-time operational monitoring — both are complementary, not alternatives. Every record is stamped with `pipeline_env` (`api` / `eval` / `local`) so golden-runner traces and dev calls can be filtered out of production analytics. `make eval` sets `PIPELINE_ENV=eval` automatically. | ✅ | `app/core/trace_store.py` | `TRACE_FILE`, `PIPELINE_ENV` |
| 19 | **PII filter on trace writes** — `PiiFilter` runs before every trace write: when enabled, SHA-256-hashes the question (non-reversible, but stable for duplicate detection) and drops `user_context`. Disabled by default (internal analytics domain, no personal data in questions). In a domain with PII in queries (HR, finance), extend `PiiFilter.apply()` with Microsoft Presidio or Azure AI Language before the hash step. | ✅ | `app/core/pii_filter.py` | `TRACE_ANONYMIZE` (default `false`) |
| 20 | **Trace viewer endpoint** — `GET /traces` surfaces recent runs without needing MLflow | 🔜 | planned |
| 21 | **Health check endpoint** — `GET /health` reports DB connectivity, LLM reachability and config validity | 🔜 | planned |

---

## Governance — scope and access

| # | Practice | Status | File |
|---|---|---|---|
| 22 | **Intent classification** — question classified as in-scope / out-of-scope against the domain vocabulary before any data access | ✅ | `app/stages/intent.py` |
| 23 | **View selection with confidence threshold** — questions with view-selection confidence < 0.4 are refused rather than guessed | ✅ | `app/stages/view_selection.py` |
| 24 | **Metadata grounding** — SQL is generated from approved view definitions (column names, types, grain, limitations), not inferred from the user's wording | ✅ | `app/stages/metadata.py`, `app/stages/sql_generation.py` |
| 25 | **Domain vocabulary aliases** — alternative names for metrics are loaded from view metadata so intent classification understands synonyms | ✅ | `app/stages/intent.py`, `src/metadata/metrics/` |
| 26 | **Answer caveats from metadata** — answer stage injects the `limitations` declared in view YAML as explicit caveats | ✅ | `app/stages/answer.py` |
| 27 | **Data quality caveats** — freshness / NULL rate / row count health injected as caveats at answer time | 🔜 | planned |
| 28 | **Persona-based access control** — `DemoAuthService` resolves `X-User-Role` header to one of three personas (analyst / editor / admin), each with an explicit allowed-views list. Role is stamped on the trace. **DEMO ONLY** — in production replace with Azure AD / OIDC JWT validation; never resolve permissions from a plain header. See `app/core/auth.py` module docstring for the production replacement pattern. | ✅ | `app/core/auth.py`, `app/api/routes.py` |
| 29 | **Access enforcement at execution** — access context validated in the execution stage; query refused if it references views the user cannot see | 🔜 | planned |
| 30 | **Approved join register** — cross-view joins blocked unless declared in a central join allowlist | 🔜 | planned |
| 31 | **Clarification stage** — ambiguous questions returned with a clarifying question rather than a low-confidence guess | 🔜 | planned |

---

## CI / CD

| # | Practice | Status | Where |
|---|---|---|---|
| 35 | **GitHub Actions CI on every push and PR** — runs on `push` to `main` and on all pull requests targeting `main` | ✅ | `.github/workflows/ci.yml` |
| 36 | **Lint gate (ruff)** — CI fails if any Python file under `src/` has a lint error; runs before tests | ✅ | `.github/workflows/ci.yml` |
| 37 | **Full unit test suite in CI** — all 115 tests run in CI with no external dependencies (LLM and DB are fully mocked) | ✅ | `.github/workflows/ci.yml` |
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
| 45 | **MLflow UI available locally** — `make mlflow-ui` launches MLflow at `localhost:5000` with no additional setup; `mlflow.db` and `mlruns/` are committed so the UI works immediately after `git clone` | ✅ | `Makefile`, `mlflow.db`, `mlruns/` |

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
