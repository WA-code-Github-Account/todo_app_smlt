"""Utility helper functions for the Todo CLI application.

This module provides common utilities including ID generation,
input validation, text formatting, and table rendering.
"""

from todo.exceptions import EmptyTitleError


def generate_task_id(last_id: int) -> int:
    """Generate a unique task identifier.

    Creates a task ID as a simple incrementing number.

    Args:
        last_id: The last used ID to increment from.

    Returns:
        A unique task ID integer.

    Example:
        >>> task_id = generate_task_id(5)
        >>> task_id  # 6
    """
    return last_id + 1


def validate_title(title: str) -> str:
    """Validate and clean a task title.

    Strips whitespace and validates that the title is not empty.

    Args:
        title: The task title to validate.

    Returns:
        The cleaned (stripped) title.

    Raises:
        EmptyTitleError: If the title is empty or contains only whitespace.
    """
    cleaned = title.strip()
    if not cleaned:
        raise EmptyTitleError()
    return cleaned


def truncate_text(text: str, max_length: int = 30) -> str:
    """Truncate text to a maximum length with ellipsis.

    If the text exceeds max_length, it is truncated and '...' is appended.

    Args:
        text: The text to truncate.
        max_length: Maximum allowed length (default: 30).

    Returns:
        The original text if within limit, or truncated text with '...'.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."


def format_table(headers: list[str], rows: list[list[str]], col_widths: list[int] | None = None) -> str:
    """Format data as an ASCII table.

    Creates a formatted table with borders using ASCII characters
    for Windows compatibility.

    Args:
        headers: List of column header strings.
        rows: List of rows, where each row is a list of cell values.
        col_widths: Optional list of column widths. If None, auto-calculated.

    Returns:
        A formatted table string ready for display.
    """
    if col_widths is None:
        col_widths = []
        for i, header in enumerate(headers):
            max_width = len(header)
            for row in rows:
                if i < len(row):
                    max_width = max(max_width, len(row[i]))
            col_widths.append(min(max_width, 25))

    def make_row(cells: list[str], sep: str = "|") -> str:
        padded = []
        for i, cell in enumerate(cells):
            width = col_widths[i] if i < len(col_widths) else 10
            padded.append(f" {cell:<{width}} ")
        return sep + sep.join(padded) + sep

    def make_separator(fill: str = "-") -> str:
        parts = []
        for width in col_widths:
            parts.append(fill * (width + 2))
        return "+" + "+".join(parts) + "+"

    lines = []
    lines.append(make_separator())
    lines.append(make_row(headers))
    lines.append(make_separator())

    for row in rows:
        padded_row = row + [""] * (len(headers) - len(row))
        lines.append(make_row(padded_row))

    lines.append(make_separator())

    return "\n".join(lines)
