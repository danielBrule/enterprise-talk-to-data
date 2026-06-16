import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

_repo_root = Path(__file__).resolve().parents[3]
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
        self.azure_openai_default_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
        self.azure_openai_api_version = os.getenv(
            "AZURE_OPENAI_API_VERSION",
            "2024-02-01",
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

    def get_azure_openai_deployment(self, task: str | None = None) -> str:
        if task == "schema_retrieval":
            return (
                self.azure_openai_schema_retrieval_deployment
                or self.azure_openai_default_deployment
            )
        if task == "sql_generation":
            return (
                self.azure_openai_sql_generation_deployment
                or self.azure_openai_default_deployment
            )
        if task == "summary":
            return (
                self.azure_openai_summary_deployment
                or self.azure_openai_default_deployment
            )
        return self.azure_openai_default_deployment


settings = Settings()
