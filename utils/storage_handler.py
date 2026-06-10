import json
import os
from pathlib import Path
from models.person import User
from models.project import Project

DEFAULT_DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "storage.json"
DATA_FILE_ENV = "PROJECT_CLI_DATA_FILE"

def get_data_file(path=None):
    """Returns the active storage path, allowing tests or users to override it."""
    return Path(path or os.environ.get(DATA_FILE_ENV, DEFAULT_DATA_FILE))

def _empty_store():
    return {"users": [], "projects": []}

def load_data(path=None):
    """Loads and instantiates Users and Projects from the local JSON store."""
    data_file = get_data_file(path)
    if not data_file.exists():
        data_file.parent.mkdir(parents=True, exist_ok=True)
        data_file.write_text(json.dumps(_empty_store(), indent=4))
        return [], []

    try:
        with data_file.open("r") as f:
            data = json.load(f)
            
        users = [User.from_dict(u) for u in data.get("users", [])]
        projects = [Project.from_dict(p) for p in data.get("projects", [])]
        return users, projects
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        print(f"Data store could not be loaded: {exc}")
        return [], []

def save_data(users, projects, path=None):
    """Serializes the running memory structures back down to disk securely."""
    data_file = get_data_file(path)
    data_file.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "users": [user.to_dict() for user in users],
        "projects": [project.to_dict() for project in projects]
    }
    with data_file.open("w") as f:
        json.dump(data, f, indent=4)
