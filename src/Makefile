.PHONY: help venv install apply-sql-views start-backend infra-init infra-apply tests

VENV := .venv
PYTHON := python
VENV_PYTHON := .venv\Scripts\python.exe

help:
	@echo Available targets:
	@echo   venv
	@echo   install
	@echo   start-backend
	@echo   apply-sql-views
	@echo   infra-init
	@echo   infra-apply ENV=dev
	@echo   tests

venv:
	@if not exist ".venv\Scripts\python.exe" ($(PYTHON) -m venv .venv) else (echo Virtual environment already exists.)

install: venv
	".venv\Scripts\python.exe" -m pip --version
	@if exist "requirements.txt" (".venv\Scripts\python.exe" -m pip install --no-cache-dir -r "requirements.txt") else (echo No requirements.txt found.)

check: install
	@echo Running syntax checks...
	".venv\Scripts\python.exe" -c "import py_compile, pathlib; [py_compile.compile(str(p), doraise=True) for p in pathlib.Path('backend').rglob('*.py')]"

start-backend: install
	@echo Starting backend...
	".venv\Scripts\python.exe" -m backend.main

apply-sql-views: install
	@echo Deploying SQL views...
	".venv\Scripts\python.exe" backend\db\deploy_views.py

infra-init:
	@echo Initializing Terraform in infra/terraform
	terraform -chdir=infra/terraform init

infra-apply:
	@echo Applying Terraform infrastructure for environment $(ENV)
	@if not defined ENV (echo ENV is not set. Use ENV=dev or ENV=prod && exit 1)
	terraform -chdir=infra/terraform apply -parallelism=1 -var-file=envs/$(ENV)/terraform.tfvars -auto-approve

tests: install
	@echo Running tests...
	@set PYTHONPATH=%CD% && ".venv\Scripts\python.exe" -m pytest backend/tests/ -v