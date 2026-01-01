"""Task data model for the Todo CLI application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo task.

    Attributes:
        id: Unique identifier for the task (must be positive integer).
        description: Text description of the task (must be non-empty).
        is_complete: Whether the task has been completed (defaults to False).
    """

    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self) -> None:
        """Validate task after initialization."""
        if self.id < 1:
            raise ValueError("Task ID must be a positive integer")
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty or whitespace-only")
