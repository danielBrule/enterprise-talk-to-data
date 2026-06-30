# Enterprise Talk to Data

A natural-language-to-SQL pipeline over real Le Figaro article data, scraped by [lefigaro-harvester](https://github.com/danielBrule/lefigaro-harvester). Users ask plain-English questions; the system classifies intent, selects the right database views, generates and validates SQL, executes it, and returns a natural-language answer — all through a single `/ask` endpoint.

## Contents

- [How it works](#how-it-works)
- [Repository layout](#repository-layout)
- [Configuration](#configuration)
- [Running locally](#running-locally)
  - [Backend](#backend)
  - [Frontend](#frontend)
- [Production practices](#production-practices)
- [Testing](#testing)
- [Infrastructure](#infrastructure)
  - [Resources created](#resources-created)
  - [Deploying](#deploying)

## How it works

```
POST /api/v0/ask  {"question": "Which articles had the most comments last week?"}
```

The request passes through 7 sequential stages. Each stage either passes control to the next (`None`), stops the pipeline with a user-facing refusal (`Refusal`), or — in the final stage — returns the answer (`Success`).

| # | Stage | LLM | Refuses when |
|---|---|---|---|
| 1 | **Intent** | schema_retrieval | question is out of scope, off-domain, or requires external data |
| 2 | **View selection** | schema_retrieval | confidence < 0.4, or no relevant view identified |
| 3 | **Metadata** | — | no schema/metrics metadata found for the selected views |
| 4 | **SQL generation** | sql_generation | LLM returns no query or unparseable JSON |
| 5 | **SQL validation** | — | query violates safety rules (see below) |
| 6 | **Execution** | — | database unavailable or query errors |
| 7 | **Answer** | summary | never refuses — falls back to row count if LLM unavailable |

**SQL safety rules (stage 5):** SELECT only · `analytics.*` views only · no DDL/DML · no multi-statement · `TOP`/`LIMIT` required (max 500 rows).

**Stage 1 short-circuits** (exit after intent, no SQL or DB access):
- `system_info` — returns the list of views the caller's role can see
- `clarifying` — ambiguous question returned as a clarifying question to the user
- `data_quality` — returns a markdown quality report; "refresh data quality" triggers `DataQualityService.refresh_all()` first

## Repository layout

```
src/
  Dockerfile           — container image (build context: repo root)
  docker-compose.yml   — local container stack
  mlflow.db            — MLflow experiment metadata (SQLite, committed)
  mlruns/              — MLflow artifact store (committed alongside mlflow.db)
  evaluation_results/  — golden evaluation JSON reports, one per run
  backend/
    app/
      api/           — FastAPI routes (/ask, /metadata/*, /articles, …)
      core/          — config, logger, SQL safety validator
      db/            — Azure SQL connection and query execution
      evaluation/    — golden runner: replays curated questions, checks answerability
      models/        — Pydantic API models, PipelineContext, TraceRecord
      prompts/       — versioned prompt builders (intent, view selection, SQL gen, answer)
      services/      — LLMService (Azure OpenAI), metadata loader, pipeline composer
      stages/        — one file per pipeline step: service + stage + result type
    tests/
      integration/   — endpoint smoke tests (requires running server)
      test_*.py      — unit tests (225 tests, no external dependencies)
  frontend/          — React + Vite + Tailwind chat UI (see Frontend section below)
  metadata/
    schema_descriptions/  — column-level view documentation (YAML)
    metrics/              — view purpose, business meaning, limitations (YAML)
    glossary/             — domain term definitions (YAML)
    example_questions/    — golden questions for evaluation
  sql/               — view DDL and security scripts
  infra/             — Terraform modules for Azure deployment

Makefile              — task runner for all `make` commands above (repo root, sibling to src/)
.github/workflows/    — CI: lint + pytest on every push/PR to main (repo root, sibling to src/)
```

## Configuration

Copy `.env.example` to `.env` and fill in:

```env
# Azure SQL
AZURE_SQL_SERVER=
AZURE_SQL_DATABASE=
AZURE_SQL_USERNAME=
AZURE_SQL_PASSWORD=

# Azure OpenAI — one endpoint, three task-specific deployments (no shared default)
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_API_VERSION=2024-02-01
AZURE_OPENAI_SCHEMA_RETRIEVAL_DEPLOYMENT=   # intent + view selection (lightweight model)
AZURE_OPENAI_SQL_GENERATION_DEPLOYMENT=     # SQL generation (reasoning-capable model)
AZURE_OPENAI_SUMMARY_DEPLOYMENT=            # answer generation (instruction-following model)
```

Three separate Azure OpenAI deployments are required — one per pipeline stage (`SCHEMA_RETRIEVAL`, `SQL_GENERATION`, `SUMMARY`) — so each stage's model tier and token budget can be tuned independently. Pointing all three at the same deployment name is fine for local development; only in production would you typically split them onto different model tiers.

If you provisioned infrastructure with Terraform, retrieve these values from its outputs:

```powershell
terraform -chdir=src/infra/terraform output   # shows endpoint and deployment names
```

## Running locally

**Prerequisites:** Python 3.12+, Poetry, `make` (`choco install make` on Windows), Node.js LTS (`winget install OpenJS.NodeJS.LTS` on Windows).

Install Poetry once:
```powershell
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### Backend

```powershell
# 1. Install all dependencies (creates .venv automatically)
make install

# 2. Configure environment
copy .env.example .env
# Edit .env with Azure SQL and Azure OpenAI credentials

# 3. Deploy SQL views to the database (first time or after view changes)
make apply-sql-views

# 4. Start the backend
make start-backend
```

The API is then available at `http://localhost:8000`.

| URL | Description |
|---|---|
| `http://localhost:8000/docs` | Interactive Swagger UI |
| `http://localhost:8000/api/v0/ask` | Main pipeline endpoint (POST) |
| `http://localhost:8000/api/v0/metadata/views` | Schema descriptions |
| `http://localhost:8000/api/v0/metadata/metrics` | Metrics metadata |
| `http://localhost:8000/api/v0/metadata/glossary` | Domain glossary |

**Example request:**

```bash
curl -X POST http://localhost:8000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Which articles had the most comments last week?"}'
```

### Frontend

A React + Vite + Tailwind chat UI lives in `src/frontend/`. It talks to the backend at `http://localhost:8000` — start the backend first.

**Prerequisite:** Node.js LTS — `winget install OpenJS.NodeJS.LTS` on Windows.

```powershell
# First time
make install-frontend

# Start the dev server (keep backend running in a separate terminal)
make start-frontend
```

The UI is then available at `http://localhost:5173`.

- Chat with role selector (analyst / editor / admin)
- Thumbs up / down feedback per answer
- Right panel: source view, filters, SQL, row count, confidence
- Conversation context panel

For production, build the static bundle (`make build-frontend`) and serve from FastAPI via `StaticFiles`.

## Production practices

[`PRODUCTION_PRACTICES.md`](PRODUCTION_PRACTICES.md) maps every safety, resilience, cost-control and governance mechanism to the file that implements it and the env var that controls it.

## Testing

```powershell
make tests        # 225 unit tests, no external dependencies required
make eval         # golden runner, fast mode — stages 1–5, no DB required
make eval MODE=full  # full eval — all 7 stages, requires live .env
make mlflow-ui    # browse eval results at http://localhost:5000
```

`mlflow.db` and `mlruns/` are committed to the repo, so `make mlflow-ui` shows real evaluation history immediately after `git clone` — no eval run required first. This is a pragmatic choice for a single-developer demo; a production setup would point at a remote tracking server instead (Azure ML has native MLflow support).

The unit tests mock all external dependencies (LLM, database) and run fully offline. They include spot-check assertions on expected answers for curated questions, verified against known outputs from the production dataset.

The golden runner replays curated questions from `metadata/example_questions/golden_questions.yml` through the live pipeline. Fast mode covers intent through SQL validation without hitting the database. Full mode runs all 7 stages including execution and answer generation. Pass rate, token usage and model names per stage are logged to MLflow on every run.

**Evaluation scope:** questions are self-authored against a known dataset. The pass rate measures pipeline stability and answerability. A production evaluation would extend to second-party questions and systematic answer scoring against ground truth.

**CI:** [`.github/workflows/ci.yml`](../.github/workflows/ci.yml) runs lint (`ruff check`) and the full pytest suite on every push and pull request to `main`.

## Infrastructure

Terraform provisions the Azure resources needed to run the pipeline. **Azure SQL is not managed by Terraform** and must be provisioned separately.

### Resources created

| Resource | Name | Purpose |
|---|---|---|
| Resource Group | `rg-lefigaro-talk2data-{env}` | Container for all project resources |
| Azure OpenAI account | `openai-lefigaro-{env}` | Cognitive Services endpoint (SKU S0) |
| OpenAI deployment | `talk2data-gpt41mini-schema-retrieval` | Used by intent classification and view selection stages |
| OpenAI deployment | `talk2data-gpt41mini-sql-generation` | Used by SQL generation stage |
| OpenAI deployment | `talk2data-gpt41mini-summary` | Used by answer generation stage |

Default model for all three deployments is `gpt-4.1-mini`. Override per deployment via Terraform variables (`schema_retrieval_model`, `sql_generation_model`, `summary_model`).

### Deploying

Copy the example tfvars for your target environment and fill in your Azure IDs:

```powershell
copy src\infra\terraform\envs\dev\terraform.tfvars.example src\infra\terraform\envs\dev\terraform.tfvars
copy src\infra\terraform\envs\prod\terraform.tfvars.example src\infra\terraform\envs\prod\terraform.tfvars
```

Required variables: `subscription_id`, `tenant_id`, `client_id`, `user_object_id`. Optional overrides: `location` (default `eastus`), `resource_group_name`, `openai_account_name`, model names. The real `terraform.tfvars` files are gitignored — only the `.example` templates are committed. `envs/prod/` is scaffolding for a second environment, not a deployed one.

```powershell
make infra-init          # terraform init
make infra-apply ENV=dev  # deploy to dev
make infra-apply ENV=prod # deploy to prod
```

After apply, retrieve the OpenAI endpoint and deployment names to populate your `.env`:

```powershell
terraform -chdir=src/infra/terraform output
```
