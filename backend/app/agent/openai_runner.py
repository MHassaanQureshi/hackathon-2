"""
OpenAI Agent Runner — Phase III (Stub).

Placeholder for OpenAI Agents SDK integration (evaluation mode).
Enable by setting LLM_PROVIDER=openai in environment.

Full implementation deferred — requires:
  - OPENAI_API_KEY configured
  - openai-agents SDK integration
  - MCP tool bridge for OpenAI function calling format

Returns AgentResult (same contract as gemini_runner).
"""
import logging

from app.agent import AgentResult

logger = logging.getLogger(__name__)


async def run(
    messages: list[dict],
    user_id: int,
    token: str,
) -> AgentResult:
    """
    OpenAI Agents SDK runner — not yet implemented.

    To activate:
      1. Set OPENAI_API_KEY in .env
      2. Implement this function using the openai-agents SDK
      3. Map TOOL_DECLARATIONS to OpenAI function schemas
      4. Bridge tool calls to app.agent.mcp.tools functions

    Raises NotImplementedError until implementation is complete.
    """
    logger.warning(
        "OpenAI runner called but not yet implemented. "
        "Set LLM_PROVIDER=gemini for the working provider."
    )
    raise NotImplementedError(
        "OpenAI provider is not yet configured. "
        "Set OPENAI_API_KEY, implement openai_runner.run(), "
        "then switch LLM_PROVIDER=openai."
    )
