"""Integration tests for the TodoCLI class."""

import pytest
from io import StringIO
from unittest.mock import patch

from todo.cli import TodoCLI
from todo.service import TaskService


class TestTodoCLIInitialization:
    """Tests for TodoCLI initialization."""

    def test_initialization_with_service(self) -> None:
        """Test that CLI can be initialized with a service."""
        service = TaskService()
        cli = TodoCLI(service)
        assert cli._service is service


class TestMenuDisplay:
    """Tests for menu display."""

    @patch("builtins.print")
    def test_display_menu_shows_all_options(self, mock_print: patch) -> None:
        """Test that menu displays all 7 options."""
        service = TaskService()
        cli = TodoCLI(service)
        cli._display_menu()

        # Check that menu header was printed
        calls = [str(call) for call in mock_print.call_args_list]
        menu_output = "".join(calls)

        assert "=== Todo Menu ===" in menu_output
        assert "1. Add Task" in menu_output
        assert "2. View Tasks" in menu_output
        assert "3. Update Task" in menu_output
        assert "4. Delete Task" in menu_output
        assert "5. Mark Complete" in menu_output
        assert "6. Mark Incomplete" in menu_output
        assert "7. Exit" in menu_output


class TestGetValidTaskId:
    """Tests for _get_valid_task_id method."""

    def test_accepts_valid_positive_id(self) -> None:
        """Test that valid positive ID is accepted."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="5"):
            result = cli._get_valid_task_id("Enter ID: ")
        assert result == 5

    def test_rejects_non_numeric_input(self) -> None:
        """Test that non-numeric input is rejected."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="abc"):
            with patch("builtins.print") as mock_print:
                result = cli._get_valid_task_id("Enter ID: ")
        assert result is None
        mock_print.assert_called_with("Error: Invalid task ID. Please enter a number.")

    def test_rejects_zero(self) -> None:
        """Test that zero ID is rejected."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="0"):
            with patch("builtins.print") as mock_print:
                result = cli._get_valid_task_id("Enter ID: ")
        assert result is None
        mock_print.assert_called_with("Error: Task ID must be a positive integer.")

    def test_rejects_negative_number(self) -> None:
        """Test that negative ID is rejected."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="-1"):
            with patch("builtins.print") as mock_print:
                result = cli._get_valid_task_id("Enter ID: ")
        assert result is None
        mock_print.assert_called_with("Error: Task ID must be a positive integer.")


class TestAddTask:
    """Tests for _add_task method."""

    def test_add_task_success(self) -> None:
        """Test successful task addition."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="Buy groceries"):
            with patch("builtins.print") as mock_print:
                cli._add_task()

        # Verify task was added
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Buy groceries"
        # Verify success message
        mock_print.assert_called_with("Task added: [1] Buy groceries")

    def test_add_task_empty_description_shows_error(self) -> None:
        """Test that empty description shows error message."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value=""):
            with patch("builtins.print") as mock_print:
                cli._add_task()

        # Verify no task was added
        assert len(service.get_all_tasks()) == 0
        # Verify error message
        mock_print.assert_called_with("Error: Task description cannot be empty.")

    def test_add_task_whitespace_only_description_shows_error(self) -> None:
        """Test that whitespace-only description shows error."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_input", return_value="   "):
            with patch("builtins.print") as mock_print:
                cli._add_task()

        assert len(service.get_all_tasks()) == 0
        mock_print.assert_called_with("Error: Task description cannot be empty.")


class TestViewTasks:
    """Tests for _view_tasks method."""

    def test_view_empty_list_shows_message(self) -> None:
        """Test that empty list shows appropriate message."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch("builtins.print") as mock_print:
            cli._view_tasks()

        mock_print.assert_called_with("No tasks yet. Add one!")

    def test_view_tasks_shows_all_tasks(self) -> None:
        """Test that viewing tasks shows all tasks with status."""
        service = TaskService()
        cli = TodoCLI(service)

        # Add some tasks
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.mark_complete(1, True)

        with patch("builtins.print") as mock_print:
            cli._view_tasks()

        # Check that tasks are printed
        calls = [str(call) for call in mock_print.call_args_list]
        output = "".join(calls)

        assert "Task 1" in output
        assert "Task 2" in output
        assert "[X]" in output  # Completed task
        assert "[ ]" in output  # Incomplete task


