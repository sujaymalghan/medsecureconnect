from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, medical_records, consent,lab
from app.core.mongodb import connect_to_mongo, close_mongo_connection
from app.core.permit import permit

app = FastAPI(
    title="MedSecure Connect API",
    description="HIPAA-Compliant Telehealth API with Dynamic Consent",
    version="1.0.0"
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(medical_records.router, prefix="/api/medical-records", tags=["Medical Records"])
app.include_router(consent.router, prefix="/api/consents", tags=["Consents"])
app.include_router(lab.router, prefix="/api/lab", tags=["Lab"])

