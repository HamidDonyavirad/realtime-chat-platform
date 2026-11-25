from sqlalchemy.orm import relationship,Mapped,mapped_column
from uuid import UUID,uuid4
from sqlalchemy import ForeignKey,DateTime,func,UniqueConstraint,Text,Index
from datetime import datetime

from app.db.base import Base

class Message(Base):
    __tablename__ = 'message'
    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "user_id",
            "client_message_id",
            name = "uq_conversation_id_and_user_id_and_client_message_id",

        ),
        Index(
            "index_conversation_id_and_created_at",
            "conversation_id",
            "created_at",
            "id"
        )
        )
    
    id :Mapped[UUID] = mapped_column(
        primary_key=True,
        default = uuid4,
    )

    conversation_id :Mapped[UUID] = mapped_column(
        ForeignKey('conversation.id'), nullable=False,
    )

    user_id :Mapped[int] = mapped_column(
        nullable=False,
    )

    client_message_id :Mapped[UUID] = mapped_column(
        nullable=False,
    )

    content :Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    reply_to_message_id :Mapped[UUID|None] = mapped_column(
        ForeignKey('message.id'),
        nullable=True,
    )

    created_at :Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,

    )

    updated_at :Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,

    )

    deleted_at :Mapped[datetime|None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )



    conversation :Mapped["Conversation"] = relationship(
        back_populates="messages",
    )


    reply_to : Mapped["Message|None"] = relationship(
        remote_side = "Message.id",
        back_populates = "replies",
    )

    replies : Mapped[list["Message"]] = relationship(
        back_populates = "reply_to",
    )