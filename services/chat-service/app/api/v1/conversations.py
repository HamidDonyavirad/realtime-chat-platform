from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.security.dependencies import get_current_user
from app.schemas.conversation import (CreateConversationRequest,ConversationResponse)
from app.security.dependencies import get_current_user
from app.services.conversation_service import ConversationService
from app.schemas.message import (MessageResponse,SendMessageRequest)
from app.services.message_service import MessageService




router = APIRouter()

@router.post("",status_code=status.HTTP_201_CREATED,response_model=ConversationResponse)
async def create_conversation(
        data: CreateConversationRequest,
        current_user: Depends = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)

    conversation = await service.create_conversation(
        current_user_id=current_user.id,
        other_user_id=data.user_id,
    )
    return ConversationResponse(id=conversation.id)



@router.post("{conversation_id}/messages",status_code=status.HTTP_201_CREATED,response_model=MessageResponse)
async def send_message(
        conversation_id: UUID,
        data: SendMessageRequest,
        current_user: Depends = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    service = ConversationService(db)
    message = await service.send_message(
        conversation_id=conversation_id,
        sender_id=current_user.id,
        message=data.content,
    )
    return MessageResponse(
        id=message.id,
        conversation_id=message.conversation_id,
        sender_id=message.sender_id,
        content=message.content,
        created_at=message.created_at,
    )

@router.get("/{conversation_id}/messages",response_model=list[MessageResponse])
async def get_messages(
        conversation_id: UUID,
        current_user: Depends = Depends(get_current_user),
        db: AsyncSession = Depends(get_db),
):
    service = MessageService(db)
    messages = await service.get_messages(
        conversation_id=conversation_id,
        user_id=current_user.id,
    )

    return [
        MessageResponse(
            id=message.id,
            conversation_id=message.conversation_id,
            sender_id=message.sender_id,
            content=message.content,
            created_at=message.created_at,
        )
        for message in messages
    ]

