# CLI Commands Contract: Phase I - Todo CLI Application

**Feature**: 001-phase1-todo-cli
**Date**: 2025-12-30

## Overview

This document defines the CLI command contracts for user interactions. Since this is a menu-driven console application, contracts define the input/output behavior for each menu option.

## Main Menu

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

## Command Contracts

### Command 1: Add Task

**Input**:
```
Enter task description: [user input]
```

**Validation**:
- If empty or whitespace-only: "Error: Task description cannot be empty."

**Output (Success)**:
```
Task added: [1] Buy groceries
```

**Output (Error)**:
```
Error: Task description cannot be empty.
```

---

### Command 2: View Tasks

**Input**: None (displays immediately)

**Output (Empty List)**:
```
No tasks yet. Add one!
```

**Output (With Tasks)**:
```
Tasks:
[ ] [1] Buy groceries
[X] [2] Call mom
[ ] [3] Finish report
```

**Format**: `[status] [id] description`
- Status: `[X]` for complete, `[ ]` for incomplete
- ID: Task ID in brackets
- Description: Task text

---

### Command 3: Update Task

**Input**:
```
Enter task ID to update: [user input]
Enter new description: [user input]
```

**Validation - Task ID**:
- If not a number: "Error: Invalid task ID. Please enter a number."
- If less than 1: "Error: Task ID must be a positive integer."
- If not found: "Error: Task [id] not found."

**Validation - Description**:
- If empty or whitespace-only: "Error: Task description cannot be empty."

**Output (Success)**:
```
Task 1 updated.
```

**Output (Error - Not Found)**:
```
Error: Task 5 not found.
```

**Output (Error - Invalid Description)**:
```
Error: Task description cannot be empty.
```

---

### Command 4: Delete Task

**Input**:
```
Enter task ID to delete: [user input]
```

**Validation**:
- If not a number: "Error: Invalid task ID. Please enter a number."
- If less than 1: "Error: Task ID must be a positive integer."
- If not found: "Error: Task [id] not found."

**Output (Success)**:
```
Task 1 deleted.
```

**Output (Error - Not Found)**:
```
Error: Task 5 not found.
```

---

### Command 5: Mark Complete

**Input**:
```
Enter task ID to mark complete: [user input]
```

**Validation**:
- If not a number: "Error: Invalid task ID. Please enter a number."
- If less than 1: "Error: Task ID must be a positive integer."
- If not found: "Error: Task [id] not found."

**Output (Success)**:
```
Task 1 marked as complete.
```

**Output (Error - Not Found)**:
```
Error: Task 5 not found.
```

---

### Command 6: Mark Incomplete

**Input**:
```
Enter task ID to mark incomplete: [user input]
```

**Validation**:
- If not a number: "Error: Invalid task ID. Please enter a number."
- If less than 1: "Error: Task ID must be a positive integer."
- If not found: "Error: Task [id] not found."

**Output (Success)**:
```
Task 1 marked as incomplete.
```

**Output (Error - Not Found)**:
```
Error: Task 5 not found.
```

---

### Command 7: Exit

**Input**: None

**Output**:
```
Goodbye!
```

**Action**: Application terminates with exit code 0

## Invalid Menu Choice

**Input**: Any value not 1-7

**Output**:
```
Invalid choice. Please try again.
```

**Action**: Return to main menu (no menu redisplay)

## Error Message Summary

| Error Type | Message |
|------------|---------|
| Empty description | "Error: Task description cannot be empty." |
| Invalid ID (not a number) | "Error: Invalid task ID. Please enter a number." |
| Invalid ID (not positive) | "Error: Task ID must be a positive integer." |
| Task not found | "Error: Task [id] not found." |
| Invalid menu choice | "Invalid choice. Please try again." |
| Exit | "Goodbye!" |
| Empty task list | "No tasks yet. Add one!" |
