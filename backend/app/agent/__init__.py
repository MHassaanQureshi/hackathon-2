"""
Agent package — Phase III AI-Powered Conversational Task Interface.

Shared types used by all LLM runners and the chat endpoint.
"""
from dataclasses import dataclass, field
from pydantic import BaseModel


class ToolCallRecord(BaseModel):
    """A single MCP tool invocation — included in ChatResponse for observability."""
    tool_name: str
    arguments: dict


@dataclass
class AgentResult:
    """
    Standardized return type from any LLM runner (Gemini or OpenAI).
    Both gemini_runner.run() and openai_runner.run() MUST return this type.
    """
    assistant_message: str
    tool_calls: list[ToolCallRecord] = field(default_factory=list)
