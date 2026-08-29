import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
from httpx import AsyncClient,ASGITransport
from sqlalchemy.pool import NullPool

from app.db.base import Base
from app.main import app
from app.db.database import get_db
from app.core.config import settings

TEST_DATABASE_URL = settings.database_test_url

test_engine = create_async_engine(TEST_DATABASE_URL,echo=False, poolclass=NullPool)

TestingSessionLocal = async_sessionmaker(bind=test_engine,class_=AsyncSession,expire_on_commit=False,)

@pytest_asyncio.fixture
async def db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest_asyncio.fixture
async def client(db):
    async def override_get_db():
        yield db

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient( transport=transport,base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()
