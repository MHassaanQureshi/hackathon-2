"""Task service layer for in-memory task storage and CRUD operations."""

from typing import List, Optional

from todo.models import Task


class TaskService:
    """Manages in-memory task storage and CRUD operations.

    All data is stored in memory during runtime only and is lost when
    the application exits.
    """

    def __init__(self) -> None:
        """Initialize the task service with empty storage."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Create a new task with auto-generated ID.

        Args:
            description: The task description text.

        Returns:
            The newly created Task.
        """
        task = Task(id=self._next_id, description=description.strip())
        self._next_id += 1
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order.

        Returns:
            A copy of the task list to prevent external mutation.
        """
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID.

        Args:
            task_id: The ID of the task to find.

        Returns:
            The Task if found, None otherwise.
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> Optional[Task]:
        """Update a task's description by ID.

        Args:
            task_id: The ID of the task to update.
            new_description: The new description text.

        Returns:
            The updated Task if found, None otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.description = new_description.strip()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete.

        Returns:
            True if the task was deleted, False if not found.
        """
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int, complete: bool = True) -> Optional[Task]:
        """Set task completion status by ID.

        Args:
            task_id: The ID of the task to mark.
            complete: True to mark complete, False to mark incomplete.

        Returns:
            The updated Task if found, None otherwise.
        """
        task = self.get_task_by_id(task_id)
        if task:
            task.is_complete = complete
        return task
