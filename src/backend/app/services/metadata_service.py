import yaml
from pathlib import Path
from typing import Any

# Get the metadata directory relative to this file
_service_dir = Path(__file__).resolve().parent.parent
_metadata_dir = _service_dir.parent.parent / "metadata"


async def get_views_metadata() -> list[dict[str, Any]]:
    """Load all view definitions from sql/views/*.sql files and corresponding metadata."""
    views = []
    schema_dir = _metadata_dir / "schema_descriptions"

    if schema_dir.exists():
        for yaml_file in sorted(schema_dir.glob("*.yml")):
            try:
                with open(yaml_file, "r") as f:
                    data = yaml.safe_load(f)
                    if data:
                        views.append(data)
            except Exception as e:
                print(f"Error loading view schema {yaml_file}: {e}")

    return views


async def get_metrics_metadata() -> list[dict[str, Any]]:
    """Load all metrics metadata from metadata/metrics/*.yml files."""
    metrics = []
    metrics_dir = _metadata_dir / "metrics"

    if metrics_dir.exists():
        for yaml_file in sorted(metrics_dir.glob("*.yml")):
            try:
                with open(yaml_file, "r") as f:
                    data = yaml.safe_load(f)
                    if data:
                        metrics.append(data)
            except Exception as e:
                print(f"Error loading metrics {yaml_file}: {e}")

    return metrics


async def get_glossary_metadata() -> list[dict[str, Any]]:
    """Load all glossary metadata from metadata/glossary/*.yml files."""
    glossary = []
    glossary_dir = _metadata_dir / "glossary"

    if glossary_dir.exists():
        for yaml_file in sorted(glossary_dir.glob("*.yml")):
            try:
                with open(yaml_file, "r") as f:
                    data = yaml.safe_load(f)
                    if data:
                        glossary.append(data)
            except Exception as e:
                print(f"Error loading glossary {yaml_file}: {e}")

    return glossary
