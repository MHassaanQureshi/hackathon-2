"""
Task model.
SQLModel class representing tasks table.
"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Task(SQLModel, table=True):
    """
    Task model for user todo items.

    Attributes:
        id: Primary key
        user_id: Foreign key to users table (owner)
        title: Task title (required, max 100 characters)
        description: Task description (optional, max 500 characters)
        completed: Task completion status (default False)
        created_at: Timestamp of task creation
        updated_at: Timestamp of last update
        user: Relationship to owner user (many-to-one)
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=100)
    description: Optional[str] = Field(default=None, max_length=500)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="tasks")
