"""
Unit tests for the CLI Project Management Tool.

Tests cover:
- User model creation and operations
- Project model creation and operations
- Task model creation and operations
- Data persistence and loading
- Helper functions
"""

import unittest
import os
import json
import tempfile
from models import User, Project, Task
from utils import (
    DataStore,
    find_user_by_id,
    find_user_by_email,
    find_project_by_id,
    find_task_by_id,
    get_user_projects,
    get_project_tasks
)


class TestUserModel(unittest.TestCase):
    """Test cases for the User model."""
    
    def test_user_creation(self):
        """Test basic user creation."""
        user = User("John Doe", "john@example.com")
        self.assertEqual(user.name, "John Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertIsNotNone(user.id)
    
    def test_user_id_auto_increment(self):
        """Test that user IDs auto-increment."""
        initial_counter = User._id_counter
        user1 = User("User One", "user1@example.com")
        user2 = User("User Two", "user2@example.com")
        self.assertEqual(user2.id, user1.id + 1)
    
    def test_user_name_validation(self):
        """Test name validation."""
        user = User("Test", "valid@example.com")
        with self.assertRaises(ValueError):
            user.name = ""
    
    def test_user_email_validation(self):
        """Test email validation."""
        user = User("Test User", "test@example.com")
        with self.assertRaises(ValueError):
            user.email = "invalid-email"
    
    def test_user_to_dict(self):
        """Test user to_dict conversion."""
        user = User("Jane Doe", "jane@example.com")
        user_dict = user.to_dict()
        self.assertEqual(user_dict["name"], "Jane Doe")
        self.assertEqual(user_dict["email"], "jane@example.com")
        self.assertIn("id", user_dict)
    
    def test_user_from_dict(self):
        """Test user from_dict creation."""
        data = {
            "id": 1001,
            "name": "Bob Smith",
            "email": "bob@example.com",
            "projects": []
        }
        user = User.from_dict(data)
        self.assertEqual(user.id, 1001)
        self.assertEqual(user.name, "Bob Smith")
        self.assertEqual(user.email, "bob@example.com")
    
    def test_user_add_project(self):
        """Test adding projects to user."""
        user = User("Test", "test@example.com")
        user.add_project(2000)
        user.add_project(2001)
        self.assertIn(2000, user.projects)
        self.assertIn(2001, user.projects)
    
    def test_user_remove_project(self):
        """Test removing projects from user."""
        user = User("Test", "test@example.com")
        user.add_project(2000)
        user.remove_project(2000)
        self.assertNotIn(2000, user.projects)


class TestProjectModel(unittest.TestCase):
    """Test cases for the Project model."""
    
    def test_project_creation(self):
        """Test basic project creation."""
        project = Project("Test Project", "Description", "2025-12-31", 1000)
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "Description")
        self.assertEqual(project.due_date, "2025-12-31")
        self.assertEqual(project.owner_id, 1000)
        self.assertIsNotNone(project.id)
    
    def test_project_date_validation(self):
        """Test date validation."""
        with self.assertRaises(ValueError):
            Project("Test", "Desc", "12/31/2025", 1000)
    
    def test_project_title_validation(self):
        """Test title validation."""
        project = Project("Valid", "Description", "2025-12-31", 1000)
        with self.assertRaises(ValueError):
            project.title = ""
    
    def test_project_add_task(self):
        """Test adding tasks to project."""
        project = Project("Test", "Desc", "2025-12-31", 1000)
        project.add_task(3000)
        project.add_task(3001)
        self.assertIn(3000, project.tasks)
        self.assertIn(3001, project.tasks)
    
    def test_project_add_contributor(self):
        """Test adding contributors to project."""
        project = Project("Test", "Desc", "2025-12-31", 1000)
        project.add_contributor(1001)
        self.assertIn(1001, project.contributors)
        self.assertIn(1000, project.contributors)  # Owner should be included
    
    def test_project_to_dict(self):
        """Test project to_dict conversion."""
        project = Project("Alpha", "Project Alpha", "2025-06-30", 1000)
        proj_dict = project.to_dict()
        self.assertEqual(proj_dict["title"], "Alpha")
        self.assertEqual(proj_dict["owner_id"], 1000)
        self.assertIn("id", proj_dict)
    
    def test_project_from_dict(self):
        """Test project from_dict creation."""
        data = {
            "id": 2001,
            "title": "Beta",
            "description": "Project Beta",
            "due_date": "2025-12-31",
            "owner_id": 1000,
            "tasks": [3000],
            "contributors": [1000, 1001],
            "created_at": "2024-01-01 10:00:00"
        }
        project = Project.from_dict(data)
        self.assertEqual(project.id, 2001)
        self.assertEqual(project.title, "Beta")
        self.assertEqual(project.tasks, [3000])


