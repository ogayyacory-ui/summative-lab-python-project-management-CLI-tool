import argparse
import sys

from rich.console import Console
from rich.table import Table

from models.project import Project
from models.task import Task
from models.user import User
from utils.storage_manager import load_data, save_data

console = Console()


def find_user(users, name):
    return next((user for user in users if user.name.lower() == name.lower()), None)


def find_project(users, title):
    for user in users:
        project = next((p for p in user.projects if p.title.lower() == title.lower()), None)
        if project:
            return user, project
    return None, None


def handle_add_user(args):
    users, _, _ = load_data()
    if find_user(users, args.name):
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' already exists.")
        sys.exit(1)

    try:
        users.append(User(name=args.name, email=args.email))
        save_data(users)
        console.print(f"[bold green]Success:[/bold green] Created user '{args.name}'.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        sys.exit(1)


def handle_list_users(args):
    users, _, _ = load_data()
    table = Table(title="Registered Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    table.add_column("Projects", style="green")

    for user in users:
        table.add_row(user.name, user.email, str(len(user.projects)))
    console.print(table)


def handle_view_user(args):
    users, _, _ = load_data()
    user = find_user(users, args.name)
    if not user:
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)

    table = Table(title=f"User Profile: {user.name}")
    table.add_column("Project", style="cyan")
    table.add_column("Due Date", style="green")
    table.add_column("Tasks", style="magenta")
    for project in user.projects:
        table.add_row(project.title, project.due_date, str(len(project.tasks)))

    console.print(f"[bold cyan]Name:[/bold cyan] {user.name}")
    console.print(f"[bold cyan]Email:[/bold cyan] {user.email}")
    console.print(table)


def handle_update_user(args):
    users, _, _ = load_data()
    user = find_user(users, args.name)
    if not user:
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)

    try:
        if args.email:
            user.email = args.email
        save_data(users)
        console.print(f"[bold green]Success:[/bold green] Updated user '{args.name}'.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        sys.exit(1)


def handle_delete_user(args):
    users, _, _ = load_data()
    filtered_users = [user for user in users if user.name.lower() != args.name.lower()]
    if len(filtered_users) == len(users):
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)

    save_data(filtered_users)
    console.print(f"[bold green]Success:[/bold green] Deleted user '{args.name}'.")


def handle_add_project(args):
    users, _, _ = load_data()
    user = find_user(users, args.user)
    if not user:
        console.print(f"[bold red]Error:[/bold red] Project owner '{args.user}' not found.")
        sys.exit(1)

    _, existing_project = find_project(users, args.title)
    if existing_project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' already exists.")
        sys.exit(1)

    try:
        user.add_project(
            Project(
                title=args.title,
                description=args.description,
                due_date=args.due_date,
            )
        )
        save_data(users)
        console.print(f"[bold green]Success:[/bold green] Project '{args.title}' initialized.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        sys.exit(1)


def handle_list_projects(args):
    users, _, _ = load_data()
    table = Table(title="Projects")
    table.add_column("Title", style="cyan")
    table.add_column("Owner", style="magenta")
    table.add_column("Due Date", style="green")
    table.add_column("Description")
    table.add_column("Tasks", justify="right")

    for user in users:
        if args.user and user.name.lower() != args.user.lower():
            continue
        for project in user.projects:
            table.add_row(
                project.title,
                user.name,
                project.due_date,
                project.description,
                str(len(project.tasks)),
            )
    console.print(table)


def handle_view_project(args):
    users, _, _ = load_data()
    owner, project = find_project(users, args.title)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)

    console.print(f"[bold cyan]Title:[/bold cyan] {project.title}")
    console.print(f"[bold cyan]Owner:[/bold cyan] {owner.name}")
    console.print(f"[bold cyan]Due Date:[/bold cyan] {project.due_date}")
    console.print(f"[bold cyan]Description:[/bold cyan] {project.description}")


