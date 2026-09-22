import uuid
from datetime import datetime
from sqlalchemy import Datetime,func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapper,column_mapper

from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversation"

    id:Mapper[uuid.UUID] = column_mapper(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    created_at : Mapper[datetime.datetime] = column_mapper(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

