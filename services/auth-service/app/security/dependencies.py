from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import UserRepository


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db))->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception

        if token_type != "access":
            raise credentials_exception

        user_id = UUID(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    repository = UserRepository(db)

    user = await repository.get_user_by_id(user_id)

    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is inactive")
    return user

