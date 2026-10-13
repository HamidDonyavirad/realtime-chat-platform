from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.security.websocket import get_websocket_user_id
from app.services.conversation_service import ConversationService
from app.websocket.manager import ConnectionManager

router = APIRouter()

manager = ConnectionManager()

@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket,conversation_id: UUID,):
    try:
        user_id = await get_websocket_user_id(
            websocket
        )

    except ValueError:
        return

    async with AsyncSessionLocal() as db:
        conversation_service = ConversationService(db)

        is_member = await conversation_service.check_membership(
            conversation_id=conversation_id,
            user_id=user_id,
        )

    if not is_member:
        await websocket.close(code=1008)
        return

    await manager.connect(
        user_id=user_id,
        websocket=websocket,
    )

    manager.join_conversation(
        conversation_id=conversation_id,
        user_id=user_id,
    )

    try:
        while True:
            data = await websocket.receive_json()

            await websocket.send_json({
                "type": "echo",
                "data": data,
            })

    except WebSocketDisconnect:
        manager.leave_conversation(
            conversation_id=conversation_id,
            user_id=user_id,
        )

        manager.disconnect(user_id)