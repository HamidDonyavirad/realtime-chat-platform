from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
)

async def get_current_user(
        token: str = Depends(oauth2_scheme),
    ) ->UUID:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=["HS256"]
        )
        if payload.get("type") != "access":
            raise credentials_exception

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        return UUID(user_id)

    except (JWTError, ValidationError):
        raise credentials_exception