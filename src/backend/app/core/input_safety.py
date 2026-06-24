import re

from .config import settings
from .logger import logger


class InputSafetyError(Exception):
    """Raised when user input contains patterns associated with prompt injection."""
    pass


# SQL comment markers that could be used to append or comment-out prompt fragments
_SQL_COMMENT_RE = re.compile(r"--|/\*|\*/")

# Instruction-override phrases commonly used in prompt injection attacks
_INJECTION_PHRASES = [
    r"ignore\s+(previous|prior|above|all)\s+instructions",
    r"forget\s+(previous|prior|your|all)\s+instructions",
    r"disregard\s+(previous|prior|above|all|your)\s+instructions",
    r"you\s+are\s+now\s+",
    r"\bsystem\s*:",
    r"\bassistant\s*:",
    r"\[inst\]",           # Llama instruction token
    r"<\|im_start\|>",    # ChatML token
    r"<\|system\|>",      # ChatML system token
    r"<\|im_sep\|>",
]
_INJECTION_RE = re.compile("|".join(_INJECTION_PHRASES), re.IGNORECASE)

# Control characters excluding tab (\x09), newline (\x0a), carriage return (\x0d)
_CONTROL_CHAR_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")


def validate_user_input(text: str) -> None:
    """
    Validate user input against prompt injection patterns before it enters any prompt.

    Raises InputSafetyError (with a user-facing reason) if:
    - Input exceeds MAX_QUESTION_LENGTH characters
    - Control characters are present (excluding tab, newline, carriage return)
    - SQL comment markers are present (--, /*, */)
    - Instruction-override phrases are detected

    Logs a security.injection_attempt entry for each violation before raising.
    """
    if not isinstance(text, str) or not text.strip():
        raise InputSafetyError("Question must be a non-empty string.")

    preview = text[:100].replace("\n", " ")

    if len(text) > settings.max_question_length:
        logger.warning(
            "security.injection_attempt pattern=length_exceeded len=%s limit=%s preview=%s",
            len(text), settings.max_question_length, preview,
        )
        raise InputSafetyError(
            f"Question exceeds the maximum allowed length of {settings.max_question_length} characters."
        )

    if m := _CONTROL_CHAR_RE.search(text):
        logger.warning(
            "security.injection_attempt pattern=control_char char=0x%02x preview=%s",
            ord(m.group()), preview,
        )
        raise InputSafetyError("Question contains invalid control characters and cannot be processed.")

    if m := _SQL_COMMENT_RE.search(text):
        logger.warning(
            "security.injection_attempt pattern=sql_comment matched=%r preview=%s",
            m.group(), preview,
        )
        raise InputSafetyError(
            f"Question contains '{m.group()}' which is not allowed. "
            "If this is a legitimate question, please rephrase it."
        )

    if m := _INJECTION_RE.search(text):
        logger.warning(
            "security.injection_attempt pattern=instruction_phrase matched=%r preview=%s",
            m.group(), preview,
        )
        raise InputSafetyError(
            "Question contains patterns that cannot be processed. "
            "Please rephrase your analytics question."
        )
