"""In-memory storage implementation for the Todo CLI application.

This module provides a simple dictionary-based storage backend for
managing tasks during a session. Data is not persisted between runs.
"""

from todo.exceptions import TaskNotFoundError
from todo.models import Task, TaskStatus


class TaskStorage:
    """In-memory storage for task management.

    Provides CRUD operations for tasks using a dictionary backend.
    Tasks are stored by their ID for efficient lookup.

    Attributes:
        _tasks: Private dictionary mapping task IDs to Task objects.
    """

    def __init__(self) -> None:
        """Initialize an empty task storage."""
        self._tasks: dict[str, Task] = {}

    def add(self, task: Task) -> Task:
        """Add a new task to storage.

        Args:
            task: The task to add.

        Returns:
            The added task.
        """
        self._tasks[task.id] = task
        return task

    def get_all(self) -> list[Task]:
        """Retrieve all tasks from storage.

        Returns:
            List of all tasks, may be empty.
        """
        return list(self._tasks.values())

    def get_by_id(self, task_id: str) -> Task | None:
        """Retrieve a task by its ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The task if found, None otherwise.
        """
        return self._tasks.get(task_id)

    def get_by_status(self, status: str) -> list[Task]:
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
        task_id: str,
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
            raise TaskNotFoundError(task_id)

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return task

    def delete(self, task_id: str) -> bool:
        """Delete a task from storage.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            True if the task was deleted successfully.

        Raises:
            TaskNotFoundError: If no task exists with the given ID.
        """
        if task_id not in self._tasks:
            raise TaskNotFoundError(task_id)

        del self._tasks[task_id]
        return True

    def toggle_status(self, task_id: str) -> Task:
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
            raise TaskNotFoundError(task_id)

        task.status = TaskStatus.toggle(task.status)
        return task

    def clear(self) -> None:
        """Remove all tasks from storage.

        Primarily useful for testing purposes.
        """
        self._tasks.clear()


# Module-level storage instance for use throughout the application
storage = TaskStorage()
