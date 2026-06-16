"""
Deploy SQL views to Azure SQL or local SQL Server.

Usage:
    python deploy_views.py

This script loads environment variables from the process environment,
then from `.env` if that file exists.

Requires environment variables:
    AZURE_SQL_SERVER - SQL Server address
    AZURE_SQL_DATABASE - Database name
    AZURE_SQL_USERNAME - Username
    AZURE_SQL_PASSWORD - Password
"""

import os
import sys
from pathlib import Path

try:
    import pyodbc
except ImportError:
    print("Error: pyodbc not installed. Install with: pip install pyodbc")
    sys.exit(1)


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return

    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            os.environ.setdefault(key, value)


def get_connection():
    """Create a connection to Azure SQL."""
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")

    if not all([server, database, username, password]):
        raise ValueError(
            "Missing environment variables: AZURE_SQL_SERVER, AZURE_SQL_DATABASE, "
            "AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD"
        )

    connection_string = (
        f"Driver={{ODBC Driver 18 for SQL Server}};"
        f"Server={server};"
        f"Database={database};"
        f"UID={username};"
        f"PWD={password};"
    )

    return pyodbc.connect(connection_string)


def deploy_views(views_dir: str = "sql/views"):
    """Deploy all SQL view files from the views directory."""
    views_path = Path(views_dir)

    if not views_path.exists():
        print(f"Error: {views_dir} directory not found.")
        sys.exit(1)

    sql_files = sorted(views_path.glob("*.sql"))

    if not sql_files:
        print(f"No SQL files found in {views_dir}")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        for sql_file in sql_files:
            print(f"Deploying {sql_file.name}...", end=" ")
            with open(sql_file, "r", encoding="utf-8") as f:
                sql_script = f.read()

            for statement in sql_script.split("GO"):
                statement = statement.strip()
                if statement:
                    cursor.execute(statement)

            conn.commit()
            print("✓")

        cursor.close()
        conn.close()
        print("\nAll views deployed successfully.")

    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    load_env_file(Path(".env"))
    deploy_views()
