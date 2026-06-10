from models.person import User
from models.project import Project
from models.task import Task
from utils.storage_handler import load_data, save_data


def test_save_and_load_round_trip(tmp_path):
    data_file = tmp_path / "storage.json"
    users = [User("Ada", "ada@example.com")]
    project = Project("CLI", "Build project tracker", "2026-06-30", "Ada")
    project.add_task(Task("Write tests", "Ada", "Completed"))

    save_data(users, [project], path=data_file)
    loaded_users, loaded_projects = load_data(path=data_file)

    assert loaded_users[0].name == "Ada"
    assert loaded_projects[0].title == "CLI"
    assert loaded_projects[0].tasks[0].status == "Completed"


def test_load_data_creates_missing_store(tmp_path):
    data_file = tmp_path / "nested" / "storage.json"

    users, projects = load_data(path=data_file)

    assert users == []
    assert projects == []
    assert data_file.exists()


def test_load_data_handles_corrupt_json(tmp_path):
    data_file = tmp_path / "storage.json"
    data_file.write_text("{not json")

    users, projects = load_data(path=data_file)

    assert users == []
    assert projects == []
