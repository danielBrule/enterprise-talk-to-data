.PHONY: help venv install apply-sql-views

VENV := .venv
PYTHON := python
VENV_PYTHON := .venv\Scripts\python.exe

help:
	@echo Available targets:
	@echo   venv
	@echo   install
	@echo   apply-sql-views

venv:
	@if not exist ".venv\Scripts\python.exe" ($(PYTHON) -m venv .venv) else (echo Virtual environment already exists.)

install: venv
	".venv\Scripts\python.exe" -m pip --version
	@if exist "requirements.txt" (".venv\Scripts\python.exe" -m pip install --no-cache-dir -r "requirements.txt") else (echo No requirements.txt found.)

apply-sql-views: install
	@echo Deploying SQL views...
	".venv\Scripts\python.exe" backend\db\deploy_views.py