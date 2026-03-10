"""
Tests for POST /api/{user_id}/chat endpoint — Phase III.

Covers:
  (a) 403 when path user_id does not match token
  (b) 401 with no/invalid token
  (c) 200 with valid token and valid message (run_agent mocked)
  (d) New conversation created when conversation_id is null
  (e) Existing conversation loaded when conversation_id provided
"""
import pytest
from unittest.mock import AsyncMock, patch
from httpx import AsyncClient

from app.main import app
from app.agent import AgentResult, ToolCallRecord


@pytest.mark.asyncio
async def test_401_missing_token():
    """No Authorization header → 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post("/api/1/chat", json={"message": "hello"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_401_invalid_token():
    """Malformed token → 401."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        resp = await client.post(
            "/api/1/chat",
            json={"message": "hello"},
            headers={"Authorization": "Bearer not.a.valid.token"},
        )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_403_user_id_mismatch(authenticated_client, test_user):
    """Path user_id differs from token user_id → 403."""
    client, token = authenticated_client
    wrong_id = test_user.id + 999
    resp = await client.post(
        f"/api/{wrong_id}/chat",
        json={"message": "hello"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert resp.status_code == 403
    assert "Forbidden" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_200_valid_request_creates_conversation(authenticated_client, test_user):
    """Valid request with no conversation_id → 200, conversation_id returned."""
    client, token = authenticated_client
    mock_result = AgentResult(
        assistant_message="Task added!",
        tool_calls=[ToolCallRecord(tool_name="add_task", arguments={"title": "Buy milk"})],
    )
    with patch("app.agent.llm_provider.run_agent", new=AsyncMock(return_value=mock_result)):
        resp = await client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add task buy milk"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp.status_code == 200
    data = resp.json()
    assert data["response"] == "Task added!"
    assert isinstance(data["conversation_id"], int)
    assert len(data["tool_calls"]) == 1
    assert data["tool_calls"][0]["tool_name"] == "add_task"


@pytest.mark.asyncio
async def test_200_existing_conversation_loaded(authenticated_client, test_user):
    """Providing an existing conversation_id reuses it."""
    client, token = authenticated_client
    mock_result = AgentResult(assistant_message="Here are your tasks.", tool_calls=[])

    # First request — create conversation
    with patch("app.agent.llm_provider.run_agent", new=AsyncMock(return_value=mock_result)):
        resp1 = await client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "list tasks"},
            headers={"Authorization": f"Bearer {token}"},
        )
    conv_id = resp1.json()["conversation_id"]

    # Second request — reuse conversation
    with patch("app.agent.llm_provider.run_agent", new=AsyncMock(return_value=mock_result)):
        resp2 = await client.post(
            f"/api/{test_user.id}/chat",
            json={"conversation_id": conv_id, "message": "what about pending ones?"},
            headers={"Authorization": f"Bearer {token}"},
        )
    assert resp2.status_code == 200
    assert resp2.json()["conversation_id"] == conv_id
