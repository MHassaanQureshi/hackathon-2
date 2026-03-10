"""
Conversation and Message models.
Phase III — AI-Powered Conversational Task Interface.

Tables:
  conversations — groups messages per user session
  messages      — individual chat turns (user + assistant)
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class Conversation(SQLModel, table=True):
    """
    Represents a single chat session for a user.

    Attributes:
        id: Primary key
        user_id: FK → users.id — all queries filtered by this
        created_at: Timestamp of first message
        updated_at: Timestamp of last message
        messages: Relationship to messages in this conversation
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: List["Message"] = Relationship(back_populates="conversation")


class Message(SQLModel, table=True):
    """
    Represents one chat turn (user or assistant message).

    Attributes:
        id: Primary key
        conversation_id: FK → conversations.id
        user_id: FK → users.id (redundant FK for fast user-scoped queries)
        role: "user" or "assistant"
        content: Full message text (max 8000 chars)
        created_at: Timestamp — used to reconstruct ordered history
        conversation: Relationship to parent conversation
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    role: str = Field(max_length=16)  # "user" or "assistant"
    content: str = Field(max_length=8000)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: Optional[Conversation] = Relationship(back_populates="messages")
