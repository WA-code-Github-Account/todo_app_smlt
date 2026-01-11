# SPEC-003: Update Task

**Feature ID:** FEAT-003
**Feature Name:** Update Task
**Version:** 1.0.0
**Status:** DRAFT
**Author:** SW-001 (Spec Writer Subagent)
**Approved By:** PA-001 (Pending)
**Date:** 2025-12-30

---

## 1. Overview

### 1.1 User Story
> As a user, I want to modify a task's title or description so that I can correct mistakes or add more detail.

### 1.2 Description
The Update Task feature allows users to modify the title and/or description of an existing task identified by its unique ID. Users can update one or both fields. Fields not specified remain unchanged.

### 1.3 Priority
**P0 - Critical** (Core feature required for MVP)

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System SHALL accept task ID as required input | MUST |
| FR-002 | System SHALL accept new title as optional input | MUST |
| FR-003 | System SHALL accept new description as optional input | MUST |
| FR-004 | System SHALL update only specified fields | MUST |
| FR-005 | System SHALL preserve unchanged fields | MUST |
| FR-006 | System SHALL validate task ID exists | MUST |
| FR-007 | System SHALL reject empty title if provided | MUST |
| FR-008 | System SHALL display confirmation after update | MUST |
| FR-009 | System SHALL require at least one field to update | MUST |
| FR-010 | System SHALL trim whitespace from inputs | SHOULD |

### 2.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-001 | Command SHALL complete within 100ms | SHOULD |
| NFR-002 | Error messages SHALL be user-friendly | MUST |
| NFR-003 | Code SHALL follow PEP 8 standards | MUST |
| NFR-004 | All functions SHALL have type hints | MUST |
| NFR-005 | All public functions SHALL have docstrings | MUST |

---

## 3. Technical Design

### 3.1 CLI Interface

```
Command: todo update <id> [options]

Arguments:
  id                 Task ID (required, positional)

Options:
  -t, --title        New task title (optional)
  -d, --description  New task description (optional)
  -h, --help         Show help message

Examples:
  todo update task_a1b2c3 -t "Buy organic groceries"
  todo update task_a1b2c3 -d "From the farmers market"
  todo update task_a1b2c3 -t "New title" -d "New description"
  todo update task_a1b2c3 --title "Updated" --description "Also updated"
```

### 3.2 Storage Interface

```python
def update_task(
    task_id: str,
    title: str | None = None,
    description: str | None = None
) -> Task:
    """Update an existing task.

    Args:
        task_id: The unique identifier of the task to update.
        title: New title (optional, None means no change).
        description: New description (optional, None means no change).

    Returns:
        Task: The updated task object.

    Raises:
        TaskNotFoundError: If no task exists with the given ID.
        ValueError: If title is provided but empty.
        ValueError: If neither title nor description is provided.
    """

def get_task_by_id(task_id: str) -> Task | None:
    """Retrieve a task by its ID.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        Task | None: The task if found, None otherwise.
    """
```

### 3.3 Component Interaction

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
│  Command    │  Business logic for update
│ (update.py) │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Storage    │  Find and update task in memory
│ (memory.py) │
└─────────────┘
    │
    ▼
Output (confirmation message)
```

### 3.4 Update Logic

```python
def execute_update(task_id: str, title: str | None, description: str | None) -> None:
    # 1. Validate at least one field provided
    if title is None and description is None:
        raise ValueError("At least one of --title or --description required")

    # 2. Find existing task
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task {task_id} not found")

    # 3. Validate new title if provided
    if title is not None and not title.strip():
        raise ValueError("Title cannot be empty")

    # 4. Update only provided fields
    updated_task = storage.update_task(
        task_id=task_id,
        title=title.strip() if title else None,
        description=description.strip() if description else None
    )

    # 5. Display confirmation
    print(f"Task {task_id} updated successfully!")
```

---

## 4. Acceptance Criteria

### 4.1 Happy Path

```gherkin
Scenario: Update task title only
  Given a task exists with ID "task_abc123" and title "Old title"
  When I execute "todo update task_abc123 -t 'New title'"
  Then the task title is changed to "New title"
  And the task description remains unchanged
  And I see the message "Task task_abc123 updated successfully!"

Scenario: Update task description only
  Given a task exists with ID "task_abc123" and description "Old desc"
  When I execute "todo update task_abc123 -d 'New description'"
  Then the task description is changed to "New description"
  And the task title remains unchanged
  And I see the message "Task task_abc123 updated successfully!"

Scenario: Update both title and description
  Given a task exists with ID "task_abc123"
  When I execute "todo update task_abc123 -t 'New title' -d 'New desc'"
  Then the task title is changed to "New title"
  And the task description is changed to "New desc"
  And I see the message "Task task_abc123 updated successfully!"
