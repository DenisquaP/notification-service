from fastapi import FastAPI
from pydantic_models.models import (
    PostRequest,
    Response,
    ReadRequest
)
from dotenv import load_dotenv
import os

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
    """_summary_

    Args:
        body (PostRequest): Request body. To learn more
        check pydantic_models/models.py class PostRequest

    Returns:
        Response: dict of 2 vals: success and errors
    """
    body = body.dict()
    if body['key'] in ['registration', 'new_login']:
        try:
            await mongo.create_user(
                str(body['user_id']),
                body['email']
                )
            send_email(
                EMAIL,
                f"Test message to {EMAIL}"
            )
            if body['key'] == 'registration':
                return {"success": True}
        except ValueError as e:
            return {"success": False, 'error': str(e)}
    await mongo.create_notification(
        str(body['user_id']),
        body['key'],
        str(body['target_id']),
        body['data']
    )
    response = {"success": True, 'error': None}
    return response


@app.get(
    '/list',
    status_code=200,
    tags=['notification']
)
async def get_listing(user_id: str, skip: int = 0, limit: int = 10) -> dict:
    """_summary_

    Args:
        user_id (str): User`s uuid by str.
        skip (int, optional): Count of message to skip. Defaults to 0.
        limit (int, optional): Count of message limit to show.
        Defaults to 10.

    Returns:
        dict: a dict of user`s notifications and count of them
    """
    try:
        result = await mongo.get_notifications(user_id, skip, limit)
    except ValueError as e:
        return {'success': False, 'error': e}
    return result


@app.post(
    '/read',
    response_model=Response,
    tags=['notification']
)
async def read_message(body: ReadRequest) -> dict:
    """_summary_

    Args:
        body (ReadRequest): user_id and notification_id

    Returns:
        dict: success and errors
    """
    body = body.dict()
    try:
        await mongo.update(str(body["user"]), str(body["notification_id"]))
    except ValueError as e:
        return {"success": False, "error": e}
    return {"success": True}
