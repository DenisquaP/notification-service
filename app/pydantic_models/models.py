from pydantic import BaseModel, UUID4


class PostRequest(BaseModel):
    user_id: UUID4
    target_id: UUID4 | None = None
    key: str = 'registration'
    data: dict | None = None


class Response(BaseModel):
    success: bool


class ReadRequest(BaseModel):
    user_id: UUID4
    notification_id: str
