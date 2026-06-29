# Task runner for enterprise-talk-to-data.
#
# Requires: poetry (https://python-poetry.org/docs/#installation)
#           make   (choco install make on Windows)
#           node   (https://nodejs.org — LTS, for frontend targets)
#
# PowerShell auto-detection:
#   Windows     -> powershell (Windows PowerShell 5.1, always present)
#   macOS/Linux -> pwsh (PowerShell 7)
# Override with: make env PWSH=pwsh

ifeq ($(OS),Windows_NT)
    PWSH ?= powershell
else
    PWSH ?= pwsh
endif

.PHONY: help env pdf clean-pdf install check start-backend apply-sql-views apply-sql-indexes infra-init infra-apply tests eval mlflow-ui scaffold-frontend install-frontend start-frontend build-frontend

help:   ## show this help
	@echo ""
	@echo "  Setup"
	@echo "  -----"
	@echo "  install          install all dependencies via Poetry"
	@echo "  env              install deps then verify PDF toolchain"
	@echo ""
	@echo "  Docs / PDF"
	@echo "  ----------"
	@echo "  pdf              generate docs/pdf/*.pdf from Markdown sources"
	@echo "  clean-pdf        remove generated PDFs"
	@echo ""
	@echo "  Python"
	@echo "  ------"
	@echo "  check            syntax-check all .py files under src/backend/"
	@echo "  tests            run pytest against src/backend/tests/"
	@echo "  eval             run golden evaluation  MODE=fast|full  OUTPUT=path  LIMIT=N"
	@echo "  mlflow-ui        launch MLflow UI at http://localhost:5000"
	@echo "  start-backend    start the FastAPI backend server"
	@echo ""
	@echo "  Frontend  (requires Node.js LTS)"
	@echo "  --------"
	@echo "  scaffold-frontend  create src/frontend with React + Vite (run once)"
	@echo "  install-frontend   npm install in src/frontend"
	@echo "  start-frontend     vite dev server at http://localhost:5173"
	@echo "  build-frontend     production build to src/frontend/dist"
	@echo ""
	@echo "  SQL"
	@echo "  ---"
	@echo "  apply-sql-views    deploy analytics views to the database"
	@echo "  apply-sql-indexes  apply performance indexes (idempotent)"
	@echo ""
	@echo "  Infrastructure  (src/infra/terraform)"
	@echo "  --------------------------------------"
	@echo "  infra-init       terraform init"
	@echo "  infra-apply      terraform apply  -- requires ENV=dev or ENV=prod"
	@echo ""

# ── Setup ─────────────────────────────────────────────────────────────────────

install:  ## install all dependencies via Poetry (creates .venv if needed)
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; poetry install"

env: install   ## install deps then verify PDF toolchain (pandoc, wkhtmltopdf, mmdc)
	@echo Checking PDF toolchain:
	-@$(PWSH) -NoProfile -Command "if (Get-Command pandoc -EA 0) { '  ok   pandoc' } else { Write-Warning 'missing pandoc      -> https://pandoc.org/installing.html' }"
	-@$(PWSH) -NoProfile -Command "if (Get-Command wkhtmltopdf -EA 0) { '  ok   wkhtmltopdf' } else { Write-Warning 'missing wkhtmltopdf -> https://wkhtmltopdf.org/downloads.html' }"
	-@$(PWSH) -NoProfile -Command "if (Get-Command mmdc -EA 0) { '  ok   mmdc' } else { Write-Warning 'missing mmdc        -> npm install -g @mermaid-js/mermaid-cli' }"

# ── Docs / PDF ────────────────────────────────────────────────────────────────

pdf:       ## generate docs/pdf/*.pdf from Markdown sources
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; poetry run python scripts/build_pdfs.py docs/"

clean-pdf: ## remove generated PDFs
	@$(PWSH) -NoProfile -Command "Remove-Item docs/pdf/*.pdf -Force -ErrorAction SilentlyContinue; Write-Host 'Removed generated PDFs.'"

# ── Python ────────────────────────────────────────────────────────────────────

check: install  ## syntax-check all Python files under src/backend/
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; poetry run python -c \"import py_compile, pathlib; [py_compile.compile(str(p), doraise=True) for p in pathlib.Path('src/backend').rglob('*.py')]\""

tests: install check  ## run pytest against src/backend/tests/
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; $$env:PYTHONPATH = 'src'; poetry run pytest src/backend/tests/ -v"

eval: install  ## run golden evaluation — MODE=fast|full (default fast), OUTPUT=path, LIMIT=N, RUN=label, CONCURRENCY=N (default 5; use 3-5 for full mode)
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; $$env:PYTHONPATH = 'src'; $$env:PIPELINE_ENV = 'eval'; poetry run python -m backend.evaluation_runner --mode $(or $(MODE),fast) $(if $(OUTPUT),--output $(OUTPUT),) $(if $(LIMIT),--limit $(LIMIT),) $(if $(RUN),--eval-run $(RUN),) $(if $(CONCURRENCY),--concurrency $(CONCURRENCY),)"

mlflow-ui:  ## launch MLflow UI at http://localhost:5000 (no install needed)
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; poetry run mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns"

start-backend: install  ## start the FastAPI backend server
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; $$env:PYTHONPATH = 'src'; poetry run python -m backend.main"

# ── Frontend ──────────────────────────────────────────────────────────────────

scaffold-frontend:  ## create src/frontend with React + Vite template (run once)
	@$(PWSH) -NoProfile -Command "npm.cmd create vite@latest src/frontend -- --template react"

install-frontend:  ## npm install in src/frontend (requires Node.js LTS)
	@$(PWSH) -NoProfile -Command "Set-Location src/frontend; npm.cmd install"

start-frontend:  ## start Vite dev server at http://localhost:5173
	@$(PWSH) -NoProfile -Command "Set-Location src/frontend; npm.cmd run dev"

build-frontend:  ## production build to src/frontend/dist
	@$(PWSH) -NoProfile -Command "Set-Location src/frontend; npm.cmd run build"

# ── SQL ───────────────────────────────────────────────────────────────────────

apply-sql-views: install  ## deploy analytics views to the database
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; $$env:PYTHONPATH = 'src'; poetry run python src/backend/db/deploy_views.py"

apply-sql-indexes: install  ## apply performance indexes (idempotent, safe to re-run)
	@$(PWSH) -NoProfile -Command "$$env:PATH = \"$$env:APPDATA\Python\Scripts;$$env:PATH\"; $$env:PYTHONPATH = 'src'; poetry run python src/backend/db/deploy_indexes.py"

# ── Infrastructure ────────────────────────────────────────────────────────────

infra-init:  ## terraform init  (src/infra/terraform)
	terraform -chdir=src/infra/terraform init

infra-apply:  ## terraform apply  (ENV=dev|prod)
	@$(PWSH) -NoProfile -Command "if (-not '$(ENV)') { Write-Error 'ENV is not set. Use: make infra-apply ENV=dev'; exit 1 }; terraform -chdir=src/infra/terraform apply -parallelism=1 -var-file=envs/$(ENV)/terraform.tfvars -auto-approve"
