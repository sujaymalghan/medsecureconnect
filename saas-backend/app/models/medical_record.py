from datetime import datetime
from app.core.mongodb import mongodb
from app.core.config import settings

async def create_medical_record(record_data: dict):
    db = mongodb.client[settings.MONGO_DB_NAME]
    collection = db["medical_records"]
    record_data["created_at"] = datetime.utcnow()
    result = await collection.insert_one(record_data)
    return str(result.inserted_id)

async def get_medical_record(record_id: str):
    db = mongodb.client[settings.MONGO_DB_NAME]
    collection = db["medical_records"]
    record = await collection.find_one({"_id": record_id})
    return record
