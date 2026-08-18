from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_session_maker,
    )
from app.core.config import settings

engine = create_async_engine(
    settings.database_url,
    echo=False
    )

AsyncSessionLocal = async_session_maker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
    )

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session