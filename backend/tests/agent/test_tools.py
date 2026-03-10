"""
Tests for MCP tool functions — Phase III.

Covers:
  (a) add_task returns correct structure on 201
  (b) list_tasks returns array on 200
  (c) complete_task returns updated completed flag
  (d) delete_task returns {deleted: true}
  (e) add_task rejects title >100 chars without calling REST
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
import httpx

from app.agent.mcp import tools


FAKE_TOKEN = "fake.jwt.token"
FAKE_USER_ID = 1


@pytest.mark.asyncio
async def test_add_task_success():
    """add_task returns {success, task_id, title} on 201."""
    mock_resp = MagicMock()
    mock_resp.status_code = 201
    mock_resp.json.return_value = {"id": 42, "title": "Buy milk", "completed": False}
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_resp)

    with patch("app.agent.mcp.tools.httpx.AsyncClient", return_value=mock_client):
        result = await tools.add_task(
            user_id=FAKE_USER_ID, title="Buy milk", token=FAKE_TOKEN
        )

    assert result["success"] is True
    assert result["task_id"] == 42
    assert result["title"] == "Buy milk"


@pytest.mark.asyncio
async def test_add_task_title_too_long():
    """add_task rejects title >100 chars without calling REST API."""
    long_title = "A" * 101
    with patch("app.agent.mcp.tools.httpx.AsyncClient") as mock_cls:
        result = await tools.add_task(
            user_id=FAKE_USER_ID, title=long_title, token=FAKE_TOKEN
        )
    # httpx.AsyncClient should NOT have been instantiated
    mock_cls.assert_not_called()
    assert result["success"] is False
    assert "100" in result["error"]


@pytest.mark.asyncio
async def test_list_tasks_returns_array():
    """list_tasks returns {tasks: [...], count: N}."""
    task_list = [
        {"id": 1, "title": "Task A", "completed": False},
        {"id": 2, "title": "Task B", "completed": True},
    ]
    mock_resp = MagicMock()
    mock_resp.json.return_value = task_list
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.get = AsyncMock(return_value=mock_resp)

    with patch("app.agent.mcp.tools.httpx.AsyncClient", return_value=mock_client):
        result = await tools.list_tasks(user_id=FAKE_USER_ID, token=FAKE_TOKEN)

    assert result["count"] == 2
    assert len(result["tasks"]) == 2


@pytest.mark.asyncio
async def test_complete_task_returns_completed_flag():
    """complete_task returns {task_id, completed, title}."""
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"id": 5, "title": "Dentist", "completed": True}
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.post = AsyncMock(return_value=mock_resp)

    with patch("app.agent.mcp.tools.httpx.AsyncClient", return_value=mock_client):
        result = await tools.complete_task(
            user_id=FAKE_USER_ID, task_id=5, token=FAKE_TOKEN
        )

    assert result["completed"] is True
    assert result["task_id"] == 5
    assert result["title"] == "Dentist"


@pytest.mark.asyncio
async def test_delete_task_returns_deleted_true():
    """delete_task returns {deleted: True, task_id}."""
    mock_resp = MagicMock()
    mock_resp.raise_for_status = MagicMock()

    mock_client = AsyncMock()
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=False)
    mock_client.delete = AsyncMock(return_value=mock_resp)

    with patch("app.agent.mcp.tools.httpx.AsyncClient", return_value=mock_client):
        result = await tools.delete_task(
            user_id=FAKE_USER_ID, task_id=7, token=FAKE_TOKEN
        )

    assert result["deleted"] is True
    assert result["task_id"] == 7
