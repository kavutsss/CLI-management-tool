"""
Project model representing a project that can contain tasks.
"""

from datetime import datetime


class Project:
    """
    Represents a project in the system.
    
    Attributes:
        id: Unique identifier for the project
        title: Project title
        description: Project description
        due_date: Project due date
        owner_id: ID of the user who owns the project
        tasks: List of task IDs in the project
        contributors: List of user IDs contributing to the project
    """
    
    _id_counter = 2000
    
    def __init__(self, title, description, due_date, owner_id, project_id=None):
        """
        Initialize a new Project.
        
        Args:
            title (str): Project title
            description (str): Project description
            due_date (str): Due date in format YYYY-MM-DD
            owner_id (int): ID of the project owner
            project_id (int, optional): Custom project ID. Auto-generated if not provided
        """
        if project_id is None:
            self.id = Project._id_counter
            Project._id_counter += 1
        else:
            self.id = project_id
            if project_id >= Project._id_counter:
                Project._id_counter = project_id + 1
        
        self._title = title
        self._description = description
        self._due_date = self._validate_date(due_date)
        self.owner_id = owner_id
        self.tasks = []
        self.contributors = [owner_id]
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def _validate_date(date_str):
        """
        Validate date format.
        
        Args:
            date_str (str): Date string to validate
            
        Returns:
            str: Validated date string
            
        Raises:
            ValueError: If date format is invalid
        """
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
    
    @property
    def title(self):
        """Get the project title."""
        return self._title
    
    @title.setter
    def title(self, value):
        """Set the project title."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value
    
    @property
    def description(self):
        """Get the project description."""
        return self._description
    
    @description.setter
    def description(self, value):
        """Set the project description."""
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value
    
    @property
    def due_date(self):
        """Get the project due date."""
        return self._due_date
    
    @due_date.setter
    def due_date(self, value):
        """Set the project due date."""
        self._due_date = self._validate_date(value)
    
    def add_task(self, task_id):
        """
        Add a task to the project.
        
        Args:
            task_id (int): The ID of the task to add
        """
        if task_id not in self.tasks:
            self.tasks.append(task_id)
    
    def remove_task(self, task_id):
        """
        Remove a task from the project.
        
        Args:
            task_id (int): The ID of the task to remove
        """
        if task_id in self.tasks:
            self.tasks.remove(task_id)
    
    def add_contributor(self, user_id):
        """
        Add a contributor to the project.
        
        Args:
            user_id (int): The ID of the user to add as contributor
        """
        if user_id not in self.contributors:
            self.contributors.append(user_id)
    
    def remove_contributor(self, user_id):
        """
        Remove a contributor from the project.
        
        Args:
            user_id (int): The ID of the user to remove
        """
        if user_id in self.contributors and user_id != self.owner_id:
            self.contributors.remove(user_id)
    
    def to_dict(self):
        """
        Convert project instance to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the project
        """
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "due_date": self._due_date,
            "owner_id": self.owner_id,
            "tasks": self.tasks,
            "contributors": self.contributors,
            "created_at": self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Project instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing project data
            
        Returns:
            Project: A new Project instance
        """
        project = cls(
            data["title"],
            data["description"],
            data["due_date"],
            data["owner_id"],
            data.get("id")
        )
        project.tasks = data.get("tasks", [])
        project.contributors = data.get("contributors", [project.owner_id])
        project.created_at = data.get("created_at", project.created_at)
        return project
    
    def __str__(self):
        """String representation of the project."""
        return f"Project(ID: {self.id}, Title: {self._title}, Due: {self._due_date}, Owner: {self.owner_id})"
    
    def __repr__(self):
        """Developer-friendly representation of the project."""
        return f"Project(id={self.id}, title='{self._title}', due_date='{self._due_date}')"
