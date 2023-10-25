from pydantic import BaseModel, UUID4
# from typing import Any


class PostRequest(BaseModel):
    user_id: UUID4
    target_id: UUID4 | None = None
    key: str = 'registration'
    data: dict | None = None


class PostResponse(BaseModel):
    success: bool
