import argparse
import sys
from utils.storage_manager import load_data, save_data
from models.user import User
from models.project import Project
from models.task import Task

from rich.console import Console
from rich.table import Table

console = Console()

# ==================== COMMAND HANDLERS ====================

def handle_add_user(args):
    users, projects, tasks = load_data()
    if any(u.name.lower() == args.name.lower() for u in users):
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' already exists.")
        sys.exit(1)
    try:
        users.append(User(name=args.name, email=args.email))
        save_data(users, projects, tasks)
        console.print(f"[bold green]Success:[/bold green] Created user '{args.name}'.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")

def handle_list_users(args):
    users, _, _ = load_data()
    table = Table(title="👥 Registered Users")
    table.add_column("Name", style="cyan")
    table.add_column("Email", style="magenta")
    for u in users:
        table.add_row(u.name, u.email)
    console.print(table)

def handle_view_user(args):
    users, _, _ = load_data()
    user = next((u for u in users if u.name.lower() == args.name.lower()), None)
    if not user:
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)
    console.print(f"[bold cyan]User Profile:[/bold cyan]\nName: {user.name}\nEmail: {user.email}")

def handle_update_user(args):
    users, projects, tasks = load_data()
    user = next((u for u in users if u.name.lower() == args.name.lower()), None)
    if not user:
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)
    try:
        if args.email:
            user.email = args.email
        save_data(users, projects, tasks)
        console.print(f"[bold green]Success:[/bold green] Updated user '{args.name}'.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")

def handle_delete_user(args):
    users, projects, tasks = load_data()
    filtered_users = [u for u in users if u.name.lower() != args.name.lower()]
    if len(filtered_users) == len(users):
        console.print(f"[bold red]Error:[/bold red] User '{args.name}' not found.")
        sys.exit(1)
    save_data(filtered_users, projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Deleted user '{args.name}'.")

def handle_add_project(args):
    users, projects, tasks = load_data()
    if not any(u.name.lower() == args.user.lower() for u in users):
        console.print(f"[bold red]Error:[/bold red] Project Owner '{args.user}' not found.")
        sys.exit(1)
    if any(p.title.lower() == args.title.lower() for p in projects):
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' already exists.")
        sys.exit(1)
    try:
        projects.append(Project(title=args.title, description=args.description, due_date="ASAP", owner=args.user))
        save_data(users, projects, tasks)
        console.print(f"[bold green]Success:[/bold green] Project '{args.title}' initialized.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")

def handle_list_projects(args):
    _, projects, _ = load_data()
    if args.user:
        projects = [p for p in projects if p.owner.lower() == args.user.lower()]
    
    table = Table(title="🗂️ Systems Projects Pipeline")
    table.add_column("Title", style="cyan")
    table.add_column("Owner", style="magenta")
    table.add_column("Description", style="green")
    for p in projects:
        table.add_row(p.title, p.owner, p.description)
    console.print(table)

def handle_view_project(args):
    _, projects, _ = load_data()
    p = next((proj for proj in projects if proj.title.lower() == args.title.lower()), None)
    if not p:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)
    console.print(f"[bold cyan]Project details:[/bold cyan]\nTitle: {p.title}\nOwner: {p.owner}\nDesc: {p.description}")

