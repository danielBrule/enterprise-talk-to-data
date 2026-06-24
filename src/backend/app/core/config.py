import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

_repo_root = Path(__file__).resolve().parents[4]
_backend_root = Path(__file__).resolve().parent.parent.parent

# Load environment variables from repository root first, then fallback to backend/.env.
load_dotenv(_repo_root / ".env", override=False)
load_dotenv(_backend_root / ".env", override=False)

API_VERSION = "0.1.0"
API_PREFIX = f"/api/v{API_VERSION.split('.')[0]}"


def _build_connection_string() -> str:
    server = os.getenv("AZURE_SQL_SERVER", "")
    database = os.getenv("AZURE_SQL_DATABASE", "")
    username = os.getenv("AZURE_SQL_USERNAME", "")
    password = os.getenv("AZURE_SQL_PASSWORD", "")
    driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    if not all([server, database, username, password]):
        return ""

    quoted_driver = quote_plus(driver)
    quoted_username = quote_plus(username)
    quoted_password = quote_plus(password)
    quoted_server = quote_plus(server, safe=",:")
    quoted_database = quote_plus(database)

    return (
        f"mssql+pyodbc://{quoted_username}:{quoted_password}@{quoted_server}/{quoted_database}"
        f"?driver={quoted_driver}"
    )


class Settings:
    def __init__(self) -> None:
        self.database_url = _build_connection_string()

        self.azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", "")
        self.azure_openai_api_key = os.getenv("AZURE_OPENAI_API_KEY", "")
        self.azure_openai_api_version = os.getenv(
            "AZURE_OPENAI_API_VERSION",
            "2024-06-01",
        )
        self.azure_openai_schema_retrieval_deployment = os.getenv(
            "AZURE_OPENAI_SCHEMA_RETRIEVAL_DEPLOYMENT",
            "",
        )
        self.azure_openai_sql_generation_deployment = os.getenv(
            "AZURE_OPENAI_SQL_GENERATION_DEPLOYMENT",
            "",
        )
        self.azure_openai_summary_deployment = os.getenv(
            "AZURE_OPENAI_SUMMARY_DEPLOYMENT",
            "",
        )

        # ── Timeouts ──────────────────────────────────────────────────────────
        self.sql_query_timeout_seconds: int = int(os.getenv("SQL_QUERY_TIMEOUT_SECONDS", "30"))
        self.llm_timeout_seconds: int = int(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
        self.pipeline_timeout_seconds: int = int(os.getenv("PIPELINE_TIMEOUT_SECONDS", "120"))

        # ── Input safety ──────────────────────────────────────────────────────
        self.max_question_length: int = int(os.getenv("MAX_QUESTION_LENGTH", "1000"))

        # ── Cost control ──────────────────────────────────────────────────────
        # 0 = disabled. Set to a positive integer to enforce a per-request token budget.
        self.max_tokens_per_request: int = int(os.getenv("MAX_TOKENS_PER_REQUEST", "10000"))

    def get_azure_openai_deployment(self, task: str | None = None) -> str:
        # No default fallback — each task must be explicitly configured via its own env var.
        # An empty string here surfaces as a ValueError in LLMService.generate_response.
        if task == "schema_retrieval":
            return self.azure_openai_schema_retrieval_deployment
        if task == "sql_generation":
            return self.azure_openai_sql_generation_deployment
        if task == "summary":
            return self.azure_openai_summary_deployment
        return ""


settings = Settings()
