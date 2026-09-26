from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.models.conversation_member import ConversationMember

class ConversationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db


    async def create(self,conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        await self.db.flush()
        return conversation

    async def add_member(self,member: ConversationMember) -> ConversationMember:
        self.db.add(member)
        await self.db.flush()
        return member

    async def get_by_id(self,conversation_id: UUID) -> Conversation | None:
        result = await self.db.execute(select(Conversation).where(Conversation.id == conversation_id))
        return result.scalar_one_or_none()

    async def is_member(self,conversation_id: UUID,user_id:UUID) -> bool:
        result = await self.db.execute(select(ConversationMember).where(ConversationMember.conversation_id == conversation_id,user.id == user_id))
        return result.scalar_one_or_none() is not None
