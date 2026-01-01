# Tasks: Phase I - Todo CLI Application

**Input**: Design documents from `/specs/001-phase1-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Reference Documents**:
- Spec: `specs/001-phase1-todo-cli/spec.md`
- Plan: `specs/001-phase1-todo-cli/plan.md`
- Data Model: `specs/001-phase1-todo-cli/data-model.md`
- Contracts: `specs/001-phase1-todo-cli/contracts/cli-commands.md`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, etc.)
- Include exact file paths in descriptions

---

## Phase 1: Project Setup

**Purpose**: Initialize project structure per implementation plan

- [x] T001 Create `todo/` directory and `todo/__init__.py` package marker file
- [x] T002 Create `tests/` directory with `__init__.py` files for test packages

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Data Model & Storage (Foundational)

**Purpose**: Core infrastructure - MUST complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

### Task Model & Validation

- [x] T003 [P] [Foundation] Create `todo/models.py` with Task dataclass containing:
  - `id: int` field (required, positive integer)
  - `description: str` field (required, non-empty, non-whitespace-only)
  - `is_complete: bool` field (required, defaults to False)
  - Reference: `data-model.md` section "Task"

- [x] T004 [P] [Foundation] Add `__post_init__` validation to Task dataclass:
  - Validate `id >= 1`
  - Validate `description` is not empty or whitespace-only
  - Raise `ValueError` with descriptive messages for invalid data
  - Reference: `plan.md` section "Data Model", `spec.md` FR-011

### Service Layer & In-Memory Storage

- [x] T005 [P] [Foundation] Create `todo/service.py` with TaskService class:
  - `__init__()`: Initialize `_tasks: List[Task]` and `_next_id: int = 1`
  - Reference: `plan.md` section "Service Layer", `data-model.md` section "TaskService"

- [x] T006 [Foundation] Implement `add_task(description: str) -> Task` method in TaskService:
  - Create Task with auto-generated ID from `_next_id`
  - Increment `_next_id` after task creation
  - Append task to `_tasks` list
  - Return the created Task
  - Reference: `plan.md` "add_task()", `spec.md` FR-001, FR-002

- [x] T007 [Foundation] Implement `get_all_tasks() -> List[Task]` method in TaskService:
  - Return copy of `_tasks` list to prevent external mutation
  - Reference: `plan.md` "get_all_tasks()", `spec.md` FR-005

- [x] T008 [Foundation] Implement `get_task_by_id(task_id: int) -> Optional[Task]` method:
  - Search `_tasks` for task with matching ID
  - Return task if found, None otherwise
  - Reference: `plan.md` "get_task_by_id()", `spec.md` FR-010

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add Task (Priority: P1)

**Goal**: Users can add new tasks to their todo list

**Independent Test**: Add a task and verify it appears in the task list with correct ID

### Implementation

- [x] T009 [US1] Implement CLI `_add_task()` method in `todo/cli.py`:
  - Prompt user for task description using `_get_input("Enter task description: ")`
  - Validate description is not empty/whitespace-only
  - Call `_service.add_task(description)` on valid input
  - Print success message with format: "Task added: [id] description"
  - Print error message on invalid input: "Error: Task description cannot be empty."
  - Reference: `spec.md` User Story 1, `contracts/cli-commands.md` "Command 1: Add Task"

**Checkpoint**: Add Task feature complete and testable

---

## Phase 4: User Story 2 - View Task List (Priority: P1)

**Goal**: Users can see all their tasks with completion status

**Independent Test**: Add multiple tasks and verify they all display correctly

### Implementation

- [x] T010 [US2] Implement CLI `_view_tasks()` method in `todo/cli.py`:
  - Call `_service.get_all_tasks()` to retrieve all tasks
  - If list empty: print "No tasks yet. Add one!"
  - If tasks exist: display each task with format "[status] [id] description"
  - Status format: "[X]" for complete, "[ ]" for incomplete
  - Reference: `spec.md` User Story 2, `contracts/cli-commands.md` "Command 2: View Tasks"

**Checkpoint**: View Task List feature complete and testable

---

## Phase 5: User Story 3 - Update Task (Priority: P1)

**Goal**: Users can modify task descriptions

**Independent Test**: Update a task and verify the change is reflected

### Implementation

- [x] T011 [US3] Implement `update_task(task_id: int, new_description: str) -> Optional[Task]`:
  - Find task by ID using `get_task_by_id()`
  - If found: update `task.description` with stripped description
  - Return updated task, or None if not found
  - Reference: `plan.md` "update_task()", `spec.md` FR-006

- [x] T012 [US3] Implement CLI `_update_task()` method in `todo/cli.py`:
  - Call `_get_valid_task_id("Enter task ID to update: ")` for ID input
  - On valid ID, prompt for new description
  - Validate new description is not empty/whitespace-only
  - Call `_service.update_task()` on valid input
  - Print success: "Task {id} updated."
  - Print error if task not found: "Error: Task {id} not found."
  - Reference: `spec.md` User Story 3, `contracts/cli-commands.md` "Command 3: Update Task"

**Checkpoint**: Update Task feature complete and testable

---

## Phase 6: User Story 4 - Delete Task (Priority: P1)

**Goal**: Users can remove tasks from their list

**Independent Test**: Delete a task and verify it no longer appears

### Implementation

- [x] T013 [US4] Implement `delete_task(task_id: int) -> bool` method in TaskService:
  - Search `_tasks` for task with matching ID
  - If found: remove from list using `del`, return True
  - If not found: return False
  - Reference: `plan.md` "delete_task()", `spec.md` FR-007

- [x] T014 [US4] Implement CLI `_delete_task()` method in `todo/cli.py`:
  - Call `_get_valid_task_id("Enter task ID to delete: ")` for ID input
  - On valid ID, call `_service.delete_task()`
  - Print success: "Task {id} deleted."
  - Print error if task not found: "Error: Task {id} not found."
  - Reference: `spec.md` User Story 4, `contracts/cli-commands.md` "Command 4: Delete Task"

**Checkpoint**: Delete Task feature complete and testable

---

## Phase 7: User Story 5 - Mark Complete/Incomplete (Priority: P1)

**Goal**: Users can toggle task completion status

**Independent Test**: Mark tasks complete/incomplete and verify status changes

### Implementation

- [x] T015 [US5] Implement `mark_complete(task_id: int, complete: bool) -> Optional[Task]`:
  - Find task by ID using `get_task_by_id()`
  - If found: set `task.is_complete = complete`
  - Return updated task, or None if not found
  - Reference: `plan.md` "mark_complete()", `spec.md` FR-008, FR-009

- [x] T016 [US5] Implement CLI `_mark_complete(complete: bool)` method in `todo/cli.py`:
  - Prompt for task ID with context-appropriate message
  - Call `_service.mark_complete(task_id, complete)`
  - Print success: "Task {id} marked as complete/incomplete."
  - Print error if task not found: "Error: Task {id} not found."
  - Reference: `spec.md` User Story 5, `contracts/cli-commands.md` "Commands 5-6"

**Checkpoint**: Mark Complete/Incomplete feature complete and testable

---

## Phase 8: CLI Infrastructure & Menu System

**Purpose**: Menu-driven console interface that orchestrates all features

### Menu Display & Input Handling

- [x] T017 [CLI] Implement `_display_menu()` method in TodoCLI:
  - Print menu header: "=== Todo Menu ==="
  - Print numbered options 1-7:
    1. Add Task
    2. View Tasks
    3. Update Task
    4. Delete Task
    5. Mark Complete
    6. Mark Incomplete
    7. Exit
  - Reference: `contracts/cli-commands.md` "Main Menu"

- [x] T018 [CLI] Implement `_get_input(prompt: str) -> str` method:
  - Accept prompt string
  - Call Python `input(prompt)`
  - Return stripped input
  - Reference: `plan.md` "CLI Input Handling"

- [x] T019 [CLI] Implement `_handle_choice(choice: str)` method:
  - Map choices to handler methods:
    - "1" -> `_add_task`
    - "2" -> `_view_tasks`
    - "3" -> `_update_task`
    - "4" -> `_delete_task`
    - "5" -> `_mark_complete(True)`
    - "6" -> `_mark_complete(False)`
    - "7" -> Exit application
  - Print "Invalid choice. Please try again." for unknown choices
  - Reference: `plan.md` "_handle_choice()"

### Input Validation Helpers

- [x] T020 [CLI] Implement `_get_valid_task_id(prompt: str) -> Optional[int]` method:
  - Call `_get_input(prompt)` to get user input
  - Try to parse as integer
  - Validate ID is positive (>= 1)
  - Print appropriate error for invalid input
  - Return valid ID or None on error
  - Reference: `plan.md` "_get_valid_task_id()", `spec.md` Edge Cases

### Application Lifecycle

- [x] T021 [CLI] Implement `run()` method in TodoCLI:
  - Display menu
  - Get user choice
  - Handle choice
  - Loop continues until choice "7" (exit)
  - Reference: `plan.md` "CLI Interface", `quickstart.md` "Running the Application"

- [x] T022 [Entry] Create `todo.py` entry point at repository root:
  - Create TaskService instance
  - Create TodoCLI instance with service
  - Call `cli.run()` to start application
  - Add shebang: `#!/usr/bin/env python3`
  - Reference: `plan.md` "Application Entry Point", `quickstart.md` "Running the Application"

