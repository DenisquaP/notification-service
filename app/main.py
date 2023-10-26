from fastapi import FastAPI
from pydantic_models.models import (
    PostRequest,
    Response,
    ReadRequest
)
from uuid import uuid4
import time
from dotenv import load_dotenv
import os

from tables import notifications
from send_email import send_email

load_dotenv()
EMAIL = os.getenv("EMAIL")


app = FastAPI(
    title="Notifications App"
)


@app.post(
    '/create',
    status_code=201,
    tags=['notification'],
    response_model=Response
)
async def create_notif(body: PostRequest) -> Response:
    body = body.dict()
    print(body)
    if body['key'] == 'registration':
        await send_email(
            EMAIL,
            "some message"
        )
        return {"success": True}
    elif body['key'] == "new_login":
        await send_email(
            EMAIL,
            "some message"
        )
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
async def get_listing(user_id: str, skip: int = 0, limit: int = 10) -> dict:
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
            "list": all_required[skip:limit]
        }
    }
    return result


@app.post(
    '/read',
    response_model=Response,
    tags=['notification']
)
async def read_message(body: ReadRequest):
    body = body.dict()
    await notifications.update_one(
        {"user_id": str(body["user_id"]), "id": str(body["notification_id"])},  # noqa 501
        {"$set": {"is_new": False}}
    )
    return {"success": True}
