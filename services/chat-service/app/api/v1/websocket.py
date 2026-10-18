from uuid import UUID
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import AsyncSessionLocal
from app.security.websocket import get_websocket_user_id
from app.services.conversation_service import ConversationService
from app.services.message_service import MessageService
from app.websocket.manager import manager

router = APIRouter()



@router.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket,conversation_id: UUID,):
    try:
        user_id = await get_websocket_user_id(websocket)

    except (ValueError, Exception) :
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

    await manager.connect(user_id,websocket,)
    manager.join_conversation(conversation_id,user_id)

    try:
        while True:
            data = await websocket.receive_json()

            if not isinstance(data, dict):
                await websocket.send_json({
                    "type":"error",
                    "detail":"Expected a JSON object"
                })
                continue

            if data.get("type") != "message":
                await websocket.send_json({
                    "type":"error",
                    "detail":"Unsupported message type"
                })
                continue

            content = data.get("content")

            if not isinstance(content, dict):
                await websocket.send_json({
                    "type":"error",
                    "detail":"Content must be a string"
                })
                continue

            try:
                async with AsyncSessionLocal() as db:
                    service = MessageService(db)

                    message = await service.send_message(
                        conversation_id=conversation_id,
                        sender_id=user_id,
                        content=content
                    )
            except Exception :
                await websocket.send_json({
                    "type":"error",
                    "detail":"Could not send message"
                })
                continue

            payload = {
                "type":"message",
                "data":{
                    "id":str(message.id),
                    "conversation_id":str(message.conversation_id),
                    "sender_id":str(message.sender_id),
                    "content":message.content,
                    "created_at":message.created_at.isoformat(),
                },
            }

            await websocket.send_json({
                "type":"message_sent",
                "data":payload["data"]
            })

            await manager.broadcast_to_conversation(
                conversation_id=conversation_id,
                message=payload,
                exclude_user_id=user_id,
            )

    except WebSocketDisconnect :
        pass


    finally:
        manager.leave_conversation(conversation_id,user_id)
        manager.disconnect(user_id,websocket)