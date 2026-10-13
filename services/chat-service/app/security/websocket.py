from uuid import UUID
from fastapi import WebSocket
from jose import jwt,JWTError


from app.core.config import settings

async def get_websocket_user_id (
        websocket: WebSocket,

) -> UUID:
    token = websocket.query_params.get('token')

    if not token:
        await websocket.close(code=1008)
        raise ValueError("Missing authentication token")

    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm],
        )
        user_id = payload.get('sub')
        token_type = payload.get('type')

        if not user_id or token_type != "access":
            raise ValueError('Invalid token')

        return UUID(user_id)
    except (JWTError, ValueError) :
        await websocket.close(code=1008)
        raise