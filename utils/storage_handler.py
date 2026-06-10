import os
import json
from models.person import User
from models.project import Project

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/storage.json")

def load_data():
    """Loads and instantiates Users and Projects from the local JSON store."""
    if not os.path.exists(DATA_FILE):
        # Create folder and initial database structure if missing
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w") as f:
            json.dump({"users": [], "projects": []}, f)
        return [], []

    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            
        users = [User.from_dict(u) for u in data.get("users", [])]
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return users, projects
    except (json.JSONDecodeError, KeyError):
        print("[bold red]Data store corruption found. Resetting system configuration.[/bold red]")
        return [], []

def save_data(users, projects):
    """Serializes the running memory structures back down to disk securely."""
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    data = {
        "users": [user.to_dict() for user in users],
        "projects": [project.to_dict() for project in projects]
    }
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)