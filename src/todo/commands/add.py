"""Add command implementation for the Todo CLI application.

This module provides the functionality to add new tasks to the todo list.
"""

import sys

from todo.exceptions import EmptyTitleError
from todo.models import Task
from todo.storage import storage
from todo.utils import validate_title


def add_task(title: str, description: str = "") -> None:
    """Add a new task to the todo list.

    Creates a new task with the provided title and optional description.
    The task is assigned a unique ID and stored with 'incomplete' status.

    Args:
        title: The task title (required, cannot be empty).
        description: Optional task description (defaults to empty string).

    Raises:
        SystemExit: If the title is empty or contains only whitespace.
    """
    try:
        cleaned_title = validate_title(title)
    except EmptyTitleError:
        print("Error: Task title cannot be empty")
        sys.exit(1)

    # Create a task with ID 0 to indicate it needs a new ID
    cleaned_description = description.strip() if description else ""

    task = Task(
        id=0,  # Will be assigned a proper ID by the storage
        title=cleaned_title,
        description=cleaned_description,
    )

    task = storage.add(task)
    print(f"Task added successfully! ID: {task.id}")