class TestTaskModel(unittest.TestCase):
    """Test cases for the Task model."""
    
    def test_task_creation(self):
        """Test basic task creation."""
        task = Task("Complete Design", 2000, 1000)
        self.assertEqual(task.title, "Complete Design")
        self.assertEqual(task.project_id, 2000)
        self.assertEqual(task.assigned_to, 1000)
        self.assertEqual(task.status, "pending")
    
    def test_task_status_validation(self):
        """Test status validation."""
        with self.assertRaises(ValueError):
            Task("Test", 2000, 1000, status="invalid_status")
    
    def test_task_mark_complete(self):
        """Test marking task as complete."""
        task = Task("Test Task", 2000, 1000)
        task.mark_complete()
        self.assertEqual(task.status, "completed")
        self.assertIsNotNone(task.completed_at)
    
    def test_task_mark_in_progress(self):
        """Test marking task as in progress."""
        task = Task("Test Task", 2000, 1000)
        task.mark_in_progress()
        self.assertEqual(task.status, "in_progress")
    
    def test_task_to_dict(self):
        """Test task to_dict conversion."""
        task = Task("Work Item", 2000, 1000, description="Important work")
        task_dict = task.to_dict()
        self.assertEqual(task_dict["title"], "Work Item")
        self.assertEqual(task_dict["status"], "pending")
        self.assertEqual(task_dict["description"], "Important work")
    
    def test_task_from_dict(self):
        """Test task from_dict creation."""
        data = {
            "id": 3001,
            "title": "Review Code",
            "project_id": 2000,
            "assigned_to": 1000,
            "status": "in_progress",
            "description": "Code review",
            "created_at": "2024-01-01 10:00:00",
            "completed_at": None
        }
        task = Task.from_dict(data)
        self.assertEqual(task.id, 3001)
        self.assertEqual(task.title, "Review Code")
        self.assertEqual(task.status, "in_progress")


class TestDataStore(unittest.TestCase):
    """Test cases for the DataStore persistence layer."""
    
    def setUp(self):
        """Set up temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.store = DataStore(self.test_dir)
    
    def tearDown(self):
        """Clean up temporary files."""
        import shutil
        shutil.rmtree(self.test_dir)
    
    def test_save_and_load_users(self):
        """Test saving and loading users."""
        users = [
            User("Alice", "alice@example.com"),
            User("Bob", "bob@example.com")
        ]
        self.store.save_users(users)
        loaded = self.store.load_users()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].name, "Alice")
        self.assertEqual(loaded[1].name, "Bob")
    
    def test_save_and_load_projects(self):
        """Test saving and loading projects."""
        projects = [
            Project("Project A", "Description A", "2025-12-31", 1000),
            Project("Project B", "Description B", "2025-06-30", 1000)
        ]
        self.store.save_projects(projects)
        loaded = self.store.load_projects()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Project A")
        self.assertEqual(loaded[1].title, "Project B")
    
    def test_save_and_load_tasks(self):
        """Test saving and loading tasks."""
        tasks = [
            Task("Task 1", 2000, 1000),
            Task("Task 2", 2000, 1001, status="in_progress")
        ]
        self.store.save_tasks(tasks)
        loaded = self.store.load_tasks()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].title, "Task 1")
        self.assertEqual(loaded[1].status, "in_progress")


class TestHelperFunctions(unittest.TestCase):
    """Test cases for helper functions."""
    
    def setUp(self):
        """Set up test data."""
        self.users = [
            User("Alice", "alice@example.com"),
            User("Bob", "bob@example.com")
        ]
        self.projects = [
            Project("Project A", "Desc A", "2025-12-31", self.users[0].id),
            Project("Project B", "Desc B", "2025-06-30", self.users[1].id)
        ]
        self.tasks = [
            Task("Task 1", self.projects[0].id, self.users[0].id),
            Task("Task 2", self.projects[0].id, self.users[1].id)
        ]
    
    def test_find_user_by_id(self):
        """Test finding user by ID."""
        user = find_user_by_id(self.users, self.users[0].id)
        self.assertEqual(user.name, "Alice")
    
    def test_find_user_by_email(self):
        """Test finding user by email."""
        user = find_user_by_email(self.users, "bob@example.com")
        self.assertEqual(user.name, "Bob")
    
    def test_find_project_by_id(self):
        """Test finding project by ID."""
        project = find_project_by_id(self.projects, self.projects[0].id)
        self.assertEqual(project.title, "Project A")
    
    def test_find_task_by_id(self):
        """Test finding task by ID."""
        task = find_task_by_id(self.tasks, self.tasks[0].id)
        self.assertEqual(task.title, "Task 1")
    
    def test_get_user_projects(self):
        """Test getting projects for a user."""
        user_projects = get_user_projects(self.users[0], self.projects)
        self.assertEqual(len(user_projects), 1)
        self.assertEqual(user_projects[0].title, "Project A")
    
    def test_get_project_tasks(self):
        """Test getting tasks for a project."""
        project_tasks = get_project_tasks(self.projects[0], self.tasks)
        self.assertEqual(len(project_tasks), 2)
        self.assertEqual(project_tasks[0].title, "Task 1")


class TestRelationships(unittest.TestCase):
    """Test cases for relationships between entities."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User("TestUser", "test@example.com")
        self.project = Project("TestProject", "Desc", "2025-12-31", self.user.id)
        self.task = Task("TestTask", self.project.id, self.user.id)
    
    def test_user_project_relationship(self):
        """Test one-to-many relationship: User -> Projects."""
        self.user.add_project(self.project.id)
        self.assertIn(self.project.id, self.user.projects)
    
    def test_project_task_relationship(self):
        """Test one-to-many relationship: Project -> Tasks."""
        self.project.add_task(self.task.id)
        self.assertIn(self.task.id, self.project.tasks)
    
    def test_project_contributor_relationship(self):
        """Test many-to-many relationship: Project <- Contributors."""
        other_user = User("OtherUser", "other@example.com")
        self.project.add_contributor(other_user.id)
        self.assertIn(self.user.id, self.project.contributors)
        self.assertIn(other_user.id, self.project.contributors)


if __name__ == "__main__":
    unittest.main()
