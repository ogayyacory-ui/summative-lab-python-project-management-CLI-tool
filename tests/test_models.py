import pytest

from models.person import User
from models.project import Project
from models.task import Task


def test_user_inherits_person_validation():
    user = User(" Ada ", "ada@example.com")

    assert user.name == "Ada"
    assert user.email == "ada@example.com"


def test_invalid_email_is_rejected():
    with pytest.raises(ValueError, match="Invalid email"):
        User("Ada", "ada.example.com")


def test_project_tracks_tasks_and_progress():
    project = Project("CLI", "Build project tracker", "2026-06-30", "Ada")
    first = Task("Write models", "Ada")
    second = Task("Write tests", "Ada")

    project.add_task(first)
    project.add_task(second)
    first.mark_complete()

    assert project.find_task("write models") is first
    assert project.progress == 50.0


def test_project_rejects_duplicate_tasks():
    project = Project("CLI", "Build project tracker", "2026-06-30", "Ada")
    project.add_task(Task("Write tests", "Ada"))

    with pytest.raises(ValueError, match="already exists"):
        project.add_task(Task("write tests", "Ada"))


def test_task_rejects_unknown_status():
    with pytest.raises(ValueError, match="Task status"):
        Task("Deploy", "Ada", status="Blocked")
