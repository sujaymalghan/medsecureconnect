from fastapi import APIRouter, Depends, HTTPException
from app.schemas.medical_record import MedicalRecordCreate, MedicalRecordResponse
from app.core.security import get_current_user
from app.core.authorization import permission_required
from app.models.medical_record import create_medical_record, get_medical_record
from app.core.permit import permit
from datetime import datetime
from app.core.mongodb import mongodb
from app.core.config import settings


router = APIRouter()

@router.post("/", response_model=MedicalRecordResponse)
async def create_record(record: MedicalRecordCreate, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can create records.")

    record_dict = record.dict()
    record_id = await create_medical_record(record_dict)

    await permit.resources.create(
        resource_key=f"medical_record:{record_id}",
        resource={
            "tenant": current_user["tenant_id"],
            "attributes": {
                "patient_username": record.patient_username,
                "doctor_username": record.doctor_username
            }
        }
    )

    return MedicalRecordResponse(
        id=record_id,
        patient_username=record.patient_username,
        doctor_username=record.doctor_username,
        diagnosis=record.diagnosis,
        notes=record.notes,
        created_at=datetime.utcnow()
    )

@router.get("/{record_id}", response_model=MedicalRecordResponse)
async def get_record(record_id: str, _: None = Depends(permission_required("view", "medical_record"))):
    record = await get_medical_record(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return MedicalRecordResponse(
        id=str(record["_id"]),
        patient_username=record["patient_username"],
        doctor_username=record["doctor_username"],
        diagnosis=record["diagnosis"],
        notes=record.get("notes"),
        created_at=record["created_at"]
    )

from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.core.permit import permit
from app.core.mongodb import mongodb
from app.core.config import settings

router = APIRouter()

@router.get("/all")
async def get_all_records(current_user: dict = Depends(get_current_user)):
    decision = await permit.check(user="admin", action="read", resource="medical_record")
    print("Allowed:", decision)
    print("Reasons:", decision)


    print(f"Checking permission for user: {current_user['sub']}, action: read, resource: medical_record")
    is_allowed = await permit.check(
        user=current_user["sub"],
        action="read",
        resource="medical_record"
    )
    if not is_allowed:
        raise HTTPException(status_code=403, detail="Access denied by Permit")

    db = mongodb.client[settings.MONGO_DB_NAME]
    records = await db["medical_records"].find().to_list(100)

    return [
        {
            "id": str(record["_id"]),
            "patient_username": record["patient_username"]
        }
        for record in records
    ]


@router.get("/patient/{patient_username}")
async def get_records_by_patient(patient_username: str, current_user: dict = Depends(get_current_user)):
    db = mongodb.client[settings.MONGO_DB_NAME]
    records = await db["medical_records"].find({"patient_username": patient_username}).to_list(100)
    return [{"id": str(r["_id"]), "patient_username": r["patient_username"], "doctor_username": r["doctor_username"], "diagnosis": r["diagnosis"], "notes": r.get("notes")} for r in records]

@router.get("/doctor/{doctor_username}")
async def get_records_by_doctor(doctor_username: str, current_user: dict = Depends(get_current_user)):
    db = mongodb.client[settings.MONGO_DB_NAME]
    records = await db["medical_records"].find({"doctor_username": doctor_username}).to_list(100)
    return [{"id": str(r["_id"]), "patient_username": r["patient_username"], "doctor_username": r["doctor_username"], "diagnosis": r["diagnosis"], "notes": r.get("notes")} for r in records]

