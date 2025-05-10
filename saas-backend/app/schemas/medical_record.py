from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MedicalRecordCreate(BaseModel):
    patient_username: str
    doctor_username: str
    diagnosis: str
    notes: Optional[str] = None

class MedicalRecordResponse(BaseModel):
    id: str
    patient_username: str
    doctor_username: str
    diagnosis: str
    notes: Optional[str]
    created_at: datetime
