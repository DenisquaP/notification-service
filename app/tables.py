from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()


client = AsyncIOMotorClient(
    os.getenv("DB_URL")
)
db = client["notification"]
notifications = db["notifications"]
