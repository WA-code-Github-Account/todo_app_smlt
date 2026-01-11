"""List command implementation for the Todo CLI application.

This module provides the functionality to list and filter tasks.
"""

import sys

from todo.models import TaskStatus
from todo.storage import storage
from todo.utils import format_table, truncate_text


def list_tasks(status: str | None = None) -> None:
    """List all tasks or filter by status.

    Displays tasks in a formatted table with ID, title, status, and description.
    Supports filtering by 'complete' or 'incomplete' status.

    Args:
        status: Optional filter ('complete' or 'incomplete').
                If None, all tasks are displayed.

    Raises:
        SystemExit: If an invalid status filter is provided.
    """
    if status is not None:
        if not TaskStatus.is_valid(status):
            print("Error: Invalid status filter. Use 'complete' or 'incomplete'")
            sys.exit(1)
        tasks = storage.get_by_status(status)
        filter_msg = f" (filtered: {status})"
    else:
        tasks = storage.get_all()
        filter_msg = ""

    if not tasks:
        if status:
            print(f"No tasks found matching filter: {status}")
        else:
            print("No tasks found.")
            print("\nUse 'todo add <title>' to create your first task.")
        return

    headers = ["ID", "Title", "Status", "Description"]
    rows = []

    for task in tasks:
        rows.append([
            str(task.id),  # Convert numeric ID to string for display
            truncate_text(task.title, 20),
            task.status,
            truncate_text(task.description, 25) if task.description else "",
        ])

    print(format_table(headers, rows, col_widths=[12, 20, 10, 25]))

    complete_count = sum(1 for t in tasks if t.status == TaskStatus.COMPLETE)
    incomplete_count = len(tasks) - complete_count

    print(f"\nTotal: {len(tasks)} task(s){filter_msg}", end="")
    if not status:
        print(f" ({complete_count} complete, {incomplete_count} incomplete)")
    else:
        print()
