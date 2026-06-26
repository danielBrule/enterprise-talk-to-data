# Tech Stack

## Cloud & infrastructure

| Technology | Role |
|---|---|
| **Azure OpenAI** | LLM inference — three task-specific deployments (intent/view selection, SQL generation, answer summarisation) |
| **Azure SQL Database** | Analytics data store — four views exposed via pyodbc / SQLAlchemy |
| **Azure Identity** | Credential chain for Azure OpenAI and SQL authentication |
| **Terraform** | Infrastructure as code — provisions resource group, OpenAI account and deployments |
| **Docker** | Container image for the backend; ODBC Driver 18 baked in |
| **GitHub Actions** | CI — lint (ruff) + full unit test suite on every push and PR |

---

## Backend runtime

| Library | Version | Role |
|---|---|---|
| **Python** | 3.12+ | Runtime |
| **FastAPI** | ≥ 0.120 | REST API framework — 7-stage pipeline endpoint, metadata routes, data quality routes |
| **Uvicorn** | ≥ 0.24 | ASGI server (standard extras — includes websocket and HTTP/2 support) |
| **SQLAlchemy** | ≥ 2.0 | Database connection management and query execution |
| **pyodbc** | ≥ 5.1 | ODBC driver bridge for Azure SQL Server (ODBC Driver 18) |
| **openai** | ≥ 1.30 | Azure OpenAI SDK — LLM calls across all three deployments |
| **azure-identity** | ≥ 1.16 | `DefaultAzureCredential` and `ClientSecretCredential` for token-based auth |
| **python-dotenv** | ≥ 1.0 | `.env` loading for local development |
| **PyYAML** | ≥ 6.0 | View metadata, golden questions, and approved join register |
| **pandas** | ≥ 2.2 | SQL result serialisation to JSON-serialisable records |

---

## SQL safety & parsing

| Library | Version | Role |
|---|---|---|
| **sqlglot** | ≥ 30.11 | AST-based SQL validation — parses in tsql dialect; checks statement type, forbidden nodes, dbo access, row limit, and cross-view join policy. Replaces regex approach; correctly handles string literals, CTEs and subqueries |

---

## Observability & evaluation

| Library | Version | Role |
|---|---|---|
| **MLflow** | ≥ 3.14 | Experiment tracking — every golden eval run logs pass/fail, token usage per stage, model names and latency. SQLite backend (`mlflow.db`) committed to git so the UI works after clone |
| **SQLite** | stdlib | Local store for MLflow (`mlflow.db`), analytics traces + feedback (`data/analytics/analytics.db`), and data quality results (`data/data_quality/data_quality.db`) |

---

## Development & testing

| Library | Version | Role |
|---|---|---|
| **pytest** | ≥ 8.0 | Test runner |
| **pytest-asyncio** | ≥ 0.21 | Async test support (all pipeline stages are async) |
| **httpx** | ≥ 0.27 | HTTP client used by FastAPI `TestClient` in API tests |
| **ruff** | ≥ 0.5 | Linter — enforced in CI |
| **black** | ≥ 24.0 | Formatter |

---

## Key design decisions

- **Three LLM deployments** — intent/view selection, SQL generation, and answer summarisation use separate Azure OpenAI deployments so model tier and token budget can be tuned independently per task.
- **sqlglot over regex** — SQL safety validation uses AST parsing (tsql dialect) rather than regex. Regex cannot distinguish SQL keywords in string literals from actual statements and cannot resolve CTE aliases; the AST can.
- **SQLite for local persistence** — MLflow and data quality results use SQLite to keep the stack self-contained for demo purposes. Both could be swapped for Azure SQL with a one-line connection string change.
- **Sequential data quality checks** — Azure SQL Basic/Standard tier has a limited concurrent connection pool; health checks run sequentially rather than in parallel to avoid TCP connection exhaustion.
- **AskResponse enrichment fields** — `source_view`, `metric_definitions`, `filters_applied`, `sql`, `row_count`, `confidence`, `latency_ms`, and `token_usage` are surfaced as top-level fields on every response (not buried in the trace object). `filters_applied` is LLM self-reported from the SQL generation stage (structured JSON output) rather than parsed from the SQL AST, which avoids coupling the display layer to a SQL parser and lets the model describe filters in natural-language terms. All fields default to null/empty on early refusals.
