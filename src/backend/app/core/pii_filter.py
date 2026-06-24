import hashlib


class PiiFilter:
    """
    Scrubs PII-bearing fields from a serialised trace dict before persistence.

    Enabled via TRACE_ANONYMIZE=true. When enabled:
    - 'question' is replaced with its SHA-256 hash. The hash is non-reversible
      but stable, so duplicate questions can still be detected across runs without
      storing the raw text.
    - 'user_context' is dropped entirely — it may contain role, team ID or user
      identity that should not be persisted in an analytics store.

    This is the minimum viable anonymisation hook. In a deployment where questions
    may carry names, account references, or other personal data (HR, finance,
    customer analytics), extend this class or replace its body with a call to
    Microsoft Presidio (open-source, self-hosted) or Azure AI Language PII
    detection before the hash step. The interface — apply(dict) -> dict — stays
    the same; only the implementation changes.

    Default: disabled (TRACE_ANONYMIZE=false). This system handles internal
    newspaper analytics queries that do not contain personal data, so anonymisation
    is off by default. Enable it if the pipeline is reused in a domain where
    questions could carry PII.
    """

    def __init__(self, enabled: bool = False) -> None:
        self.enabled = enabled

    def apply(self, trace_dict: dict) -> dict:
        if not self.enabled:
            return trace_dict

        result = dict(trace_dict)
        if result.get("question"):
            result["question"] = hashlib.sha256(
                result["question"].encode()
            ).hexdigest()
        result.pop("user_context", None)
        return result
