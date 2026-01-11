# Todo CLI

A simple, fast, in-memory command-line todo application built with Python and Typer.

## Features

- **Add Task** - Create new tasks with title and optional description
- **List Tasks** - View all tasks with status filtering
- **Update Task** - Modify task title or description
- **Delete Task** - Remove tasks with confirmation
- **Toggle Status** - Mark tasks complete or incomplete

## Prerequisites

- Python 3.13 or higher
- UV package manager

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd todo
```

### 2. Install with UV

```bash
uv sync
```

### 3. Verify installation

```bash
uv run todo --version
```

## Quick Start

```bash
# Add your first task
uv run todo add "Learn Python"

# Add a task with description
uv run todo add "Read documentation" -d "Focus on Typer library"

# View all tasks
uv run todo list

# Mark a task complete
uv run todo toggle 1

# Delete a task
uv run todo delete 1 -f
```

## Usage

### Add a Task

Create a new task with a title and optional description.

```bash
# Basic usage
todo add "Task title"

# With description
todo add "Task title" -d "Task description"
todo add "Task title" --description "Task description"
```

**Examples:**
```bash
todo add "Buy groceries"
todo add "Complete report" -d "Q4 financial report by Friday"
todo add "Call mom" --description "Wish her happy birthday"
```

### List Tasks

View all tasks or filter by status.

```bash
# List all tasks
todo list

# Filter by status
todo list -s incomplete
todo list -s complete
todo list --status incomplete
```

**Output:**
```
┌──────────────┬─────────────────────┬────────────┬─────────────────────────┐
│ ID           │ Title               │ Status     │ Description             │
├──────────────┼─────────────────────┼────────────┼─────────────────────────┤
│ 1            │ Buy groceries       │ incomplete │ Milk, eggs, bread       │
│ 2            │ Complete report     │ complete   │ Q4 financial report     │
└──────────────┴─────────────────────┴────────────┴─────────────────────────┘

Total: 2 task(s) (1 complete, 1 incomplete)
```

### Update a Task

Modify a task's title and/or description.

```bash
# Update title
todo update <task_id> -t "New title"
todo update <task_id> --title "New title"

# Update description
todo update <task_id> -d "New description"
todo update <task_id> --description "New description"

# Update both
todo update <task_id> -t "New title" -d "New description"
```

**Examples:**
```bash
todo update 1 -t "Buy organic groceries"
todo update 1 -d "From the farmers market"
todo update 1 -t "Shopping" -d "Weekly groceries"
```

### Delete a Task

Remove a task from the list.

```bash
# With confirmation prompt
todo delete <task_id>

# Skip confirmation
todo delete <task_id> -f
todo delete <task_id> --force
```

**Examples:**
```bash
todo delete 1      # Asks for confirmation
todo delete 1 -f   # Deletes immediately
```

### Toggle Status

Switch a task between complete and incomplete.

```bash
todo toggle <task_id>
```

**Example:**
```bash
todo toggle 1
# Output: ✓ Task '1' marked as complete!
#         Title: Buy groceries
#         Status: incomplete → complete
```

## Command Reference

| Command | Description | Options |
|---------|-------------|---------|
| `todo add <title>` | Add a new task | `-d, --description` |
| `todo list` | List all tasks | `-s, --status` |
| `todo update <id>` | Update a task | `-t, --title`, `-d, --description` |
| `todo delete <id>` | Delete a task | `-f, --force` |
| `todo toggle <id>` | Toggle task status | - |
| `todo --version` | Show version | - |
| `todo --help` | Show help | - |

## Project Structure

```
todo/
├── src/todo/
│   ├── __init__.py      # Package metadata
│   ├── main.py          # CLI entry point
│   ├── exceptions.py    # Custom exceptions
│   ├── models/          # Data models
│   │   └── task.py      # Task dataclass
│   ├── storage/         # Storage layer
│   │   └── memory.py    # In-memory storage
│   ├── commands/        # CLI commands
│   │   ├── add.py
│   │   ├── list.py
│   │   ├── update.py
│   │   ├── delete.py
│   │   └── toggle.py
│   └── utils/           # Utilities
│       └── helpers.py
├── specs/               # Specifications
├── pyproject.toml       # Project config
└── README.md
```

## Technology Stack

- **Python 3.13+** - Modern Python with latest features
- **Typer** - CLI framework built on Click
- **UV** - Fast Python package manager
- **File-Based Storage** - Tasks are persisted in todos.json in the current directory

## Limitations

- No concurrent access support (single user)
- Task IDs are generated per session

## Development

### Run directly

```bash
cd src
python -m todo.main --help
```

### Run tests

```bash
python test_integration.py
```

## License

MIT License - see LICENSE file for details.

## Quick Reference - All Commands

### Adding Tasks
```bash
uv run todo add "Task title"
uv run todo add "Task title" -d "Task description"
```

### Listing Tasks
```bash
uv run todo list
uv run todo list -s complete      # Show only completed tasks
uv run todo list -s incomplete    # Show only incomplete tasks
```

### Updating Task Title
```bash
uv run todo update 1 -t "New title for task 1"
uv run todo update 2 -t "New title for task 2"
uv run todo update 3 -t "New title for task 3"
# ... and so on for any task ID
```

### Updating Task Description
```bash
uv run todo update 1 -d "New description for task 1"
uv run todo update 2 -d "New description for task 2"
uv run todo update 3 -d "New description for task 3"
# ... and so on for any task ID
```

### Updating Both Title and Description
```bash
uv run todo update 1 -t "New title" -d "New description"
uv run todo update 2 -t "New title" -d "New description"
uv run todo update 3 -t "New title" -d "New description"
# ... and so on for any task ID
```

### Toggling Task Status (Complete/Incomplete)
```bash
uv run todo toggle 1    # Toggle status of task 1
uv run todo toggle 2    # Toggle status of task 2
uv run todo toggle 3    # Toggle status of task 3
# ... and so on for any task ID
```

### Deleting Tasks
```bash
uv run todo delete 1        # Delete task 1 with confirmation prompt
uv run todo delete 1 -f     # Delete task 1 without confirmation (force)
uv run todo delete 2 -f     # Delete task 2 without confirmation (force)
uv run todo delete 3 -f     # Delete task 3 without confirmation (force)
# ... and so on for any task ID
```

### Help Commands
```bash
uv run todo --help          # Show all commands
uv run todo add --help      # Show help for add command
uv run todo update --help   # Show help for update command
uv run todo delete --help   # Show help for delete command
uv run todo toggle --help   # Show help for toggle command
uv run todo list --help     # Show help for list command
```

---

Built with Claude Code for Hackathon 2 Part 1 using SpecKit Plus framework.
