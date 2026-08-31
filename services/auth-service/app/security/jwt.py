from datetime import datetime,timezone,timedelta
from jose import jwt

from app.core.config import settings


def create_access_token(user_id:str) ->str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": user_id,
        "type":"access",
        "exp": expire
    }
    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )

