from typing import List
from models.task import Task

class Project:
    """Represents a Project containing multiple tasks."""
    
    def __init__(self, title: str, description: str, due_date: str, tasks: List[Task] = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.tasks = tasks if tasks is not None else []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    def add_task(self, task: Task):
        """Appends a new task to the project workspace."""
        self.tasks.append(task)

    def find_task(self, title: str):
        """Finds a task by title within this project."""
        return next((task for task in self.tasks if task.title.lower() == title.lower()), None)

    def to_dict(self) -> dict:
        """Serializes the project object and nested task models into a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Factory method restoring deep nested Task structures inside Project instances."""
        tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return cls(
            title=data["title"],
            description=data["description"],
            due_date=data.get("due_date", "ASAP"),
            tasks=tasks
        )
