from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.message import Messages

class MessageRepository:
    def __init__(self,db:AsyncSession):
        self.db = db

    async def create (self,message:Message) -> Message:
        self.db.add(message)
        await self.db.flush()
        return message

    async def get_conversation_messages(self,conversation_id:UUID) -> List[Message]:
        result = await self.db.execute(select(Messages).where(Messages.conversation_id == conversation_id)).order_by (Messages.created_at.asc())
        return list(result.scalars().all())