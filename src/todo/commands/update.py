"""Update command implementation for the Todo CLI application.

This module provides the functionality to update existing tasks.
"""

import sys

from todo.exceptions import EmptyTitleError, TaskNotFoundError
from todo.storage import storage
from todo.utils import validate_title


def update_task(
    task_id: str,  # Keep as str to accept user input, will convert to int
    title: str | None = None,
    description: str | None = None,
) -> None:
    """Update an existing task's title and/or description.

    At least one of title or description must be provided.
    Only the provided fields are updated; others remain unchanged.

    Args:
        task_id: The unique identifier of the task to update.
        title: New title (optional, None means no change).
        description: New description (optional, None means no change).

    Raises:
        SystemExit: If no fields provided, task not found, or title is empty.
    """
    if title is None and description is None:
        print("Error: At least one of --title or --description is required")
        sys.exit(1)

    # Convert the string task_id to an integer
    try:
        task_id_int = int(task_id)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Task IDs must be numbers.")
        sys.exit(1)

    cleaned_title: str | None = None
    if title is not None:
        try:
            cleaned_title = validate_title(title)
        except EmptyTitleError:
            print("Error: Title cannot be empty")
            sys.exit(1)

    cleaned_description: str | None = None
    if description is not None:
        cleaned_description = description.strip()

    try:
        storage.update(
            task_id=task_id_int,
            title=cleaned_title,
            description=cleaned_description,
        )
        print(f"Task '{task_id_int}' updated successfully!")
    except TaskNotFoundError:
        print(f"Error: Task '{task_id_int}' not found")
        sys.exit(1)
