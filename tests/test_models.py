"""Unit tests for the Task dataclass."""

import pytest

from todo.models import Task


class TestTaskCreation:
    """Tests for valid Task creation."""

    def test_create_task_with_required_fields(self) -> None:
        """Test creating a task with all required fields."""
        task = Task(id=1, description="Buy groceries")
        assert task.id == 1
        assert task.description == "Buy groceries"
        assert task.is_complete is False

    def test_create_task_with_all_fields(self) -> None:
        """Test creating a task with all fields specified."""
        task = Task(id=2, description="Call mom", is_complete=True)
        assert task.id == 2
        assert task.description == "Call mom"
        assert task.is_complete is True

    def test_create_task_defaults_to_incomplete(self) -> None:
        """Test that is_complete defaults to False."""
        task = Task(id=3, description="Finish report")
        assert task.is_complete is False


class TestTaskValidation:
    """Tests for Task validation."""

    def test_rejects_empty_description(self) -> None:
        """Test that empty description raises ValueError."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Task(id=1, description="")

    def test_rejects_whitespace_only_description(self) -> None:
        """Test that whitespace-only description raises ValueError."""
        with pytest.raises(ValueError, match="whitespace-only"):
            Task(id=1, description="   ")

    def test_rejects_zero_id(self) -> None:
        """Test that zero ID raises ValueError."""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=0, description="Test task")

    def test_rejects_negative_id(self) -> None:
        """Test that negative ID raises ValueError."""
        with pytest.raises(ValueError, match="positive integer"):
            Task(id=-1, description="Test task")

    def test_rejects_description_with_only_tabs(self) -> None:
        """Test that tab-only description raises ValueError."""
        with pytest.raises(ValueError, match="whitespace-only"):
            Task(id=1, description="\t\t")

    def test_rejects_description_with_newlines_only(self) -> None:
        """Test that newline-only description raises ValueError."""
        with pytest.raises(ValueError, match="whitespace-only"):
            Task(id=1, description="\n\n")


class TestTaskEquality:
    """Tests for Task equality."""

    def test_tasks_with_same_values_are_equal(self) -> None:
        """Test that two tasks with same values are equal."""
        task1 = Task(id=1, description="Buy groceries")
        task2 = Task(id=1, description="Buy groceries")
        assert task1 == task2

    def test_tasks_with_different_ids_are_not_equal(self) -> None:
        """Test that tasks with different IDs are not equal."""
        task1 = Task(id=1, description="Buy groceries")
        task2 = Task(id=2, description="Buy groceries")
        assert task1 != task2

    def test_tasks_with_different_descriptions_are_not_equal(self) -> None:
        """Test that tasks with different descriptions are not equal."""
        task1 = Task(id=1, description="Buy groceries")
        task2 = Task(id=1, description="Buy food")
        assert task1 != task2


class TestTaskRepr:
    """Tests for Task string representation."""

    def test_task_repr_contains_id_and_description(self) -> None:
        """Test that repr contains task ID and description."""
        task = Task(id=1, description="Test task")
        repr_str = repr(task)
        assert "id=1" in repr_str
        assert "description='Test task'" in repr_str
