import uuid
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped , mapped_colemn

from app.db.base import Base

class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id :Mapped[str] = mapped_colemn(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id :Mapped[str] = mapped_colemn(
        UUID(as_uuid=True),
        ForeignKey("user.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    token_hash :Mapped[str] = mapped_colemn(
        String(255),
        unique=True,
        nullable=False,
    )

    expires_at :Mapped[str] = mapped_colemn(
        DateTime(timezone=True),
        nullable=False,
    )

    is_revoked :Mapped[bool] = mapped_colemn(
        Boolean,
        default=False,
        nullable=False,
    )

    created_at :Mapped[datetime] = mapped_colemn(
        DateTime(timezone=True),
        nullable=False,
    )

    revoked_at :Mapped[datetime | None] = mapped_colemn(
        DateTime(timezone=True),
        nullable=True,
    )