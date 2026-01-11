"""Command handlers for the Todo CLI application.

This package contains the implementation of all CLI commands.
Each command is implemented in its own module.
"""

from todo.commands.add import add_task
from todo.commands.delete import delete_task
from todo.commands.list import list_tasks
from todo.commands.toggle import toggle_status
from todo.commands.update import update_task

__all__ = [
    "add_task",
    "list_tasks",
    "update_task",
    "delete_task",
    "toggle_status",
]
