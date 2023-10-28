from pydantic import BaseModel, UUID4
from typing import Optional


class PostRequest(BaseModel):
    user_id: UUID4
    target_id: UUID4 | None = None
    key: str = 'registration'
    data: dict | None = None
    email: str | None = ''


class Response(BaseModel):
    success: bool
    error: Optional[str]


class ReadRequest(BaseModel):
    user_id: UUID4
    notification_id: str
