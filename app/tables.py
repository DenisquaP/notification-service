from uuid import uuid4
from motor.motor_asyncio import AsyncIOMotorClient
import time


class MongoManager:
    def __init__(self, url: str, db: str) -> None:
        self.client = AsyncIOMotorClient(
            url
        )
        self.db = self.client[db]
        self.notifications = self.db["notifications"]
        self.users = self.db['users']

    async def get_notifications(
            self, user_id: str, skip: int = 0, limit: int = 10
    ) -> list:
        """_summary_

        Args:
            user_id (str): user`s uuid by str
            skip (int, optional): Count of skipping messages. Defaults to 0.
            limit (int, optional): Count of limit of messages. Defaults to 10.

        Raises:
            ValueError: if user does not exists

        Returns:
            list: list of user`s notifications
        """
        user = await self.check_user(user_id)
        if not user:
            raise ValueError("User does not exists")
        cursor = self.notifications.find({"user_id": user_id})
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

    async def create_notification(
        self,
        user_id: str,
        key: str,
        target_id: str,
        data: dict
    ) -> None:
        """_summary_

        Args:
            user_id (str): User`s uuid by str
            key (str): Key of operation
            target_id (str): Target`s uuid by str
            data (dict): dict of data
        """
        notif = {
            "id": str(uuid4()),
            "timestamp": time.time(),
            "is_new": True,
            "user_id": user_id,
            "key": key,
            "target_id": target_id,
            "data": data
        }
        await self.notifications.insert_one(notif)

    async def create_user(self, user_id: str, email: str) -> None:
        """_summary_

        Args:
            user_id (str): User`s uuid by str
            email (str): User`s email

        Raises:
            ValueError: If user exists in db
        """
        user = await self.check_user(user_id)
        print(user)
        if user:
            print(1)
            raise ValueError("User is already exists")
        await self.users.insert_one({
            "user_id": user_id,
            "email": email
        })

    async def check_user(self, user_id: str) -> bool:
        """_summary_

        Args:
            user_id (str): User`s uuid

        Returns:
            bool: True if exists else False
        """
        user = await self.users.find_one({"user_id": user_id})
        return True if user else False

    async def check_notification(
            self, notification_id: str, user_id: str
            ) -> bool:
        """_summary_

        Args:
            notification_id (str): Notification`s uuid by str
            user_id (str): User`s uuid by str

        Returns:
            bool: True if exists else False
        """
        notification = await self.notifications.find_one({
            "user_id": user_id,
            'notification_id': notification_id
            })
        return 1 if notification else 0

    async def update(self, user_id: str, notification_id: str) -> None:
        """_summary_

        Args:
            user_id (str): User`s uuid by str
            notification_id (str): Notification`s uuid by str

        Raises:
            ValueError: If notification does not exists
        """
        user = await self.check_user(user_id)
        notification = await self.check_notification(notification_id, user_id)
        if user and notification:
            await self.notifications.update_one(
                {"user_id": user_id, "id": notification_id},  # noqa 501
                {"$set": {"is_new": False}}
            )
        else:
            raise ValueError("Notification does not exists")
