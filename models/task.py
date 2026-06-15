"""
Task model representing a task within a project.
"""

from datetime import datetime


class Task:
    """
    Represents a task in a project.
    
    Attributes:
        id: Unique identifier for the task
        title: Task title
        status: Task status (pending, in_progress, completed)
        assigned_to: ID of the user assigned to the task
        project_id: ID of the project the task belongs to
        description: Task description
    """
    
    _id_counter = 3000
    VALID_STATUSES = ["pending", "in_progress", "completed"]
    
    def __init__(self, title, project_id, assigned_to, status="pending", 
                 description="", task_id=None):
        """
        Initialize a new Task.
        
        Args:
            title (str): Task title
            project_id (int): ID of the project this task belongs to
            assigned_to (int): ID of the user assigned to this task
            status (str): Task status (default: "pending")
            description (str): Task description
            task_id (int, optional): Custom task ID. Auto-generated if not provided
        """
        if task_id is None:
            self.id = Task._id_counter
            Task._id_counter += 1
        else:
            self.id = task_id
            if task_id >= Task._id_counter:
                Task._id_counter = task_id + 1
        
        self._title = title
        self.project_id = project_id
        self.assigned_to = assigned_to
        self._status = self._validate_status(status)
        self._description = description
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.completed_at = None
    
    @staticmethod
    def _validate_status(status):
        """
        Validate task status.
        
        Args:
            status (str): Status to validate
            
        Returns:
            str: Validated status
            
        Raises:
            ValueError: If status is invalid
        """
        if status not in Task.VALID_STATUSES:
            raise ValueError(f"Status must be one of {Task.VALID_STATUSES}")
        return status
    
    @property
    def title(self):
        """Get the task title."""
        return self._title
    
    @title.setter
    def title(self, value):
        """Set the task title."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value
    
    @property
    def status(self):
        """Get the task status."""
        return self._status
    
    @status.setter
    def status(self, value):
        """Set the task status."""
        self._status = self._validate_status(value)
        if value == "completed":
            self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @property
    def description(self):
        """Get the task description."""
        return self._description
    
    @description.setter
    def description(self, value):
        """Set the task description."""
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value
    
    def mark_complete(self):
        """Mark the task as completed."""
        self.status = "completed"
        self.completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def mark_in_progress(self):
        """Mark the task as in progress."""
        self.status = "in_progress"
    
    def mark_pending(self):
        """Mark the task as pending."""
        self.status = "pending"
    
    def to_dict(self):
        """
        Convert task instance to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the task
        """
        return {
            "id": self.id,
            "title": self._title,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "status": self._status,
            "description": self._description,
            "created_at": self.created_at,
            "completed_at": self.completed_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Task instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing task data
            
        Returns:
            Task: A new Task instance
        """
        task = cls(
            data["title"],
            data["project_id"],
            data["assigned_to"],
            data.get("status", "pending"),
            data.get("description", ""),
            data.get("id")
        )
        task.created_at = data.get("created_at", task.created_at)
        task.completed_at = data.get("completed_at", None)
        return task
    
    def __str__(self):
        """String representation of the task."""
        return f"Task(ID: {self.id}, Title: {self._title}, Status: {self._status}, Assigned to: {self.assigned_to})"
    
    def __repr__(self):
        """Developer-friendly representation of the task."""
        return f"Task(id={self.id}, title='{self._title}', status='{self._status}')"