def handle_update_project(args):
    users, projects, tasks = load_data()
    p = next((proj for proj in projects if proj.title.lower() == args.title.lower()), None)
    if not p:
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)
    if args.description:
        p.description = args.description
    save_data(users, projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Updated project '{args.title}'.")

def handle_delete_project(args):
    users, projects, tasks = load_data()
    filtered_projects = [p for p in projects if p.title.lower() != args.title.lower()]
    if len(filtered_projects) == len(projects):
        console.print(f"[bold red]Error:[/bold red] Project '{args.title}' not found.")
        sys.exit(1)
    save_data(users, filtered_projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Project '{args.title}' removed.")

def handle_add_task(args):
    users, projects, tasks = load_data()
    if not any(p.title.lower() == args.project.lower() for p in projects):
        console.print(f"[bold red]Error:[/bold red] Project target space '{args.project}' not found.")
        sys.exit(1)
    try:
        new_task = Task(title=args.title, project_title=args.project)
        tasks.append(new_task)
        save_data(users, projects, tasks)
        console.print(f"[bold green]Success:[/bold green] Task created with ID {new_task.task_id}.")
    except ValueError as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")

def handle_list_tasks(args):
    _, _, tasks = load_data()
    table = Table(title="📋 Operational System Tasks")
    table.add_column("ID", style="yellow")
    table.add_column("Title", style="cyan")
    table.add_column("Project", style="blue")
    table.add_column("Assignee", style="magenta")
    table.add_column("Status", style="green")
    for t in tasks:
        table.add_row(str(t.task_id), t.title, t.project_title, t.assigned_to, t.status)
    console.print(table)

def handle_view_task(args):
    _, _, tasks = load_data()
    t = next((tk for tk in tasks if tk.task_id == args.task_id), None)
    if not t:
        console.print(f"[bold red]Error:[/bold red] Task ID {args.task_id} not found.")
        sys.exit(1)
    console.print(f"[bold cyan]Task [{t.task_id}]:[/bold cyan] {t.title}\nProject: {t.project_title}\nAssignee: {t.assigned_to}\nStatus: {t.status}")

def handle_update_task(args):
    users, projects, tasks = load_data()
    t = next((tk for tk in tasks if tk.task_id == args.task_id), None)
    if not t:
        console.print(f"[bold red]Error:[/bold red] Task ID {args.task_id} not found.")
        sys.exit(1)
    if args.title:
        t.title = args.title
    save_data(users, projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Updated Task ID {args.task_id}.")

def handle_complete_task(args):
    users, projects, tasks = load_data()
    t = next((tk for tk in tasks if tk.task_id == args.task_id), None)
    if not t:
        console.print(f"[bold red]Error:[/bold red] Task ID {args.task_id} not found.")
        sys.exit(1)
    t.mark_complete()
    save_data(users, projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Task ID {args.task_id} marked as completed.")

def handle_assign_task(args):
    users, projects, tasks = load_data()
    t = next((tk for tk in tasks if tk.task_id == args.task_id), None)
    if not t:
        console.print(f"[bold red]Error:[/bold red] Task ID {args.task_id} not found.")
        sys.exit(1)
    if not any(u.name.lower() == args.user.lower() for u in users):
        console.print(f"[bold red]Error:[/bold red] User '{args.user}' does not exist.")
        sys.exit(1)
    t.assigned_to = args.user
    save_data(users, projects, tasks)
    console.print(f"[bold green]Success:[/bold green] Task ID {args.task_id} assigned to '{args.user}'.")

def handle_delete_task(args):
    users, projects, tasks = load_data()
    filtered_tasks = [t for t in tasks if t.task_id != args.task_id]
    if len(filtered_tasks) == len(tasks):
        console.print(f"[bold red]Error:[/bold red] Task ID {args.task_id} not found.")
        sys.exit(1)
    save_data(users, projects, filtered_tasks)
    console.print(f"[bold green]Success:[/bold green] Task ID {args.task_id} removed.")

# ==================== ARGPARSE CLI DEFINITION ====================

EPILOG_EXAMPLES = """
Examples:
  main.py add-user --name "Alex Johnson" --email "alex@example.com"
  main.py add-project --user "Alex Johnson" --title "CLI Tool" --description "Build a CLI"
  main.py add-task --project "CLI Tool" --title "Implement features"
  main.py list-projects --user "Alex Johnson"
  main.py complete-task --task-id 1
"""

def main():
    parser = argparse.ArgumentParser(
        description="Project Management CLI Tool - Manage users, projects, and tasks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=EPILOG_EXAMPLES
    )
    
    subparsers = parser.add_subparsers(dest="command", title="Available commands", metavar="...")

    # --- User Subcommands ---
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

    # --- Project Subcommands ---
    p_add_proj = subparsers.add_parser("add-project", help="Create a new project")
    p_add_proj.add_argument("--user", required=True)
    p_add_proj.add_argument("--title", required=True)
    p_add_proj.add_argument("--description", default="No description")
    p_add_proj.set_defaults(func=handle_add_project)

    p_list_proj = subparsers.add_parser("list-projects", help="List projects")
    p_list_proj.add_argument("--user", help="Filter projects by user assignment")
    p_list_proj.set_defaults(func=handle_list_projects)

    p_view_proj = subparsers.add_parser("view-project", help="View project details")
    p_view_proj.add_argument("--title", required=True)
    p_view_proj.set_defaults(func=handle_view_project)

    p_up_proj = subparsers.add_parser("update-project", help="Update project information")
    p_up_proj.add_argument("--title", required=True)
    p_up_proj.add_argument("--description")
    p_up_proj.set_defaults(func=handle_update_project)

    p_del_proj = subparsers.add_parser("delete-project", help="Delete a project")
    p_del_proj.add_argument("--title", required=True)
    p_del_proj.set_defaults(func=handle_delete_project)

    # --- Task Subcommands ---
    p_add_task = subparsers.add_parser("add-task", help="Add a task to a project")
    p_add_task.add_argument("--project", required=True)
    p_add_task.add_argument("--title", required=True)
    p_add_task.set_defaults(func=handle_add_task)

    subparsers.add_parser("list-tasks", help="List tasks").set_defaults(func=handle_list_tasks)

    p_view_task = subparsers.add_parser("view-task", help="View task details")
    p_view_task.add_argument("--task-id", type=int, required=True)
    p_view_task.set_defaults(func=handle_view_task)

    p_up_task = subparsers.add_parser("update-task", help="Update task information")
    p_up_task.add_argument("--task-id", type=int, required=True)
    p_up_task.add_argument("--title")
    p_up_task.set_defaults(func=handle_update_task)

    p_comp_task = subparsers.add_parser("complete-task", help="Mark task as completed")
    p_comp_task.add_argument("--task-id", type=int, required=True)
    p_comp_task.set_defaults(func=handle_complete_task)

    p_assign_task = subparsers.add_parser("assign-task", help="Assign task to user")
    p_assign_task.add_argument("--task-id", type=int, required=True)
    p_assign_task.add_argument("--user", required=True)
    p_assign_task.set_defaults(func=handle_assign_task)

    p_del_task = subparsers.add_parser("delete-task", help="Delete a task")
    p_del_task.add_argument("--task-id", type=int, required=True)
    p_del_task.set_defaults(func=handle_delete_task)

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()