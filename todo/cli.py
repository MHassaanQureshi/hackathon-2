"""Console interface and menu system for the Todo CLI application."""

from typing import Optional

from todo.service import TaskService


class TodoCLI:
    """Console-based menu interface for task management."""

    def __init__(self, service: TaskService) -> None:
        """Initialize the CLI with a task service.

        Args:
            service: The TaskService instance for task operations.
        """
        self._service = service

    def run(self) -> None:
        """Run the main application loop."""
        while True:
            self._display_menu()
            choice = self._get_input("Enter choice: ").strip()
            self._handle_choice(choice)

    def _display_menu(self) -> None:
        """Print the main menu."""
        print("\n=== Todo Menu ===")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Update Task")
        print("4. Delete Task")
        print("5. Mark Complete")
        print("6. Mark Incomplete")
        print("7. Exit")

    def _get_input(self, prompt: str) -> str:
        """Get user input with prompt.

        Args:
            prompt: The prompt string to display.

        Returns:
            The user's input string.
        """
        return input(prompt)

    def _handle_choice(self, choice: str) -> None:
        """Route user choice to appropriate handler.

        Args:
            choice: The menu choice entered by the user.
        """
        handlers = {
            "1": self._add_task,
            "2": self._view_tasks,
            "3": self._update_task,
            "4": self._delete_task,
            "5": lambda: self._mark_complete(True),
            "6": lambda: self._mark_complete(False),
        }
        if choice == "7":
            print("Goodbye!")
            exit(0)
        handler = handlers.get(choice)
        if handler:
            handler()
        else:
            print("Invalid choice. Please try again.")

    def _get_valid_task_id(self, prompt: str) -> Optional[int]:
        """Get and validate a task ID from user input.

        Args:
            prompt: The prompt string to display.

        Returns:
            The validated task ID, or None if invalid.
        """
        try:
            task_id = int(self._get_input(prompt))
            if task_id < 1:
                print("Error: Task ID must be a positive integer.")
                return None
            return task_id
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return None

    def _add_task(self) -> None:
        """Add a new task."""
        description = self._get_input("Enter task description: ").strip()
        if not description:
            print("Error: Task description cannot be empty.")
            return
        task = self._service.add_task(description)
        print(f"Task added: [{task.id}] {task.description}")

    def _view_tasks(self) -> None:
        """Display all tasks."""
        tasks = self._service.get_all_tasks()
        if not tasks:
            print("No tasks yet. Add one!")
            return
        print("\nTasks:")
        for task in tasks:
            status = "[X]" if task.is_complete else "[ ]"
            print(f"{status} [{task.id}] {task.description}")

    def _update_task(self) -> None:
        """Update an existing task."""
        task_id = self._get_valid_task_id("Enter task ID to update: ")
        if task_id is None:
            return
        new_description = self._get_input("Enter new description: ").strip()
        if not new_description:
            print("Error: Task description cannot be empty.")
            return
        task = self._service.update_task(task_id, new_description)
        if task:
            print(f"Task {task_id} updated.")
        else:
            print(f"Error: Task {task_id} not found.")

    def _delete_task(self) -> None:
        """Delete a task."""
        task_id = self._get_valid_task_id("Enter task ID to delete: ")
        if task_id is None:
            return
        if self._service.delete_task(task_id):
            print(f"Task {task_id} deleted.")
        else:
            print(f"Error: Task {task_id} not found.")

    def _mark_complete(self, complete: bool) -> None:
        """Mark a task as complete or incomplete.

        Args:
            complete: True to mark complete, False to mark incomplete.
        """
        task_id = self._get_valid_task_id(
            "Enter task ID to mark complete: " if complete
            else "Enter task ID to mark incomplete: "
        )
        if task_id is None:
            return
        action = "complete" if complete else "incomplete"
        task = self._service.mark_complete(task_id, complete)
        if task:
            print(f"Task {task_id} marked as {action}.")
        else:
            print(f"Error: Task {task_id} not found.")
