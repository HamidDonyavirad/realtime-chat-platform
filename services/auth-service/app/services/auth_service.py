from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import RegisterRequest
from app.security.password import hash_password, verify_password


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
