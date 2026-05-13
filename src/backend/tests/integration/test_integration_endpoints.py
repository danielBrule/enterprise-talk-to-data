#!/usr/bin/env python3
"""
Integration tests for FastAPI endpoints.
This script starts the server and tests all endpoints to ensure they work.
Run with: python backend/tests/integration/test_integration_endpoints.py
"""

import subprocess
import time
import requests
import sys
import os
from pathlib import Path

# Get the project root (3 levels up from this file)
project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(project_root))


def start_server():
    """Start the FastAPI server in the background."""
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root)
    return subprocess.Popen(
        [
            str(project_root / ".venv" / "Scripts" / "python.exe"),
            "-m",
            "uvicorn",
            "backend.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            "8000",
            "--log-level",
            "error",
        ],
        env=env,
        cwd=str(project_root),
    )


def test_endpoints():
    """Test all API endpoints."""
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        ("/health", "GET"),
        ("/version", "GET"),
        ("/api/v0/articles", "GET"),
        ("/api/v0/keywords", "GET"),
        ("/api/v0/contributors", "GET"),
        ("/api/v0/errors", "GET"),
        ("/api/v0/metadata/views", "GET"),
        ("/api/v0/metadata/metrics", "GET"),
        ("/api/v0/metadata/glossary", "GET"),
        (
            "/api/v0/metadata/select-views?question=Which+articles+have+the+most+comments",
            "POST",
        ),
    ]

    print("Testing FastAPI endpoints...")
    results = []

    for endpoint, method in endpoints:
        try:
            if method == "GET":
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
            else:  # POST
                response = requests.post(f"{base_url}{endpoint}", timeout=10)

            status = (
                "✓ PASS"
                if response.status_code == 200
                else f"✗ FAIL ({response.status_code})"
            )
            print(f"{status}: {method} {endpoint}")
            results.append(
                (
                    endpoint,
                    response.status_code,
                    response.text[:100] if response.status_code != 200 else "OK",
                )
            )
        except requests.exceptions.RequestException as e:
            print(f"✗ FAIL: {method} {endpoint} - {e}")
            results.append((endpoint, "ERROR", str(e)))


def main():
    print("Starting FastAPI server for integration testing...")
    print(f"Project root: {project_root}\n")

    # Start the server
    server_process = start_server()

    # Wait for server to start
    time.sleep(3)

    try:
        # Test the endpoints
        results = test_endpoints()

        # Summary
        print("\n" + "=" * 60)
        print("INTEGRATION TEST SUMMARY")
        print("=" * 60)

        passed = sum(1 for _, status, _ in results if status == 200)
        total = len(results)

        for endpoint, status, details in results:
            print(f"{endpoint}: {'PASS' if status == 200 else f'FAIL ({status})'}")

        print(f"\nPassed: {passed}/{total}")

        if passed == total:
            print("🎉 All endpoints are working!")
            return 0
        else:
            print("❌ Some endpoints failed.")
            return 1

    finally:
        # Stop the server
        server_process.terminate()
        server_process.wait()


if __name__ == "__main__":
    sys.exit(main())
