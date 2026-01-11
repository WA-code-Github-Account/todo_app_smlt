"""Main CLI entry point for the Todo application.

This module defines the Typer application and wires up all commands.
"""

from typing import Annotated, Optional

import typer

from todo import __app_name__, __version__
from todo.commands.add import add_task
from todo.commands.delete import delete_task
from todo.commands.list import list_tasks
from todo.commands.toggle import toggle_status
from todo.commands.update import update_task

app = typer.Typer(
    name="todo",
    help="A simple CLI todo application for managing your tasks.",
    add_completion=False,
)


def version_callback(value: bool) -> None:
    """Display version information and exit."""
    if value:
        print(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            "-v",
            help="Show version and exit.",
            callback=version_callback,
            is_eager=True,
        ),
    ] = None,
) -> None:
    """Todo CLI - Manage your tasks from the command line."""
    pass


@app.command()
def add(
    title: Annotated[str, typer.Argument(help="The task title")],
    description: Annotated[
        str,
        typer.Option(
            "--description",
            "-d",
            help="Optional task description",
        ),
    ] = "",
) -> None:
    """Add a new task to your todo list."""
    add_task(title, description)


@app.command(name="list")
def list_cmd(
    status: Annotated[
        Optional[str],
        typer.Option(
            "--status",
            "-s",
            help="Filter by status: 'complete' or 'incomplete'",
        ),
    ] = None,
) -> None:
    """List all tasks or filter by status."""
    list_tasks(status)


@app.command()
def update(
    task_id: Annotated[str, typer.Argument(help="The task ID to update")],
    title: Annotated[
        Optional[str],
        typer.Option(
            "--title",
            "-t",
            help="New task title",
        ),
    ] = None,
    description: Annotated[
        Optional[str],
        typer.Option(
            "--description",
            "-d",
            help="New task description",
        ),
    ] = None,
) -> None:
    """Update an existing task's title or description."""
    update_task(task_id, title, description)


@app.command()
def delete(
    task_id: Annotated[str, typer.Argument(help="The task ID to delete")],
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Skip confirmation prompt",
        ),
    ] = False,
) -> None:
    """Delete a task from your todo list."""
    delete_task(task_id, force)


@app.command()
def toggle(
    task_id: Annotated[str, typer.Argument(help="The task ID to toggle")],
) -> None:
    """Toggle a task's status between complete and incomplete."""
    toggle_status(task_id)


if __name__ == "__main__":
    app()
