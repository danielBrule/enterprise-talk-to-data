"""
Demo authentication service.

DEMO ONLY — this module hardcodes three personas and resolves the caller's role
from a plain HTTP header (X-User-Role). It exists to demonstrate that the
pipeline architecture supports role-based access control, not to provide real
security.

In production, replace DemoAuthService with calls to your organisation's
identity provider:
  - Azure Active Directory / Entra ID (recommended for Azure-hosted systems):
    validate a Bearer token with the Microsoft Identity Library (MSAL) or
    FastAPI-Azure-Auth; the resolved claims give you the user's groups or
    app roles, which you map to allowed views.
  - Any OIDC-compatible provider (Okta, Auth0, Keycloak): validate the JWT,
    extract the roles claim, map to allowed views from a policy store.

In production, never resolve permissions from a plain header. Headers are
trivially spoofable. Use signed tokens (JWT) or server-side sessions.
The X-User-Role header used here is only acceptable in a closed demo
environment with no real data or real users.

The role → allowed-views mapping itself should live in a policy store or
a configuration file managed by the data governance team, not in application
code. Hardcoding it here makes the demo self-contained.
"""
from dataclasses import dataclass, field


# ── All analytics views currently in the system ───────────────────────────────
# Update this list when new views are added. Roles are defined in terms of
# subsets of this list so a new view is admin-only by default until explicitly
# granted to a role.
_ALL_VIEWS: list[str] = [
    "analytics.vw_article_engagement",
    "analytics.vw_keyword_engagement",
    "analytics.vw_top_contributors",
    "analytics.vw_ingestion_errors",
]

# Analyst sees all editorial/content views; excluded from operational pipeline
# data (ingestion_errors) which is only relevant to the data engineering team.
_ANALYST_VIEWS: list[str] = [
    "analytics.vw_article_engagement",
    "analytics.vw_keyword_engagement",
    "analytics.vw_top_contributors",
]

# Editor sees article and contributor performance only; keyword engagement is
# strategic/commercial data outside editorial scope.
_EDITOR_VIEWS: list[str] = [
    "analytics.vw_article_engagement",
    "analytics.vw_top_contributors",
]


@dataclass
class ResolvedUser:
    """Authenticated caller with their permitted view list."""
    role: str
    allowed_views: list[str] = field(default_factory=list)


class AuthError(Exception):
    """Raised when the caller's identity cannot be resolved."""


# ── Hardcoded persona registry ────────────────────────────────────────────────
# Keyed by the value expected in the X-User-Role header (case-insensitive).
_PERSONAS: dict[str, ResolvedUser] = {
    "analyst": ResolvedUser(role="analyst", allowed_views=_ANALYST_VIEWS),
    "editor":  ResolvedUser(role="editor",  allowed_views=_EDITOR_VIEWS),
    "admin":   ResolvedUser(role="admin",   allowed_views=_ALL_VIEWS),
}

# Default persona when no X-User-Role header is present. Using the most
# restrictive non-admin role keeps the API usable in development without
# headers while avoiding accidental privilege escalation.
_DEFAULT_ROLE = "analyst"


class DemoAuthService:
    """
    Resolves an X-User-Role header value to a ResolvedUser.

    DEMO ONLY — see module docstring for the production replacement pattern.
    """

    def resolve(self, role_header: str | None) -> ResolvedUser:
        """
        Return the ResolvedUser for the given role string.

        - None / missing header → default to analyst (demo convenience).
        - Unrecognised role → AuthError (fail loudly; do not silently downgrade).
        """
        role = (role_header or _DEFAULT_ROLE).strip().lower()
        if role not in _PERSONAS:
            raise AuthError(
                f"Unknown role '{role}'. "
                f"Valid roles: {', '.join(_PERSONAS)}."
            )
        return _PERSONAS[role]
