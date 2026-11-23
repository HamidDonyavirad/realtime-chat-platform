from sqlalchemy.orm import Mapped,relationship, mapped_column
from uuid import uuid4,UUID
from datetime import datetime,timezone
from sqlalchemy import DateTime,func,Enum as SAEnum,ForeignKey,CheckConstraint, Index,or_,and_
from enum import Enum as PyEnum


from app.db.base import Base

class ConversationMemberRole(str, PyEnum):
    admin = 'admin'
    member = 'member'
    owner = 'owner'

class ConversationMemberLeaveReason(str, PyEnum):
    removed = 'removed'
    left = 'left'



class ConversationMember(Base):
    __tablename__ = 'conversation_member'
    __table_args__ = (
        Index(
                "uq_active_conversation_member_id",
                ConversationMember.conversation_id,
                ConversationMember.user_id,
                unique=True,
                postgresql_where=ConversationMember.left_at.is_(None)
            ),
        CheckConstraint(
            or_(
                and_(
                    column("left_at").is_(None),
                    column("leave_reason").is_(None),
                    ),
                and_(
                    column("left_at").is_not(None),
                    column("leave_reason").is_not(None),
                    )
                ),
            name="ck_conversation_member_left_at_and_leave_reason",
                ),
                    ),


    id : Mapped[UUID]= mapped_column(
        primary_key=True,
        default=uuid4,

    )

    conversation_id : Mapped[UUID]= mapped_column(
        ForeignKey('conversation.id'), nullable=False,
    )

    user_id : Mapped[int]= mapped_column(nullable=False)

    role : Mapped[ConversationMemberRole]= mapped_column(
        SAEnum(ConversationMemberRole),
        nullable=False,

    )

    joined_at : Mapped[datetime]= mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    left_at : Mapped[datetime|None]= mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    leave_reason : Mapped[ConversationMemberLeaveReason|None]= mapped_column(
        SAEnum(ConversationMemberLeaveReason),
        nullable=True,
    )



    conversation : Mapped["Conversation"]= relationship(back_populates="conversation_members")