from fastapi import Depends, HTTPException
from app.core.security import get_current_user
from app.core.permit import permit

def permission_required(action: str, resource_type: str):
    async def permission_checker(record_id: str, current_user: dict = Depends(get_current_user)):
        resource_key = f"{resource_type}:{record_id}"

        print(f"Checking permission for user: {current_user['sub']}, action: {action}, resource: {resource_key}")

        allowed = await permit.check(
            user=current_user["sub"],
            action=action,
            resource=resource_key
        )

        if not allowed:
            raise HTTPException(status_code=403, detail="Permission Denied")
    return permission_checker
