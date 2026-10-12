# learning-e2e-apps
Repository dedicated to learn from scratch how to deploy Apps [Python FastAPI PostgreSQL Docker CI/CD AWS]. With explanations :)

## Overview

This project is a REST API built with **FastAPI** to manage a To Do List. It includes CRUD operations for tasks, file attachment functionality, and asynchronous endpoints. The project is designed to be modular and scalable, making it a great learning resource for deploying applications with modern tools and technologies.

---

## Project Structure

- **`main.py`**: The entry point of the application. It initializes the FastAPI app and includes the routers defined in the `routers` folder.
- **`routers/`**: Contains the route definitions for the API.
  - **`todo.py`**: Handles all routes related to the To Do List.
  - **`support.py`**: (Placeholder) May contain additional routes or helper functions.
- **`env/`**: Virtual environment containing the dependencies required to run the application.
- **`async_requests.sh` and `async_request.txt`**: Auxiliary files, possibly for testing or demonstrating asynchronous requests.

---

## Features

### Models and Data
- **`TodoI`**: A Pydantic model that defines the structure of a To Do item with the following fields:
  - `id`: Optional integer ID of the task.
  - `description`: A string (1-100 characters) describing the task.
  - `completed`: A boolean indicating whether the task is completed.
  - `file_name`: Optional string for the name of an attached file.
  - `file_size`: Optional integer for the size of an attached file.

- **`TODO_LIST`**: A pre-populated list of tasks for demonstration purposes.

### API Endpoints
#### To Do List Management
- **`GET /api/to_do`**: Retrieve all tasks or filter by completion status.
- **`GET /api/to_do/{todo_id}`**: Retrieve a specific task by its ID.
- **`POST /api/to_do`**: Create a new task by providing `id`, `description`, and `completed` in the request body.
- **`POST /api/create_to_do`**: Create a new task using the `TodoI` model.

#### File Attachment
- **`POST /api/todo/{todo_id}/attach-file`**: Attach a file (as bytes) to a task and update its size.
- **`POST /api/todo/{todo_id}/attach-file-upload`**: Attach a file (as `UploadFile`) to a task and update its name and size.

#### Asynchronous Endpoint
- **`GET /api/async-endpoint`**: Simulates a long-running task with a 2-second delay.

---

## How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/learning-e2e-apps.git
   cd learning-e2e-apps