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
        
        with self.assertRaises(ValueError):
            user.email = "bad_email_format"

    def test_project_task_aggregation(self):
        """Validates nested structural composition model dependencies."""
        project = Project(title="Alpha", description="Test", due_date="2026-12-31", owner="Alice")
        task = Task(title="Setup CI")
        project.add_task(task)
        
        self.assertEqual(len(project.tasks), 1)
        self.assertEqual(project.tasks[0].title, "Setup CI")
        self.assertEqual(project.tasks[0].status, "Pending")
        
        project.tasks[0].mark_complete()
        self.assertEqual(project.tasks[0].status, "Completed")

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"users": [{"name": "Bob", "email": "bob@net.com"}], "projects": []}')
    def test_storage_loader(self, mock_file, mock_exists):
        """Validates system data layer unmarshaling engine behaviors."""
        users, projects, tasks = load_data()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].name, "Bob")
        self.assertEqual(len(projects), 0)
        self.assertEqual(len(tasks), 0)

    @patch("utils.storage_handler.os.makedirs")
    @patch("builtins.open", new_callable=mock_open)
    def test_storage_writer(self, mock_file, mock_makedirs):
        """Confirms programmatic updates commit structure schema properly."""
        users = [User(name="Charlie", email="charlie@io.com")]
        projects = []
        tasks = []
        save_data(users, projects, tasks)
        
        mock_file.assert_called_once()
        handle = mock_file()
        written_data = "".join(call.args[0] for call in handle.write.call_args_list)
        parsed = json.loads(written_data)
        self.assertEqual(parsed["users"][0]["name"], "Charlie")
        self.assertEqual(parsed["tasks"], [])

if __name__ == "__main__":
    unittest.main()
