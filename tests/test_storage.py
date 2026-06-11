import unittest
from unittest.mock import patch, mock_open
import json

from models.user import User
from models.project import Project
from models.task import Task
from utils.storage_manager import load_data, save_data

class TestProjectTrackerSystem(unittest.TestCase):

    def test_user_creation_and_inheritance(self):
        """Verifies properties, setters, encapsulation, and inheritance traits."""
        user = User(name="Alice", email="alice@dev.com")
        self.assertEqual(user.name, "Alice")
        self.assertEqual(user.email, "alice@dev.com")
        self.assertEqual(user.projects, [])
        
        with self.assertRaises(ValueError):
            user.email = "bad_email_format"

    def test_project_task_aggregation(self):
        """Validates nested structural composition model dependencies."""
        user = User(name="Alice", email="alice@dev.com")
        project = Project(title="Alpha", description="Test", due_date="2026-12-31")
        task = Task(title="Setup CI", assigned_to="Alice")
        user.add_project(project)
        project.add_task(task)
        
        self.assertEqual(len(user.projects), 1)
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Setup CI")
        self.assertEqual(project.tasks[0].assigned_to, "Alice")
        self.assertEqual(project.tasks[0].status, "Pending")
        
        project.tasks[0].mark_complete()
        self.assertEqual(project.tasks[0].status, "Completed")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"users": [{"name": "Bob", "email": "bob@net.com", "projects": [{"title": "Alpha", "description": "Test", "due_date": "2026-12-31", "tasks": [{"title": "Setup CI", "assigned_to": "Bob", "status": "Pending"}]}]}]}')
    def test_storage_loader(self, mock_file, mock_exists):
        """Validates system data layer unmarshaling engine behaviors."""
        users, projects, tasks = load_data()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Bob")
        self.assertEqual(len(users[0].projects), 1)
        self.assertEqual(len(projects), 1)
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0].title, "Setup CI")

    @patch("utils.storage_handler.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_storage_writer(self, mock_file, mock_makedirs):
        """Confirms programmatic updates commit structure schema properly."""
        users = [User(name="Charlie", email="charlie@io.com")]
        users[0].add_project(Project(title="CLI", description="Build tracker", due_date="2026-06-30"))
        users[0].projects[0].add_task(Task(title="Write tests", assigned_to="Charlie"))
        save_data(users)
        
        mock_file.assert_called_once()
        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        parsed = json.loads(written_data)
        self.assertEqual(parsed["users"][0]["name"], "Charlie")
        self.assertEqual(parsed["users"][0]["projects"][0]["title"], "CLI")
        self.assertEqual(parsed["users"][0]["projects"][0]["tasks"][0]["title"], "Write tests")
        self.assertNotIn("tasks", parsed)

if __name__ == "__main__":
    unittest.main()
