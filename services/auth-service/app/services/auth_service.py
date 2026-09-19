from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone

from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.repositories.refresh_token_repository import RefreshTokenRepository
from app.repositories.user_repository import UserRepository
from app.schemas.auth import RegisterRequest, LoginRequest
from app.security.password import hash_password, verify_password
from app.security.refresh_token import generate_refresh_token,hash_refresh_token
from app.security.jwt import create_access_token
from app.core.config import settings


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

    async def login(self,data:LoginRequest) -> tuple[str,str]:
        email = data.email.strip().lower()
        user = await self.user_repository.get_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

        if not verify_password(data.password, user.hashed_password):
            raise HTTPException (status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect email or password")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User account is inactive")

        access_token = create_access_token(str(user.id))
        refresh_token = generate_refresh_token()
        refresh_token_model = RefreshToken(
            user_id=user.id,
            token_hash = hash_refresh_token(refresh_token),
            expires_at = datetime.now(timezone.utc)+timedelta(days=settings.refresh_token_expire_days),
            created_at = datetime.now(timezone.utc),
            )

        refresh_token_repository = RefreshTokenRepository(self.user_repository.db)
        await refresh_token_repository.create(refresh_token_model)
        return access_token, refresh_token


    async def refresh(self,refresh_token:str) -> tuple[str,str]:
        token_hash = hash_refresh_token(refresh_token)
        refresh_token_repository = RefreshTokenRepository(self.user_repository.db)
        stored_token = await refresh_token_repository.get_by_hash(token_hash)
        if stored_token is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token")
        if stored_token.is_revoked:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh token has been revoked")

        if stored_token.expires_at <= datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Refresh token expired")

        user = await self.user_repository.get_by_id(stored_token.user_id)

        if user is None or not user.is_active:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid refresh token")

        access_token = create_access_token(str(user.id))
        return access_token, refresh_token

    async def logout(self,refresh_token:str) -> None:

        token_hash = hash_refresh_token(refresh_token)
        stored_token = await self.user_repository.get_by_hash(token_hash)
        if stored_token is None:
            return
        await self.user_repository.revoke(stored_token)
