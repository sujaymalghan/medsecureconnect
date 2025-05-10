from fastapi import APIRouter, Depends, HTTPException
from app.core.security import get_current_user
from app.schemas.consent import GrantConsentRequest
from app.models.consent import grant_consent, revoke_consent

router = APIRouter()

@router.post("/grant")
async def grant(grant_request: GrantConsentRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can grant consent.")

    consent_data = {
        "patient_username": current_user["sub"],
        "grantee_username": grant_request.grantee_username
    }
    await grant_consent(consent_data)
    return {"message": "Consent granted."}

@router.delete("/revoke")
async def revoke(grant_request: GrantConsentRequest, current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "patient":
        raise HTTPException(status_code=403, detail="Only patients can revoke consent.")

    await revoke_consent(current_user["sub"], grant_request.grantee_username)
    return {"message": "Consent revoked."}
