"""
Task schemas.
Pydantic models for task request/response validation.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    """
    Task creation request.

    Attributes:
        title: Task title (required, max 100 characters)
        description: Task description (optional, max 500 characters)
    """
    title: str = Field(..., min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")


class TaskUpdate(BaseModel):
    """
    Task update request.
    All fields are optional.

    Attributes:
        title: New task title (optional, max 100 characters)
        description: New task description (optional, max 500 characters)
        completed: New completion status (optional)
    """
    title: Optional[str] = Field(None, min_length=1, max_length=100, description="Task title")
    description: Optional[str] = Field(None, max_length=500, description="Task description")
    completed: Optional[bool] = Field(None, description="Completion status")


class TaskResponse(BaseModel):
    """
    Task response model.

    Attributes:
        id: Task ID
        user_id: Owner user ID
        title: Task title
        description: Task description (can be null)
        completed: Completion status
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    id: int
    user_id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
