"""
MCP Tool Layer — Phase III.

Five async tools that call Phase II REST endpoints via httpx.
Each tool is stateless, requires a JWT token, and returns structured JSON.
LLM never accesses the database directly — all operations go through these tools.

Stubs for: list_tasks, complete_task, delete_task, update_task
(Implemented progressively per user story phase)
"""
import httpx
from typing import Optional

from app.config import settings


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def _base_url() -> str:
    return settings.PHASE2_API_BASE_URL


# ---------------------------------------------------------------------------
# add_task — T013 (US1)
# ---------------------------------------------------------------------------

async def add_task(
    user_id: int,
    title: str,
    token: str,
    description: Optional[str] = None,
) -> dict:
    """
    Create a new task for the authenticated user.
    Calls: POST /api/v1/tasks

    Returns: {task_id, title, success: true}
    """
    # Title length validation (FR-011)
    if len(title) > 100:
        return {"success": False, "error": "Title exceeds 100 character limit. Please provide a shorter title."}

    payload: dict = {"title": title}
    if description:
        if len(description) > 500:
            return {"success": False, "error": "Description exceeds 500 character limit. Please provide a shorter description."}
        payload["description"] = description

    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{_base_url()}/tasks",
            json=payload,
            headers=_auth_headers(token),
            timeout=10.0,
        )
        resp.raise_for_status()
        task = resp.json()
        return {"success": True, "task_id": task.get("id"), "title": task.get("title")}


# ---------------------------------------------------------------------------
# list_tasks — T019 (US2)
# ---------------------------------------------------------------------------

async def list_tasks(user_id: int, token: str) -> dict:
    """
    Retrieve all tasks for the authenticated user.
    Calls: GET /api/v1/tasks

    Returns: {tasks: [...], count: int}
    """
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{_base_url()}/tasks",
            headers=_auth_headers(token),
            timeout=10.0,
        )
        resp.raise_for_status()
        tasks = resp.json()
        return {"tasks": tasks, "count": len(tasks)}


# ---------------------------------------------------------------------------
# complete_task — T022 (US3)
# ---------------------------------------------------------------------------

async def complete_task(user_id: int, task_id: int, token: str) -> dict:
    """
    Toggle the completion status of a task.
    Calls: POST /api/v1/tasks/{task_id}/toggle

    Returns: {task_id, completed, title}
    """
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{_base_url()}/tasks/{task_id}/toggle",
            headers=_auth_headers(token),
            timeout=10.0,
        )
        resp.raise_for_status()
        task = resp.json()
        return {
            "task_id": task.get("id"),
            "completed": task.get("completed"),
            "title": task.get("title"),
        }


# ---------------------------------------------------------------------------
# delete_task — T028 (US5)
# ---------------------------------------------------------------------------

async def delete_task(user_id: int, task_id: int, token: str) -> dict:
    """
    Delete a task permanently.
    Calls: DELETE /api/v1/tasks/{task_id}

    Returns: {deleted: true, task_id}
    """
    async with httpx.AsyncClient() as client:
        resp = await client.delete(
            f"{_base_url()}/tasks/{task_id}",
            headers=_auth_headers(token),
            timeout=10.0,
        )
        resp.raise_for_status()
        return {"deleted": True, "task_id": task_id}


# ---------------------------------------------------------------------------
# update_task — T025 (US4)
# ---------------------------------------------------------------------------

async def update_task(
    user_id: int,
    task_id: int,
    token: str,
    title: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """
    Update the title and/or description of a task.
    Calls: PATCH /api/v1/tasks/{task_id}

    Returns: updated task object
    """
    if title is not None and len(title) > 100:
        return {"success": False, "error": "Title exceeds 100 character limit. Please provide a shorter title."}
    if description is not None and len(description) > 500:
        return {"success": False, "error": "Description exceeds 500 character limit."}

    payload: dict = {}
    if title is not None:
        payload["title"] = title
    if description is not None:
        payload["description"] = description

    async with httpx.AsyncClient() as client:
        resp = await client.patch(
            f"{_base_url()}/tasks/{task_id}",
            json=payload,
            headers=_auth_headers(token),
            timeout=10.0,
        )
        resp.raise_for_status()
        return resp.json()
