# Data Model: Phase I - Todo CLI Application

**Feature**: 001-phase1-todo-cli
**Date**: 2025-12-30

## Overview

This document defines the data model for the Phase I Todo CLI application. All data is stored in-memory during runtime only.

## Entities

### Task

Represents a single todo item.

| Field | Type | Required | Default | Validation |
|-------|------|----------|---------|------------|
| `id` | int | Yes | N/A | Must be positive integer (>= 1) |
| `description` | str | Yes | N/A | Must be non-empty, non-whitespace-only |
| `is_complete` | bool | Yes | False | N/A |

### TaskService

Manages in-memory task storage and CRUD operations.

| Attribute | Type | Purpose |
|-----------|------|---------|
| `_tasks` | List[Task] | Stores all tasks in insertion order |
| `_next_id` | int | Tracks next available ID (starts at 1) |

## Validation Rules

### Task Initialization

```python
def __post_init__(self):
    if not self.description or not self.description.strip():
        raise ValueError("Task description cannot be empty or whitespace-only")
    if self.id < 1:
        raise ValueError("Task ID must be a positive integer")
```

### Input Validation (CLI Layer)

| Input | Validation |
|-------|------------|
| Menu choice | Must be 1-7 |
| Task ID | Must be positive integer |
| Task description | Must be non-empty after strip |

## State Transitions

### Task Completion Status

```
Incomplete (default) <---> Complete
```

The `is_complete` boolean can be toggled via:
- `mark_complete(task_id, True)` - sets to complete
- `mark_complete(task_id, False)` - sets to incomplete

### Task Lifecycle

```
[Created] ---> [Updated] ---> [Deleted]
     |
     +---> [Marked Complete]
     +---> [Marked Incomplete]
```

## In-Memory Storage Behavior

### ID Generation

- IDs start at 1
- IDs increment by 1 for each new task
- Deleted task IDs are NOT reused (gaps in ID sequence are expected)

### List Operations

| Operation | Data Structure | Complexity |
|-----------|---------------|------------|
| Add task | List append | O(1) |
| Get all tasks | List iteration | O(n) |
| Find by ID | List iteration | O(n) |
| Delete by ID | List delete | O(n) |
| Update by ID | List iteration + modify | O(n) |

### Storage Limits

- Practical limit: Several hundred tasks (depends on system memory)
- No hard limit enforced (Python list can grow as needed)
- All data lost when application exits (in-memory only)
