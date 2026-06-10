from typing import List
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
        if not value.strip():
            raise ValueError("Project title cannot be empty.")
        self._title = value

    def add_task(self, task: Task):
        """Appends a task object to the project's task collection."""
        self.tasks.append(task)

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
            owner=data["owner"]
        )
        project.tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
        return project

    def __repr__(self) -> str:
        return f"<Project: {self.title} (Owner: {self.owner}) - Tasks: {len(self.tasks)}>"