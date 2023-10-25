from fastapi import FastAPI
from pydantic_models.models import (
    PostRequest,
    PostResponse
)
from uuid import uuid4
import time
from tables import notifications


app = FastAPI(
    title="Notifications App"
)


async def send_email():
    pass


@app.post(
    '/create',
    status_code=201,
    tags=['notification'],
    response_model=PostResponse
)
async def create_notif(body: PostRequest):
    body = body.dict()
    if body['key'] == 'registration':
        await send_email()
        return {"success": True}
    notif = {
        "id": str(uuid4()),
        "timestamp": time.time(),
        "is_new": True,
        "user_id": str(body['user_id']),
        "key": body['key'],
        "target_id": str(body['target_id']),
        "data": body['data']
    }
    await notifications.insert_one(notif)
    response = {"success": True}
    return response


@app.get(
    '/list',
    status_code=200,
    tags=['notification']
)
async def get_listing(user_id: str, skip: int = 0, limit: int = 10):
    cursor = notifications.find({"user_id": user_id})
    new = 0
    all = 0
    all_required = []
    for entry in await cursor.to_list(length=100):
        entry.pop('_id')
        if entry['is_new']:
            new += 1
        all += 1
        all_required.append(entry)
    result = {
        "success": True,
        "data": {
            "elements": all,
            "new": new,
            "request": {
                "user_id": user_id,
                "skip": skip,
                "limit": limit,
            },
            "list": all_required
        }
    }
    return result
