"""
Gemini Agent Runner — Phase III.

Implements the agentic loop using google-genai with native function calling.
Supports all 5 MCP tools: add_task, list_tasks, complete_task, update_task, delete_task.

Called by llm_provider.py when LLM_PROVIDER=gemini.
Returns AgentResult (standardized — provider-agnostic).
"""
import json
import logging
from typing import Any

from google import genai
from google.genai import types

from app.agent import AgentResult, ToolCallRecord
from app.agent.mcp import tools
from app.config import settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# System prompt — defines agent behaviour and all tool usage rules
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are a helpful task management assistant. You help users manage their todo tasks through natural conversation.

You have access to five tools:
- add_task: Create a new task. Use when user wants to add, create, or remind themselves of something.
- list_tasks: Retrieve all the user's tasks. Use when user asks to see, show, or list their tasks.
- complete_task: Toggle a task's completion status. Use when user says "mark done", "complete", "finish", or "unmark".
- update_task: Update a task's title or description. Use when user wants to rename, change, or edit a task.
- delete_task: Permanently delete a task. IMPORTANT: Always ask for explicit confirmation before calling this tool.

Rules you MUST follow:
1. Never hallucinate task IDs. If you don't know the task ID, call list_tasks first to look it up by title.
2. If multiple tasks match a name the user mentions, list the candidates and ask which one they mean.
3. Always ask "Are you sure you want to delete '[task title]'?" before calling delete_task.
4. If the API returns an authentication error (401), tell the user their session has expired and to log in again.
5. If the user asks about something unrelated to task management (weather, news, etc.), politely decline and explain you only help with tasks.
6. If a task title would exceed 100 characters, tell the user and ask for a shorter title.
7. Always confirm actions in a friendly, conversational tone.
8. When listing tasks, format them clearly — e.g., numbered list with completion status.
9. If there are no tasks, say so conversationally and offer to add one.
"""

# ---------------------------------------------------------------------------
# Tool function declarations for Gemini
# ---------------------------------------------------------------------------

TOOL_DECLARATIONS = [
    types.FunctionDeclaration(
        name="add_task",
        description="Create a new task for the user.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "title": types.Schema(
                    type=types.Type.STRING,
                    description="The task title (required, max 100 characters).",
                ),
                "description": types.Schema(
                    type=types.Type.STRING,
                    description="Optional task description (max 500 characters).",
                ),
            },
            required=["title"],
        ),
    ),
    types.FunctionDeclaration(
        name="list_tasks",
        description="Retrieve all tasks belonging to the authenticated user.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={},
        ),
    ),
    types.FunctionDeclaration(
        name="complete_task",
        description="Toggle the completion status of a task (mark done or undone).",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "task_id": types.Schema(
                    type=types.Type.INTEGER,
                    description="The numeric ID of the task to toggle.",
                ),
            },
            required=["task_id"],
        ),
    ),
    types.FunctionDeclaration(
        name="update_task",
        description="Update the title and/or description of an existing task.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "task_id": types.Schema(
                    type=types.Type.INTEGER,
                    description="The numeric ID of the task to update.",
                ),
                "title": types.Schema(
                    type=types.Type.STRING,
                    description="New title (max 100 characters). Omit to keep existing.",
                ),
                "description": types.Schema(
                    type=types.Type.STRING,
                    description="New description (max 500 characters). Omit to keep existing.",
                ),
            },
            required=["task_id"],
        ),
    ),
    types.FunctionDeclaration(
        name="delete_task",
        description="Permanently delete a task. Only call after explicit user confirmation.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "task_id": types.Schema(
                    type=types.Type.INTEGER,
                    description="The numeric ID of the task to delete.",
                ),
            },
            required=["task_id"],
        ),
    ),
]

# ---------------------------------------------------------------------------
# Tool dispatcher — maps tool name → MCP tool function
# ---------------------------------------------------------------------------

async def _dispatch_tool(
    tool_name: str,
    tool_args: dict,
    user_id: int,
    token: str,
) -> Any:
    """Call the appropriate MCP tool and return its result."""
    if tool_name == "add_task":
        return await tools.add_task(
            user_id=user_id,
            title=tool_args["title"],
            description=tool_args.get("description"),
            token=token,
        )
    elif tool_name == "list_tasks":
        return await tools.list_tasks(user_id=user_id, token=token)
    elif tool_name == "complete_task":
        return await tools.complete_task(
            user_id=user_id,
            task_id=int(tool_args["task_id"]),
            token=token,
        )
    elif tool_name == "update_task":
        return await tools.update_task(
            user_id=user_id,
            task_id=int(tool_args["task_id"]),
            title=tool_args.get("title"),
            description=tool_args.get("description"),
            token=token,
        )
    elif tool_name == "delete_task":
        return await tools.delete_task(
            user_id=user_id,
            task_id=int(tool_args["task_id"]),
            token=token,
        )
    else:
        return {"error": f"Unknown tool: {tool_name}"}


# ---------------------------------------------------------------------------
# Main runner
# ---------------------------------------------------------------------------

async def run(
    messages: list[dict],
    user_id: int,
    token: str,
) -> AgentResult:
    """
    Run the Gemini agentic loop.

    Args:
        messages: Conversation history [{role, content}, ...]
        user_id: Authenticated user's ID
        token: Raw JWT token — forwarded to MCP tools

    Returns:
        AgentResult with assistant_message and tool_calls made
    """
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    gemini_tools = [types.Tool(function_declarations=TOOL_DECLARATIONS)]
    tool_calls_made: list[ToolCallRecord] = []

    # Build Gemini contents from conversation history
    contents: list[types.Content] = []
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part(text=msg["content"])],
            )
        )

    # Agentic loop — runs until Gemini produces a text response with no function calls
    max_iterations = 10  # safety limit to prevent infinite loops
    iteration = 0

    while iteration < max_iterations:
        iteration += 1
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=gemini_tools,
                temperature=0,
            ),
        )

        candidate = response.candidates[0]
        parts = candidate.content.parts

        # Collect function calls from this response
        function_call_parts = [p for p in parts if p.function_call is not None]
        text_parts = [p for p in parts if p.text is not None and p.text.strip()]

        if not function_call_parts:
            # No tool calls — final text response
            final_text = " ".join(p.text for p in text_parts) if text_parts else ""
            logger.info(
                "Gemini loop complete after %d iteration(s), %d tool call(s)",
                iteration,
                len(tool_calls_made),
            )
            return AgentResult(
                assistant_message=final_text,
                tool_calls=tool_calls_made,
            )

        # Append model's turn to contents
        contents.append(candidate.content)

        # Execute each function call and collect results
        function_response_parts: list[types.Part] = []
        for part in function_call_parts:
            fc = part.function_call
            tool_name = fc.name
            tool_args = dict(fc.args) if fc.args else {}

            logger.info("Tool call: %s(%s)", tool_name, tool_args)
            tool_calls_made.append(
                ToolCallRecord(tool_name=tool_name, arguments=tool_args)
            )

            try:
                result = await _dispatch_tool(tool_name, tool_args, user_id, token)
            except Exception as exc:
                logger.error("Tool %s failed: %s", tool_name, exc)
                result = {"error": str(exc)}

            function_response_parts.append(
                types.Part(
                    function_response=types.FunctionResponse(
                        name=tool_name,
                        response={"result": json.dumps(result)},
                    )
                )
            )

        # Append tool results as a user turn so Gemini can respond
        contents.append(
            types.Content(role="user", parts=function_response_parts)
        )

    # Safety fallback if max iterations reached
    logger.warning("Gemini loop hit max_iterations=%d", max_iterations)
    return AgentResult(
        assistant_message="I wasn't able to complete that request. Please try again.",
        tool_calls=tool_calls_made,
    )