def handle_update_project(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.title)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)

    if args.description:
        project.description = args.description
    if args.due_date:
        project.due_date = args.due_date
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Updated project '{args.title}'.")


def handle_delete_project(args):
    users, _, _ = load_data()
    owner, project = find_project(users, args.title)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)

    owner.projects = [p for p in owner.projects if p.title.lower() != args.title.lower()]
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Project '{args.title}' removed.")


def handle_add_task(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)
    if project.find_task(args.title):
        console.print(f"[bold red]Error:[/bold red] Task '{args.title}' already exists in this project.")
        sys.exit(1)

    try:
        project.add_task(Task(title=args.title, assigned_to=args.assigned_to))
        save_data(users)
        console.print(f"[bold green]Success:[/bold green] Task '{args.title}' created.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        sys.exit(1)


def handle_list_tasks(args):
    users, _, _ = load_data()
    table = Table(title="Tasks")
    table.add_column("Project", style="blue")
    table.add_column("Task", style="cyan")
    table.add_column("Assignee", style="magenta")
    table.add_column("Status", style="green")

    for user in users:
        for project in user.projects:
            if args.project and project.title.lower() != args.project.lower():
                continue
            for task in project.tasks:
                table.add_row(project.title, task.title, task.assigned_to, task.status)
    console.print(table)


def handle_view_task(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)

    task = project.find_task(args.task)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{args.task}' not found.")
        sys.exit(1)

    console.print(f"[bold cyan]Task:[/bold cyan] {task.title}")
    console.print(f"[bold cyan]Project:[/bold cyan] {project.title}")
    console.print(f"[bold cyan]Assignee:[/bold cyan] {task.assigned_to}")
    console.print(f"[bold cyan]Status:[/bold cyan] {task.status}")


def handle_update_task(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)

    task = project.find_task(args.task)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{args.task}' not found.")
        sys.exit(1)

    if args.title:
        task.title = args.title
    if args.assigned_to:
        task.assigned_to = args.assigned_to
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Updated task '{args.task}'.")


def handle_complete_task(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)

    task = project.find_task(args.task)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{args.task}' not found.")
        sys.exit(1)

    task.mark_complete()
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Task '{args.task}' marked as completed.")


def handle_assign_task(args):
    users, _, _ = load_data()
    if not find_user(users, args.user):
        console.print(f"[bold red]Error:[/bold red] User '{args.user}' does not exist.")
        sys.exit(1)

    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)

    task = project.find_task(args.task)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{args.task}' not found.")
        sys.exit(1)

    task.assigned_to = args.user
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Task '{args.task}' assigned to '{args.user}'.")


def handle_delete_task(args):
    users, _, _ = load_data()
    _, project = find_project(users, args.project)
    if not project:
        console.print(f"[bold red]Error:[/bold red] Project '{args.project}' not found.")
        sys.exit(1)

    task = project.find_task(args.task)
    if not task:
        console.print(f"[bold red]Error:[/bold red] Task '{args.task}' not found.")
        sys.exit(1)

    project.tasks = [t for t in project.tasks if t.title.lower() != args.task.lower()]
    save_data(users)
    console.print(f"[bold green]Success:[/bold green] Task '{args.task}' removed.")


EPILOG_EXAMPLES = """
Examples:
  main.py add-user --name "Alex Johnson" --email "alex@example.com"
  main.py add-project --user "Alex Johnson" --title "CLI Tool" --description "Build a CLI" --due-date 2026-06-30
  main.py add-task --project "CLI Tool" --title "Implement features" --assigned-to "Alex Johnson"
  main.py list-projects --user "Alex Johnson"
  main.py complete-task --project "CLI Tool" --task "Implement features"
"""


