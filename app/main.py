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
from tables import MongoManager
from send_email import send_email

load_dotenv()
EMAIL = os.getenv("EMAIL")
DB_URL = os.getenv("DB_URL")


app = FastAPI(
    title="Notifications App"
)

mongo = MongoManager(DB_URL, 'notification')


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
        try:
            await mongo.create_user(str(body['user_id']))
            # send_email(
            #     EMAIL,
            #     f"Test message to {EMAIL}"
            # )
            return {"success": True}
        except ValueError as e:
            return {"success": True, 'Error': e}
    elif body['key'] == "new_login":
        send_email(
            EMAIL,
            f"Test message to {EMAIL}"
        )
    notif = {
        "id": str(uuid4()),
        "timestamp": time.time(),
        "is_new": True,
        "user_id": str(body['user_id']),
        "key": body['key'],
        "target_id": str(body.get('target_id')),
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
    result = await mongo.get_notifications(user_id, skip, limit)
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
