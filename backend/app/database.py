"""
Database configuration and session management.
Uses SQLModel with async PostgreSQL (asyncpg driver).
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.config import settings


# Create async engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True
)

# Create async session factory
async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency that provides async database session.
    Yields session and ensures it's closed after use.
    """
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables():
    """
    Create all database tables.
    Called on application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """
    Close database engine.
    Called on application shutdown.
    """
    await engine.dispose()
