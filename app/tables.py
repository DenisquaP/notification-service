# from pymongo import MongoClient
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(
    "mongodb+srv://DenisPis:CosmoWins1@notification.e67b7fu.mongodb.net/?retryWrites=true&w=majority"  # noqa 501
)
db = client["notification"]
notifications = db["notifications"]
