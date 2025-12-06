from fastapi import HTTPException
from pydantic import BaseModel, EmailStr

from src.presentation.api.products import router
from src.presentation.dependencies import UserServiceDep


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: str
    is_active: bool

@router.post("/register", response_model=UserResponse)
async def register_user(
        data:UserRegister,
        service:UserServiceDep
):
    try:
        user = await service.create_user(data.name, data.email, data.password)
        return UserResponse(
            id=str(user.id),
            email=str(user.email),
            is_active=user.is_active
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))