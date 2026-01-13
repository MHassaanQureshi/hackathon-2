"""
Task service.
Business logic for task CRUD operations with user isolation.
"""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException, status

from app.models.task import Task


async def create_task(
    db: AsyncSession,
    user_id: int,
    title: str,
    description: Optional[str] = None
) -> Task:
    """
    Create a new task for a user.

    Args:
        db: Database session
        user_id: ID of the user creating the task
        title: Task title
        description: Optional task description

    Returns:
        Created Task object
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description
    )

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def get_user_tasks(
    db: AsyncSession,
    user_id: int
) -> List[Task]:
    """
    Retrieve all tasks for a user.
    Tasks are sorted by creation date (newest first).

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        List of Task objects belonging to the user
    """
    result = await db.execute(
        select(Task)
        .where(Task.user_id == user_id)
        .order_by(Task.created_at.desc())
    )
    tasks = result.scalars().all()
    return list(tasks)


async def get_task_by_id(
    db: AsyncSession,
    task_id: int,
    user_id: int
) -> Optional[Task]:
    """
    Get a specific task by ID with ownership validation.

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the user (for ownership check)

    Returns:
        Task object if found and owned by user, None otherwise
    """
    result = await db.execute(
        select(Task)
        .where(Task.id == task_id, Task.user_id == user_id)
    )
    task = result.scalar_one_or_none()
    return task


async def update_task(
    db: AsyncSession,
    task_id: int,
    user_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    completed: Optional[bool] = None
) -> Task:
    """
    Update a task with ownership validation.

    Args:
        db: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for ownership check)
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)

    Returns:
        Updated Task object

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    task = await get_task_by_id(db, task_id, user_id)

    if task is None:
        # Check if task exists but belongs to another user
        result = await db.execute(select(Task).where(Task.id == task_id))
        existing_task = result.scalar_one_or_none()

        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this task"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    # Update fields if provided
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed

    task.updated_at = datetime.utcnow()

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task


async def delete_task(
    db: AsyncSession,
    task_id: int,
    user_id: int
) -> None:
    """
    Delete a task with ownership validation.

    Args:
        db: Database session
        task_id: ID of the task to delete
        user_id: ID of the user (for ownership check)

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    task = await get_task_by_id(db, task_id, user_id)

    if task is None:
        # Check if task exists but belongs to another user
        result = await db.execute(select(Task).where(Task.id == task_id))
        existing_task = result.scalar_one_or_none()

        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to delete this task"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    await db.delete(task)
    await db.commit()


async def toggle_task_completion(
    db: AsyncSession,
    task_id: int,
    user_id: int
) -> Task:
    """
    Toggle task completion status.

    Args:
        db: Database session
        task_id: ID of the task
        user_id: ID of the user (for ownership check)

    Returns:
        Updated Task object with toggled completion status

    Raises:
        HTTPException: 404 if task not found, 403 if not owned by user
    """
    task = await get_task_by_id(db, task_id, user_id)

    if task is None:
        # Check if task exists but belongs to another user
        result = await db.execute(select(Task).where(Task.id == task_id))
        existing_task = result.scalar_one_or_none()

        if existing_task:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not authorized to modify this task"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

    # Toggle completion
    task.completed = not task.completed
    task.updated_at = datetime.utcnow()

    db.add(task)
    await db.commit()
    await db.refresh(task)

    return task