```

### 4.2 Edge Cases

```gherkin
Scenario: Task ID not found
  Given no task exists with ID "task_invalid"
  When I execute "todo update task_invalid -t 'New title'"
  Then no task is modified
  And I see the error "Error: Task 'task_invalid' not found"
  And the exit code is 1

Scenario: Empty title provided
  Given a task exists with ID "task_abc123"
  When I execute "todo update task_abc123 -t ''"
  Then no task is modified
  And I see the error "Error: Title cannot be empty"
  And the exit code is 1

Scenario: Whitespace-only title provided
  Given a task exists with ID "task_abc123"
  When I execute "todo update task_abc123 -t '   '"
  Then no task is modified
  And I see the error "Error: Title cannot be empty"
  And the exit code is 1

Scenario: No update fields provided
  Given a task exists with ID "task_abc123"
  When I execute "todo update task_abc123"
  Then no task is modified
  And I see the error "Error: At least one of --title or --description is required"
  And the exit code is 1

Scenario: Update description to empty (clear it)
  Given a task exists with ID "task_abc123" with description "Old desc"
  When I execute "todo update task_abc123 -d ''"
  Then the task description is changed to empty string
  And I see the message "Task task_abc123 updated successfully!"

Scenario: Preserve status during update
  Given a task exists with ID "task_abc123" and status "complete"
  When I execute "todo update task_abc123 -t 'New title'"
  Then the task status remains "complete"
  And the task title is changed to "New title"
```

### 4.3 Error Scenarios

```gherkin
Scenario: Missing required ID argument
  Given the todo application is running
  When I execute "todo update"
  Then I see the error "Error: Missing required argument: id"
  And usage help is displayed
  And the exit code is 1

Scenario: Invalid option provided
  Given the todo application is running
  When I execute "todo update task_abc123 --invalid"
  Then I see the error "Error: Unknown option: --invalid"
  And the exit code is 1
```

---

## 5. Test Cases

### 5.1 Unit Tests

| Test ID | Description | Input | Expected Output |
|---------|-------------|-------|-----------------|
| TC-001 | Update title only | id, title="New" | Title updated, desc unchanged |
| TC-002 | Update description only | id, desc="New" | Desc updated, title unchanged |
| TC-003 | Update both fields | id, title, desc | Both updated |
| TC-004 | Task not found | invalid_id | TaskNotFoundError |
| TC-005 | Empty title rejected | id, title="" | ValueError |
| TC-006 | No fields provided | id only | ValueError |
| TC-007 | Clear description | id, desc="" | Desc cleared |
| TC-008 | Status preserved | update complete task | Status unchanged |
| TC-009 | Whitespace trimmed | title="  test  " | title="test" |

### 5.2 Integration Tests

| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| IT-001 | CLI update title | Add task, run `todo update <id> -t "New"` | Title changed |
| IT-002 | CLI task not found | Run `todo update invalid -t "New"` | Error displayed |
| IT-003 | CLI no fields | Run `todo update <id>` | Error displayed |

---

## 6. Error Handling

### 6.1 Error Codes

| Code | Name | Message | Cause |
|------|------|---------|-------|
| E201 | TASK_NOT_FOUND | "Error: Task '{id}' not found" | Invalid task ID |
| E202 | EMPTY_TITLE | "Error: Title cannot be empty" | Empty/whitespace title |
| E203 | NO_FIELDS | "Error: At least one of --title or --description is required" | No update fields |
| E204 | MISSING_ARG | "Error: Missing required argument: id" | No ID provided |
| E205 | INVALID_OPT | "Error: Unknown option: {option}" | Invalid CLI option |

### 6.2 Error Response Format

```
Error: {error_message}

Usage: todo update <id> [options]

For more information, try 'todo update --help'
```

---

## 7. Dependencies

### 7.1 Internal Dependencies
- `models/task.py` - Task data model
- `storage/memory.py` - In-memory storage
- `utils/helpers.py` - Validation utilities

### 7.2 External Dependencies
- Python 3.13+
- CLI framework (typer/argparse)

---

## 8. Implementation Notes

### 8.1 File Locations
```
src/todo/
├── commands/
│   └── update.py       # Update command implementation
├── models/
│   └── task.py         # Task model
├── storage/
│   └── memory.py       # In-memory storage
└── utils/
    └── helpers.py      # Validation utilities
```

### 8.2 Custom Exceptions
```python
class TaskNotFoundError(Exception):
    """Raised when a task ID does not exist in storage."""
    pass
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
