"""Unit tests for the TaskService class."""

import pytest

from todo.service import TaskService


class TestTaskServiceInitialization:
    """Tests for TaskService initialization."""

    def test_initial_state_is_empty(self) -> None:
        """Test that a new service starts with no tasks."""
        service = TaskService()
        assert service.get_all_tasks() == []

    def test_first_task_gets_id_1(self) -> None:
        """Test that the first task created gets ID 1."""
        service = TaskService()
        task = service.add_task("First task")
        assert task.id == 1


class TestAddTask:
    """Tests for the add_task method."""

    def test_add_task_creates_task_with_correct_id(self) -> None:
        """Test that add_task creates task with correct ID."""
        service = TaskService()
        task = service.add_task("Buy groceries")
        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.is_complete is False

    def test_add_multiple_tasks_get_incrementing_ids(self) -> None:
        """Test that multiple tasks get incrementing IDs."""
        service = TaskService()
        task1 = service.add_task("Task 1")
        task2 = service.add_task("Task 2")
        task3 = service.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_strips_whitespace_from_description(self) -> None:
        """Test that add_task strips whitespace from description."""
        service = TaskService()
        task = service.add_task("  Test task  ")
        assert task.description == "Test task"

    def test_added_task_appears_in_get_all_tasks(self) -> None:
        """Test that added task appears in get_all_tasks."""
        service = TaskService()
        service.add_task("Test task")
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].description == "Test task"


class TestGetAllTasks:
    """Tests for the get_all_tasks method."""

    def test_get_all_tasks_returns_copy(self) -> None:
        """Test that get_all_tasks returns a copy, not the original list."""
        service = TaskService()
        service.add_task("Test task")
        tasks1 = service.get_all_tasks()
        tasks2 = service.get_all_tasks()
        assert tasks1 is not tasks2

    def test_get_all_tasks_returns_copy_of_tasks(self) -> None:
        """Test that modifying returned list doesn't affect internal state."""
        service = TaskService()
        service.add_task("Test task")
        tasks = service.get_all_tasks()
        tasks.append(None)  # type: ignore
        tasks = service.get_all_tasks()
        assert len(tasks) == 1


class TestGetTaskById:
    """Tests for the get_task_by_id method."""

    def test_get_existing_task(self) -> None:
        """Test getting an existing task by ID."""
        service = TaskService()
        service.add_task("Task 1")
        task = service.get_task_by_id(1)
        assert task is not None
        assert task.description == "Task 1"

    def test_get_nonexistent_task_returns_none(self) -> None:
        """Test that getting a non-existent task returns None."""
        service = TaskService()
        task = service.get_task_by_id(999)
        assert task is None

    def test_get_task_after_deletion_returns_none(self) -> None:
        """Test that getting a deleted task returns None."""
        service = TaskService()
        service.add_task("Task 1")
        service.delete_task(1)
        task = service.get_task_by_id(1)
        assert task is None


class TestUpdateTask:
    """Tests for the update_task method."""

    def test_update_task_description(self) -> None:
        """Test updating a task's description."""
        service = TaskService()
        service.add_task("Old description")
        task = service.update_task(1, "New description")
        assert task is not None
        assert task.description == "New description"

    def test_update_nonexistent_task_returns_none(self) -> None:
        """Test that updating a non-existent task returns None."""
        service = TaskService()
        task = service.update_task(999, "New description")
        assert task is None

    def test_update_task_strips_whitespace(self) -> None:
        """Test that update strips whitespace from new description."""
        service = TaskService()
        service.add_task("Original")
        service.update_task(1, "  New description  ")
        task = service.get_task_by_id(1)
        assert task is not None
        assert task.description == "New description"


class TestDeleteTask:
    """Tests for the delete_task method."""

    def test_delete_existing_task_returns_true(self) -> None:
        """Test that deleting an existing task returns True."""
        service = TaskService()
        service.add_task("Task to delete")
        result = service.delete_task(1)
        assert result is True

    def test_delete_removes_task_from_list(self) -> None:
        """Test that deleting removes the task from the list."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        tasks = service.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0].id == 2

    def test_delete_nonexistent_task_returns_false(self) -> None:
        """Test that deleting a non-existent task returns False."""
        service = TaskService()
        result = service.delete_task(999)
        assert result is False


class TestMarkComplete:
    """Tests for the mark_complete method."""

    def test_mark_complete(self) -> None:
        """Test marking a task as complete."""
        service = TaskService()
        service.add_task("Task")
        task = service.mark_complete(1, True)
        assert task is not None
        assert task.is_complete is True

    def test_mark_incomplete(self) -> None:
        """Test marking a task as incomplete."""
        service = TaskService()
        service.add_task("Task")
        service.mark_complete(1, True)  # First mark complete
        task = service.mark_complete(1, False)  # Then mark incomplete
        assert task is not None
        assert task.is_complete is False

    def test_mark_complete_on_nonexistent_returns_none(self) -> None:
        """Test that marking a non-existent task returns None."""
        service = TaskService()
        task = service.mark_complete(999, True)
        assert task is None

    def test_task_defaults_to_incomplete(self) -> None:
        """Test that a new task defaults to incomplete."""
        service = TaskService()
        service.add_task("Task")
        task = service.get_task_by_id(1)
        assert task is not None
        assert task.is_complete is False


class TestIdSequence:
    """Tests for ID sequence behavior."""

    def test_deleted_task_id_not_reused(self) -> None:
        """Test that deleted task IDs are not reused."""
        service = TaskService()
        service.add_task("Task 1")
        service.add_task("Task 2")
        service.delete_task(1)
        service.add_task("Task 3")
        tasks = service.get_all_tasks()
        assert len(tasks) == 2
        ids = [t.id for t in tasks]
        assert ids == [2, 3]
