# Implementation Plan: Phase I - Todo CLI Application

**Branch**: `001-phase1-todo-cli` | **Date**: 2025-12-30 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-phase1-todo-cli/spec.md`

## Summary

Build an in-memory Python console application for task management with basic CRUD operations (Add, View, Update, Delete, Mark Complete/Incomplete). The application stores all data in memory during runtime only, with no persistence, databases, or external dependencies. Users interact through a text-based menu interface.

## Technical Context

**Language/Version**: Python 3.x (standard library only)
**Primary Dependencies**: None (uses Python standard library only)
**Storage**: In-memory Python data structures (list/dict)
**Testing**: Python unittest or pytest (to be determined)
**Target Platform**: Any system with Python 3.x installed (Linux, macOS, Windows)
**Project Type**: Single standalone Python script
**Performance Goals**: Instant response (< 1 second for all operations)
**Constraints**:
- No databases (SQL, NoSQL)
- No file storage
- No web frameworks or APIs
- No external services or network access
- No authentication
- Must run in standard console/terminal
**Scale/Scope**: Single user, in-memory data, up to hundreds of tasks

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Compliance | Notes |
|-----------|------------|-------|
| I. Spec-Driven Development | PASS | Plan derived strictly from approved spec |
| II. Agent Behavior Rules | PASS | No new features introduced; follows spec exactly |
| III. Phase Governance | PASS | Phase I scope only; no future-phase concepts |
| IV. Technology Constraints | PASS | Python only; no databases, files, web frameworks |
| V. Quality Principles | PASS | Clean architecture with separation of concerns |

**Result**: ALL GATES PASS - No violations requiring justification.

## Project Structure

### Documentation (this feature)

```text
specs/001-phase1-todo-cli/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
hackathon-2/
├── todo.py              # Main application entry point
├── todo/
│   ├── __init__.py      # Package marker
│   ├── models.py        # Task data model
│   ├── service.py       # Task business logic (in-memory storage)
│   └── cli.py           # Console interface and menu system
└── tests/
    ├── test_models.py   # Task model unit tests
    ├── test_service.py  # Service layer unit tests
    └── test_cli.py      # CLI integration tests
```

**Structure Decision**: Single Python package `todo/` with clear separation:
- `models.py`: Task dataclass with validation
- `service.py`: In-memory task storage and CRUD operations
- `cli.py`: Menu-driven console interface
- `todo.py`: Application entry point

This structure follows clean architecture principles while remaining simple for Phase I.

---

## Phase 0: Research

*No external research required.* Phase I uses only Python standard library with well-established patterns for console applications. All technical decisions are based on standard Python practices.

### Technical Decisions

| Decision | Rationale |
|----------|-----------|
| Use Python dataclass for Task | Type-safe, minimal boilerplate, Python 3.7+ |
| Store tasks in a list | Simple, preserves insertion order, easy to iterate |
| Use list index + 1 for task IDs | Simple integer IDs starting at 1 |
| Use input() for user input | Standard Python built-in for console input |
| Use dataclasses.validate() for validation | Built-in validation support in Python 3.10+ or manual validation |
| Main menu loop with numbered options | Clear, discoverable interface |

---

## Phase 1: Design

### Data Model

**File**: `todo/models.py`

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    """Represents a single todo task."""
    id: int
    description: str
    is_complete: bool = False

    def __post_init__(self):
        """Validate task after initialization."""
        if not self.description or not self.description.strip():
            raise ValueError("Task description cannot be empty or whitespace-only")
        if self.id < 1:
            raise ValueError("Task ID must be a positive integer")
```

**Validation Rules**:
- `id` must be a positive integer (>= 1)
- `description` must be non-empty and not whitespace-only
- `is_complete` defaults to `False`

### Service Layer

**File**: `todo/service.py`

