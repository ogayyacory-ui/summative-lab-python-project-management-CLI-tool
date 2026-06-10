# Python Project Management CLI Tool

A small multi-user project tracker built with Python, `argparse`, JSON file
persistence, and Rich terminal output.

## Features

- Register users with validated names and email addresses.
- Create projects owned by registered users.
- Add tasks to projects and assign them to users.
- Mark tasks complete and view project progress.
- Persist all users, projects, and tasks in `data/storage.json`.
- Override the storage file with `PROJECT_CLI_DATA_FILE` for testing or demos.

## Setup

```bash
pipenv install --dev
```

If you are not using Pipenv, install the packages from `requirement.txt` and
install `pytest` for the test suite.

## Usage

```bash
python main.py add-user --name Ada --email ada@example.com
python main.py add-project --user Ada --title CLI --desc "Build tracker" --due 2026-06-30
python main.py add-task --project CLI --title "Write tests" --assignee Ada
python main.py complete-task --project CLI --task "Write tests"
python main.py list-projects
python main.py list-users
```

Run `python main.py --help` or add `--help` after any subcommand to see the
available options.

## Tests

```bash
python -m pytest -q
```

The tests cover model validation, project/task behavior, JSON persistence, and
key CLI flows.
