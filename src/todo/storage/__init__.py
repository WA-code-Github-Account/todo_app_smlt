"""Storage package for the Todo CLI application.

This package contains storage implementations for persisting tasks.
Currently provides file-based storage with JSON persistence.
"""

from todo.storage.file import FileStorage, storage

__all__ = ["FileStorage", "storage"]
