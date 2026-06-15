# CLI Project Management Tool

A command-line project management tool designed for teams to manage users, projects, and tasks with a clean, intuitive interface.

## Features

- **User Management**: Add, list, and view team members with email validation
- **Project Management**: Create projects with descriptions and due dates
- **Task Management**: Assign tasks to projects and track their status
- **Data Persistence**: All data is saved to JSON files automatically
- **Rich CLI Output**: Beautiful, color-coded tables and formatted output
- **Relationship Management**: Organize users, projects, and tasks with proper relationships

## Project Structure

```
CLI-management-tool/
├── main.py                 # CLI entry point
├── requirements.txt        # Python dependencies
├── test_management_tool.py # Unit tests
├── README.md              # This file
├── models/                # Data model classes
│   ├── __init__.py
│   ├── user.py           # User model
│   ├── project.py        # Project model
│   └── task.py           # Task model
├── utils/                 # Utility functions
│   ├── __init__.py
│   ├── storage.py        # JSON persistence
│   └── helpers.py        # Helper functions
└── data/                  # Data storage (auto-created)
    ├── users.json
    ├── projects.json
    └── tasks.json
```

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/kavutsss/CLI-management-tool.git
   cd CLI-management-tool
   ```

2. **Create a virtual environment** (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### User Commands

#### Add a User
```bash
python main.py add-user "John Doe" "john@example.com"
```

#### List All Users
```bash
python main.py list-users
```

#### Get User Details
```bash
python main.py get-user 1000
```

### Project Commands

#### Add a Project
```bash
python main.py add-project "Project Alpha" "Build new feature" "2025-12-31" 1000
```

Arguments:
- `title`: Project name
- `description`: Project description
- `due_date`: Due date in YYYY-MM-DD format
- `owner_id`: User ID of the project owner

#### List All Projects
```bash
python main.py list-projects
```

#### Get Project Details
```bash
python main.py get-project 2000
```

#### List User's Projects
```bash
python main.py list-user-projects 1000
```

### Task Commands

#### Add a Task
```bash
python main.py add-task "Complete design mockups" 2000 1000 --description "UI and UX designs"
```

Arguments:
- `title`: Task title
- `project_id`: ID of the project
- `assigned_to`: User ID to assign the task to
- `--description`: Optional task description

#### List Project Tasks
```bash
python main.py list-tasks 2000
```

#### Get Task Details
```bash
python main.py get-task 3000
```

#### Complete a Task
```bash
python main.py complete-task 3000
```

## Data Model

### User
- **ID**: Auto-generated unique identifier
- **Name**: Full name of the user
- **Email**: Email address (must be valid)
- **Projects**: List of project IDs owned by the user

### Project
- **ID**: Auto-generated unique identifier
- **Title**: Project name
- **Description**: Project details
- **Due Date**: Expected completion date (YYYY-MM-DD)
- **Owner ID**: ID of the user who owns the project
- **Tasks**: List of task IDs in the project
- **Contributors**: List of user IDs contributing to the project
- **Created At**: Timestamp of creation

### Task
- **ID**: Auto-generated unique identifier
- **Title**: Task name
- **Description**: Task details
- **Status**: One of "pending", "in_progress", or "completed"
- **Project ID**: ID of the parent project
- **Assigned To**: User ID assigned to the task
- **Created At**: Timestamp of creation
- **Completed At**: Timestamp when completed (if applicable)

## Relationships

### One-to-Many: User → Projects
- A user can own multiple projects
- Each project has one owner

### One-to-Many: Project → Tasks
- A project can contain multiple tasks
- Each task belongs to one project

### Many-to-Many: Project ↔ Contributors
- A project can have multiple contributors
- A user can contribute to multiple projects

## Testing

Run the unit tests to verify all functionality:

```bash
python -m unittest test_management_tool.py
```

Run tests with verbose output:

```bash
python -m unittest test_management_tool.py -v
```

### Test Coverage

The test suite includes:
- User model creation and validation
- Project model creation and validation
- Task model creation and validation
- Data persistence (save/load operations)
- Helper functions for searching and filtering
- Relationship tests between entities

## Data Persistence

All data is automatically persisted to JSON files in the `data/` directory:

- `data/users.json`: User information
- `data/projects.json`: Project information
- `data/tasks.json`: Task information

These files are created automatically on first run and updated with each operation.

## OOP Features

The tool demonstrates several OOP concepts:

- **Classes**: User, Project, Task models
- **Properties**: @property decorators for controlled access
- **Class Methods**: `from_dict()` for object instantiation from JSON
- **Instance Methods**: CRUD operations on each model
- **Class Attributes**: ID counters for auto-generation
- **Inheritance**: Potential for Person base class
- **Encapsulation**: Private attributes with validation through properties

## Error Handling

The tool includes robust error handling for:
- Invalid email formats
- Non-existent user/project/task IDs
- Invalid date formats
- File I/O errors
- JSON parsing errors
- Duplicate email registration

## Dependencies

- **rich** (13.7.0): For beautiful CLI output with tables and panels

## Known Issues

- Email must contain "@" symbol for basic validation
- Due date must be in YYYY-MM-DD format
- Project owner cannot be removed from contributors list
- Task status updates do not cascade to parent project

## Future Enhancements

- Task dependencies
- Project milestones
- User roles and permissions
- Task comments and attachments
- Due date notifications
- Bulk operations
- Export to CSV
- API backend integration

## Contributing

To contribute to this project:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is open source and available under the MIT License.

## Author

Created as a comprehensive CLI management tool demonstrating Python OOP, data persistence, and command-line interface design.

## Quick Start Example

```bash
# Add users
python main.py add-user "Alice Johnson" "alice@company.com"
python main.py add-user "Bob Smith" "bob@company.com"

# List users
python main.py list-users

# Create a project
python main.py add-project "Website Redesign" "Modernize company website" "2025-06-30" 1000

# Add tasks
python main.py add-task "Create mockups" 2000 1000 --description "Design UI mockups"
python main.py add-task "Implement frontend" 2000 1001 --description "Build React components"

# List project tasks
python main.py list-tasks 2000

# Complete a task
python main.py complete-task 3000

# View project details
python main.py get-project 2000
```

## Support

For issues or questions, please open an issue on GitHub.