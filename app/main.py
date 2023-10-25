from fastapi import FastAPI
from pydantic_models.models import (
    PostRequest,
    PostResponse
)
# from tables import notification


app = FastAPI()


@app.post(
    '/create',
    status_code=201,
    response_class=PostResponse,
    tags=['notification']
)
async def create_notif(body: PostRequest):
    print(body)
    return {"success": True}


@app.get(
    '/list',
    status_code=200,
    tags=['notification']
)
async def get_listing(user_id: str, skip: int = 0, limit: int = 0):
    result = {
        "success": True,
        "data": {
            "elements": 23,
            "new": 12,
            "request": {
                "user_id": user_id,
                "skip": 0,
                "limit": 10,
            },
            "list": None
        }
    }
    return result
