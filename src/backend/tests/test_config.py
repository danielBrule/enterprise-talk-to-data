import backend.app.core.config as config


def test_build_connection_string_from_env(monkeypatch):
    monkeypatch.setenv("AZURE_SQL_SERVER", "server.database.windows.net,1433")
    monkeypatch.setenv("AZURE_SQL_DATABASE", "testdb")
    monkeypatch.setenv("AZURE_SQL_USERNAME", "testuser")
    monkeypatch.setenv("AZURE_SQL_PASSWORD", "secret")
    monkeypatch.setenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    connection_string = config._build_connection_string()

    assert connection_string.startswith("mssql+pyodbc://")
    assert "server.database.windows.net" in connection_string
    assert "testdb" in connection_string


def test_build_connection_string_missing_env(monkeypatch):
    for key in [
        "AZURE_SQL_SERVER",
        "AZURE_SQL_DATABASE",
        "AZURE_SQL_USERNAME",
        "AZURE_SQL_PASSWORD",
    ]:
        monkeypatch.delenv(key, raising=False)

    assert config._build_connection_string() == ""


def test_api_version_is_defined():
    assert config.API_VERSION == "0.1.0"


def test_azure_openai_task_specific_deployments(monkeypatch):
    monkeypatch.setenv("AZURE_OPENAI_DEPLOYMENT", "default-deploy")
    monkeypatch.setenv("AZURE_OPENAI_SCHEMA_RETRIEVAL_DEPLOYMENT", "schema-deploy")
    monkeypatch.setenv("AZURE_OPENAI_SQL_GENERATION_DEPLOYMENT", "sql-deploy")
    monkeypatch.setenv("AZURE_OPENAI_SUMMARY_DEPLOYMENT", "summary-deploy")

    settings = config.Settings()
    print(settings.get_azure_openai_deployment("schema_retrieval"))
    assert settings.get_azure_openai_deployment("schema_retrieval") == "schema-deploy"
    assert settings.get_azure_openai_deployment("sql_generation") == "sql-deploy"
    assert settings.get_azure_openai_deployment("summary") == "summary-deploy"
    assert settings.get_azure_openai_deployment(None) == "default-deploy"

    monkeypatch.delenv("AZURE_OPENAI_SCHEMA_RETRIEVAL_DEPLOYMENT", raising=False)
    settings = config.Settings()
    assert settings.get_azure_openai_deployment("schema_retrieval") == "default-deploy"
