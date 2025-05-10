from app.core.mongodb import mongodb
from app.core.config import settings

async def grant_consent(consent_data: dict):
    db = mongodb.client[settings.MONGO_DB_NAME]
    consents_collection = db["consents"]
    await consents_collection.insert_one(consent_data)

async def revoke_consent(patient_username: str, grantee_username: str):
    db = mongodb.client[settings.MONGO_DB_NAME]
    consents_collection = db["consents"]
    await consents_collection.delete_one({
        "patient_username": patient_username,
        "grantee_username": grantee_username
    })

async def check_consent(patient_username: str, grantee_username: str):
    db = mongodb.client[settings.MONGO_DB_NAME]
    consents_collection = db["consents"]
    consent = await consents_collection.find_one({
        "patient_username": patient_username,
        "grantee_username": grantee_username
    })
    return bool(consent)
