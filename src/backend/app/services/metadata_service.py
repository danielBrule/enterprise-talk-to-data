import yaml
from pathlib import Path
from typing import Any

from ..core.logger import logger

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
                logger.warning("metadata.load_failed file=%s error=%s", yaml_file.name, e)

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
                logger.warning("metadata.load_failed file=%s error=%s", yaml_file.name, e)

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
                logger.warning("metadata.load_failed file=%s error=%s", yaml_file.name, e)

    return glossary


async def get_view_aliases() -> dict[str, list[str]]:
    """Return aliases for each view, keyed by view_name. Only views with aliases are included."""
    schema_views = await get_views_metadata()
    return {
        v["view_name"]: v["aliases"]
        for v in schema_views
        if "view_name" in v and v.get("aliases")
    }


async def get_context_for_views(view_names: list[str]) -> dict[str, dict[str, Any]]:
    """
    Return merged schema and metric metadata for the specified views, keyed by view name.

    Combines schema_descriptions (column list) with metrics (purpose, business_meaning,
    limitations, example_questions) so callers get a single rich context object per view.
    Views that are not found in the metadata files are silently omitted.
    """
    schema_views = await get_views_metadata()
    metrics_views = await get_metrics_metadata()

    schema_by_view = {v["view_name"]: v for v in schema_views if "view_name" in v}
    metrics_by_view = {v["view_name"]: v for v in metrics_views if "view_name" in v}

    context: dict[str, dict[str, Any]] = {}
    for view_name in view_names:
        schema = schema_by_view.get(view_name, {})
        metrics = metrics_by_view.get(view_name, {})
        if not schema and not metrics:
            continue
        context[view_name] = {
            "view_name": view_name,
            "description": schema.get("description", metrics.get("purpose", "")),
            "purpose": metrics.get("purpose", ""),
            "business_meaning": metrics.get("business_meaning", ""),
            "columns": schema.get("columns") or metrics.get("columns", []),
            "limitations": metrics.get("limitations", []),
            "example_questions": metrics.get("example_questions", []),
        }

    return context
