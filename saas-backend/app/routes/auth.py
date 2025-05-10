from fastapi import APIRouter, HTTPException
from app.models.user import verify_password, create_user, get_user_by_username
from app.schemas.user import LoginRequest, LoginResponse, RegisterRequest
from app.core.security import create_access_token

router = APIRouter()

@router.post("/register")
async def register(register_data: RegisterRequest):
    user_dict = register_data.dict()

    if len(user_dict["password"]) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters long.")
    
    existing_user = await get_user_by_username(user_dict["username"])
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered.")

    user = await create_user(user_dict)
    if not user:
        raise HTTPException(status_code=500, detail="Failed to create user.")

    return {"message": "User created successfully."}

@router.post("/login", response_model=LoginResponse)
async def login(login_data: LoginRequest):
    user = await get_user_by_username(login_data.username)
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password.")

    access_token = create_access_token(
        data={"sub": user["username"], "role": user["role"], "tenant_id": user.get("tenant_id", None)}
    )

    return {"access_token": access_token, "token_type": "bearer"}
