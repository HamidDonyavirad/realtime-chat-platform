from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.messages import Messages
from app.repositories.message_repository import MessageRepository
from app.repositories.conversation_repository import ConversationRepository

class MessagesService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.message_repository = MessageRepository(db)
        self.conversation_repository = ConversationRepository(db)

    async def send_message(
            self,
            conversation_id: UUID,
            sender_id: UUID,
            content: str,
    ) -> Message:
        is_member = await self.conversation_repository.is_member(conversation_id, sender_id)
        if not is_member:
            raise HTTPException(status_code=status.HTTP_403, detail="You are not a member of this conversation")

        content = content.strip()
        if not content:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message content cannot be empty")

        message = Message(
            conversation_id=conversation_id,
            sender_id=sender_id,
            content=content,
        )

        await self.message_repository.create(message)
        await self.db.commit()
        await self.db.refresh(message)
        return message

    async def get_messages(
            self,
            conversation_id: UUID,
            user_id: UUID,
    ) -> List[Message]:
        is_member = await self.conversation_repository.is_member(conversation_id, user_id)

        if not is_member:
            raise HTTPException(status_code=status.HTTP_403, detail="You are not a member of this conversation")
        return await self.message_repository.get_conversation_messages(conversation_id)