"""
Conversation service.
CRUD operations for Conversation and Message persistence.
All queries are scoped to user_id — no cross-user access possible.
"""
from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.conversation import Conversation, Message


async def get_or_create_conversation(
    db: AsyncSession,
    user_id: int,
    conversation_id: Optional[int] = None,
) -> Conversation:
    """
    Return an existing conversation if conversation_id is provided and
    belongs to user_id; otherwise create a new one.

    Raises ValueError if conversation_id is provided but not found / not owned.
    """
    if conversation_id is not None:
        result = await db.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id,
            )
        )
        conv = result.scalar_one_or_none()
        if conv is None:
            raise ValueError(
                f"Conversation {conversation_id} not found for user {user_id}"
            )
        # Touch updated_at
        conv.updated_at = datetime.utcnow()
        db.add(conv)
        await db.commit()
        await db.refresh(conv)
        return conv

    # Create new conversation
    conv = Conversation(user_id=user_id)
    db.add(conv)
    await db.commit()
    await db.refresh(conv)
    return conv


async def add_message(
    db: AsyncSession,
    conversation_id: int,
    user_id: int,
    role: str,
    content: str,
) -> Message:
    """
    Persist a single message to the messages table.

    Args:
        db: Async DB session
        conversation_id: Parent conversation id
        user_id: Owner user id
        role: "user" or "assistant"
        content: Full message text
    """
    msg = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
    )
    db.add(msg)
    await db.commit()
    await db.refresh(msg)
    return msg


async def get_history(
    db: AsyncSession,
    conversation_id: int,
) -> list[Message]:
    """
    Return all messages for a conversation ordered by created_at ascending.
    Used to rebuild context window for each LLM call.
    """
    result = await db.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    )
    return list(result.scalars().all())
