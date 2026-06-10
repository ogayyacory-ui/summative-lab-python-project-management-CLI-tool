import argparse
import sys
from rich.console import Console
from rich.table import Table

from utils.storage_handler import load_data, save_data
from models.person import User
from models.project import Project
from models.task import Task

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Simulated Multi-User CLI Project Tracker Application")
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # --- CLI Subcommand definition ---
    # add-user
    parser_user = subparsers.add_parser("add-user", help="Register a new system user profile")
    parser_user.add_argument("--name", required=True, help="Unique string identifier name")
    parser_user.add_argument("--email", required=True, help="Contact email address")

    # add-project
    parser_proj = subparsers.add_parser("add-project", help="Create and attach a project to a specific user")
    parser_proj.add_argument("--user", required=True, help="The project owner's username")
    parser_proj.add_argument("--title", required=True, help="Unique project title name")
    parser_proj.add_argument("--desc", required=True, help="Detailed descriptive overview string")
    parser_proj.add_argument("--due", required=True, help="Target due date string (YYYY-MM-DD)")

    # add-task
    parser_task = subparsers.add_parser("add-task", help="Append a project action task item")
    parser_task.add_argument("--project", required=True, help="Title of parent destination project")
    parser_task.add_argument("--title", required=True, help="Task title assignment line item")
    parser_task.add_argument("--assignee", required=True, help="User identity handling this assignment")

    # list-projects
    subparsers.add_parser("list-projects", help="Enumerate all projects, assignments, and nested progression statuses")

    # complete-task
    parser_comp = subparsers.add_parser("complete-task", help="Mark an active target milestone task as complete")
    parser_comp.add_argument("--project", required=True, help="Target project scope context")
    parser_comp.add_argument("--task", required=True, help="Exact title string of target completed task item")

    args = parser.parse_args()
    
    # Gracefully catch running system with no args parsed
    if not args.command:
        parser.print_help()
        sys.exit(0)

    # Initialize Application State Datastore
    users, projects = load_data()

    try:
        if args.command == "add-user":
            if any(u.name.lower() == args.name.lower() for u in users):
                console.print(f"[bold red]Error: User named '{args.name}' already exists![/bold red]")
                sys.exit(1)
            
            new_user = User(name=args.name, email=args.email)
            users.append(new_user)
            save_data(users, projects)
            console.print(f"[bold green]Successfully registered active account profile: {new_user}[/bold green]")

        elif args.command == "add-project":
            # Guard validation: Verify User existence
            if not any(u.name.lower() == args.user.lower() for u in users):
                console.print(f"[bold red]Error: Specified user allocation target '{args.user}' does not exist.[/bold red]")
                sys.exit(1)
            if any(p.title.lower() == args.title.lower() for p in projects):
                console.print(f"[bold red]Error: Project entity '{args.title}' already defined globally.[/bold red]")
                sys.exit(1)
                
            new_project = Project(title=args.title, description=args.desc, due_date=args.due, owner=args.user)
            projects.append(new_project)
            save_data(users, projects)
            console.print(f"[bold green]Project established and assigned successfully: {new_project}[/bold green]")

        elif args.command == "add-task":
            # Query reference Project target
            project = next((p for p in projects if p.title.lower() == args.project.lower()), None)
            if not project:
                console.print(f"[bold red]Error: Referenced project base configuration workspace '{args.project}' not found.[/bold red]")
                sys.exit(1)
            # Guard validation: Verify Assignee User profile existence
            if not any(u.name.lower() == args.assignee.lower() for u in users):
                console.print(f"[bold red]Error: System cannot assign tasks to '{args.assignee}' as they are not registered.[/bold red]")
                sys.exit(1)

            new_task = Task(title=args.title, assigned_to=args.assignee)
            project.add_task(new_task)
            save_data(users, projects)
            console.print(f"[bold green]Task item safely introduced into runtime scopes: {new_task}[/bold green]")

        elif args.command == "list-projects":
            if not projects:
                console.print("[yellow]No project profiles generated in internal memory databases.[/yellow]")
                sys.exit(0)
            
            table = Table(title="Global Enterprise Project Tracker Framework Overview", show_lines=True)
            table.add_column("Project Context Workspace", style="cyan", no_wrap=True)
            table.add_column("Owner", style="magenta")
            table.add_column("Due Date Target", style="green")
            table.add_column("Tasks/Action Items (Assignee -> Execution Status)", style="yellow")

            for proj in projects:
                task_lines = []
                for t in proj.tasks:
                    status_color = "green" if t.status == "Completed" else "red"
                    task_lines.append(f"• {t.title} ({t.assigned_to} -> [{status_color}]{t.status}[/{status_color}])")
                
                tasks_output = "\n".join(task_lines) if task_lines else "[dim italic]No active sprint tasks linked.[/dim italic]"
                table.add_row(f"[bold]{proj.title}[/bold]\n[dim]{proj.description}[/dim]", proj.owner, proj.due_date, tasks_output)
            
            console.print(table)

        elif args.command == "complete-task":
            project = next((p for p in projects if p.title.lower() == args.project.lower()), None)
            if not project:
                console.print(f"[bold red]Error: Target project context target workspace framework '{args.project}' missing.[/bold red]")
                sys.exit(1)
                
            task = next((t for t in project.tasks if t.title.lower() == args.task.lower()), None)
            if not task:
                console.print(f"[bold red]Error: Task target tracker element title line item '{args.task}' not found in project.[/bold red]")
                sys.exit(1)

            task.mark_complete()
            save_data(users, projects)
            console.print(f"[bold green]Success! Task state updated: {task}[/bold green]")

    except ValueError as val_err:
        console.print(f"[bold red]Data Constraint Validation Failure: {val_err}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    main()