```python
from typing import List, Optional
from todo.models import Task

class TaskService:
    """In-memory task storage and CRUD operations."""

    def __init__(self):
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, description: str) -> Task:
        """Create a new task with auto-generated ID."""
        task = Task(id=self._next_id, description=description.strip())
        self._next_id += 1
        self._tasks.append(task)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks in insertion order."""
        return self._tasks.copy()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Find a task by its ID."""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: int, new_description: str) -> Optional[Task]:
        """Update a task's description by ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.description = new_description.strip()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID. Returns True if deleted."""
        for i, task in enumerate(self._tasks):
            if task.id == task_id:
                del self._tasks[i]
                return True
        return False

    def mark_complete(self, task_id: int, complete: bool = True) -> Optional[Task]:
        """Set task completion status by ID."""
        task = self.get_task_by_id(task_id)
        if task:
            task.is_complete = complete
        return task
```

**In-Memory Storage Design**:
- `_tasks`: List[Task] - stores all tasks in insertion order
- `_next_id`: int - tracks next available ID (starts at 1, increments forever)
- Deleted tasks are removed from the list (creates ID gaps, as specified)

### CLI Interface

**File**: `todo/cli.py`

```python
from todo.service import TaskService

class TodoCLI:
    """Console-based menu interface for task management."""

    def __init__(self, service: TaskService):
        self._service = service

    def run(self):
        """Main application loop."""
        while True:
            self._display_menu()
            choice = self._get_input("Enter choice: ").strip()
            self._handle_choice(choice)

    def _display_menu(self):
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
        """Get user input with prompt."""
        return input(prompt)

    def _handle_choice(self, choice: str):
        """Route user choice to appropriate handler."""
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

    def _add_task(self):
        """Add a new task."""
        description = self._get_input("Enter task description: ").strip()
        if not description:
            print("Error: Task description cannot be empty.")
            return
        task = self._service.add_task(description)
        print(f"Task added: [{task.id}] {task.description}")

    def _view_tasks(self):
        """Display all tasks."""
        tasks = self._service.get_all_tasks()
        if not tasks:
            print("No tasks yet. Add one!")
            return
        print("\nTasks:")
        for task in tasks:
            status = "[X]" if task.is_complete else "[ ]"
            print(f"{status} [{task.id}] {task.description}")

    def _update_task(self):
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

    def _delete_task(self):
        """Delete a task."""
        task_id = self._get_valid_task_id("Enter task ID to delete: ")
        if task_id is None:
            return
        if self._service.delete_task(task_id):
            print(f"Task {task_id} deleted.")
        else:
            print(f"Error: Task {task_id} not found.")

    def _mark_complete(self, complete: bool):
        """Mark a task as complete or incomplete."""
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

    def _get_valid_task_id(self, prompt: str) -> Optional[int]:
        """Get and validate a task ID from user input."""
        try:
            task_id = int(self._get_input(prompt))
            if task_id < 1:
                print("Error: Task ID must be a positive integer.")
                return None
            return task_id
        except ValueError:
            print("Error: Invalid task ID. Please enter a number.")
            return None
```

### Application Entry Point

**File**: `todo.py` (repository root)

```python
#!/usr/bin/env python3
"""Todo CLI Application - Phase I"""

from todo.cli import TodoCLI
from todo.service import TaskService

def main():
    """Application entry point."""
    service = TaskService()
    cli = TodoCLI(service)
    cli.run()

if __name__ == "__main__":
    main()
```

---

## Complexity Tracking

> No constitution violations requiring justification. Simple, straightforward implementation.

---

## Quickstart

### Running the Application

```bash
# From repository root
python todo.py

# Or with python3
python3 todo.py
```

### Expected User Flow

1. Application displays main menu
2. User selects option (1-6) or 7 to exit
3. Application prompts for required information
4. Application provides feedback (success/error message)
5. Application returns to main menu

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_models.py
```

---

## Acceptance Summary

| Feature | Implementation |
|---------|----------------|
| Add Task | `service.add_task()` + `cli._add_task()` |
| View Task List | `service.get_all_tasks()` + `cli._view_tasks()` |
| Update Task | `service.update_task()` + `cli._update_task()` |
| Delete Task | `service.delete_task()` + `cli._delete_task()` |
| Mark Complete | `service.mark_complete(complete=True)` + `cli._mark_complete(True)` |
| Mark Incomplete | `service.mark_complete(complete=False)` + `cli._mark_complete(False)` |

All five features map directly to approved user stories with no additions or modifications.
