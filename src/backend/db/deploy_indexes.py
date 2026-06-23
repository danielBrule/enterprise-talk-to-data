"""
Apply performance indexes to Azure SQL.

Usage:
    make apply-sql-indexes
    poetry run python src/backend/db/deploy_indexes.py
"""

import os
import sys
from pathlib import Path

try:
    import pyodbc
except ImportError:
    print("Error: pyodbc not installed.")
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
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def get_connection():
    server = os.getenv("AZURE_SQL_SERVER")
    database = os.getenv("AZURE_SQL_DATABASE")
    username = os.getenv("AZURE_SQL_USERNAME")
    password = os.getenv("AZURE_SQL_PASSWORD")
    driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server")

    if not all([server, database, username, password]):
        raise ValueError("Missing AZURE_SQL_SERVER, AZURE_SQL_DATABASE, AZURE_SQL_USERNAME, AZURE_SQL_PASSWORD")

    return pyodbc.connect(
        f"Driver={{{driver}}};Server={server};Database={database};UID={username};PWD={password};"
    )


def deploy_indexes(indexes_dir: str = "src/sql/indexes") -> None:
    indexes_path = Path(indexes_dir)
    if not indexes_path.exists():
        print(f"Error: {indexes_dir} not found.")
        sys.exit(1)

    sql_files = sorted(indexes_path.glob("*.sql"))
    if not sql_files:
        print(f"No SQL files found in {indexes_dir}")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()

        for sql_file in sql_files:
            print(f"Applying {sql_file.name}...", end=" ")
            sql = sql_file.read_text(encoding="utf-8")
            for statement in sql.split("\n\n"):
                statement = statement.strip()
                if statement and not statement.startswith("--"):
                    cursor.execute(statement)
            conn.commit()
            print("done")

        cursor.close()
        conn.close()
        print("\nAll indexes applied.")

    except pyodbc.Error as e:
        print(f"\nDatabase error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    load_env_file(Path(".env"))
    deploy_indexes()
