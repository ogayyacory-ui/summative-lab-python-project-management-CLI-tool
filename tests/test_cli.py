import json
import os
import subprocess
import sys


def run_cli(tmp_path, *args):
    env = os.environ.copy()
    env["PROJECT_CLI_DATA_FILE"] = str(tmp_path / "storage.json")
    return subprocess.run(
        [sys.executable, "main.py", *args],
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_cli_creates_nested_user_project_task_flow(tmp_path):
    add_user = run_cli(tmp_path, "add-user", "--name", "Ada", "--email", "ada@example.com")
    assert add_user.returncode == 0
    assert "Created user 'Ada'" in add_user.stdout

    add_project = run_cli(
        tmp_path,
        "add-project",
        "--user",
        "Ada",
        "--title",
        "CLI",
        "--description",
        "Build tracker",
        "--due-date",
        "2026-06-30",
    )
    assert add_project.returncode == 0
    assert "Project 'CLI' initialized" in add_project.stdout

    add_task = run_cli(
        tmp_path,
        "add-task",
        "--project",
        "CLI",
        "--title",
        "Write tests",
        "--assigned-to",
        "Ada",
    )
    assert add_task.returncode == 0
    assert "Task 'Write tests' created" in add_task.stdout

    complete_task = run_cli(
        tmp_path,
        "complete-task",
        "--project",
        "CLI",
        "--task",
        "Write tests",
    )
    assert complete_task.returncode == 0
    assert "marked as completed" in complete_task.stdout

    saved = json.loads((tmp_path / "storage.json").read_text())
    task = saved["users"][0]["projects"][0]["tasks"][0]
    assert task == {
        "title": "Write tests",
        "assigned_to": "Ada",
        "status": "Completed",
    }


def test_cli_rejects_duplicate_user(tmp_path):
    first = run_cli(tmp_path, "add-user", "--name", "Ada", "--email", "ada@example.com")
    second = run_cli(tmp_path, "add-user", "--name", "Ada", "--email", "ada@example.com")

    assert first.returncode == 0
    assert second.returncode == 1
    assert "already exists" in second.stdout


def test_cli_help_lists_subcommands(tmp_path):
    result = run_cli(tmp_path, "--help")

    assert result.returncode == 0
    assert "add-user" in result.stdout
    assert "add-project" in result.stdout
    assert "add-task" in result.stdout
