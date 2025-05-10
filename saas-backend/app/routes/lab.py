from fastapi import APIRouter, Depends, HTTPException
from app.core.mongodb import mongodb
from app.schemas.user import User
from app.core.security import get_current_user
from app.core.config import settings
from bson import ObjectId

router = APIRouter()


@router.get("/orders")
async def get_lab_orders(current_user: User = Depends(get_current_user)):
    if current_user["role"] != "lab":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db = mongodb.client[settings.MONGO_DB_NAME]
    medical_records = db["medical_records"]
    records_cursor = db["medical_records"].find({"test_status": "pending"})
    orders = []
    async for record in records_cursor:
        orders.append({
            "id": str(record["_id"]),
            "patient_username": record.get("patient_username", ""),
            "test_name": record.get("test_name", ""),
            "status": record.get("test_status", ""),
            "result": record.get("test_result", None),
        })
    return orders

@router.patch("/orders/{order_id}")
async def update_order_status(order_id: str, data: dict, current_user: User = Depends(get_current_user)):
    if current_user.role != "lab":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    db = mongodb.client[settings.MONGO_DB_NAME]
    await db["medical_records"].update_one(
        {"_id": ObjectId(order_id)},
        {"$set": {"test_status": data.get("status")}}
    )
    return {"message": "Status updated"}
