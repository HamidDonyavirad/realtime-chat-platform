import uuid
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember
from app.repositories.conversation_repository import ConversationRepository


class ConversationService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repository = ConversationRepository(db)

    async def create_conversation(
            self,
            current_user_id: UUID,
            other_user_id: UUID,
    ) -> Conversation:

        if current_user_id == other_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot create a conversation with yourself")
        conversation = Conversation(id=uuid.uuid4())
        self.db.add(conversation)
        await self.db.flush()

        first_member = ConversationMember(conversation_id=conversation.id, user_id=current_user_id)
        second_member = ConversationMember(conversation_id=conversation.id, user_id=other_user_id)

        self.db.add(first_member)
        self.db.add(second_member)

        await self.db.commit()
        await self.db.refresh(conversation)
        return conversation

    async def check_membership(self, conversation_id: UUID, user_id:UUID) -> bool:
        return await self.repository.is_member(conversation_id, user_id)