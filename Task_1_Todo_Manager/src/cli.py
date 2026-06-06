import sys
import logging
from datetime import datetime
from tabulate import tabulate

from src.config import (
    APP_NAME, VERSION, AUTHOR, INTERNSHIP,
    COLOR_HEADER, COLOR_SUCCESS, COLOR_WARNING, COLOR_ERROR, COLOR_MUTED, COLOR_RESET
)
from src.manager import TaskManager, logger

def print_banner() -> None:
    """Displays the application's startup banner and metadata."""
    banner = f"""
{COLOR_HEADER}======================================================================
  _____          _      _       _        _        _     _ 
 |_   _|__    __| | ___| |     (_)___  _| |_     | |   (_)___| |_ 
   | |/ _ \\  / _` |/ _ \\ |     | / __|/ _` __|    | |   | / __| __|
   | | (_) || (_| |  __/ |___  | \\__ \\ (_| |_     | |___| \\__ \\ |_ 
   |_|\\___/  \\__,_|\\___|_____| |_|___/\\__,\\__|    |_____|_|___/\\__|
                                                                   
{APP_NAME}
Version: {VERSION}
Author: {AUTHOR}
Internship: {INTERNSHIP}
======================================================================{COLOR_RESET}"""
    print(banner)

def print_help() -> None:
    """Displays commands and instructions."""
    print(f"\n{COLOR_HEADER}--- HELP & USAGE INSTRUCTIONS ---{COLOR_RESET}")
    print("This application allows you to manage tasks with priority, status, and due dates.")
    print("\nAvailable Operations:")
    print("  [1] Add Task          - Enter title, description, priority (LOW/MEDIUM/HIGH), and due date.")
    print("  [2] View All Tasks    - Displays tasks in a formatted table.")
    print("  [3] Update Task       - Update specific fields of a task by its ID.")
    print("  [4] Delete Task       - Remove a task by its ID (requires confirmation).")
    print("  [5] Complete Task     - Mark a task's status as COMPLETED.")
    print("  [6] Mark Pending      - Revert a task's status to PENDING.")
    print("  [7] Search Tasks      - Find tasks by a search term.")
    print("  [8] Sort Tasks        - Sort tasks by priority level or due date.")
    print("  [9] Productivity Stats- Display total, completed, pending, and percentage.")
    print("  [A] About Project     - Show metadata and internship info.")
    print("  [H] Help              - Print this instruction manual.")
    print("  [V] Version Info      - Print current app version.")
    print("  [Q] Quit              - Safely save all files and exit.")
    print(f"{COLOR_MUTED}* Date format expected: YYYY-MM-DD (e.g. 2026-06-30){COLOR_RESET}")

def print_about() -> None:
    """Displays information about the project development context."""
    print(f"\n{COLOR_HEADER}--- ABOUT THIS PROJECT ---{COLOR_RESET}")
    print(f"Application:   {APP_NAME}")
    print(f"Version:       {VERSION}")
    print(f"Developer:     {AUTHOR}")
    print(f"Internship:    {INTERNSHIP}")
    print("Organization:  CODSOFT")
    print("\nTechnical Highlights:")
    print(" - Modular implementation pattern following PEP-8.")
    print(" - Dataclass modelling with enum type safety.")
    print(" - Safe atomic file system writes via temporary files.")
    print(" - UTF-8 character encoding support across all layers.")
    print(" - UTF-8 application event logger saved to logs/application.log.")

def print_version() -> None:
    """Displays current software version."""
    print(f"\n{COLOR_SUCCESS}{APP_NAME} - Version {VERSION}{COLOR_RESET}")

def validate_date(date_str: str) -> bool:
    """Validates date format to match YYYY-MM-DD."""
    if not date_str:
        return True  # Due date can be optional
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def get_tasks_table(tasks) -> str:
    """Formats tasks into a beautiful aligned table using tabulate."""
    if not tasks:
        return f"{COLOR_WARNING}No tasks registered in the system.{COLOR_RESET}"
    
    headers = ["ID", "Title", "Priority", "Due Date", "Status", "Created"]
    table_data = []
    for t in tasks:
        # Format colors depending on priority and status
        p_color = COLOR_RESET
        if t.priority.value == "HIGH":
            p_color = COLOR_ERROR
        elif t.priority.value == "MEDIUM":
            p_color = COLOR_WARNING
        else:
            p_color = COLOR_MUTED
            
        s_color = COLOR_SUCCESS if t.status.value == "COMPLETED" else COLOR_WARNING
        
        created_formatted = datetime.fromisoformat(t.created_time).strftime("%Y-%m-%d %H:%M")
        
        table_data.append([
            t.task_id,
            t.title,
            f"{p_color}{t.priority.value}{COLOR_RESET}",
            t.due_date if t.due_date else "N/A",
            f"{s_color}{t.status.value}{COLOR_RESET}",
            created_formatted
        ])
        
    return tabulate(table_data, headers=headers, tablefmt="fancy_grid")

class TodoCLI:
    """Runs the main terminal execution interface for Task Manager."""

    def __init__(self) -> None:
        self.manager = TaskManager()

    def run(self) -> None:
        """Starts the interactive session loop."""
        logger.info("Application started session.")
        print_banner()
        print_help()
        
        while True:
            try:
                print(f"\n{COLOR_HEADER}====================================={COLOR_RESET}")
                choice = input(f"{COLOR_HEADER}Enter menu option [1-9, A, H, V, Q]: {COLOR_RESET}").strip().upper()
                
                if choice == "1":
                    self.add_task_menu()
                elif choice == "2":
                    self.view_tasks_menu()
                elif choice == "3":
                    self.update_task_menu()
                elif choice == "4":
                    self.delete_task_menu()
                elif choice == "5":
                    self.complete_task_menu()
                elif choice == "6":
                    self.pending_task_menu()
                elif choice == "7":
                    self.search_tasks_menu()
                elif choice == "8":
                    self.sort_tasks_menu()
                elif choice == "9":
                    self.statistics_menu()
                elif choice == "A":
                    print_about()
                elif choice == "H":
                    print_help()
                elif choice == "V":
                    print_version()
                elif choice == "Q":
                    self.quit_app()
                    break
                else:
                    print(f"{COLOR_ERROR}Invalid selection. Press 'H' to view options.{COLOR_RESET}")
            except KeyboardInterrupt:
                # Handle Ctrl+C gracefully
                print(f"\n\n{COLOR_WARNING}KeyboardInterrupt detected. Saving database and shutting down...{COLOR_RESET}")
                self.quit_app()
                break
            except Exception as e:
                print(f"{COLOR_ERROR}An unexpected error occurred: {e}{COLOR_RESET}")
                logger.error(f"Global CLI Error: {e}", exc_info=True)

    def add_task_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- ADD NEW TASK ---{COLOR_RESET}")
        title = input("Enter Task Title: ").strip()
        if not title:
            print(f"{COLOR_ERROR}Validation Error: Title cannot be empty.{COLOR_RESET}")
            return
            
        description = input("Enter Task Description: ").strip()
        
        priority = input("Enter Priority (LOW, MEDIUM, HIGH) [Default: MEDIUM]: ").strip().upper()
        if priority and priority not in ["LOW", "MEDIUM", "HIGH"]:
            print(f"{COLOR_ERROR}Validation Error: Priority must be LOW, MEDIUM, or HIGH.{COLOR_RESET}")
            return
        if not priority:
            priority = "MEDIUM"

        due_date = input("Enter Due Date (YYYY-MM-DD) [Optional]: ").strip()
        if due_date and not validate_date(due_date):
            print(f"{COLOR_ERROR}Validation Error: Date must match YYYY-MM-DD format.{COLOR_RESET}")
            return
            
        task = self.manager.add_task(title, description, priority, due_date)
        print(f"{COLOR_SUCCESS}Success: Task added successfully with ID: {task.task_id}{COLOR_RESET}")

    def view_tasks_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- CURRENT TASKS LIST ---{COLOR_RESET}")
        print(get_tasks_table(self.manager.tasks))

    def update_task_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- UPDATE TASK FIELDS ---{COLOR_RESET}")
        try:
            task_id = int(input("Enter ID of task to update: ").strip())
        except ValueError:
            print(f"{COLOR_ERROR}Validation Error: Task ID must be an integer.{COLOR_RESET}")
            return

        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"{COLOR_ERROR}Error: Task with ID {task_id} not found.{COLOR_RESET}")
            return

        print(f"{COLOR_MUTED}Leaving a field empty keeps current value.{COLOR_RESET}")
        
        title = input(f"New Title [{task.title}]: ").strip()
        title = title if title else None
        
        description = input(f"New Description [{task.description}]: ").strip()
        description = description if description else None
        
        priority = input(f"New Priority ({task.priority.value}) [LOW, MEDIUM, HIGH]: ").strip().upper()
        if priority and priority not in ["LOW", "MEDIUM", "HIGH"]:
            print(f"{COLOR_ERROR}Validation Error: Priority must be LOW, MEDIUM, or HIGH.{COLOR_RESET}")
            return
        priority = priority if priority else None

        due_date = input(f"New Due Date ({task.due_date if task.due_date else 'None'}) [YYYY-MM-DD]: ").strip()
        if due_date and not validate_date(due_date):
            print(f"{COLOR_ERROR}Validation Error: Date must match YYYY-MM-DD format.{COLOR_RESET}")
            return
        due_date = due_date if due_date else None

        if self.manager.update_task(task_id, title, description, priority, due_date):
            print(f"{COLOR_SUCCESS}Success: Task updated successfully.{COLOR_RESET}")
        else:
            print(f"{COLOR_ERROR}Error: Task update failed.{COLOR_RESET}")

    def delete_task_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- DELETE TASK ---{COLOR_RESET}")
        try:
            task_id = int(input("Enter ID of task to delete: ").strip())
        except ValueError:
            print(f"{COLOR_ERROR}Validation Error: Task ID must be an integer.{COLOR_RESET}")
            return

        task = self.manager.get_task_by_id(task_id)
        if not task:
            print(f"{COLOR_ERROR}Error: Task with ID {task_id} not found.{COLOR_RESET}")
            return

        confirm = input(f"{COLOR_WARNING}Are you sure you want to delete Task '{task.title}'? (y/N): {COLOR_RESET}").strip().lower()
        if confirm == 'y':
            if self.manager.delete_task(task_id):
                print(f"{COLOR_SUCCESS}Success: Task deleted successfully.{COLOR_RESET}")
            else:
                print(f"{COLOR_ERROR}Error: Delete operation failed.{COLOR_RESET}")
        else:
            print(f"{COLOR_MUTED}Delete operation cancelled.{COLOR_RESET}")

    def complete_task_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- MARK TASK COMPLETE ---{COLOR_RESET}")
        try:
            task_id = int(input("Enter ID of task to complete: ").strip())
        except ValueError:
            print(f"{COLOR_ERROR}Validation Error: Task ID must be an integer.{COLOR_RESET}")
            return

        if self.manager.mark_complete(task_id):
            print(f"{COLOR_SUCCESS}Success: Task marked as COMPLETED.{COLOR_RESET}")
        else:
            print(f"{COLOR_ERROR}Error: Task ID not found.{COLOR_RESET}")

    def pending_task_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- MARK TASK PENDING ---{COLOR_RESET}")
        try:
            task_id = int(input("Enter ID of task: ").strip())
        except ValueError:
            print(f"{COLOR_ERROR}Validation Error: Task ID must be an integer.{COLOR_RESET}")
            return

        if self.manager.mark_pending(task_id):
            print(f"{COLOR_SUCCESS}Success: Task marked as PENDING.{COLOR_RESET}")
        else:
            print(f"{COLOR_ERROR}Error: Task ID not found.{COLOR_RESET}")

    def search_tasks_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- SEARCH TASKS ---{COLOR_RESET}")
        query = input("Enter search keyword: ").strip()
        if not query:
            print(f"{COLOR_ERROR}Validation Error: Search query cannot be empty.{COLOR_RESET}")
            return
            
        results = self.manager.search_tasks(query)
        print(f"\nFound {len(results)} matches:")
        print(get_tasks_table(results))

    def sort_tasks_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- SORT TASKS ---{COLOR_RESET}")
        sort_choice = input("Sort by [priority / due_date]: ").strip().lower()
        if sort_choice not in ["priority", "due_date"]:
            print(f"{COLOR_ERROR}Validation Error: Choose 'priority' or 'due_date'.{COLOR_RESET}")
            return
            
        sorted_list = self.manager.get_sorted_tasks(sort_choice)
        print(get_tasks_table(sorted_list))

    def statistics_menu(self) -> None:
        print(f"\n{COLOR_HEADER}--- PRODUCTIVITY STATISTICS ---{COLOR_RESET}")
        stats = self.manager.get_productivity_statistics()
        
        # Format a dashboard card
        card = f"""┌──────────────────────────────────────┐
│  Productivity Dashboard              │
├──────────────────────────────────────┤
│  Total Tasks Registered : {stats['total']:<10} │
│  Completed Tasks        : {stats['completed']:<10} │
│  Pending Tasks          : {stats['pending']:<10} │
│  Completion Progress    : {stats['percentage']:<9}% │
└──────────────────────────────────────┘"""
        print(COLOR_SUCCESS + card + COLOR_RESET)

    def quit_app(self) -> None:
        """Saves current state and prints a parting signature."""
        print(f"\n{COLOR_SUCCESS}Saving database. Thank you for using To-Do List Manager!{COLOR_RESET}")
        logger.info("Application session shutdown successfully.")
        sys.exit(0)
