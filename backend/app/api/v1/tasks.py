"""
Task API endpoints.
Handles task CRUD operations with user authentication.
"""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task as task_service


router = APIRouter()


@router.get("", response_model=List[TaskResponse])
async def get_tasks(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> List[TaskResponse]:
    """
    Get all tasks for the authenticated user.
    Tasks are sorted by creation date (newest first).

    Args:
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        List of user's tasks
    """
    tasks = await task_service.get_user_tasks(db, current_user.id)
    return tasks


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Create a new task for the authenticated user.

    Args:
        request: Task creation data (title, description)
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Created task

    Raises:
        HTTPException: 400 if validation fails
    """
    task = await task_service.create_task(
        db,
        user_id=current_user.id,
        title=request.title,
        description=request.description
    )
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    request: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Update a task.
    Only the task owner can update their tasks.

    Args:
        task_id: ID of the task to update
        request: Task update data (title, description, completed)
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Updated task

    Raises:
        HTTPException: 400 if validation fails
        HTTPException: 403 if task belongs to another user
        HTTPException: 404 if task not found
    """
    task = await task_service.update_task(
        db,
        task_id=task_id,
        user_id=current_user.id,
        title=request.title,
        description=request.description,
        completed=request.completed
    )
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete a task.
    Only the task owner can delete their tasks.

    Args:
        task_id: ID of the task to delete
        current_user: Authenticated user from JWT token
        db: Database session

    Raises:
        HTTPException: 403 if task belongs to another user
        HTTPException: 404 if task not found
    """
    await task_service.delete_task(db, task_id=task_id, user_id=current_user.id)


@router.post("/{task_id}/toggle", response_model=TaskResponse)
async def toggle_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> TaskResponse:
    """
    Toggle task completion status.
    Only the task owner can toggle their tasks.

    Args:
        task_id: ID of the task to toggle
        current_user: Authenticated user from JWT token
        db: Database session

    Returns:
        Task with toggled completion status

    Raises:
        HTTPException: 403 if task belongs to another user
        HTTPException: 404 if task not found
    """
    task = await task_service.toggle_task_completion(
        db,
        task_id=task_id,
        user_id=current_user.id
    )
    return task
