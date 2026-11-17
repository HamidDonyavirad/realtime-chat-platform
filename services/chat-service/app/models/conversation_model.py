from sqlalchemy.orm import Mapped,mapped_column
from uuid import uuid4,UUID
from enum import Enum as PyEnum
from datetime import datetime,timezone
from sqlalchemy import CheckConstraint,String,DateTime, or_,and_,column ,Enum as SAEnum, func

from app.db.base import Base

class ConversationType(str, PyEnum):
    direct = 'direct'
    group ='group'
    channel ='channel'


class ConversationModel(Base):
    __tablename__ = 'conversations'
    __table_args__ = (CheckConstraint(
        or_(
            and_(
                column("type") == "direct",
                column("title").is_(None) ,
                column("description").is_(None),
            ),
            and_(
                column("type").in_(['group', 'channel']),
                column("title").is_not(None),
            )
        ),
        name = "ck_conversation_type_fields",
        ),
    )


    id :Mapped [UUID] = mapped_column(
        primary_key=True,
        default=uuid4
    )

    type :Mapped [ConversationType] = mapped_column(
        SAEnum(ConversationType),
        nullable=False,

    )

    title :Mapped [str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description :Mapped [str | None] = mapped_column(
        String(500),
        nullable=True

    )

    created_at :Mapped [datetime] = mapped_column(
        DateTime(timezone=True),
         server_default=func.now(),
        nullable=False,
    )

    updated_at :Mapped [datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,

    )

    deleted_at :Mapped [datetime|None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )