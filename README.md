# Todo CLI Application

A command-line interface (CLI) todo application built with Python for managing your tasks efficiently from the terminal.

## Features

- Add new tasks with descriptions
- View all tasks with completion status
- Update existing task descriptions
- Delete tasks
- Mark tasks as complete or incomplete
- Interactive menu-driven interface
- In-memory task storage

## Project Structure

```
hackathon-2/
├── todo/
│   ├── __init__.py
│   ├── models.py       # Task data model
│   ├── service.py      # Task service layer (CRUD operations)
│   └── cli.py          # Console interface and menu system
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_service.py
│   └── test_cli.py
├── todo.py             # Application entry point
└── README.md
```

## Requirements

- Python 3.7+

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hackathon-2
```

2. (Optional) Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Usage

Run the application:
```bash
python todo.py
```

### Menu Options

Once the application starts, you'll see an interactive menu:

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

### Examples

**Adding a Task:**
- Select option `1`
- Enter your task description
- The task will be assigned a unique ID

**Viewing Tasks:**
- Select option `2`
- All tasks will be displayed with their ID, status, and description
- `[X]` indicates a completed task
- `[ ]` indicates an incomplete task

**Updating a Task:**
- Select option `3`
- Enter the task ID you want to update
- Enter the new description

**Deleting a Task:**
- Select option `4`
- Enter the task ID you want to delete

**Marking Tasks:**
- Select option `5` to mark a task as complete
- Select option `6` to mark a task as incomplete
- Enter the task ID when prompted

## Architecture

### Components

- **models.py**: Contains the `Task` dataclass with validation logic
  - Ensures task IDs are positive integers
  - Validates that descriptions are non-empty

- **service.py**: Contains the `TaskService` class for business logic
  - Manages in-memory task storage
  - Handles CRUD operations
  - Auto-generates unique task IDs

- **cli.py**: Contains the `TodoCLI` class for user interaction
  - Provides menu-driven interface
  - Handles user input validation
  - Displays formatted output

## Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=todo tests/
```

## Limitations

- **In-Memory Storage**: All tasks are stored in memory and will be lost when the application exits
- **No Persistence**: Tasks are not saved to disk
- **Single User**: Designed for single-user local usage

## Future Enhancements

Potential improvements for future versions:
- Persistent storage (JSON, SQLite, or database)
- Task priorities and due dates
- Task categories/tags
- Search and filter functionality
- Export/import tasks
- Web or GUI interface

## Development

This project follows Spec-Driven Development (SDD) practices and includes:
- Feature specifications in `specs/`
- Architecture Decision Records in `history/adr/`
- Prompt History Records in `history/prompts/`

## License

This project is developed as part of the GIAIC Quarter 5 Hackathon 2.

## Contributing

This is a hackathon project. For contributions or issues, please contact the project maintainers.
