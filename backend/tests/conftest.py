"""
Pytest configuration and fixtures.
Provides test database, test client, and authentication fixtures.
"""
import asyncio
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.main import app
from app.database import get_db
from app.models.user import User
from app.services.auth import hash_password, create_access_token


# Test database URL (SQLite for testing)
TEST_DATABASE_URL = "postgresql://neondb_owner:npg_yFlOh6vwx7YE@ep-falling-sea-ahlrmgo8-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


# Create test engine
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

# Create test session factory
test_async_session_maker = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Create test database and provide session.
    Tables are created before each test and dropped after.
    """
    # Create tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Provide session
    async with test_async_session_maker() as session:
        yield session

    # Drop tables
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture(scope="function")
async def test_client(test_db: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test client with database session override.
    """
    async def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
async def test_user(test_db: AsyncSession) -> User:
    """
    Create a test user in the database.
    Returns User object for use in tests.
    """
    user = User(
        email="test@example.com",
        hashed_password=hash_password("testpassword123")
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
async def test_user_token(test_user: User) -> str:
    """
    Create JWT token for test user.
    Returns token string for authorization headers.
    """
    token = create_access_token(
        data={"sub": str(test_user.id), "email": test_user.email}
    )
    return token


@pytest.fixture(scope="function")
async def authenticated_client(
    test_client: AsyncClient,
    test_user_token: str
) -> AsyncClient:
    """
    Create test client with authentication header.
    """
    test_client.headers["Authorization"] = f"Bearer {test_user_token}"
    return test_client
