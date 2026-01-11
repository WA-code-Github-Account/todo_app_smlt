# SPEC-005: Toggle Status

**Feature ID:** FEAT-005
**Feature Name:** Toggle Status (Mark Complete/Incomplete)
**Version:** 1.0.0
**Status:** DRAFT
**Author:** SW-001 (Spec Writer Subagent)
**Approved By:** PA-001 (Pending)
**Date:** 2025-12-30

---

## 1. Overview

### 1.1 User Story
> As a user, I want to mark a task as complete or incomplete so that I can track my progress on todo items.

### 1.2 Description
The Toggle Status feature allows users to flip a task's status between "complete" and "incomplete". If a task is incomplete, it becomes complete. If it's complete, it becomes incomplete. This provides a simple one-command way to manage task completion.

### 1.3 Priority
**P0 - Critical** (Core feature required for MVP)

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System SHALL accept task ID as required input | MUST |
| FR-002 | System SHALL validate task ID exists | MUST |
| FR-003 | System SHALL toggle incomplete → complete | MUST |
| FR-004 | System SHALL toggle complete → incomplete | MUST |
| FR-005 | System SHALL display the new status after toggle | MUST |
| FR-006 | System SHALL preserve all other task fields | MUST |
| FR-007 | System SHALL show visual indicator of status change | SHOULD |

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
Command: todo toggle <id>

Arguments:
  id                 Task ID (required, positional)

Options:
  -h, --help         Show help message

Examples:
  todo toggle task_a1b2c3
```

### 3.2 Output Format

**When toggling to complete:**
```
✓ Task 'task_a1b2c3' marked as complete!

  Title: Buy groceries
  Status: incomplete → complete
```

**When toggling to incomplete:**
```
○ Task 'task_a1b2c3' marked as incomplete.

  Title: Buy groceries
  Status: complete → incomplete
```

### 3.3 Storage Interface

```python
def toggle_task_status(task_id: str) -> Task:
    """Toggle a task's status between complete and incomplete.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        Task: The updated task with toggled status.

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
│  Command    │  Business logic for toggle
│ (toggle.py) │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Storage    │  Find task, flip status, save
│ (memory.py) │
└─────────────┘
    │
    ▼
Output (status change message)
```

### 3.5 Toggle Logic

```python
def execute_toggle(task_id: str) -> None:
    # 1. Find existing task
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise TaskNotFoundError(f"Task '{task_id}' not found")

    # 2. Record old status
    old_status = task.status

    # 3. Toggle status
    updated_task = storage.toggle_task_status(task_id)
    new_status = updated_task.status

    # 4. Display result with visual indicator
    if new_status == "complete":
        print(f"✓ Task '{task_id}' marked as complete!")
    else:
        print(f"○ Task '{task_id}' marked as incomplete.")

    print(f"\n  Title: {updated_task.title}")
    print(f"  Status: {old_status} → {new_status}")
```

### 3.6 Status Values

```python
class TaskStatus:
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"

def toggle(current: str) -> str:
    """Toggle between complete and incomplete status."""
    if current == TaskStatus.INCOMPLETE:
        return TaskStatus.COMPLETE
    return TaskStatus.INCOMPLETE
```

---

## 4. Acceptance Criteria

### 4.1 Happy Path

```gherkin
Scenario: Toggle incomplete task to complete
  Given a task exists with ID "task_abc123" and status "incomplete"
  When I execute "todo toggle task_abc123"
  Then the task status is changed to "complete"
  And I see "✓ Task 'task_abc123' marked as complete!"
  And I see "Status: incomplete → complete"

Scenario: Toggle complete task to incomplete
  Given a task exists with ID "task_abc123" and status "complete"
  When I execute "todo toggle task_abc123"
  Then the task status is changed to "incomplete"
  And I see "○ Task 'task_abc123' marked as incomplete."
  And I see "Status: complete → incomplete"

Scenario: Toggle same task multiple times
  Given a task exists with ID "task_abc123" and status "incomplete"
  When I execute "todo toggle task_abc123"
  Then the task status is "complete"
  When I execute "todo toggle task_abc123"
  Then the task status is "incomplete"
  When I execute "todo toggle task_abc123"
  Then the task status is "complete"
```

### 4.2 Edge Cases

```gherkin
Scenario: Task ID not found
  Given no task exists with ID "task_invalid"
  When I execute "todo toggle task_invalid"
  Then no task is modified
  And I see the error "Error: Task 'task_invalid' not found"
  And the exit code is 1

Scenario: Preserve other fields when toggling
  Given a task exists with ID "task_abc123"
  And the task has title "Buy groceries"
  And the task has description "Milk and eggs"
  When I execute "todo toggle task_abc123"
  Then the task status is toggled
  And the task title remains "Buy groceries"
  And the task description remains "Milk and eggs"
  And the task ID remains "task_abc123"

Scenario: Toggle newly created task
  Given I execute "todo add 'New task'"
  And the task is created with status "incomplete"
  When I execute "todo toggle {new_task_id}"
  Then the task status is changed to "complete"
```

### 4.3 Error Scenarios

```gherkin
Scenario: Missing required ID argument
  Given the todo application is running
  When I execute "todo toggle"
  Then I see the error "Error: Missing required argument: id"
  And usage help is displayed
  And the exit code is 1

Scenario: Invalid option provided
  Given the todo application is running
  When I execute "todo toggle task_abc123 --invalid"
  Then I see the error "Error: Unknown option: --invalid"
  And the exit code is 1

Scenario: Extra arguments provided
  Given the todo application is running
  When I execute "todo toggle task_abc123 extra_arg"
  Then I see the error "Error: Unexpected argument: extra_arg"
  And the exit code is 1
```

---

## 5. Test Cases

### 5.1 Unit Tests

| Test ID | Description | Input | Expected Output |
|---------|-------------|-------|-----------------|
| TC-001 | Toggle incomplete → complete | status="incomplete" | status="complete" |
| TC-002 | Toggle complete → incomplete | status="complete" | status="incomplete" |
| TC-003 | Task not found | invalid id | TaskNotFoundError |
| TC-004 | Preserve title after toggle | Toggle task | Title unchanged |
| TC-005 | Preserve description after toggle | Toggle task | Description unchanged |
| TC-006 | Preserve ID after toggle | Toggle task | ID unchanged |
| TC-007 | Double toggle returns original | Toggle twice | Original status |
| TC-008 | Triple toggle changes status | Toggle 3 times | Opposite of original |

### 5.2 Integration Tests

| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| IT-001 | CLI toggle to complete | Add task, run `todo toggle <id>` | Status is complete |
| IT-002 | CLI toggle to incomplete | Toggle complete task | Status is incomplete |
| IT-003 | Verify in list | Toggle task, run `todo list` | New status shown |
| IT-004 | Task not found | Run `todo toggle invalid` | Error displayed |

---

## 6. Error Handling

### 6.1 Error Codes

| Code | Name | Message | Cause |
|------|------|---------|-------|
| E401 | TASK_NOT_FOUND | "Error: Task '{id}' not found" | Invalid task ID |
| E402 | MISSING_ARG | "Error: Missing required argument: id" | No ID provided |
| E403 | INVALID_OPT | "Error: Unknown option: {option}" | Invalid CLI option |
| E404 | UNEXPECTED_ARG | "Error: Unexpected argument: {arg}" | Extra arguments |

### 6.2 Error Response Format

```
Error: {error_message}

Usage: todo toggle <id>

For more information, try 'todo toggle --help'
```

---

## 7. Dependencies

### 7.1 Internal Dependencies
- `models/task.py` - Task data model
- `storage/memory.py` - In-memory storage
- `utils/helpers.py` - Status constants

### 7.2 External Dependencies
- Python 3.13+
- CLI framework (typer/argparse)

---

## 8. Implementation Notes

### 8.1 File Locations
```
src/todo/
├── commands/
│   └── toggle.py       # Toggle command implementation
├── models/
│   └── task.py         # Task model with status
├── storage/
│   └── memory.py       # In-memory storage
└── utils/
    └── helpers.py      # Status constants
```

### 8.2 Visual Indicators
- `✓` (U+2713) - Check mark for complete
- `○` (U+25CB) - Circle for incomplete

**Fallback for terminals without Unicode:**
- `[x]` - For complete
- `[ ]` - For incomplete

### 8.3 Status Constants
```python
# In utils/helpers.py or models/task.py

class TaskStatus:
    """Task status constants."""
    INCOMPLETE: str = "incomplete"
    COMPLETE: str = "complete"

    @classmethod
    def toggle(cls, current: str) -> str:
        """Toggle between status values."""
        return cls.COMPLETE if current == cls.INCOMPLETE else cls.INCOMPLETE

    @classmethod
    def is_valid(cls, status: str) -> bool:
        """Check if status value is valid."""
        return status in (cls.INCOMPLETE, cls.COMPLETE)
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
