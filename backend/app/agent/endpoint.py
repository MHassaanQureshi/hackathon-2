"""
Chat Endpoint — Phase III.

POST /api/{user_id}/chat

Responsibilities (in order):
  1. Validate JWT via get_current_user() dependency
  2. Verify path user_id == token user_id → 403 if mismatch
  3. Create or fetch Conversation from DB
  4. Persist user Message to DB
  5. Load conversation history from DB
  6. Call llm_provider.run_agent() — token forwarded to MCP tools (never to LLM)
  7. Persist assistant Message to DB
  8. Return ChatResponse

No in-memory session storage. Server is stateless.
"""
import logging
import time

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.models.user import User
from app.schemas.agent import ChatRequest, ChatResponse
from app.services import conversation as conversation_service
from app.agent.llm_provider import run_agent
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()
_bearer = HTTPBearer()


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    summary="Send a natural-language message to the AI task assistant",
    tags=["agent"],
)
async def chat(
    user_id: int,
    body: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> ChatResponse:
    """
    Natural-language chat endpoint.
    Validates JWT, persists conversation in DB, routes to LLM provider.
    """
    # Step 1 — JWT validated by get_current_user()

    # Step 2 — Verify path user_id matches authenticated user
    if user_id != current_user.id:
        logger.warning(
            "user_id mismatch: path=%d token=%d", user_id, current_user.id
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden: user_id in path does not match authenticated user",
        )

    token = credentials.credentials  # raw JWT — forwarded to MCP tools only
    selected_provider = settings.LLM_PROVIDER
    logger.info(
        "Chat request: user_id=%d provider=%s conversation_id=%s",
        user_id,
        selected_provider,
        body.conversation_id,
    )
    start_time = time.monotonic()

    # Step 3 — Create or fetch conversation
    try:
        conversation = await conversation_service.get_or_create_conversation(
            db=db,
            user_id=user_id,
            conversation_id=body.conversation_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    # Step 4 — Persist user message
    await conversation_service.add_message(
        db=db,
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=body.message,
    )

    # Step 5 — Load full conversation history (for LLM context window)
    history_msgs = await conversation_service.get_history(
        db=db,
        conversation_id=conversation.id,
    )
    messages = [{"role": m.role, "content": m.content} for m in history_msgs]

    # Step 6 — Run agent (token forwarded to MCP tools — never passed to LLM)
    result = await _run_agent_safe(
        messages=messages,
        user_id=user_id,
        token=token,
    )

    elapsed_ms = int((time.monotonic() - start_time) * 1000)
    logger.info(
        "Agent completed: user_id=%d provider=%s tool_calls=%d elapsed_ms=%d",
        user_id,
        selected_provider,
        len(result.tool_calls),
        elapsed_ms,
    )
    for tc in result.tool_calls:
        logger.info("  Tool: %s(%s)", tc.tool_name, tc.arguments)

    # Step 7 — Persist assistant message
    await conversation_service.add_message(
        db=db,
        conversation_id=conversation.id,
        user_id=user_id,
        role="assistant",
        content=result.assistant_message,
    )

    # Step 8 — Return response
    return ChatResponse(
        conversation_id=conversation.id,
        response=result.assistant_message,
        tool_calls=result.tool_calls,
    )


async def _run_agent_safe(messages: list[dict], user_id: int, token: str):
    """Wrap run_agent with structured error handling."""
    from app.agent import AgentResult
    try:
        return await run_agent(messages=messages, user_id=user_id, token=token)
    except httpx.HTTPStatusError as exc:
        code = exc.response.status_code
        if code == 401:
            msg = "Your session has expired. Please log in again."
        elif code == 404:
            msg = "I couldn't find that task. It may have already been deleted."
        else:
            msg = "Something went wrong while performing that action. Please try again."
        logger.error("MCP tool HTTP %d: %s", code, exc)
        return AgentResult(assistant_message=msg)
    except NotImplementedError as exc:
        logger.error("Provider not implemented: %s", exc)
        return AgentResult(
            assistant_message=f"This provider is not yet configured: {exc}"
        )
    except Exception as exc:
        logger.error("Agent execution error: %s", exc, exc_info=True)
        # Surface LLM/API errors as a readable assistant message rather than HTTP 500
        err_str = str(exc)
        if "PERMISSION_DENIED" in err_str or "leaked" in err_str or "API key" in err_str:
            msg = "The AI service rejected the request due to an invalid or revoked API key. Please contact the administrator."
        elif "quota" in err_str.lower() or "rate" in err_str.lower():
            msg = "The AI service is temporarily unavailable due to rate limits. Please try again in a moment."
        else:
            msg = "Something went wrong while processing your request. Please try again."
        return AgentResult(assistant_message=msg)
