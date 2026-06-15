"""
CLI Project Management Tool - Main entry point.

This tool allows administrators to manage users, projects, and tasks
through a command-line interface with structured commands.
"""

import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from models import User, Project, Task
from utils import (
    DataStore,
    find_user_by_id,
    find_user_by_email,
    find_project_by_id,
    find_task_by_id,
    get_user_projects,
    get_project_tasks,
    validate_user_exists,
    validate_project_exists,
    validate_task_exists
)


class ProjectManager:
    """
    Main project management application.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize the project manager.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.console = Console()
        self.store = DataStore(data_dir)
        self.users = []
        self.projects = []
        self.tasks = []
        self.load_all_data()
    
    def load_all_data(self):
        """Load all data from storage."""
        self.users = self.store.load_users()
        self.projects = self.store.load_projects()
        self.tasks = self.store.load_tasks()
    
    def save_all_data(self):
        """Save all data to storage."""
        self.store.save_users(self.users)
        self.store.save_projects(self.projects)
        self.store.save_tasks(self.tasks)
    
    # User Commands
    def add_user(self, name, email):
        """
        Add a new user.
        
        Args:
            name (str): User's name
            email (str): User's email
        """
        # Check if email already exists
        existing = find_user_by_email(self.users, email)
        if existing:
            self.console.print(f"[red]Error: User with email {email} already exists[/red]")
            return
        
        try:
            user = User(name, email)
            self.users.append(user)
            self.save_all_data()
            self.console.print(f"[green]✓ User added successfully: {user.name} (ID: {user.id})[/green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def list_users(self):
        """List all users."""
        if not self.users:
            self.console.print("[yellow]No users found[/yellow]")
            return
        
        table = Table(title="All Users", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Name", style="green", width=20)
        table.add_column("Email", style="blue", width=25)
        table.add_column("Projects", style="yellow", width=10)
        
        for user in self.users:
            project_count = len(user.projects)
            table.add_row(str(user.id), user.name, user.email, str(project_count))
        
        self.console.print(table)
    
    def get_user(self, user_id):
        """
        Display details for a specific user.
        
        Args:
            user_id (int): ID of the user
        """
        user = find_user_by_id(self.users, user_id)
        if not user:
            self.console.print(f"[red]User with ID {user_id} not found[/red]")
            return
        
        user_projects = get_user_projects(user, self.projects)
        
        info_text = f"[bold cyan]User Details[/bold cyan]\n"
        info_text += f"ID: {user.id}\n"
        info_text += f"Name: {user.name}\n"
        info_text += f"Email: {user.email}\n"
        info_text += f"Projects: {len(user_projects)}"
        
        self.console.print(Panel(info_text, border_style="blue"))
        
        if user_projects:
            self.console.print("[bold]Associated Projects:[/bold]")
            for proj in user_projects:
                self.console.print(f"  • {proj.title} (ID: {proj.id})")
    
    # Project Commands
    def add_project(self, title, description, due_date, owner_id):
        """
        Add a new project.
        
        Args:
            title (str): Project title
            description (str): Project description
            due_date (str): Project due date (YYYY-MM-DD)
            owner_id (int): ID of the project owner
        """
        # Validate owner exists
        exists, msg = validate_user_exists(owner_id, self.users)
        if not exists:
            self.console.print(f"[red]Error: {msg}[/red]")
            return
        
        try:
            project = Project(title, description, due_date, owner_id)
            self.projects.append(project)
            
            # Add project to owner's project list
            owner = find_user_by_id(self.users, owner_id)
            owner.add_project(project.id)
            
            self.save_all_data()
            self.console.print(f"[green]✓ Project added successfully: {project.title} (ID: {project.id})[/green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def list_projects(self):
        """List all projects."""
        if not self.projects:
            self.console.print("[yellow]No projects found[/yellow]")
            return
        
        table = Table(title="All Projects", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Title", style="green", width=20)
        table.add_column("Due Date", style="blue", width=12)
        table.add_column("Owner", style="yellow", width=15)
        table.add_column("Tasks", style="white", width=8)
        
        for project in self.projects:
            owner = find_user_by_id(self.users, project.owner_id)
            owner_name = owner.name if owner else "Unknown"
            task_count = len(project.tasks)
            table.add_row(
                str(project.id),
                project.title,
                project.due_date,
                owner_name,
                str(task_count)
            )
        
        self.console.print(table)
    
    def get_project(self, project_id):
        """
        Display details for a specific project.
        
        Args:
            project_id (int): ID of the project
        """
        project = find_project_by_id(self.projects, project_id)
        if not project:
            self.console.print(f"[red]Project with ID {project_id} not found[/red]")
            return
        
        owner = find_user_by_id(self.users, project.owner_id)
        owner_name = owner.name if owner else "Unknown"
        
        info_text = f"[bold cyan]Project Details[/bold cyan]\n"
        info_text += f"ID: {project.id}\n"
        info_text += f"Title: {project.title}\n"
        info_text += f"Description: {project.description}\n"
        info_text += f"Due Date: {project.due_date}\n"
        info_text += f"Owner: {owner_name} (ID: {project.owner_id})\n"
        info_text += f"Tasks: {len(project.tasks)}\n"
        info_text += f"Contributors: {len(project.contributors)}"
        
        self.console.print(Panel(info_text, border_style="blue"))
        
        project_tasks = get_project_tasks(project, self.tasks)
        if project_tasks:
            self.console.print("[bold]Tasks in this project:[/bold]")
            for task in project_tasks:
                status_color = "green" if task.status == "completed" else "yellow"
                self.console.print(f"  • [{status_color}]{task.title}[/{status_color}] (Status: {task.status}, ID: {task.id})")
    
    def list_user_projects(self, user_id):
        """
        List all projects for a specific user.
        
        Args:
            user_id (int): ID of the user
        """
        user = find_user_by_id(self.users, user_id)
        if not user:
            self.console.print(f"[red]User with ID {user_id} not found[/red]")
            return
        
        user_projects = get_user_projects(user, self.projects)
        
        if not user_projects:
            self.console.print(f"[yellow]User {user.name} has no projects[/yellow]")
            return
        
        table = Table(title=f"Projects for {user.name}", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Title", style="green", width=20)
        table.add_column("Due Date", style="blue", width=12)
        table.add_column("Tasks", style="yellow", width=8)
        
        for project in user_projects:
            task_count = len(project.tasks)
            table.add_row(str(project.id), project.title, project.due_date, str(task_count))
        
        self.console.print(table)
    
    # Task Commands
    def add_task(self, title, project_id, assigned_to, description=""):
        """
        Add a new task to a project.
        
        Args:
            title (str): Task title
            project_id (int): ID of the project
            assigned_to (int): ID of the user assigned to the task
            description (str): Task description
        """
        # Validate project exists
        exists, msg = validate_project_exists(project_id, self.projects)
        if not exists:
            self.console.print(f"[red]Error: {msg}[/red]")
            return
        
        # Validate user exists
        exists, msg = validate_user_exists(assigned_to, self.users)
        if not exists:
            self.console.print(f"[red]Error: {msg}[/red]")
            return
        
        try:
            task = Task(title, project_id, assigned_to, description=description)
            self.tasks.append(task)
            
            # Add task to project
            project = find_project_by_id(self.projects, project_id)
            project.add_task(task.id)
            
            self.save_all_data()
            self.console.print(f"[green]✓ Task added successfully: {task.title} (ID: {task.id})[/green]")
        except ValueError as e:
            self.console.print(f"[red]Error: {e}[/red]")
    
    def list_project_tasks(self, project_id):
        """
        List all tasks in a project.
        
        Args:
            project_id (int): ID of the project
        """
        project = find_project_by_id(self.projects, project_id)
        if not project:
            self.console.print(f"[red]Project with ID {project_id} not found[/red]")
            return
        
        project_tasks = get_project_tasks(project, self.tasks)
        
        if not project_tasks:
            self.console.print(f"[yellow]Project {project.title} has no tasks[/yellow]")
            return
        
        table = Table(title=f"Tasks in {project.title}", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="cyan", width=8)
        table.add_column("Title", style="green", width=20)
        table.add_column("Status", style="yellow", width=12)
        table.add_column("Assigned to", style="blue", width=15)
        
        for task in project_tasks:
            assigned_user = find_user_by_id(self.users, task.assigned_to)
            assigned_name = assigned_user.name if assigned_user else "Unknown"
            table.add_row(str(task.id), task.title, task.status, assigned_name)
        
        self.console.print(table)
    
    def complete_task(self, task_id):
        """
        Mark a task as completed.
        
        Args:
            task_id (int): ID of the task
        """
        task = find_task_by_id(self.tasks, task_id)
        if not task:
            self.console.print(f"[red]Task with ID {task_id} not found[/red]")
            return
        
        task.mark_complete()
        self.save_all_data()
        self.console.print(f"[green]✓ Task '{task.title}' marked as completed[/green]")
    
    def get_task(self, task_id):
        """
        Display details for a specific task.
        
        Args:
            task_id (int): ID of the task
        """
        task = find_task_by_id(self.tasks, task_id)
        if not task:
            self.console.print(f"[red]Task with ID {task_id} not found[/red]")
            return
        
        assigned_user = find_user_by_id(self.users, task.assigned_to)
        assigned_name = assigned_user.name if assigned_user else "Unknown"
        project = find_project_by_id(self.projects, task.project_id)
        project_name = project.title if project else "Unknown"
        
        info_text = f"[bold cyan]Task Details[/bold cyan]\n"
        info_text += f"ID: {task.id}\n"
        info_text += f"Title: {task.title}\n"
        info_text += f"Description: {task.description}\n"
        info_text += f"Status: {task.status}\n"
        info_text += f"Project: {project_name}\n"
        info_text += f"Assigned to: {assigned_name}\n"
        info_text += f"Created: {task.created_at}"
        
        if task.completed_at:
            info_text += f"\nCompleted: {task.completed_at}"
        
        self.console.print(Panel(info_text, border_style="blue"))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CLI Project Management Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py add-user "John Doe" "john@example.com"
  python main.py list-users
  python main.py add-project "Project Alpha" "Description" "2025-12-31" 1000
  python main.py list-projects
  python main.py add-task "Complete design" 2000 1000 --description "UI mockups"
  python main.py complete-task 3000
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # User commands
    add_user_parser = subparsers.add_parser("add-user", help="Add a new user")
    add_user_parser.add_argument("name", help="User's full name")
    add_user_parser.add_argument("email", help="User's email address")
    
    subparsers.add_parser("list-users", help="List all users")
    
    get_user_parser = subparsers.add_parser("get-user", help="Get details for a specific user")
    get_user_parser.add_argument("user_id", type=int, help="User ID")
    
    # Project commands
    add_project_parser = subparsers.add_parser("add-project", help="Add a new project")
    add_project_parser.add_argument("title", help="Project title")
    add_project_parser.add_argument("description", help="Project description")
    add_project_parser.add_argument("due_date", help="Due date (YYYY-MM-DD)")
    add_project_parser.add_argument("owner_id", type=int, help="Owner user ID")
    
    subparsers.add_parser("list-projects", help="List all projects")
    
    get_project_parser = subparsers.add_parser("get-project", help="Get details for a specific project")
    get_project_parser.add_argument("project_id", type=int, help="Project ID")
    
    user_projects_parser = subparsers.add_parser("list-user-projects", help="List projects for a user")
    user_projects_parser.add_argument("user_id", type=int, help="User ID")
    
    list_tasks_parser = subparsers.add_parser("list-tasks", help="List tasks in a project")
    list_tasks_parser.add_argument("project_id", type=int, help="Project ID")
    
    # Task commands
    add_task_parser = subparsers.add_parser("add-task", help="Add a task to a project")
    add_task_parser.add_argument("title", help="Task title")
    add_task_parser.add_argument("project_id", type=int, help="Project ID")
    add_task_parser.add_argument("assigned_to", type=int, help="User ID to assign task to")
    add_task_parser.add_argument("--description", default="", help="Task description")
    
    complete_task_parser = subparsers.add_parser("complete-task", help="Mark a task as completed")
    complete_task_parser.add_argument("task_id", type=int, help="Task ID")
    
    get_task_parser = subparsers.add_parser("get-task", help="Get details for a specific task")
    get_task_parser.add_argument("task_id", type=int, help="Task ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = ProjectManager()
    
    # Execute commands
    if args.command == "add-user":
        manager.add_user(args.name, args.email)
    elif args.command == "list-users":
        manager.list_users()
    elif args.command == "get-user":
        manager.get_user(args.user_id)
    elif args.command == "add-project":
        manager.add_project(args.title, args.description, args.due_date, args.owner_id)
    elif args.command == "list-projects":
        manager.list_projects()
    elif args.command == "get-project":
        manager.get_project(args.project_id)
    elif args.command == "list-user-projects":
        manager.list_user_projects(args.user_id)
    elif args.command == "list-tasks":
        manager.list_project_tasks(args.project_id)
    elif args.command == "add-task":
        manager.add_task(args.title, args.project_id, args.assigned_to, args.description)
    elif args.command == "complete-task":
        manager.complete_task(args.task_id)
    elif args.command == "get-task":
        manager.get_task(args.task_id)


if __name__ == "__main__":
    main()
