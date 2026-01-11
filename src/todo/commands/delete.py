"""Delete command implementation for the Todo CLI application.

This module provides the functionality to delete tasks with confirmation.
"""

import sys

from todo.exceptions import TaskNotFoundError
from todo.models import Task
from todo.storage import storage


def confirm_deletion(task: Task) -> bool:
    """Prompt user to confirm task deletion.

    Displays task details and asks for confirmation.

    Args:
        task: The task to be deleted.

    Returns:
        True if user confirms deletion, False otherwise.
    """
    print("\nAre you sure you want to delete this task?\n")
    print(f"  ID:          {task.id}")
    print(f"  Title:       {task.title}")
    print(f"  Status:      {task.status}")
    print(f"  Description: {task.description or '(none)'}")
    print()

    while True:
        response = input("Delete this task? [y/N]: ").strip().lower()
        if response in ("y", "yes"):
            return True
        if response in ("n", "no", ""):
            return False
        print("Please enter 'y' or 'n': ", end="")


def delete_task(task_id: str, force: bool = False) -> None:
    """Delete a task from the todo list.

    By default, prompts for confirmation before deletion.
    Use force=True to skip the confirmation prompt.

    Args:
        task_id: The unique identifier of the task to delete.
        force: If True, skip confirmation prompt.

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

    if not force:
        if not confirm_deletion(task):
            print("Deletion cancelled.")
            return

    try:
        storage.delete(task_id_int)
        print(f"Task '{task_id_int}' deleted successfully!")
    except TaskNotFoundError:
        print(f"Error: Task '{task_id_int}' not found")
        sys.exit(1)
