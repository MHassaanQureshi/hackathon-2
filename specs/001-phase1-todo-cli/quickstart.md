# Quickstart: Phase I - Todo CLI Application

**Feature**: 001-phase1-todo-cli
**Date**: 2025-12-30

## Prerequisites

- Python 3.x installed on your system
- No external dependencies required

## Installation

1. Navigate to the project root directory:
   ```bash
   cd /path/to/hackathon-2
   ```

2. Verify Python is available:
   ```bash
   python --version
   # or
   python3 --version
   ```

## Running the Application

From the repository root, run:

```bash
python todo.py
```

Or with Python 3:

```bash
python3 todo.py
```

## Quick Usage Guide

### Adding a Task

1. Select option `1` from the menu
2. Enter your task description
3. Press Enter

Example:
```
Enter task description: Buy groceries
Task added: [1] Buy groceries
```

### Viewing Tasks

1. Select option `2` from the menu
2. View all tasks with their status

Example:
```
Tasks:
[ ] [1] Buy groceries
[X] [2] Call mom
[ ] [3] Finish report
```

### Updating a Task

1. Select option `3` from the menu
2. Enter the task ID to update
3. Enter the new description

Example:
```
Enter task ID to update: 1
Enter new description: Buy groceries and milk
Task 1 updated.
```

### Deleting a Task

1. Select option `4` from the menu
2. Enter the task ID to delete

Example:
```
Enter task ID to delete: 1
Task 1 deleted.
```

### Marking a Task Complete

1. Select option `5` from the menu
2. Enter the task ID

Example:
```
Enter task ID to mark complete: 1
Task 1 marked as complete.
```

### Marking a Task Incomplete

1. Select option `6` from the menu
2. Enter the task ID

Example:
```
Enter task ID to mark incomplete: 1
Task 1 marked as incomplete.
```

### Exiting

1. Select option `7` from the menu
2. Application terminates

## Testing

Run the test suite:

```bash
# Run all tests
python -m pytest tests/

# Run a specific test file
python -m pytest tests/test_models.py

# Run with verbose output
python -m pytest tests/ -v
```

## Troubleshooting

### "python: command not found"

Try using `python3` instead of `python`:

```bash
python3 todo.py
```

### Application appears frozen

The application is waiting for input. Type your response and press Enter.

### Invalid task ID error

Ensure you're entering a valid task ID shown in the task list. Task IDs are positive integers starting from 1.

### Data not persisting

This is expected behavior for Phase I. All data is stored in-memory only and will be lost when the application exits. Future phases will add persistence.

## Next Steps

After implementing the application, proceed to the task phase:

```bash
/sp.tasks
```

This will generate the actionable task list for implementation.
