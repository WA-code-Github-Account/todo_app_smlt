"""File-based storage implementation for the Todo CLI application.

This module provides a JSON file-based storage backend for managing tasks
with persistence between sessions.
"""

import json
from pathlib import Path
from typing import Any, Dict, List

from todo.exceptions import TaskNotFoundError
from todo.models import Task, TaskStatus
from todo.utils import generate_task_id


class FileStorage:
    """File-based storage for task management.

    Provides CRUD operations for tasks using a JSON file backend.
    Tasks are stored persistently between sessions.

    Attributes:
        file_path: Path to the JSON file used for storage.
        _tasks: Private dictionary mapping task IDs to Task objects.
        _next_id: The next ID to assign to a new task.
    """

    def __init__(self, file_path: Path = None) -> None:
        """Initialize file-based storage.

        Args:
            file_path: Path to the JSON file for storage.
                      Defaults to Path("todos.json") in current directory.
        """
        self.file_path = file_path or Path("todos.json")
        self._tasks: Dict[int, Task] = {}  # Changed from str to int for numeric IDs
        self._next_id = 1
        self._load_from_file()

    def _load_from_file(self) -> None:
        """Load tasks from the JSON file."""
        if self.file_path.exists():
            try:
                with self.file_path.open("r", encoding="utf-8") as f:
                    data = json.load(f)
                    for task_data in data:
                        # Convert dict back to Task object
                        task = Task(
                            id=task_data["id"],
                            title=task_data["title"],
                            description=task_data["description"],
                            status=task_data["status"],
                            created_at=task_data["created_at"]  # Will be converted to datetime in Task
                        )
                        # Since datetime is stored as ISO string, we need to handle it properly
                        from datetime import datetime
                        task.created_at = datetime.fromisoformat(task_data["created_at"])
                        self._tasks[task.id] = task

                        # Update the next ID to be one more than the highest ID found
                        if task.id >= self._next_id:
                            self._next_id = task.id + 1
            except (json.JSONDecodeError, KeyError, TypeError):
                # If there's an error loading the file, start with empty storage
                self._tasks = {}
                self._next_id = 1
        else:
            # If file doesn't exist, start with empty storage
            self._tasks = {}
            self._next_id = 1

    def _save_to_file(self) -> None:
        """Save tasks to the JSON file."""
        # Convert tasks to dictionaries for JSON serialization
        data = []
        for task in self._tasks.values():
            task_dict = {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "created_at": task.created_at.isoformat()
            }
            data.append(task_dict)

        with self.file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def add(self, task: Task) -> Task:
        """Add a new task to storage.

        Args:
            task: The task to add.

        Returns:
            The added task.
        """
        # If the task doesn't have an ID yet, assign one
        if task.id is None or task.id == 0:
            task.id = self._next_id
            self._next_id = generate_task_id(self._next_id - 1)  # Increment the next ID

        self._tasks[task.id] = task
        self._save_to_file()
        return task

    def get_all(self) -> List[Task]:
        """Retrieve all tasks from storage.

        Returns:
            List of all tasks, may be empty.
        """
        return list(self._tasks.values())

    def get_by_id(self, task_id: int) -> Task | None:  # Changed from str to int
        """Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_by_status(self, status: str) -> List[Task]:
        """Retrieve tasks filtered by status.

        Args:
            status: Filter value ('complete' or 'incomplete').

        Returns:
            List of tasks matching the status filter.

        Raises:
            ValueError: If status is not 'complete' or 'incomplete'.
        """
        if not TaskStatus.is_valid(status):
            raise ValueError(
                f"Invalid status '{status}'. Use 'complete' or 'incomplete'."
            )
        return [task for task in self._tasks.values() if task.status == status]

    def update(
        self,
        task_id: int,  # Changed from str to int
        title: str | None = None,
        description: str | None = None,
    ) -> Task:
        """Update an existing task.

        Only the provided fields are updated; others remain unchanged.

        Args:
            task_id: The unique identifier of the task to update.
            title: New title (optional, None means no change).
            description: New description (optional, None means no change).

        Returns:
            The updated task.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(str(task_id))

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        self._save_to_file()
        return task

    def delete(self, task_id: int) -> bool:  # Changed from str to int
        """Delete a task from storage.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            True if the task was deleted successfully.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(str(task_id))

        del self._tasks[task_id]
        self._save_to_file()
        return True

    def toggle_status(self, task_id: int) -> Task:  # Changed from str to int
        """Toggle a task's status between complete and incomplete.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The updated task with toggled status.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        task = self._tasks.get(task_id)
        if task is None:
            raise TaskNotFoundError(str(task_id))

        task.status = TaskStatus.toggle(task.status)
        self._save_to_file()
        return task

    def clear(self) -> None:
        """Remove all tasks from storage.

        Primarily useful for testing purposes.
        """
        self._tasks.clear()
        self._next_id = 1
        self._save_to_file()


# Module-level storage instance for use throughout the application
storage = FileStorage()