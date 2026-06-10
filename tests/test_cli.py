import json

import pytest

import main


def test_cli_adds_user_project_task_and_completes_it(tmp_path, monkeypatch):
    data_file = tmp_path / "storage.json"
    monkeypatch.setenv("PROJECT_CLI_DATA_FILE", str(data_file))

    main.main(["add-user", "--name", "Ada", "--email", "ada@example.com"])
    main.main([
        "add-project",
        "--user",
        "Ada",
        "--title",
        "CLI",
        "--desc",
        "Build tracker",
        "--due",
        "2026-06-30",
    ])
    main.main(["add-task", "--project", "CLI", "--title", "Write tests", "--assignee", "Ada"])
    main.main(["complete-task", "--project", "CLI", "--task", "Write tests"])

    data = json.loads(data_file.read_text())
    assert data["users"][0]["name"] == "Ada"
    assert data["projects"][0]["tasks"][0]["status"] == "Completed"


def test_cli_rejects_duplicate_users(tmp_path, monkeypatch):
    monkeypatch.setenv("PROJECT_CLI_DATA_FILE", str(tmp_path / "storage.json"))
    main.main(["add-user", "--name", "Ada", "--email", "ada@example.com"])

    with pytest.raises(SystemExit) as exc_info:
        main.main(["add-user", "--name", "ada", "--email", "other@example.com"])

    assert exc_info.value.code == 1
