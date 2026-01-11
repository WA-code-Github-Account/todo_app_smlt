"""Custom exceptions for the Todo CLI application.

This module defines the exception hierarchy used throughout the application
for handling various error conditions in a consistent manner.
"""


class TodoError(Exception):
    """Base exception for all Todo CLI errors.

    All custom exceptions in the todo application inherit from this class,
    allowing for catch-all exception handling when needed.

    Args:
        message: Human-readable error description.
    """

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)


class TaskNotFoundError(TodoError):
    """Raised when a task with the specified ID does not exist.

    Args:
        task_id: The ID of the task that was not found.
    """

    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task '{task_id}' not found")


class ValidationError(TodoError):
    """Raised when input validation fails.

    Args:
        message: Description of the validation failure.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)


class EmptyTitleError(ValidationError):
    """Raised when a task title is empty or contains only whitespace.

    Args:
        message: Optional custom message. Defaults to standard empty title message.
    """

    def __init__(self, message: str = "Task title cannot be empty") -> None:
        super().__init__(message)
