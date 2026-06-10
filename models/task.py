class Task:
    """Represents a discrete unit of work within a project."""
    VALID_STATUSES = {"Pending", "Completed"}

    def __init__(self, title: str, assigned_to: str, status: str = "Pending"):
        self.title = title
        self.assigned_to = assigned_to
        self.status = status  # e.g., Pending, Completed

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    @property
    def assigned_to(self) -> str:
        return self._assigned_to

    @assigned_to.setter
    def assigned_to(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Task assignee cannot be empty.")
        self._assigned_to = value.strip()

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str):
        if value not in self.VALID_STATUSES:
            allowed = ", ".join(sorted(self.VALID_STATUSES))
            raise ValueError(f"Task status must be one of: {allowed}.")
        self._status = value

    def mark_complete(self):
        """Updates the task status to Completed."""
        self.status = "Completed"

    def to_dict(self) -> dict:
        """Serializes the Task object to a dictionary."""
        return {"title": self.title, "assigned_to": self.assigned_to, "status": self.status}

    @classmethod
    def from_dict(cls, data: dict):
        """Creates a Task instance from a dictionary."""
        return cls(title=data["title"], assigned_to=data["assigned_to"], status=data.get("status", "Pending"))

    def __repr__(self) -> str:
        return f"<Task: {self.title} [{self.status}] -> Assigned to: {self.assigned_to}>"
