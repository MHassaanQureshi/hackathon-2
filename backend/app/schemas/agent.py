"""
Pydantic schemas for the Phase III chat endpoint.
"""
from typing import Optional
from pydantic import BaseModel, Field

from app.agent import ToolCallRecord


class ChatRequest(BaseModel):
    """Request body for POST /api/{user_id}/chat."""
    conversation_id: Optional[int] = Field(
        default=None,
        description="Existing conversation ID. Omit to start a new conversation.",
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Raw natural-language user input.",
    )


class ChatResponse(BaseModel):
    """Response body from POST /api/{user_id}/chat."""
    conversation_id: int = Field(
        description="ID of the conversation (new or existing).",
    )
    response: str = Field(
        description="Agent's natural-language reply.",
    )
    tool_calls: list[ToolCallRecord] = Field(
        default_factory=list,
        description="All MCP tool calls made during this turn.",
    )
