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
        projects = [Project.from_dict(p) for p in raw_data.get("projects", [])]
        tasks = [Task.from_dict(t) for t in raw_data.get("tasks", [])]
        
        # Re-establish relationships / sync embedded project tasks if any
        for p in projects:
            p.tasks = [t for t in tasks if t.project_title.lower() == p.title.lower()]
            
        return users, projects, tasks
    except (json.JSONDecodeError, KeyError, FileNotFoundError):
        return [], [], []

def save_data(users: List[User], projects: List[Project], tasks: List[Task] = None):
    """Persists current state updates atomically back down to local storage."""
    data_file = get_data_file()
    tasks = tasks if tasks is not None else []
    os.makedirs(os.path.dirname(data_file), exist_ok=True)
    payload = {
        "users": [u.to_dict() for u in users],
        "projects": [p.to_dict() for p in projects],
        "tasks": [t.to_dict() for t in tasks]
    }
    with open(data_file, 'w') as f:
        json.dump(payload, f, indent=4)
