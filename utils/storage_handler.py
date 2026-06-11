import os
import json
from typing import List
from models.user import User
from models.project import Project
from models.task import Task

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'storage.json')


def get_data_file() -> str:
    """Returns the configured JSON storage path."""
    return os.environ.get("PROJECT_CLI_DATA_FILE", DEFAULT_DATA_FILE)

def load_data() -> tuple[List[User], List[Project], List[Task]]:
    """Loads all system entity states safely from localized JSON storage."""
    data_file = get_data_file()
    if not os.path.exists(data_file):
        return [], [], []
    
    try:
        with open(data_file, 'r') as f:
            raw_data = json.load(f)
            
        users = [User.from_dict(u) for u in raw_data.get("users", [])]

        # Backward compatibility for older files that stored projects at the top level.
        for project_data in raw_data.get("projects", []):
            owner = project_data.get("owner")
            project = Project.from_dict(project_data)
            if owner:
                user = next((u for u in users if u.name.lower() == owner.lower()), None)
                if user and not any(p.title.lower() == project.title.lower() for p in user.projects):
                    user.add_project(project)

        projects = [project for user in users for project in user.projects]
        tasks = [task for project in projects for task in project.tasks]
        return users, projects, tasks
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        return [], [], []

def save_data(users: List[User], projects: List[Project] = None, tasks: List[Task] = None):
    """Persists current state updates atomically back down to local storage."""
    data_file = get_data_file()
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    payload = {
        "users": [u.to_dict() for u in users]
    }
    with open(data_file, 'w') as f:
        json.dump(payload, f, indent=4)
