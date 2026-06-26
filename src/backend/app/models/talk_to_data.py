from pydantic import BaseModel, Field

from .trace import TraceRecord


class ConversationTurn(BaseModel):
    """One prior question/answer pair sent by the client for multi-turn context."""
    question: str
    sql: str | None = None
    answer: str | None = None


class AskRequest(BaseModel):
    question: str
    user_context: str | None = None
    session_id: str | None = None
    conversation_history: list[ConversationTurn] = Field(default_factory=list)


class AskResponse(BaseModel):
    answer: str | None = None
    caveats: list[str] = Field(default_factory=list)
    refused: bool = False
    refusal_reason: str | None = None
    trace: TraceRecord
