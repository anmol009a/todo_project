# To-Do List App Backend

A simple To-Do List backend application built with Django and Django Rest Framework (DRF). This app supports creating, reading, updating, and deleting (CRUD) tasks and includes user authentication, test coverage, and CI/CD integration.


# **Table of Contents**
- [To-Do List App Backend](#to-do-list-app-backend)
- [**Table of Contents**](#table-of-contents)
  - [Features](#features)
  - [Technology Stack](#technology-stack)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [API Documentation](#api-documentation)
  - [Authentication](#authentication)
  - [Testing](#testing)
    - [Run Tests](#run-tests)
  - [Deployment](#deployment)
  - [Generated Documentation](#generated-documentation)
  - [Directory Structure](#directory-structure)
  - [Contributors](#contributors)
    

## Features

- **REST API** for managing to-do items.
- Authentication using Basic Authentication.
- Full CRUD operations for to-do tasks.
- Tagging system with automatic duplicate removal.
- CI/CD pipeline using GitHub Actions.
- Deployed on a cloud server.
- 100% unit and integration test coverage.

---

## Technology Stack

- **Python 3.11+**
- **Django 4.2.7+**
- **Django REST Framework 3.14.0+**
- SQLite (default database)
- GitHub Actions for CI/CD
- Postman for API testing

---

## Prerequisites

- Python 3.11 or higher
- Virtualenv for Python virtual environment
- Git
- Internet access for installing dependencies

---

## Installation

1. Clone the repository:
    ```bash
    git clone https://<personal_access_token>@github.com/anmol009a/todo_project.git
    cd todo_project
    ```
2. Set up a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate 
    # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Apply database migrations:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5. Create a superuser (for accessing the admin panel):
    ```bash
    python manage.py createsuperuser
    ```

## Running the Application

1. Start the development server:
    ```bash
    python manage.py runserver
     ```

2. The app will be accessible at:
   - API: http://127.0.0.1:8000/api/todos/
   - Admin Panel: http://127.0.0.1:8000/admin/

## API Documentation

   - DRF Browsable API: BASEURL/api/swagger-ui
   - Swagger API: BASEURL/api/todos
   - ReDoc API: BASEURL/api/redoc

| Method | Endpoint | Description              |
| ------ | -------- | ------------------------ |
| GET    | /        | List all tasks           |
| POST   | /        | Create a new task        |
| GET    | /{id}/   | Retrieve a specific task |
| PUT    | /{id}/   | Update a specific task   |
| PATCH  | /{id}/   | Partially update a task  |
| DELETE | /{id}/   | Delete a specific task   |

## Authentication
- All API endpoints are protected with Basic Authentication.
- Use your username and password to authenticate.
  
## Testing

### Run Tests
```bash
python manage.py test
```


## Deployment
<!-- todo: deploy app -->
- Hosted on PythonAnywhere.
- Visit the live app [here](https://anmol009a.pythonanywhere.com/).

## Generated Documentation
<!-- todo: add link -->
The codebase documentation is hosted as a static site [here](https://todo.static.domains/todo_app/index.html).

## Directory Structure
```
todo_project/
├── todo_app/
│   ├── migrations/
│   ├── templates/
│   ├── tests/         
│   ├── views.py
│   ├── models.py
│   ├── urls.py
│   └── serializers.py
├── todo_project/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── requirements.txt
├── README.md
└── manage.py
```

## Contributors
Anmol Sharma - Backend Developer