def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool - Manage users, projects, and tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG_EXAMPLES,
    )

    subparsers = parser.add_subparsers(dest="command", title="Available commands", metavar="...")

    p_add_user = subparsers.add_parser("add-user", help="Create a new user")
    p_add_user.add_argument("--name", required=True)
    p_add_user.add_argument("--email", required=True)
    p_add_user.set_defaults(func=handle_add_user)

    subparsers.add_parser("list-users", help="List all users").set_defaults(func=handle_list_users)

    p_view_user = subparsers.add_parser("view-user", help="View user details")
    p_view_user.add_argument("--name", required=True)
    p_view_user.set_defaults(func=handle_view_user)

    p_up_user = subparsers.add_parser("update-user", help="Update user information")
    p_up_user.add_argument("--name", required=True)
    p_up_user.add_argument("--email")
    p_up_user.set_defaults(func=handle_update_user)

    p_del_user = subparsers.add_parser("delete-user", help="Delete a user")
    p_del_user.add_argument("--name", required=True)
    p_del_user.set_defaults(func=handle_delete_user)

    p_add_proj = subparsers.add_parser("add-project", help="Create a new project")
    p_add_proj.add_argument("--user", required=True)
    p_add_proj.add_argument("--title", required=True)
    p_add_proj.add_argument("--description", default="No description")
    p_add_proj.add_argument("--due-date", default="ASAP")
    p_add_proj.set_defaults(func=handle_add_project)

    p_list_proj = subparsers.add_parser("list-projects", help="List projects")
    p_list_proj.add_argument("--user", help="Filter projects by owner")
    p_list_proj.set_defaults(func=handle_list_projects)

    p_view_proj = subparsers.add_parser("view-project", help="View project details")
    p_view_proj.add_argument("--title", required=True)
    p_view_proj.set_defaults(func=handle_view_project)

    p_up_proj = subparsers.add_parser("update-project", help="Update project information")
    p_up_proj.add_argument("--title", required=True)
    p_up_proj.add_argument("--description")
    p_up_proj.add_argument("--due-date")
    p_up_proj.set_defaults(func=handle_update_project)

    p_del_proj = subparsers.add_parser("delete-project", help="Delete a project")
    p_del_proj.add_argument("--title", required=True)
    p_del_proj.set_defaults(func=handle_delete_project)

    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True)
    p_add_task.add_argument("--title", required=True)
    p_add_task.add_argument("--assigned-to", default="Unassigned")
    p_add_task.set_defaults(func=handle_add_task)

    p_list_tasks = subparsers.add_parser("list-tasks", help="List tasks")
    p_list_tasks.add_argument("--project", help="Filter tasks by project")
    p_list_tasks.set_defaults(func=handle_list_tasks)

    p_view_task = subparsers.add_parser("view-task", help="View task details")
    p_view_task.add_argument("--project", required=True)
    p_view_task.add_argument("--task", required=True)
    p_view_task.set_defaults(func=handle_view_task)

    p_up_task = subparsers.add_parser("update-task", help="Update task information")
    p_up_task.add_argument("--project", required=True)
    p_up_task.add_argument("--task", required=True)
    p_up_task.add_argument("--title")
    p_up_task.add_argument("--assigned-to")
    p_up_task.set_defaults(func=handle_update_task)

    p_comp_task = subparsers.add_parser("complete-task", help="Mark task as completed")
    p_comp_task.add_argument("--project", required=True)
    p_comp_task.add_argument("--task", required=True)
    p_comp_task.set_defaults(func=handle_complete_task)

    p_assign_task = subparsers.add_parser("assign-task", help="Assign task to user")
    p_assign_task.add_argument("--project", required=True)
    p_assign_task.add_argument("--task", required=True)
    p_assign_task.add_argument("--user", required=True)
    p_assign_task.set_defaults(func=handle_assign_task)

    p_del_task = subparsers.add_parser("delete-task", help="Delete a task")
    p_del_task.add_argument("--project", required=True)
    p_del_task.add_argument("--task", required=True)
    p_del_task.set_defaults(func=handle_delete_task)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
