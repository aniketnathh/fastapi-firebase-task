# FastAPI Firebase Task Manager

A simple **Task Management API** built with **FastAPI** and **Firebase**.  
Users can **sign up, log in, manage their tasks**, and store data securely in **Firestore**.

---

## Features

- User Authentication with **Firebase**
- CRUD operations for tasks:
  - Create a new task
  - Read all tasks or a single task
  - Update a task
  - Delete a task
- Store tasks in **Firestore**
- Token-based authentication for secure endpoints

---

## Project Structure

├── main.py # Main FastAPI application
├── model.py # Pydantic schemas for requests/responses
├── serviceAccountKey.json # Firebase service account (keep private)
├── Pipfile # Dependencies
├── Pipfile.lock # Lock file for reproducible environment
└── .env # Firebase config (not pushed to GitHub)


---

## Setup Instructions

1. **Clone the repository**

git clone https://github.com/your-username/fastapi-firebase-task.git
cd fastapi-firebase-task
Install dependencies

pip install pipenv
pipenv install
pipenv shell


Firebase Configuration

Create a .env file in the project root:

API_KEY=your_api_key
AUTH_DOMAIN=your_project.firebaseapp.com
PROJECT_ID=your_project_id
STORAGE_BUCKET=your_project.appspot.com
MESSAGING_SENDER_ID=your_sender_id
APP_ID=your_app_id
MEASUREMENT_ID=your_measurement_id
DATABASE_URL=


Place your serviceAccountKey.json in the root directory.

Running the API
uvicorn main:app --reload


Open your browser at: http://127.0.0.1:8000

Swagger Docs are available at the same URL.

API Endpoints
User Authentication
Method	Endpoint	Description
POST	/signup	Create a new user
POST	/login	Log in user and get token
GET	/user/me	Get current user profile
PUT	/user/update	Update user full name
Task Management
Method	Endpoint	Description
POST	/tasks/	Create a new task
GET	/tasks/	Get all tasks
GET	/tasks/{task_id}	Get a single task by ID
PUT	/tasks/{task_id}	Update a task by ID
DELETE	/tasks/{task_id}	Delete a task by ID
Example Request (Create Task)

Header:

Authorization: Bearer <your_token_here>
Content-Type: application/json


Body:

{
  "title": "Buy groceries",
  "description": "Milk, Eggs, Bread",
  "status": "Pending"
}


Response:

{
  "message": "Task created",
  "task_id": "4f5f39e3-732c-4ba6-b8af-7d27cf9de7e8"
}

Notes

Keep serviceAccountKey.json and .env private.

Make sure to install all dependencies using pipenv or pip.

Use Bearer token from login for all protected routes.