**Checkpoint**: All CLI infrastructure complete

---

## Phase 9: Integration Testing

**Purpose**: Verify all features work together correctly

- [x] T023 [Test] Create `tests/test_models.py` with unit tests for Task dataclass:
  - Test valid task creation
  - Test validation rejects empty description
  - Test validation rejects whitespace-only description
  - Test validation rejects invalid ID
  - Reference: `data-model.md` "Validation Rules"

- [x] T024 [Test] Create `tests/test_service.py` with unit tests for TaskService:
  - Test add_task creates task with correct ID
  - Test get_all_tasks returns all tasks
  - Test get_task_by_id finds existing task
  - Test get_task_by_id returns None for non-existent ID
  - Test update_task modifies description
  - Test delete_task removes task
  - Test mark_complete changes status
  - Reference: `plan.md` "Service Layer"

- [x] T025 [Test] Create `tests/test_cli.py` with integration tests for TodoCLI:
  - Test menu displays correctly
  - Test _get_valid_task_id rejects invalid input
  - Test _get_valid_task_id accepts valid ID
  - Reference: `contracts/cli-commands.md`

---

## Dependencies & Execution Order

### Phase Dependencies

| Phase | Depends On | Blocks |
|-------|-----------|--------|
| Phase 1: Setup | None | Phase 2 |
| Phase 2: Foundational | Phase 1 | All User Stories |
| Phase 3-7: User Stories | Phase 2 | Phase 8 |
| Phase 8: CLI Infrastructure | Phase 2 | Phase 9 |
| Phase 9: Integration | Phase 3-8 | Complete |

