# Research: Phase I - Todo CLI Application

**Feature**: 001-phase1-todo-cli
**Date**: 2025-12-30

## Overview

Phase I requires an in-memory Python console application with no external dependencies. This research confirms the technical approach and documents decisions.

## Technical Decisions

### Task Data Model

**Decision**: Use Python dataclass with `__post_init__` for validation

**Rationale**:
- Python dataclasses provide clean, type-annotated data structures
- `__post_init__` enables validation after initialization
- No external dependencies required
- Minimal boilerplate compared to traditional classes

**Alternatives Considered**:
- Named tuple: Less flexible for validation
- Plain dict: No type safety
- Pydantic model: External dependency (not allowed in Phase I)

### In-Memory Storage

**Decision**: Use Python list with separate ID counter

**Rationale**:
- List preserves insertion order (important for task list display)
- O(1) append operation
- Simple iteration for list view
- ID counter ensures unique, sequential IDs

**Alternatives Considered**:
- Dict by ID: Would enable faster lookup but loses insertion order
- List with embedded IDs: More complex, ID counter is simpler

### CLI Input Handling

**Decision**: Use Python built-in `input()` function with validation wrappers

**Rationale**:
- `input()` is the standard Python console input method
- Works on all platforms (Linux, macOS, Windows)
- No external dependencies needed
- Wrappers enable consistent validation and error handling

**Alternatives Considered**:
- `argparse`: Designed for command-line arguments, not interactive menus
- `click`: External dependency
- `typer`: External dependency

### Validation Strategy

**Decision**: Validate in model `__post_init__` and in CLI input handlers

**Rationale**:
- Model validation ensures data integrity at the object level
- CLI validation provides immediate user feedback
- No external validation libraries needed
- Clear separation of concerns

**Validation Rules** (from specification):
- Task ID must be positive integer (>= 1)
- Task description must be non-empty
- Task description must not be whitespace-only

### Exit Strategy

**Decision**: Use `sys.exit(0)` or return from main loop

**Rationale**:
- `sys.exit()` provides clean termination
- Return from main loop allows for cleanup if needed
- Standard Python practice for console applications

## Console Interaction Patterns

### Menu Design

```
=== Todo Menu ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Mark Complete
6. Mark Incomplete
7. Exit
```

**Pattern**:
- Numbered options for easy selection
- Consistent prompt format
- Clear feedback messages
- Error messages for invalid input

### Input Validation Flow

1. Get raw input from user
2. Strip whitespace
3. Validate format (e.g., numeric for IDs)
4. Validate business rules (e.g., non-empty description)
5. Handle or report errors
6. Proceed with operation

## Python Version Compatibility

**Target**: Python 3.x (standard library only)

**Key Features Used**:
- `dataclass` (Python 3.7+)
- Type hints (Python 3.5+, recommended 3.7+)

**Fallback for Python 3.6**:
- Remove `@dataclass` decorator
- Use explicit `__init__` method
- All other code remains compatible

## No External Dependencies Confirmed

| Category | Requirement | Solution |
|----------|-------------|----------|
| Data modeling | Task with id, description, is_complete | Python dataclass |
| Storage | In-memory list | Python list |
| Input/Output | Console interface | Python input()/print() |
| Type hints | Type annotations | Python typing module |
| Validation | Data validation | Python built-ins |

## Conclusion

Phase I can be implemented using only Python standard library with well-established patterns. No external research or dependencies required.
