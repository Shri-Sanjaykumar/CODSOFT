from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Dict, Any

class Priority(Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"

    @classmethod
    def from_str(cls, value: str) -> "Priority":
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.MEDIUM


class Status(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"

    @classmethod
    def from_str(cls, value: str) -> "Status":
        try:
            return cls[value.upper()]
        except KeyError:
            return cls.PENDING


@dataclass
class Task:
    """Represents a single productivity task in the planner."""
    task_id: int
    title: str
    description: str
    priority: Priority
    due_date: str  # YYYY-MM-DD
    status: Status
    created_time: str  # ISO Format

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the task to a dictionary format suitable for JSON storage."""
        data = asdict(self)
        data["priority"] = self.priority.value
        data["status"] = self.status.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Deserializes a dictionary into a Task object."""
        return cls(
            task_id=int(data["task_id"]),
            title=str(data["title"]),
            description=str(data["description"]),
            priority=Priority.from_str(data.get("priority", "MEDIUM")),
            due_date=str(data["due_date"]),
            status=Status.from_str(data.get("status", "PENDING")),
            created_time=str(data.get("created_time", datetime.now().isoformat()))
        )
