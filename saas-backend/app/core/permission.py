from fastapi import Depends, HTTPException
from app.core.permit import permit
from app.core.security import get_current_user

async def require_permission(action: str, resource: str, current_user: dict = Depends(get_current_user)):
    result = await permit.check(
        user=current_user["username"],  # or current_user["sub"] based on your token
        action=action,
        resource=resource
    )
    if not result.allow:
        raise HTTPException(status_code=403, detail="Unauthorized by permission policy")