class TestUpdateTask:
    """Tests for _update_task method."""

    def test_update_task_success(self) -> None:
        """Test successful task update."""
        service = TaskService()
        cli = TodoCLI(service)

        service.add_task("Original")

        with patch.object(cli, "_get_valid_task_id", return_value=1):
            with patch.object(cli, "_get_input", return_value="Updated"):
                with patch("builtins.print") as mock_print:
                    cli._update_task()

        task = service.get_task_by_id(1)
        assert task is not None
        assert task.description == "Updated"
        mock_print.assert_called_with("Task 1 updated.")

    def test_update_nonexistent_task_shows_error(self) -> None:
        """Test that updating non-existent task shows error."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_valid_task_id", return_value=999):
            with patch.object(cli, "_get_input", return_value="ignored"):
                with patch("builtins.print") as mock_print:
                    cli._update_task()

        mock_print.assert_called_with("Error: Task 999 not found.")

    def test_update_with_empty_description_shows_error(self) -> None:
        """Test that empty description shows error."""
        service = TaskService()
        cli = TodoCLI(service)

        service.add_task("Task")

        with patch.object(cli, "_get_valid_task_id", return_value=1):
            with patch.object(cli, "_get_input", return_value=""):
                with patch("builtins.print") as mock_print:
                    cli._update_task()

        mock_print.assert_called_with("Error: Task description cannot be empty.")


class TestDeleteTask:
    """Tests for _delete_task method."""

    def test_delete_task_success(self) -> None:
        """Test successful task deletion."""
        service = TaskService()
        cli = TodoCLI(service)

        service.add_task("Task to delete")

        with patch.object(cli, "_get_valid_task_id", return_value=1):
            with patch("builtins.print") as mock_print:
                cli._delete_task()

        assert len(service.get_all_tasks()) == 0
        mock_print.assert_called_with("Task 1 deleted.")

    def test_delete_nonexistent_task_shows_error(self) -> None:
        """Test that deleting non-existent task shows error."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_valid_task_id", return_value=999):
            with patch("builtins.print") as mock_print:
                cli._delete_task()

        mock_print.assert_called_with("Error: Task 999 not found.")


class TestMarkComplete:
    """Tests for _mark_complete method."""

    def test_mark_complete_success(self) -> None:
        """Test marking task as complete."""
        service = TaskService()
        cli = TodoCLI(service)

        service.add_task("Task")

        with patch.object(cli, "_get_valid_task_id", return_value=1):
            with patch("builtins.print") as mock_print:
                cli._mark_complete(True)

        task = service.get_task_by_id(1)
        assert task is not None
        assert task.is_complete is True
        mock_print.assert_called_with("Task 1 marked as complete.")

    def test_mark_incomplete_success(self) -> None:
        """Test marking task as incomplete."""
        service = TaskService()
        cli = TodoCLI(service)

        service.add_task("Task")
        service.mark_complete(1, True)

        with patch.object(cli, "_get_valid_task_id", return_value=1):
            with patch("builtins.print") as mock_print:
                cli._mark_complete(False)

        task = service.get_task_by_id(1)
        assert task is not None
        assert task.is_complete is False
        mock_print.assert_called_with("Task 1 marked as incomplete.")

    def test_mark_complete_nonexistent_shows_error(self) -> None:
        """Test that marking non-existent task shows error."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch.object(cli, "_get_valid_task_id", return_value=999):
            with patch("builtins.print") as mock_print:
                cli._mark_complete(True)

        mock_print.assert_called_with("Error: Task 999 not found.")


class TestHandleChoice:
    """Tests for _handle_choice method."""

    def test_valid_choice_routes_to_correct_handler(self) -> None:
        """Test that valid choice 7 causes SystemExit with code 0."""
        service = TaskService()
        cli = TodoCLI(service)

        # Test that choice 7 exits with code 0
        # Note: We can't easily mock exit() and print() together in pytest
        # but we can verify the exit happens with correct code
        with pytest.raises(SystemExit) as exc_info:
            cli._handle_choice("7")

        assert exc_info.value.code == 0

    def test_invalid_choice_shows_error(self) -> None:
        """Test that invalid choice shows error message."""
        service = TaskService()
        cli = TodoCLI(service)

        with patch("builtins.print") as mock_print:
            cli._handle_choice("999")

        mock_print.assert_called_with("Invalid choice. Please try again.")
