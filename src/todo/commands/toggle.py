"""Toggle command implementation for the Todo CLI application.

This module provides the functionality to toggle task status
between complete and incomplete.
"""

import sys

from todo.exceptions import TaskNotFoundError
from todo.models import TaskStatus
from todo.storage import storage


def toggle_status(task_id: str) -> None:
    """Toggle a task's status between complete and incomplete.

    If the task is incomplete, it becomes complete.
    If the task is complete, it becomes incomplete.

    Args:
        task_id: The unique identifier of the task to toggle.

    Raises:
        SystemExit: If the task is not found.
    """
    # Convert the string task_id to an integer
    try:
        task_id_int = int(task_id)
    except ValueError:
        print(f"Error: Invalid task ID '{task_id}'. Task IDs must be numbers.")
        sys.exit(1)

    task = storage.get_by_id(task_id_int)
    if task is None:
        print(f"Error: Task '{task_id_int}' not found")
        sys.exit(1)

    old_status = task.status

    try:
        updated_task = storage.toggle_status(task_id_int)
        new_status = updated_task.status

        if new_status == TaskStatus.COMPLETE:
            print(f"[x] Task '{task_id_int}' marked as complete!")
        else:
            print(f"[ ] Task '{task_id_int}' marked as incomplete.")

        print(f"\n  Title: {updated_task.title}")
        print(f"  Status: {old_status} -> {new_status}")

    except TaskNotFoundError:
        print(f"Error: Task '{task_id_int}' not found")
        sys.exit(1)
