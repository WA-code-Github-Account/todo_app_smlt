"""Task model for the Todo CLI application.

This module defines the Task dataclass and TaskStatus constants used
to represent and manage todo items throughout the application.
"""

from dataclasses import dataclass, field
from datetime import datetime


class TaskStatus:
    """Constants and utilities for task status values.

    Attributes:
        INCOMPLETE: Status value for tasks not yet completed.
        COMPLETE: Status value for completed tasks.
    """

    INCOMPLETE: str = "incomplete"
    COMPLETE: str = "complete"

    @classmethod
    def toggle(cls, current: str) -> str:
        """Toggle between complete and incomplete status.

        Args:
            current: The current status value.

        Returns:
            The opposite status value.
        """
        if current == cls.INCOMPLETE:
            return cls.COMPLETE
        return cls.INCOMPLETE

    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Check if a status value is valid.

        Args:
            status: The status value to validate.

        Returns:
            True if the status is valid, False otherwise.
        """
        return status in (cls.INCOMPLETE, cls.COMPLETE)


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique identifier for the task.
        title: Task title (required, non-empty).
        description: Task description (optional, defaults to empty string).
        status: Task status ('incomplete' or 'complete').
        created_at: Timestamp when the task was created.
    """

    id: int  # Changed from str to int for numeric IDs
    title: str
    description: str = ""
    status: str = field(default=TaskStatus.INCOMPLETE)
    created_at: datetime = field(default_factory=datetime.now)

    def is_complete(self) -> bool:
        """Check if the task is marked as complete.

        Returns:
            True if the task status is 'complete', False otherwise.
        """
        return self.status == TaskStatus.COMPLETE
