from datetime import datetime
from typing import List, Optional
from models.task import Task

class Project:
    """Represents a project belonging to an owner, containing multiple tasks."""
    def __init__(self, title: str, description: str, due_date: str, owner: str, tasks: List[Task] = None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.owner = owner  # Links back to User.name (One-to-Many relationship)
        self.tasks = tasks if tasks is not None else []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value.strip()

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project description cannot be empty.")
        self._description = value.strip()

    @property
    def due_date(self) -> str:
        return self._due_date

    @due_date.setter
    def due_date(self, value: str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except (TypeError, ValueError) as exc:
            raise ValueError("Due date must use YYYY-MM-DD format.") from exc
        self._due_date = value

    @property
    def owner(self) -> str:
        return self._owner

    @owner.setter
    def owner(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Project owner cannot be empty.")
        self._owner = value.strip()

    def add_task(self, task: Task):
        """Appends a task object to the project's task collection."""
        if not isinstance(task, Task):
            raise TypeError("Project tasks must be Task instances.")
        if self.find_task(task.title):
            raise ValueError(f"Task '{task.title}' already exists in project '{self.title}'.")
        self.tasks.append(task)

    def find_task(self, title: str) -> Optional[Task]:
        """Returns a task by title, ignoring case."""
        return next((task for task in self.tasks if task.title.lower() == title.lower()), None)

    @property
    def progress(self) -> float:
        """Returns completion percentage across this project's tasks."""
        if not self.tasks:
            return 0.0
        completed = sum(task.status == "Completed" for task in self.tasks)
        return round((completed / len(self.tasks)) * 100, 1)

    def to_dict(self) -> dict:
        """Serializes the Project object (including sub-tasks) to a dictionary."""
        return {
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "owner": self.owner,
            "tasks": [task.to_dict() for task in self.tasks]
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Project instance complete with its nested Task collections from a dictionary."""
        project = cls(
            title=data["title"],
            description=data["description"],
            due_date=data["due_date"],
            owner=data["owner"],
            tasks=[Task.from_dict(t) for t in data.get("tasks", [])]
        )
        return project

    def __repr__(self) -> str:
        return f"<Project: {self.title} (Owner: {self.owner}) - Progress: {self.progress}%>"
