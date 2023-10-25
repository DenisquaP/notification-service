from pydantic import BaseModel, Json, UUID4
from typing import Any


class PostRequest(BaseModel):
    user_id: UUID4
    key: str = 'registration'
    data: Json[Any] | None = None


class PostResponse(BaseModel):
    success: bool
