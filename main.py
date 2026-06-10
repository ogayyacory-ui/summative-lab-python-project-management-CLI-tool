import argparse
import sys
from rich.console import Console
from rich.table import Table

from utils.storage_handler import load_data, save_data
from models.person import User
from models.project import Project
from models.task import Task

console = Console()

def build_parser():
    parser = argparse.ArgumentParser(description="Multi-user CLI project tracker")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- CLI Subcommand definition ---
    # add-user
    parser_user = subparsers.add_parser("add-user", help="Register a new user")
    parser_user.add_argument("--name", required=True, help="Unique user name")
    parser_user.add_argument("--email", required=True, help="Contact email address")

    # add-project
    parser_proj = subparsers.add_parser("add-project", help="Create a project for a user")
    parser_proj.add_argument("--user", required=True, help="The project owner's username")
    parser_proj.add_argument("--title", required=True, help="Unique project title")
    parser_proj.add_argument("--desc", required=True, help="Project description")
    parser_proj.add_argument("--due", required=True, help="Due date in YYYY-MM-DD format")

    # add-task
    parser_task = subparsers.add_parser("add-task", help="Add a task to a project")
    parser_task.add_argument("--project", required=True, help="Parent project title")
    parser_task.add_argument("--title", required=True, help="Task title")
    parser_task.add_argument("--assignee", required=True, help="User assigned to this task")

    # list-projects
    subparsers.add_parser("list-projects", help="Show projects and task progress")
    subparsers.add_parser("list-users", help="Show registered users")

    # complete-task
    parser_comp = subparsers.add_parser("complete-task", help="Mark a task as complete")
    parser_comp.add_argument("--project", required=True, help="Project title")
    parser_comp.add_argument("--task", required=True, help="Task title")

    return parser

def find_user(users, name):
    return next((user for user in users if user.name.lower() == name.lower()), None)

def find_project(projects, title):
    return next((project for project in projects if project.title.lower() == title.lower()), None)

def print_projects(projects):
    if not projects:
        console.print("[yellow]No projects found.[/yellow]")
        return

    table = Table(title="Projects", show_lines=True)
    table.add_column("Project", style="cyan", no_wrap=True)
    table.add_column("Owner", style="magenta")
    table.add_column("Due", style="green")
    table.add_column("Progress", justify="right")
    table.add_column("Tasks", style="yellow")

    for project in projects:
        task_lines = []
        for task in project.tasks:
            status_color = "green" if task.status == "Completed" else "red"
            task_lines.append(f"- {task.title} ({task.assigned_to}: [{status_color}]{task.status}[/{status_color}])")

        tasks_output = "\n".join(task_lines) if task_lines else "[dim italic]No tasks yet.[/dim italic]"
        table.add_row(
            f"[bold]{project.title}[/bold]\n[dim]{project.description}[/dim]",
            project.owner,
            project.due_date,
            f"{project.progress}%",
            tasks_output,
        )

    console.print(table)

def print_users(users):
    if not users:
        console.print("[yellow]No users registered.[/yellow]")
        return

    table = Table(title="Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="green")
    for user in users:
        table.add_row(user.name, user.email)
    console.print(table)

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    
    if not args.command:
        parser.print_help()
        sys.exit(0)

    users, projects = load_data()

    try:
        if args.command == "add-user":
            if find_user(users, args.name):
                console.print(f"[bold red]Error: User '{args.name}' already exists.[/bold red]")
                sys.exit(1)
            
            new_user = User(name=args.name, email=args.email)
            users.append(new_user)
            save_data(users, projects)
            console.print(f"[bold green]Added user: {new_user.name}[/bold green]")

        elif args.command == "add-project":
            if not find_user(users, args.user):
                console.print(f"[bold red]Error: User '{args.user}' does not exist.[/bold red]")
                sys.exit(1)
            if find_project(projects, args.title):
                console.print(f"[bold red]Error: Project '{args.title}' already exists.[/bold red]")
                sys.exit(1)
                
            new_project = Project(title=args.title, description=args.desc, due_date=args.due, owner=args.user)
            projects.append(new_project)
            save_data(users, projects)
            console.print(f"[bold green]Added project: {new_project.title}[/bold green]")

        elif args.command == "add-task":
            project = find_project(projects, args.project)
            if not project:
                console.print(f"[bold red]Error: Project '{args.project}' not found.[/bold red]")
                sys.exit(1)
            if not find_user(users, args.assignee):
                console.print(f"[bold red]Error: User '{args.assignee}' is not registered.[/bold red]")
                sys.exit(1)

            new_task = Task(title=args.title, assigned_to=args.assignee)
            project.add_task(new_task)
            save_data(users, projects)
            console.print(f"[bold green]Added task: {new_task.title}[/bold green]")

        elif args.command == "list-projects":
            print_projects(projects)

        elif args.command == "list-users":
            print_users(users)

        elif args.command == "complete-task":
            project = find_project(projects, args.project)
            if not project:
                console.print(f"[bold red]Error: Project '{args.project}' not found.[/bold red]")
                sys.exit(1)
                
            task = project.find_task(args.task)
            if not task:
                console.print(f"[bold red]Error: Task '{args.task}' not found in project.[/bold red]")
                sys.exit(1)

            task.mark_complete()
            save_data(users, projects)
            console.print(f"[bold green]Completed task: {task.title}[/bold green]")

    except ValueError as val_err:
        console.print(f"[bold red]Error: {val_err}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()
