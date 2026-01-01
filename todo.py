#!/usr/bin/env python3
"""Todo CLI Application - Phase I"""

from todo.cli import TodoCLI
from todo.service import TaskService


def main() -> None:
    """Application entry point."""
    service = TaskService()
    cli = TodoCLI(service)
    cli.run()


if __name__ == "__main__":
    main()
