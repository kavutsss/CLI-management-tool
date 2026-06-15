"""
Helper functions for the CLI management tool.
"""

from models import User, Project, Task


def find_user_by_id(users, user_id):
    """
    Find a user by ID.
    
    Args:
        users (list): List of User objects
        user_id (int): ID to search for
        
    Returns:
        User or None: User object if found, None otherwise
    """
    return next((user for user in users if user.id == user_id), None)


def find_user_by_email(users, email):
    """
    Find a user by email address.
    
    Args:
        users (list): List of User objects
        email (str): Email to search for
        
    Returns:
        User or None: User object if found, None otherwise
    """
    return next((user for user in users if user.email == email), None)


def find_project_by_id(projects, project_id):
    """
    Find a project by ID.
    
    Args:
        projects (list): List of Project objects
        project_id (int): ID to search for
        
    Returns:
        Project or None: Project object if found, None otherwise
    """
    return next((project for project in projects if project.id == project_id), None)


def find_task_by_id(tasks, task_id):
    """
    Find a task by ID.
    
    Args:
        tasks (list): List of Task objects
        task_id (int): ID to search for
        
    Returns:
        Task or None: Task object if found, None otherwise
    """
    return next((task for task in tasks if task.id == task_id), None)


def get_user_projects(user, projects):
    """
    Get all projects for a specific user.
    
    Args:
        user (User): User object
        projects (list): List of all Project objects
        
    Returns:
        list: List of projects owned by the user
    """
    return [p for p in projects if p.owner_id == user.id]


def get_project_tasks(project, tasks):
    """
    Get all tasks for a specific project.
    
    Args:
        project (Project): Project object
        tasks (list): List of all Task objects
        
    Returns:
        list: List of tasks in the project
    """
    return [t for t in tasks if t.project_id == project.id]


def validate_user_exists(user_id, users):
    """
    Validate that a user exists.
    
    Args:
        user_id (int): User ID to check
        users (list): List of User objects
        
    Returns:
        tuple: (bool, str) - (exists, message)
    """
    user = find_user_by_id(users, user_id)
    if user:
        return True, f"User found: {user.name}"
    return False, f"User with ID {user_id} not found"


def validate_project_exists(project_id, projects):
    """
    Validate that a project exists.
    
    Args:
        project_id (int): Project ID to check
        projects (list): List of Project objects
        
    Returns:
        tuple: (bool, str) - (exists, message)
    """
    project = find_project_by_id(projects, project_id)
    if project:
        return True, f"Project found: {project.title}"
    return False, f"Project with ID {project_id} not found"


def validate_task_exists(task_id, tasks):
    """
    Validate that a task exists.
    
    Args:
        task_id (int): Task ID to check
        tasks (list): List of Task objects
        
    Returns:
        tuple: (bool, str) - (exists, message)
    """
    task = find_task_by_id(tasks, task_id)
    if task:
        return True, f"Task found: {task.title}"
    return False, f"Task with ID {task_id} not found"


def print_table_header(headers, widths):
    """
    Print a formatted table header.
    
    Args:
        headers (list): List of header names
        widths (list): List of column widths
    """
    row = " | ".join(header.ljust(width) for header, width in zip(headers, widths))
    print(row)
    print("-" * len(row))


def print_table_row(values, widths):
    """
    Print a formatted table row.
    
    Args:
        values (list): List of values to print
        widths (list): List of column widths
    """
    row = " | ".join(str(value).ljust(width) for value, width in zip(values, widths))
    print(row)
