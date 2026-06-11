class Task:
    """Represents an assignable unit of work within a Project with an incremental ID tracker."""
    
    _id_counter = 0

    def __init__(self, title: str, project_title: str = "", assigned_to: str = "Unassigned", status: str = "Pending", task_id: int = None):
        self.title = title
        self.project_title = project_title
        self.assigned_to = assigned_to
        self.status = status
        
        if task_id is not None:
            self.task_id = task_id
            if task_id > Task._id_counter:
                Task._id_counter = task_id
        else:
            Task._id_counter += 1
            self.task_id = Task._id_counter

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not value.strip():
            raise ValueError("Task title cannot be empty.")
        self._title = value.strip()

    def mark_complete(self):
        self.status = "Completed"

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "project_title": self.project_title,
            "assigned_to": self.assigned_to,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            title=data["title"],
            project_title=data.get("project_title", ""),
            assigned_to=data.get("assigned_to", "Unassigned"),
            status=data.get("status", "Pending"),
            task_id=data.get("task_id")
        )
