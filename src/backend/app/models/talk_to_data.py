from pydantic import BaseModel, Field

from .trace import TraceRecord


class AskRequest(BaseModel):
    question: str
    user_context: str | None = None


class AskResponse(BaseModel):
    answer: str | None = None
    caveats: list[str] = Field(default_factory=list)
    refused: bool = False
    refusal_reason: str | None = None
    trace: TraceRecord
