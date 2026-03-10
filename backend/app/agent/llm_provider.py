"""
LLM Provider Router — Phase III.

Routes agent execution to the correct provider based on the LLM_PROVIDER
environment variable. Switching providers requires no code change.

Supported:
  LLM_PROVIDER=gemini  → gemini_runner.run()   (default / development)
  LLM_PROVIDER=openai  → openai_runner.run()   (evaluation)
"""
import logging
import os

from app.agent import AgentResult

logger = logging.getLogger(__name__)


async def run_agent(
    messages: list[dict],
    user_id: int,
    token: str,
) -> AgentResult:
    """
    Entry point for agent execution.

    Args:
        messages: Conversation history [{role, content}, ...]
        user_id: Authenticated user's ID
        token: Raw JWT — forwarded to MCP tools (never to LLM)

    Returns:
        AgentResult with assistant_message and tool_calls
    """
    provider = os.environ.get("LLM_PROVIDER", "gemini").lower().strip()
    logger.info("LLM provider: %s", provider)

    if provider == "gemini":
        from app.agent import gemini_runner
        return await gemini_runner.run(messages=messages, user_id=user_id, token=token)

    elif provider == "openai":
        from app.agent import openai_runner
        return await openai_runner.run(messages=messages, user_id=user_id, token=token)

    else:
        raise ValueError(
            f"Unknown LLM_PROVIDER='{provider}'. "
            "Supported values: 'gemini', 'openai'."
        )
