# Newspaper Talk to Data

A scaffold for a "talk to data" solution focused on newspaper analytics.
The repository includes a backend API, frontend shell, SQL artifacts, metadata, evaluation assets, and infrastructure scaffolding.

## Python Environment Setup

A project-specific Python environment is created in `.venv`.

### Create the virtual environment

```powershell
cd newspaper-talk-to-data
python -m venv .venv
```

### Activate the environment (PowerShell)

```powershell
cd newspaper-talk-to-data
.\.venv\Scripts\Activate.ps1
```

### Install dependencies

Once dependencies are added, install them from `pyproject.toml` or a requirements file.

```powershell
pip install -U pip
pip install -r requirements.txt
```

## Repository Layout

- `backend/` - backend API, core logic, services, prompts, validation, and database code
- `frontend/` - frontend source code
- `sql/` - SQL views, security scripts, and tests
- `metadata/` - glossary, metrics, schema descriptions, and example questions
- `evaluations/` - benchmark questions and expected SQL/results
- `infra/` - infrastructure definitions, including Terraform
- `docs/` - documentation

## Core Services

### View Selection Service

Intelligently selects the most relevant database views for natural language questions using Azure OpenAI LLM.

**Flow:**
```
Question → Metadata Context → LLM View Selection → Selected Views + Reasoning
```

**API Endpoint:** `POST /api/v0/metadata/select-views`

**Example:**
```bash
curl -X POST "http://localhost:8000/api/v0/metadata/select-views?question=Which+articles+had+the+most+comments"
```

**Response:**
```json
{
  "question": "Which articles had the most comments?",
  "selected_views": ["analytics.vw_article_engagement"],
  "reason": "Question refers to articles and comment volume."
}
```

For more details, see [View Selection Service Documentation](docs/VIEW_SELECTION_SERVICE.md).

## Testing

### Unit Tests

Run all unit tests in the `backend/tests/` directory:

```powershell
pytest backend/tests/ -v
```

Run specific test:
```powershell
pytest backend/tests/test_services.py::test_view_selection_service -v
```

**Test Coverage:**
- Article, keyword, contributor, ingestion error services
- View selection service with LLM integration
- Fallback behavior when LLM is not configured
- Error handling for invalid responses

### Integration Tests

Test all API endpoints with a running server:

```powershell
python backend/tests/integration/test_integration_endpoints.py
```

This script:
1. Starts the backend server
2. Tests all endpoints including the new view selection endpoint
3. Reports results

**Note:** Integration tests require the server to be available and are run separately from unit tests.

## Configuration

This repo includes a reusable Terraform module structure for Azure deployment.
The Terraform configuration supports environment-specific deployments for `dev` and `prod`.

### Included resources
- Azure Resource Group: `rg-lefigaro-talk2data-<env>`
- Azure OpenAI account: `openai-lefigaro-<env>`
- OpenAI deployments:
  - `talk2data-gpt41mini-schema-retrieval`
  - `talk2data-gpt41mini-sql-generation`
  - `talk2data-gpt41mini-summary`

### Terraform layout
- `infra/terraform/` — root module and provider configuration
- `infra/terraform/modules/resource_group/` — reusable RG module
- `infra/terraform/modules/openai/` — reusable OpenAI account + deployment module
- `infra/terraform/envs/dev/terraform.tfvars` — dev input values
- `infra/terraform/envs/prod/terraform.tfvars` — prod input values

### Run Terraform
Use the Makefile wrapper from the repository root:

```powershell
make infra-init
make infra-apply ENV=dev
```

For production, point to the prod tfvars file:

```powershell
make infra-apply ENV=prod
```

## Azure SQL View Deployment

SQL view definitions are stored in `sql/views/` and use the `analytics` schema.

### Local development

1. Copy `.env.example` to `.env` and fill in your Azure SQL connection details:

   ```powershell
   copy .env.example .env
   # Edit .env with your Azure SQL server, database, username, password
   ```

2. Deploy views:

   ```powershell
   cd newspaper-talk-to-data
   make apply-sql-views
   ```

### Run the backend locally

Start the backend API once your dependencies are installed and `.env` is configured:

```powershell
cd newspaper-talk-to-data
make start-backend
```

Alternatively:

```powershell
cd newspaper-talk-to-data
.\.venv\Scripts\python.exe backend/main.py
```

Then open FastAPI docs in your browser:

- `http://localhost:8000/docs` — interactive Swagger UI
- `http://localhost:8000/redoc` — ReDoc API docs
- `http://localhost:8000/openapi.json` — raw OpenAPI schema

Example endpoints to test in the browser:

- `http://localhost:8000/api/v0/articles`
- `http://localhost:8000/api/v0/keywords`
- `http://localhost:8000/api/v0/contributors`
- `http://localhost:8000/api/v0/errors`
- `http://localhost:8000/api/v0/metadata/views` — view metadata
- `http://localhost:8000/api/v0/metadata/select-views?question=<your-question>` — view selection (POST)

### GitHub Actions / CI-CD

Add the following secrets to your GitHub repository settings:
- `AZURE_SQL_SERVER`
- `AZURE_SQL_DATABASE`
- `AZURE_SQL_USERNAME`
- `AZURE_SQL_PASSWORD`

### Local development now, online later

For local development, keep working from the `newspaper-talk-to-data` folder and use the local `.venv`.
When you are ready to run online, ensure the same SQL migration files in `sql/views/` are deployed to the Azure SQL instance using the GitHub Action or `make apply-sql-views`.
