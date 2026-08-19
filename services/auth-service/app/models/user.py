import uuid
from daatatime import datetime

from sqlalchemy import Boolean, Datetime,string, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapper, mapped_columns

from app.db.base import Base

class User(Base):
    __tablename__ = 'user'

    id : Mapper[uuid.UUID] = mapped_columns(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    email : Mapper[str] = mapped_columns(
        string(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password : Mapper[str] = mapped_columns(
        string(255),
        nullable=False,
    )

    is_active : Mapper[bool] = mapped_columns(
        boolean,
        default=True,
        nullable=False,
    )

    is_verified : Mapper[bool] = mapped_columns(
        boolean,
        default=False,
        nullable=False,
    )

    created_at : Mapper[datetime] = mapped_columns(
        Datetime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at : Mapper[datetime] = mapped_columns(
        Datetime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