### Sequential Requirements

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all features)
3. Complete Phase 3: Add Task
4. Complete Phase 4: View Tasks
5. Complete Phase 5: Update Task
6. Complete Phase 6: Delete Task
7. Complete Phase 7: Mark Complete/Incomplete
8. Complete Phase 8: CLI Infrastructure (depends on service layer)
9. Complete Phase 9: Integration Testing

### Parallel Opportunities

- T003 and T004 can run in parallel (both in models.py)
- T003 and T005 can run in parallel (models.py and service.py)
- T006 depends on T005
- T007, T008 depend on T006
- All User Story implementations (T009, T010, T011/T012, T013/T014, T015/T016) can run in parallel after Phase 2
- T017-T022 can run in parallel after Phase 2
- T023-T025 can run in parallel

---

## Implementation Strategy

### Sequential (Recommended)

1. Complete Setup + Foundational → Foundation ready
2. Implement Add Task → Test → Mark complete
3. Implement View Tasks → Test → Mark complete
4. Implement Update Task → Test → Mark complete
5. Implement Delete Task → Test → Mark complete
6. Implement Mark Complete/Incomplete → Test → Mark complete
7. Implement CLI Infrastructure → Integration test
8. Run full test suite

### After All Tasks Complete

Application should:
- Start with `python todo.py`
- Display menu
- Allow adding, viewing, updating, deleting tasks
- Allow marking tasks complete/incomplete
- Exit cleanly on option 7
- Handle all error cases per specification

---

## Notes

- [P] tasks = can run in parallel (different files, no dependencies)
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Reference documents: spec.md (what), plan.md (how), data-model.md (data), contracts/ (CLI behavior)
