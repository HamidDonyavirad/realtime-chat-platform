from fastapi import APIRouter,Depends,status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.auth import RegisterRequest,UserResponse,LoginRequest ,TokenResponse
from app.services.auth_service import AuthService
from app.security.dependencies import get_current_user
from app.models.user import User


router = APIRouter()

@router.post("/register",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
async def register(
        data:RegisterRequest,
        db:AsyncSession = Depends(get_db)
        ):
    service = AuthService(db)
    user = await  service.register(data)
    return UserResponse(
        id=user.id,
        email=user.email,
        is_active=user.is_active,
        is_verified=user.is_verified,
    )

@router.post("/login",response_model=TokenResponse)
async def login(data:LoginRequest,db:AsyncSession = Depends(get_db)) ->TokenResponse:
    service = AuthService(db)
    access_token = await service.login(data)
    return TokenResponse(access_token=access_token,token_type="bearer")

@router.get("/me",response_model=UserResponse)
async def current_user(
        current_user:User = Depends(get_current_user),
) -> UserResponse:

    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
    )