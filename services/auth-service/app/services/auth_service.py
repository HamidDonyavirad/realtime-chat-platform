from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.security.password import hash_password, verify_password
from app.security.jwt import create_access_token


class AuthService:

    def __init__(self, db: AsyncSession):
        self.user_repository = UserRepository(db)

    async def register(self,data:RegisterRequest) -> User:
        email = data.email.strip().lower()
        existing_user = await self.user_repository.get_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="Email already registered")
        user = User(
            email=email,
            hashed_password=hash_password(data.password)
        )
        return await self.user_repository.create(user)

    async def login(self,data:LoginRequest) -> str:
        email = data.email.strip().lower()
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User account is inactive")

        return create_access_token(str(user.id))
