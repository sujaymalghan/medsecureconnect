from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None

mongodb = MongoDB()

async def connect_to_mongo():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URI)
    print("Connected to MongoDB!")

async def close_mongo_connection():
    mongodb.client.close()
    print("MongoDB connection closed.")
