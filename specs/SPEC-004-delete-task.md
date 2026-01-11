# SPEC-004: Delete Task

**Feature ID:** FEAT-004
**Feature Name:** Delete Task
**Version:** 1.0.0
**Status:** DRAFT
**Author:** SW-001 (Spec Writer Subagent)
**Approved By:** PA-001 (Pending)
**Date:** 2025-12-30

---

## 1. Overview

### 1.1 User Story
> As a user, I want to delete a task from my todo list so that I can remove items that are no longer needed.

### 1.2 Description
The Delete Task feature allows users to permanently remove a task from the todo list using its unique ID. By default, the system asks for confirmation before deletion. Users can bypass confirmation using the --force flag.

### 1.3 Priority
**P0 - Critical** (Core feature required for MVP)

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System SHALL accept task ID as required input | MUST |
| FR-002 | System SHALL validate task ID exists | MUST |
| FR-003 | System SHALL prompt for confirmation by default | MUST |
| FR-004 | System SHALL support --force flag to skip confirmation | MUST |
| FR-005 | System SHALL permanently remove task from storage | MUST |
| FR-006 | System SHALL display confirmation after deletion | MUST |
| FR-007 | System SHALL abort if user declines confirmation | MUST |
| FR-008 | System SHALL display task details in confirmation prompt | SHOULD |

### 2.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-001 | Command SHALL complete within 100ms (excluding user input) | SHOULD |
| NFR-002 | Error messages SHALL be user-friendly | MUST |
| NFR-003 | Code SHALL follow PEP 8 standards | MUST |
| NFR-004 | All functions SHALL have type hints | MUST |
| NFR-005 | All public functions SHALL have docstrings | MUST |

---

## 3. Technical Design

### 3.1 CLI Interface

```
Command: todo delete <id> [options]

Arguments:
  id                 Task ID (required, positional)

Options:
  -f, --force        Skip confirmation prompt
  -h, --help         Show help message

Examples:
  todo delete task_a1b2c3              # Delete with confirmation
  todo delete task_a1b2c3 -f           # Delete without confirmation
  todo delete task_a1b2c3 --force      # Delete without confirmation
```

### 3.2 Confirmation Prompt

```
Are you sure you want to delete this task?

  ID:          task_a1b2c3
  Title:       Buy groceries
  Status:      incomplete
  Description: Milk, eggs, bread

Delete this task? [y/N]: _
```

### 3.3 Storage Interface

```python
def delete_task(task_id: str) -> bool:
    """Delete a task from storage.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        bool: True if task was deleted successfully.

    Raises:
        TaskNotFoundError: If no task exists with the given ID.
    """

def get_task_by_id(task_id: str) -> Task | None:
    """Retrieve a task by its ID.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        Task | None: The task if found, None otherwise.
    """
```

### 3.4 Component Interaction

```
User Input
    │
    ▼
┌─────────────┐
│  CLI Layer  │  Parse arguments, validate inputs
│  (main.py)  │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Command    │  Business logic for delete
│ (delete.py) │
└─────────────┘
    │
    ▼
┌─────────────┐         ┌─────────────┐
│  Storage    │◄────────│ Confirmation│  (if not --force)
│ (memory.py) │         │   Prompt    │
└─────────────┘         └─────────────┘
    │
    ▼
Output (confirmation message)
```

### 3.5 Delete Logic

```python
def execute_delete(task_id: str, force: bool = False) -> None:
    # 1. Find existing task
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task '{task_id}' not found")

    # 2. Confirm deletion (unless --force)
    if not force:
        if not confirm_deletion(task):
            print("Deletion cancelled.")
            return

    # 3. Delete from storage
    storage.delete_task(task_id)

    # 4. Display confirmation
    print(f"Task '{task_id}' deleted successfully!")
```

---

## 4. Acceptance Criteria

### 4.1 Happy Path

```gherkin
Scenario: Delete task with confirmation (user confirms)
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123"
  Then I see the confirmation prompt with task details
  When I enter "y"
  Then the task is removed from storage
  And I see the message "Task 'task_abc123' deleted successfully!"

Scenario: Delete task with --force flag
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123 --force"
  Then no confirmation prompt is shown
  And the task is removed from storage
  And I see the message "Task 'task_abc123' deleted successfully!"

Scenario: Delete task with -f flag
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123 -f"
  Then no confirmation prompt is shown
  And the task is removed from storage
  And I see the message "Task 'task_abc123' deleted successfully!"
```

### 4.2 Edge Cases

