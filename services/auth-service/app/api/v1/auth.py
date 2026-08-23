from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.auth import RegisterRequest,UserResponse
from app.services.auth_service import AuthService


router = APIRouter()

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(
        data:RegisterRequest,
        db:AsyncSession = Depends(get_db)
        ):
    service = AuthService(db)
    user = await  service.register(data)
    return UserResponse(
        id=str(user.id),
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )