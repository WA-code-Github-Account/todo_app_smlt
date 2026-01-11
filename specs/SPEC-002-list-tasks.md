# SPEC-002: List Tasks

**Feature ID:** FEAT-002
**Feature Name:** List Tasks
**Version:** 1.0.0
**Status:** DRAFT
**Author:** SW-001 (Spec Writer Subagent)
**Approved By:** PA-001 (Pending)
**Date:** 2025-12-30

---

## 1. Overview

### 1.1 User Story
> As a user, I want to view all my tasks with their status so that I can see what needs to be done.

### 1.2 Description
The List Tasks feature displays all tasks in the todo list with their ID, title, description, and status. Users can filter tasks by status (complete/incomplete) or view all tasks.

### 1.3 Priority
**P0 - Critical** (Core feature required for MVP)

---

## 2. Requirements

### 2.1 Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR-001 | System SHALL display all tasks by default | MUST |
| FR-002 | System SHALL show task ID, title, status, description | MUST |
| FR-003 | System SHALL support filtering by status | MUST |
| FR-004 | System SHALL display tasks in a formatted table | MUST |
| FR-005 | System SHALL show "No tasks found" when list is empty | MUST |
| FR-006 | System SHALL show task count in output | SHOULD |
| FR-007 | System SHALL truncate long descriptions in table view | SHOULD |
| FR-008 | System SHALL support --all flag to show all tasks | SHOULD |

### 2.2 Non-Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| NFR-001 | Command SHALL complete within 100ms | SHOULD |
| NFR-002 | Table format SHALL be readable in terminal | MUST |
| NFR-003 | Code SHALL follow PEP 8 standards | MUST |
| NFR-004 | All functions SHALL have type hints | MUST |
| NFR-005 | All public functions SHALL have docstrings | MUST |

---

## 3. Technical Design

### 3.1 CLI Interface

```
Command: todo list [options]

Options:
  -s, --status       Filter by status ('complete' or 'incomplete')
  -a, --all          Show all tasks (default behavior)
  -h, --help         Show help message

Examples:
  todo list                          # Show all tasks
  todo list -s incomplete            # Show only incomplete tasks
  todo list --status complete        # Show only completed tasks
  todo list -a                       # Show all tasks explicitly
```

### 3.2 Output Format

```
┌──────────────┬─────────────────────┬────────────┬─────────────────────────┐
│ ID           │ Title               │ Status     │ Description             │
├──────────────┼─────────────────────┼────────────┼─────────────────────────┤
│ task_a1b2c3  │ Buy groceries       │ incomplete │ Milk, eggs, bread       │
│ task_d4e5f6  │ Complete report     │ complete   │ Q4 financial report...  │
│ task_g7h8i9  │ Call mom            │ incomplete │                         │
└──────────────┴─────────────────────┴────────────┴─────────────────────────┘

Total: 3 tasks (1 complete, 2 incomplete)
```

### 3.3 Empty State Output

```
No tasks found.

Use 'todo add <title>' to create your first task.
```

### 3.4 Storage Interface

```python
def get_all_tasks() -> list[Task]:
    """Retrieve all tasks from storage.

    Returns:
        list[Task]: List of all tasks, may be empty.
    """

def get_tasks_by_status(status: str) -> list[Task]:
    """Retrieve tasks filtered by status.

    Args:
        status: Filter value ('complete' or 'incomplete').

    Returns:
        list[Task]: List of matching tasks.

    Raises:
        ValueError: If status is not 'complete' or 'incomplete'.
    """
```

### 3.5 Component Interaction

```
User Input
    │
    ▼
┌─────────────┐
│  CLI Layer  │  Parse arguments, validate filters
│  (main.py)  │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Command    │  Business logic for list
│  (list.py)  │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Storage    │  Retrieve tasks from memory
│ (memory.py) │
└─────────────┘
    │
    ▼
┌─────────────┐
│  Formatter  │  Format tasks as table
│ (helpers.py)│
└─────────────┘
    │
    ▼
Output (formatted table)
```

---

## 4. Acceptance Criteria

### 4.1 Happy Path

```gherkin
Scenario: List all tasks when tasks exist
  Given the todo list contains 3 tasks
  When I execute "todo list"
  Then I see a formatted table with all 3 tasks
  And each task shows ID, title, status, and description
  And I see the total count "Total: 3 tasks"

Scenario: List only incomplete tasks
  Given the todo list contains 2 complete and 3 incomplete tasks
  When I execute "todo list -s incomplete"
  Then I see a formatted table with only 3 incomplete tasks
  And I see the count "Total: 3 tasks (filtered)"

Scenario: List only complete tasks
  Given the todo list contains 2 complete and 3 incomplete tasks
  When I execute "todo list --status complete"
  Then I see a formatted table with only 2 complete tasks
  And I see the count "Total: 2 tasks (filtered)"
```

### 4.2 Edge Cases

```gherkin
Scenario: List tasks when no tasks exist
  Given the todo list is empty
  When I execute "todo list"
  Then I see the message "No tasks found."
  And I see the hint "Use 'todo add <title>' to create your first task."
  And the exit code is 0

Scenario: Filter returns no results
  Given the todo list contains only incomplete tasks
  When I execute "todo list -s complete"
  Then I see the message "No tasks found matching filter: complete"
  And the exit code is 0

Scenario: Long description truncation
  Given a task with a 100-character description
  When I execute "todo list"
  Then the description is truncated to 30 characters
  And "..." is appended to indicate truncation

Scenario: Long title handling
  Given a task with a 50-character title
  When I execute "todo list"
  Then the title is truncated to 25 characters
  And "..." is appended to indicate truncation
```

### 4.3 Error Scenarios

```gherkin
Scenario: Invalid status filter
  Given the todo application is running
  When I execute "todo list -s invalid"
  Then I see the error "Error: Invalid status filter. Use 'complete' or 'incomplete'"
  And the exit code is 1

Scenario: Invalid option provided
  Given the todo application is running
  When I execute "todo list --unknown"
  Then I see the error "Error: Unknown option: --unknown"
  And the exit code is 1
```

---

## 5. Test Cases

### 5.1 Unit Tests

| Test ID | Description | Input | Expected Output |
|---------|-------------|-------|-----------------|
| TC-001 | List all tasks | 3 tasks in storage | List of 3 tasks |
| TC-002 | List empty storage | No tasks | Empty list |
| TC-003 | Filter by incomplete | 2 complete, 3 incomplete | 3 incomplete tasks |
| TC-004 | Filter by complete | 2 complete, 3 incomplete | 2 complete tasks |
| TC-005 | Invalid status filter | status="invalid" | ValueError raised |
| TC-006 | Format table output | 2 tasks | Formatted table string |
| TC-007 | Truncate long description | 100 char desc | 30 chars + "..." |
| TC-008 | Count calculation | 5 tasks | "Total: 5 tasks" |

### 5.2 Integration Tests

| Test ID | Description | Steps | Expected Result |
|---------|-------------|-------|-----------------|
| IT-001 | CLI list all | Add 2 tasks, run `todo list` | Both tasks displayed |
| IT-002 | CLI filter | Add tasks, run `todo list -s complete` | Filtered results |
| IT-003 | Empty list display | Run `todo list` on empty | Empty message shown |

---

## 6. Error Handling

### 6.1 Error Codes

| Code | Name | Message | Cause |
|------|------|---------|-------|
| E101 | INVALID_STATUS | "Error: Invalid status filter. Use 'complete' or 'incomplete'" | Bad status value |
| E102 | INVALID_OPT | "Error: Unknown option: {option}" | Invalid CLI option |

### 6.2 Error Response Format

```
Error: {error_message}

Usage: todo list [options]

For more information, try 'todo list --help'
```

---

## 7. Dependencies

### 7.1 Internal Dependencies
- `models/task.py` - Task data model
- `storage/memory.py` - In-memory storage
- `utils/helpers.py` - Table formatting

### 7.2 External Dependencies
- Python 3.13+
- CLI framework (typer/argparse)

---

## 8. Implementation Notes

### 8.1 File Locations
```
src/todo/
├── commands/
│   └── list.py         # List command implementation
├── models/
│   └── task.py         # Task model
├── storage/
│   └── memory.py       # In-memory storage
└── utils/
    └── helpers.py      # Table formatting
```

### 8.2 Table Formatting Guidelines
- Column widths: ID (12), Title (20), Status (10), Description (25)
- Use box-drawing characters for borders
- Truncate with "..." for overflow
- Right-pad text for alignment

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