```gherkin
Scenario: Task ID not found
  Given no task exists with ID "task_invalid"
  When I execute "todo delete task_invalid"
  Then no confirmation prompt is shown
  And I see the error "Error: Task 'task_invalid' not found"
  And the exit code is 1

Scenario: User cancels deletion (enters 'n')
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123"
  Then I see the confirmation prompt
  When I enter "n"
  Then the task is NOT removed from storage
  And I see the message "Deletion cancelled."
  And the exit code is 0

Scenario: User cancels deletion (enters 'N')
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123"
  Then I see the confirmation prompt
  When I enter "N"
  Then the task is NOT removed from storage
  And I see the message "Deletion cancelled."

Scenario: User presses Enter (default is No)
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123"
  Then I see the confirmation prompt "[y/N]"
  When I press Enter without input
  Then the task is NOT removed from storage
  And I see the message "Deletion cancelled."

Scenario: User enters invalid response then valid
  Given a task exists with ID "task_abc123"
  When I execute "todo delete task_abc123"
  And I enter "maybe"
  Then I see "Please enter 'y' or 'n': "
  When I enter "y"
  Then the task is removed from storage

Scenario: Delete completed task
  Given a completed task exists with ID "task_abc123"
  When I execute "todo delete task_abc123 -f"
  Then the task is removed from storage
  And I see the message "Task 'task_abc123' deleted successfully!"
```

### 4.3 Error Scenarios

```gherkin
Scenario: Missing required ID argument
  Given the todo application is running
  When I execute "todo delete"
  Then I see the error "Error: Missing required argument: id"
  And usage help is displayed
  And the exit code is 1

Scenario: Invalid option provided
  Given the todo application is running
  When I execute "todo delete task_abc123 --invalid"
  Then I see the error "Error: Unknown option: --invalid"
  And the exit code is 1
```

---

## 5. Test Cases

### 5.1 Unit Tests

| Test ID | Description | Input | Expected Output |
|---------|-------------|-------|-----------------|
| TC-001 | Delete existing task | valid id | Task removed, True returned |
| TC-002 | Delete non-existent task | invalid id | TaskNotFoundError |
| TC-003 | Force flag bypasses confirm | force=True | No prompt, task deleted |
| TC-004 | User confirms deletion | input="y" | Task deleted |
| TC-005 | User cancels deletion | input="n" | Task not deleted |
| TC-006 | Default is No (Enter) | input="" | Task not deleted |
| TC-007 | Case insensitive confirm | input="Y" | Task deleted |
| TC-008 | Case insensitive cancel | input="N" | Task not deleted |

### 5.2 Integration Tests

| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| IT-001 | CLI delete with force | Add task, run `todo delete <id> -f` | Task removed |
| IT-002 | CLI task not found | Run `todo delete invalid` | Error displayed |
| IT-003 | Verify deletion | Delete task, run `todo list` | Task not in list |

---

## 6. Error Handling

### 6.1 Error Codes

| Code | Name | Message | Cause |
|------|------|---------|-------|
| E301 | TASK_NOT_FOUND | "Error: Task '{id}' not found" | Invalid task ID |
| E302 | MISSING_ARG | "Error: Missing required argument: id" | No ID provided |
| E303 | INVALID_OPT | "Error: Unknown option: {option}" | Invalid CLI option |

### 6.2 Error Response Format

```
Error: {error_message}

Usage: todo delete <id> [options]

For more information, try 'todo delete --help'
```

---

## 7. Dependencies

### 7.1 Internal Dependencies
- `models/task.py` - Task data model
- `storage/memory.py` - In-memory storage
- `utils/helpers.py` - Confirmation prompt utility

### 7.2 External Dependencies
- Python 3.13+
- CLI framework (typer/argparse)

---

## 8. Implementation Notes

### 8.1 File Locations
```
src/todo/
├── commands/
│   └── delete.py       # Delete command implementation
├── models/
│   └── task.py         # Task model
├── storage/
│   └── memory.py       # In-memory storage
└── utils/
    └── helpers.py      # Confirmation prompt
```

### 8.2 Confirmation Function
```python
def confirm_deletion(task: Task) -> bool:
    """Prompt user to confirm task deletion.

    Args:
        task: The task to be deleted.

    Returns:
        bool: True if user confirms, False otherwise.
    """
    print(f"\nAre you sure you want to delete this task?\n")
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
```

---

## 9. Approval

| Role | Agent | Status | Date |
|------|-------|--------|------|
| Author | SW-001 | COMPLETE | 2025-12-30 |
| Reviewer | PA-001 | PENDING | - |
| Approver | PA-001 | PENDING | - |

---

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-12-30 | SW-001 | Initial specification |
