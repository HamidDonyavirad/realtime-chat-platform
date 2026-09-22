import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped,mapped_column

from app.db.base import Base

class ConversationMember(Base):
    __tablename__ = 'conversation_members'

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        foreignkey('conversation.id',ondelete="CASCADE"),
        primary_key=True,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )