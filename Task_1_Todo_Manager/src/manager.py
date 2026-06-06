import logging
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.config import LOG_FILE, DATA_FILE
from src.models import Task, Priority, Status
from src.database import JsonDatabase

# Setup Logging in UTF-8
logger = logging.getLogger("Task_1_Todo_Manager")
logger.setLevel(logging.INFO)

# Create file handler for UTF-8 logging
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


class TaskManager:
    """Manages business operations on tasks and handles persistent database sync."""

    def __init__(self) -> None:
        self.db = JsonDatabase(DATA_FILE)
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self) -> None:
        """Loads tasks from the database and maps them to Task objects."""
        raw_data = self.db.load_data()
        self.tasks = [Task.from_dict(item) for item in raw_data]
        logger.info(f"Loaded {len(self.tasks)} tasks from storage.")

    def save_tasks(self) -> None:
        """Serializes current tasks and updates the persistent storage."""
        raw_data = [task.to_dict() for task in self.tasks]
        self.db.save_data(raw_data)
        logger.info("Saved task database changes to disk.")

    def add_task(self, title: str, description: str, priority_str: str, due_date: str) -> Task:
        """Creates a new task and saves it to database."""
        # Find next available ID
        next_id = max([task.task_id for task in self.tasks], default=0) + 1
        
        priority = Priority.from_str(priority_str)
        task = Task(
            task_id=next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status=Status.PENDING,
            created_time=datetime.now().isoformat()
        )
        self.tasks.append(task)
        self.save_tasks()
        logger.info(f"Task Created - ID: {task.task_id}, Title: '{task.title}'")
        return task

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None,
                    priority_str: Optional[str] = None, due_date: Optional[str] = None) -> bool:
        """Updates properties of an existing task."""
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Failed to update - Task ID {task_id} not found.")
            return False

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description
        if priority_str is not None:
            task.priority = Priority.from_str(priority_str)
        if due_date is not None:
            task.due_date = due_date

        self.save_tasks()
        logger.info(f"Task Updated - ID: {task_id}")
        return True

    def delete_task(self, task_id: int) -> bool:
        """Removes a task from the planner."""
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Failed to delete - Task ID {task_id} not found.")
            return False

        self.tasks.remove(task)
        self.save_tasks()
        logger.info(f"Task Deleted - ID: {task_id}, Title: '{task.title}'")
        return True

    def mark_complete(self, task_id: int) -> bool:
        """Marks a task's status as completed."""
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Failed to complete - Task ID {task_id} not found.")
            return False

        task.status = Status.COMPLETED
        self.save_tasks()
        logger.info(f"Task Completed - ID: {task_id}, Title: '{task.title}'")
        return True

    def mark_pending(self, task_id: int) -> bool:
        """Reverts a completed task's status to pending."""
        task = self.get_task_by_id(task_id)
        if not task:
            logger.warning(f"Failed to mark pending - Task ID {task_id} not found.")
            return False

        task.status = Status.PENDING
        self.save_tasks()
        logger.info(f"Task Reverted to Pending - ID: {task_id}, Title: '{task.title}'")
        return True

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Utility function to retrieve a specific task object by ID."""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None

    def search_tasks(self, query: str) -> List[Task]:
        """Searches tasks containing query string in title or description (case-insensitive)."""
        q = query.lower()
        results = [
            task for task in self.tasks 
            if q in task.title.lower() or q in task.description.lower()
        ]
        logger.info(f"Searched for '{query}'. Found {len(results)} matches.")
        return results

    def get_sorted_tasks(self, sort_by: str) -> List[Task]:
        """Returns tasks sorted by priority (HIGH -> LOW) or due date."""
        if sort_by.lower() == "priority":
            priority_weights = {Priority.HIGH: 3, Priority.MEDIUM: 2, Priority.LOW: 1}
            return sorted(self.tasks, key=lambda t: priority_weights.get(t.priority, 0), reverse=True)
        elif sort_by.lower() == "due_date":
            # Tasks with empty/invalid dates sorted last
            return sorted(self.tasks, key=lambda t: t.due_date if t.due_date else "9999-12-31")
        return self.tasks

    def get_productivity_statistics(self) -> Dict[str, Any]:
        """Generates task metrics and statistics."""
        total = len(self.tasks)
        completed = sum(1 for t in self.tasks if t.status == Status.COMPLETED)
        pending = total - completed
        percentage = (completed / total * 100) if total > 0 else 0.0

        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "percentage": round(percentage, 2)
        }
