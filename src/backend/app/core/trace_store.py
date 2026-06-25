import json
import pathlib
from typing import TYPE_CHECKING

from .config import settings
from .logger import logger
from .pii_filter import PiiFilter

if TYPE_CHECKING:
    from ..models.trace import TraceRecord


class TraceStore:
    """
    Appends pipeline TraceRecords to a JSONL file after every run (answered or refused).

    Designed as a single-method interface so the storage backend can be swapped
    without touching the pipeline. Only _write() needs to change.

    Current backend — local JSONL file:
      Sufficient for a demo or single-instance deployment. Zero infrastructure
      overhead; human-readable; easy to ingest into any downstream tool.

    Production backend options (Azure):
      - Azure SQL INSERT into a pipeline_traces table (same DB already used for
        analytics — natural home for query-level telemetry, easy to join with
        view-level metrics, queryable with standard SQL for pass-rate trends and
        refusal analysis).
      - Application Insights custom event (recommended for real-time operational
        monitoring: latency alerts, cost spike detection, error-rate dashboards).
        Complementary to SQL, not a replacement — ops teams use App Insights,
        data/product teams use SQL.
      Both patterns share this interface; only _write() changes.

    See PRODUCTION_PRACTICES.md §Observability for the full rationale.
    """

    def __init__(
        self,
        path: str | None = None,
        anonymize: bool | None = None,
    ) -> None:
        self._path = pathlib.Path(path or settings.trace_file)
        _anonymize = anonymize if anonymize is not None else settings.trace_anonymize
        self._filter = PiiFilter(enabled=_anonymize)

    def append(self, trace: "TraceRecord") -> None:
        """
        Persist one trace record. Never raises — write failures are logged and
        swallowed so that a disk or network error never bubbles up to the user.
        The pipeline's primary job is answering questions, not storing telemetry.
        """
        try:
            raw = json.loads(trace.model_dump_json())
            # Stamp the execution environment before filtering so eval runs and
            # manual dev calls can be filtered out of production analytics.
            # This is a store-level concern, not a TraceRecord concern — the
            # pipeline itself does not need to know where its output will land.
            raw["pipeline_env"] = settings.pipeline_env
            filtered = self._filter.apply(raw)
            self._write(json.dumps(filtered))
        except Exception as exc:
            logger.warning("trace_store.write_failed error=%s", exc)

    def read_recent(self, limit: int = 20) -> list[dict]:
        """
        Return the last `limit` records from the JSONL file, newest-first.

        Reads the whole file into memory — acceptable for the demo JSONL backend
        where the trace file is small. A production SQL backend would do
        SELECT ... ORDER BY timestamp DESC LIMIT N instead.
        """
        if not self._path.exists():
            return []
        try:
            lines = self._path.read_text(encoding="utf-8").splitlines()
            records: list[dict] = []
            for line in reversed(lines):
                line = line.strip()
                if not line:
                    continue
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
                if len(records) >= limit:
                    break
            return records
        except Exception as exc:
            logger.warning("trace_store.read_failed error=%s", exc)
            return []

    def _write(self, line: str) -> None:
        """
        Write one JSON line to the JSONL file.
        Override or replace this method to swap the storage backend.
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")
