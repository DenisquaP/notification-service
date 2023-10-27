from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncIOMotorClient(
    os.getenv("DB_URL")
)
db = client["notification"]
notifications = db["notifications"]


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

    async def create_notification():
        pass

    async def create_user(self, user_id) -> None:
        if not await self.users.find_one({"user_id": user_id}):
            await self.users.insert_one({
                "user_id": user_id
            })
        else:
            raise ValueError("User is already exists")

    @classmethod
    async def _get_db(cls, url):
        pass
