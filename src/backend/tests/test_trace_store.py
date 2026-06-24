"""
Tests for TraceStore and PiiFilter.

TraceStore tests use tmp_path (pytest fixture) so no files are written to the
working tree. All assertions are on the JSONL content, not on internal state.
"""
import hashlib
import json

from backend.app.core.pii_filter import PiiFilter
from backend.app.core.trace_store import TraceStore
from backend.app.models.trace import TraceRecord


def _trace(question: str = "top articles by comments", **kwargs) -> TraceRecord:
    return TraceRecord(question=question, **kwargs)


# ── TraceStore ────────────────────────────────────────────────────────────────

def test_append_creates_file_and_writes_valid_jsonl(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=False)
    store.append(_trace())

    lines = (tmp_path / "traces.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 1
    record = json.loads(lines[0])
    assert record["question"] == "top articles by comments"
    assert "trace_id" in record
    assert "timestamp" in record


def test_append_multiple_runs_are_separate_lines(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=False)
    store.append(_trace("first question"))
    store.append(_trace("second question"))

    lines = (tmp_path / "traces.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["question"] == "first question"
    assert json.loads(lines[1])["question"] == "second question"


def test_append_creates_missing_parent_directories(tmp_path):
    store = TraceStore(path=str(tmp_path / "nested" / "deep" / "traces.jsonl"), anonymize=False)
    store.append(_trace())
    assert (tmp_path / "nested" / "deep" / "traces.jsonl").exists()


def test_append_does_not_raise_on_write_failure(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=False)

    def _fail(line: str) -> None:
        raise OSError("disk full")

    store._write = _fail
    # Must not propagate — the pipeline should continue serving answers even if
    # the trace store is broken.
    store.append(_trace())


def test_append_includes_all_core_trace_fields(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=False)
    trace = _trace(
        execution_status="success",
        generated_sql="SELECT TOP 10 * FROM analytics.vw_test",
        row_count=10,
    )
    store.append(trace)

    record = json.loads((tmp_path / "traces.jsonl").read_text(encoding="utf-8").strip())
    assert record["execution_status"] == "success"
    assert record["generated_sql"] == "SELECT TOP 10 * FROM analytics.vw_test"
    assert record["row_count"] == 10


# ── PiiFilter ─────────────────────────────────────────────────────────────────

def test_pii_filter_disabled_preserves_all_fields():
    f = PiiFilter(enabled=False)
    result = f.apply({"question": "top articles", "user_context": "role=analyst"})
    assert result["question"] == "top articles"
    assert result["user_context"] == "role=analyst"


def test_pii_filter_enabled_hashes_question():
    f = PiiFilter(enabled=True)
    result = f.apply({"question": "top articles"})
    expected = hashlib.sha256(b"top articles").hexdigest()
    assert result["question"] == expected


def test_pii_filter_enabled_drops_user_context():
    f = PiiFilter(enabled=True)
    result = f.apply({"question": "test", "user_context": "role=admin"})
    assert "user_context" not in result


def test_pii_filter_enabled_missing_user_context_is_safe():
    f = PiiFilter(enabled=True)
    result = f.apply({"question": "test"})
    assert "user_context" not in result


def test_pii_filter_enabled_other_fields_are_unchanged():
    f = PiiFilter(enabled=True)
    result = f.apply({
        "question": "test",
        "execution_status": "success",
        "row_count": 5,
    })
    assert result["execution_status"] == "success"
    assert result["row_count"] == 5


# ── TraceStore + PiiFilter integration ───────────────────────────────────────

def test_trace_store_anonymizes_question_when_enabled(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=True)
    store.append(_trace(user_context="role=editor"))

    record = json.loads((tmp_path / "traces.jsonl").read_text(encoding="utf-8").strip())
    expected_hash = hashlib.sha256(b"top articles by comments").hexdigest()
    assert record["question"] == expected_hash
    assert "user_context" not in record


def test_trace_store_no_anonymization_by_default(tmp_path):
    store = TraceStore(path=str(tmp_path / "traces.jsonl"), anonymize=False)
    store.append(_trace(user_context="role=editor"))

    record = json.loads((tmp_path / "traces.jsonl").read_text(encoding="utf-8").strip())
    assert record["question"] == "top articles by comments"
    assert record["user_context"] == "role=editor"
