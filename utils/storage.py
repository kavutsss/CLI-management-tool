"""
Storage module for persisting data to JSON files.
"""

import json
import os
from models import User, Project, Task


class DataStore:
    """
    Handles persistence of users, projects, and tasks to JSON files.
    """
    
    def __init__(self, data_dir="data"):
        """
        Initialize the DataStore.
        
        Args:
            data_dir (str): Directory to store data files
        """
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.projects_file = os.path.join(data_dir, "projects.json")
        self.tasks_file = os.path.join(data_dir, "tasks.json")
        
        # Ensure data directory exists
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        
        # Initialize empty files if they don't exist
        self._init_files()
    
    def _init_files(self):
        """Initialize empty JSON files if they don't exist."""
        for filepath in [self.users_file, self.projects_file, self.tasks_file]:
            if not os.path.exists(filepath):
                with open(filepath, "w") as f:
                    json.dump([], f)
    
    def save_users(self, users):
        """
        Save users to JSON file.
        
        Args:
            users (list): List of User objects
        """
        try:
            data = [user.to_dict() for user in users]
            with open(self.users_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving users: {e}")
    
    def load_users(self):
        """
        Load users from JSON file.
        
        Returns:
            list: List of User objects
        """
        try:
            with open(self.users_file, "r") as f:
                data = json.load(f)
            return [User.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading users: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error loading users: {e}")
            return []
    
    def save_projects(self, projects):
        """
        Save projects to JSON file.
        
        Args:
            projects (list): List of Project objects
        """
        try:
            data = [project.to_dict() for project in projects]
            with open(self.projects_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving projects: {e}")
    
    def load_projects(self):
        """
        Load projects from JSON file.
        
        Returns:
            list: List of Project objects
        """
        try:
            with open(self.projects_file, "r") as f:
                data = json.load(f)
            return [Project.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading projects: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error loading projects: {e}")
            return []
    
    def save_tasks(self, tasks):
        """
        Save tasks to JSON file.
        
        Args:
            tasks (list): List of Task objects
        """
        try:
            data = [task.to_dict() for task in tasks]
            with open(self.tasks_file, "w") as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")
    
    def load_tasks(self):
        """
        Load tasks from JSON file.
        
        Returns:
            list: List of Task objects
        """
        try:
            with open(self.tasks_file, "r") as f:
                data = json.load(f)
            return [Task.from_dict(item) for item in data]
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading tasks: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error loading tasks: {e}")
            return []
