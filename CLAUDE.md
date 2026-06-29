# Talk-to-Data — Claude Code guide

Natural-language interface over Azure SQL analytics views. User asks a question → 7-stage FastAPI pipeline → SQL → answer.

## Stack
- **Backend** FastAPI + Poetry, Python 3.13, Azure OpenAI (3 deployments), Azure SQL via pyodbc
- **Frontend** React + Vite + Tailwind CSS v4 (`src/frontend/`)
- **Eval** MLflow (SQLite, local) + golden question runner
- **Tests** pytest, 220 tests, `PYTHONPATH=src` always required

## Commands
```powershell
make tests              # syntax check then pytest (220 tests)
make start-backend      # FastAPI → http://localhost:8000
make start-frontend     # Vite dev server → http://localhost:5173
make eval               # fast eval (stages 1–5, no DB)
make eval MODE=full     # full eval (all 7 stages, needs live DB + OpenAI)
make mlflow-ui          # MLflow UI → http://localhost:5000
make apply-sql-views    # deploy/update analytics views to Azure SQL
```

## Pipeline
```
POST /ask
  1. IntentStage         intent_v17    — classify domain, detect system_info / unanswerable
  2. ViewSelectionStage  view_sel_v1   — pick one or more analytics views
  3. MetadataStage                     — YAML lookup, no LLM
  4. SQLGenerationStage  sql_gen_v8    — generate T-SQL (SELECT TOP N)
  5. SQLValidationStage                — blocks DDL/DML, dbo.*, queries without LIMIT
  6. ExecutionStage                    — role-based access enforced here
  7. AnswerStage         answer_gen_v2 — markdown answer with table formatting
```

`system_info` intent short-circuits after stage 1 — no SQL, returns list of views the caller's role can see.

## Analytics views (`analytics` schema)
| View | Purpose |
|---|---|
| `vw_article_engagement` | Per-article metrics: comments, sentiment, replies, keyword count, **url** |
| `vw_article_keywords` | Article ↔ keyword mapping (one row per pair), **url** |
| `vw_keyword_engagement` | Per-keyword metrics |
| `vw_top_contributors` | Per-contributor metrics ("top" is view name, not a filter) |
| `vw_ingestion_errors` | Pipeline error log |

URL source: `dbo.stage_article_urls` (LEFT JOIN on `id`). Table `core_articles_urls` does **not** exist.

## Roles (`src/backend/app/core/auth.py`)
- `analyst` — article_engagement, article_keywords, keyword_engagement, top_contributors
- `editor` — article_engagement, article_keywords
- `admin` — all five views
- Default (no header): analyst

## Key files
```
src/backend/app/stages/          — one file per pipeline stage
src/backend/app/services/talk_to_data_pipeline.py  — pipeline composer
src/backend/app/prompts/         — intent.py, sql_generation.py, answer_generation.py
src/backend/app/models/trace.py  — TraceRecord (token_usage: dict[str, dict[str, Any]])
src/backend/app/core/auth.py     — role → allowed views
src/backend/app/api/routes.py    — all HTTP endpoints
src/backend/evaluation_runner.py — eval CLI + MLflow logging
src/frontend/src/App.jsx         — React chat UI
src/sql/views/                   — SQL DDL for all five views
src/metadata/                    — YAML schema descriptions and metrics per view
```

## Conventions
- `token_usage` inner dict is `dict[str, Any]` — it contains `model_name: str` alongside int counts. Never type it as `dict[str, int]`.
- `make tests` runs `make check` (syntax gate) first — do not skip.
- Makefile uses **PowerShell syntax** only (`if (-not ...)`, `$env:VAR`). Never write cmd.exe constructs (`if not defined`).
- Prompt versions are tracked in MLflow. Bump `PROMPT_VERSION` whenever a prompt changes meaningfully.
- After `make eval`, commit `mlflow.db` and `mlruns/` in the same session.

## Security
- `.env` is gitignored and must **never** be committed. It contains `AZURE_OPENAI_API_KEY` and `SQL_PASSWORD`.
- MLflow param logging must never include secrets — only prompt versions and pipeline settings.
