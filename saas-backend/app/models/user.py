from passlib.context import CryptContext
from app.core.mongodb import mongodb
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)

async def create_user(user_data: dict):
    db = mongodb.client[settings.MONGO_DB_NAME]
    users_collection = db["users"]
    existing_user = await users_collection.find_one({"username": user_data["username"]})
    if existing_user:
        return None 
    user_data["hashed_password"] = hash_password(user_data.pop("password"))
    await users_collection.insert_one(user_data)
    return user_data

async def get_user_by_username(username: str):
    db = mongodb.client[settings.MONGO_DB_NAME]
    users_collection = db["users"]
    user = await users_collection.find_one({"username": username})
    return user
