from pydantic import BaseModel
from datetime import datetime


class IngestionErrorFilter(BaseModel):
    stage: str | None = None
    error_type: str | None = None
    data_id: str | None = None


class IngestionErrorResponse(BaseModel):
    error_id: int
    stage: str
    data_id: str
    error_type: str
    error_message: str
    attempted_at: datetime
