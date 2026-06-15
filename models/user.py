"""
User model representing a team member.
"""


class User:
    """
    Represents a user in the project management system.
    
    Attributes:
        id: Unique identifier for the user
        name: User's full name
        email: User's email address
        projects: List of project IDs associated with the user
    """
    
    _id_counter = 1000
    
    def __init__(self, name, email, user_id=None):
        """
        Initialize a new User.
        
        Args:
            name (str): User's full name
            email (str): User's email address
            user_id (int, optional): Custom user ID. Auto-generated if not provided
        """
        if user_id is None:
            self.id = User._id_counter
            User._id_counter += 1
        else:
            self.id = user_id
            if user_id >= User._id_counter:
                User._id_counter = user_id + 1
        
        self._name = name
        self._email = email
        self.projects = []
    
    @property
    def name(self):
        """Get the user's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the user's name."""
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Name must be a non-empty string")
        self._name = value
    
    @property
    def email(self):
        """Get the user's email."""
        return self._email
    
    @email.setter
    def email(self, value):
        """Set the user's email."""
        if not isinstance(value, str) or "@" not in value:
            raise ValueError("Email must be a valid email address")
        self._email = value
    
    def add_project(self, project_id):
        """
        Add a project to the user's project list.
        
        Args:
            project_id (int): The ID of the project to add
        """
        if project_id not in self.projects:
            self.projects.append(project_id)
    
    def remove_project(self, project_id):
        """
        Remove a project from the user's project list.
        
        Args:
            project_id (int): The ID of the project to remove
        """
        if project_id in self.projects:
            self.projects.remove(project_id)
    
    def to_dict(self):
        """
        Convert user instance to dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the user
        """
        return {
            "id": self.id,
            "name": self._name,
            "email": self._email,
            "projects": self.projects
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a User instance from a dictionary.
        
        Args:
            data (dict): Dictionary containing user data
            
        Returns:
            User: A new User instance
        """
        user = cls(data["name"], data["email"], data.get("id"))
        user.projects = data.get("projects", [])
        return user
    
    def __str__(self):
        """String representation of the user."""
        return f"User(ID: {self.id}, Name: {self._name}, Email: {self._email})"
    
    def __repr__(self):
        """Developer-friendly representation of the user."""
        return f"User(id={self.id}, name='{self._name}', email='{self._email}')"
