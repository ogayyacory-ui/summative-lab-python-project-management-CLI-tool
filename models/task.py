class Task:
    """Represents an assignable unit of work within a Project."""

    VALID_STATUSES = {"Pending", "Completed"}

    def __init__(self, title: str, assigned_to: str = "Unassigned", status: str = "Pending"):
        self.title = title
        self.assigned_to = assigned_to
        self.status = status

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

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
        self.status = "Completed"

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            assigned_to=data.get("assigned_to", "Unassigned"),
            status=data.get("status", "Pending")
        )
