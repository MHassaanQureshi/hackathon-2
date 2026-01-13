"""
User model.
SQLModel class representing users table.
"""
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    """
    User model for authentication and task ownership.

    Attributes:
        id: Primary key
        email: Unique email address (indexed)
        hashed_password: Bcrypt hashed password (never store plaintext)
        created_at: Timestamp of user creation
        updated_at: Timestamp of last update
        tasks: Relationship to user's tasks (one-to-many)
    """
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    hashed_password: str = Field(max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks (will be defined after Task model is created)
    tasks: List["Task"] = Relationship(back_populates="user", cascade_delete=True)
