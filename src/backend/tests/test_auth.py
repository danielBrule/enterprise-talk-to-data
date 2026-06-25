"""
Tests for DemoAuthService.

Covers role resolution, default-role behaviour, and unknown-role rejection.
No HTTP layer involved — that is covered by the API integration tests.
"""
import pytest

from backend.app.core.auth import AuthError, DemoAuthService, _ALL_VIEWS, _ANALYST_VIEWS, _EDITOR_VIEWS


@pytest.fixture
def svc() -> DemoAuthService:
    return DemoAuthService()


# ── Happy-path resolution ─────────────────────────────────────────────────────

def test_resolve_analyst(svc):
    user = svc.resolve("analyst")
    assert user.role == "analyst"
    assert user.allowed_views == _ANALYST_VIEWS


def test_resolve_editor(svc):
    user = svc.resolve("editor")
    assert user.role == "editor"
    assert user.allowed_views == _EDITOR_VIEWS


def test_resolve_admin(svc):
    user = svc.resolve("admin")
    assert user.role == "admin"
    assert user.allowed_views == _ALL_VIEWS


def test_resolve_is_case_insensitive(svc):
    assert svc.resolve("ANALYST").role == "analyst"
    assert svc.resolve("Admin").role == "admin"
    assert svc.resolve("EDITOR").role == "editor"


# ── View access invariants ────────────────────────────────────────────────────

def test_admin_has_all_views_including_ingestion_errors(svc):
    admin = svc.resolve("admin")
    assert "analytics.vw_ingestion_errors" in admin.allowed_views


def test_analyst_cannot_see_ingestion_errors(svc):
    analyst = svc.resolve("analyst")
    assert "analytics.vw_ingestion_errors" not in analyst.allowed_views


def test_editor_cannot_see_keyword_engagement(svc):
    editor = svc.resolve("editor")
    assert "analytics.vw_keyword_engagement" not in editor.allowed_views


def test_analyst_can_see_keyword_engagement(svc):
    analyst = svc.resolve("analyst")
    assert "analytics.vw_keyword_engagement" in analyst.allowed_views


def test_editor_is_subset_of_analyst(svc):
    editor_views = set(svc.resolve("editor").allowed_views)
    analyst_views = set(svc.resolve("analyst").allowed_views)
    assert editor_views.issubset(analyst_views)


def test_analyst_is_subset_of_admin(svc):
    analyst_views = set(svc.resolve("analyst").allowed_views)
    admin_views = set(svc.resolve("admin").allowed_views)
    assert analyst_views.issubset(admin_views)


# ── Default / missing header ──────────────────────────────────────────────────

def test_none_header_defaults_to_analyst(svc):
    user = svc.resolve(None)
    assert user.role == "analyst"


def test_empty_string_header_defaults_to_analyst(svc):
    user = svc.resolve("")
    assert user.role == "analyst"


# ── Unknown role ──────────────────────────────────────────────────────────────

def test_unknown_role_raises_auth_error(svc):
    with pytest.raises(AuthError, match="Unknown role"):
        svc.resolve("superuser")


def test_unknown_role_error_lists_valid_roles(svc):
    with pytest.raises(AuthError) as exc_info:
        svc.resolve("god_mode")
    assert "analyst" in str(exc_info.value)
    assert "editor" in str(exc_info.value)
    assert "admin" in str(exc_info.value)
