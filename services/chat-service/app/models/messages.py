import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey,String,func,Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapper_culumn

from app.db.base import Base

class Messages(Base):
    __tablename__ = 'messages'

    id: Mapped[uuid.UUID] = mapper_culumn(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    conversation_id: Mapped[uuid.UUID] = mapper_culumn(
        UUID(as_uuid=True),
        ForeignKey('conversations.id', ondelete='CASCADE'),
        nullable=False,
        index=True,

    )

    sender_id: Mapped[uuid.UUID] = mapper_culumn(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
    )

    content: Mapped[Text] = mapper_culumn(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapper_culumn(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )