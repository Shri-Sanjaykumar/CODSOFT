# Task 1: Advanced To-Do List Manager

This is a professional command-line task manager designed to help track tasks, priorities, and deadlines. It features JSON-based persistent storage, atomic writes to protect against database corruption, and real-time productivity statistics formatting.

---

## Technical Architecture

The application is structured using modular OOP patterns to separate concerns clearly:
1. **`models.py`:** Encapsulates the core `Task` model using Python's `dataclass` and enums for priority and status fields.
2. **`database.py`:** Handles system IO. Uses pathlib for platform-independent paths and performs atomic writes (via temp files) to avoid data loss.
3. **`manager.py`:** Executes the core business operations (filtering, sorting, and calculating statistics).
4. **`cli.py`:** Standard input/output loop formatting table views using `tabulate` and colors using `colorama`.
5. **`config.py`:** Central configuration defining constants, styles, and paths.

---

## Features
- **Add Tasks:** Set a title, description, priority (LOW, MEDIUM, HIGH), and custom due date.
- **Table View:** Clean rendering of active tasks aligned using standard tabular frames.
- **Automatic Persistence:** Automatic state saves on any modifying action.
- **Productivity Dashboard:** View total tasks, completion rates, and pending counts.
- **Search & Sort:** Instantly query tasks by keyword or sort them by due dates or priorities.
- **Atomic Operations:** Ensures data integrity by writing to a temporary file before replacing the target JSON database.
- **Graceful Interrupt Handling:** Captures KeyboardInterrupts (`Ctrl+C`) cleanly without raw traceback logs.

---

## Configuration Settings
Configurations are maintained in `src/config.py`:
- **Data Path:** Saved under `data/tasks.json`.
- **Logs Path:** Application operation logs written to `logs/application.log`.
- **Console Colors:** Mapped utilizing standard ANSI colors.

---

## Running the Application
To run the planner, navigate to the repository directory and run:

```bash
python Task_1_Todo_Manager/main.py
```
