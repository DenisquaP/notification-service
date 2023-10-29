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
        notifs = await self.notifications.find_one({"user_id": user_id})
        new = 0
        all = 0
        all_required = []
        for entry in notifs["notifications"]:
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
            "key": key,
            "target_id": target_id,
            "data": data
        }
        await self.notifications.update_one(
            {"user_id": user_id},
            {"$addToSet": {"notifications": notif}}
            )

    async def create_user(self, user_id: str, email: str) -> None:
        """_summary_

        Args:
            user_id (str): User`s uuid by str
            email (str): User`s email

        Raises:
            ValueError: If user exists in db
        """
        user = await self.check_user(user_id)
        if user:
            raise ValueError("User is already exists")
        await self.notifications.insert_one({
            "user_id": user_id,
            "email": email,
            "notifications": list()
        })

    async def check_user(self, user_id: str) -> bool:
        """_summary_

        Args:
            user_id (str): User`s uuid

        Returns:
            bool: True if exists else False
        """
        user = await self.notifications.find_one({"user_id": user_id})
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
            'id': notification_id
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
        if user:
            user_all = await self.notifications.find_one(
                {"user_id": user_id, "notifications.id": notification_id}
            )
            for notif in user_all['notifications']:
                if notif["id"] == notification_id:
                    notif["is_new"] = False
            await self.notifications.replace_one(
                {'user_id': user_id},
                user_all
            )
        else:
            raise ValueError("Notification does not exists")
