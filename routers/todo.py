
import asyncio
import datetime

from fastapi import APIRouter, File, HTTPException, Body, Path, UploadFile

from typing import Annotated, Optional

from pydantic import BaseModel, Field

router = APIRouter(prefix="/api", tags=["To Do List"])


# Model for the To Do
class TodoI(BaseModel):
    id: Optional[int] = None
    description: str = Field(min_length=1, max_length=100)
    completed: bool = Field(default=False)
    date: datetime.datetime = Field(default_factory=datetime.datetime.now)
    file_content: Optional[bytes] = None
    file_name: Optional[str] = None
    file_size: Optional[int] = None


TODO_LIST: list[TodoI] = [
    TodoI(id=1, description="Laundry", completed=False),
    TodoI(id=2, description="Grocery Shopping", completed=True),
    TodoI(id=3, description="Clean the House", completed=False),
    TodoI(id=4, description="Pay Bills", completed=True),
    TodoI(id=5, description="Exercise", completed=True),
]


def _next_id() -> int:
    return max((todo.id for todo in TODO_LIST if todo.id is not None), default=0) + 1


def _get_todo_or_404(todo_id: int) -> TodoI:
    todo_item = next((todo for todo in TODO_LIST if todo.id == todo_id), None)
    if todo_item is None:
        raise HTTPException(status_code=404, detail="To Do item not found")
    return todo_item

# Path operation decorator for the to_do endpoint
# Endpoint to read all To Do items, optionally filtered by completion status
# The petition is /api/to_do?completed=true indicating that only completed To Do items should be returned.
# If no parameter is provided, /api/to_do.
@router.get("/to_do_completed", response_model=list[TodoI])
async def read_to_do(completed: Optional[bool] = None):
    if completed is not None:
        return [todo for todo in TODO_LIST if todo.completed == completed]
    return TODO_LIST


# Path operation decorator for the to_do/{todo_id} endpoint
# Function defined outside in order to be used by many decorators.
@router.get("/to_do/{todo_id}", response_model=TodoI)
async def read_todo_by_id(todo_id: int):
    return _get_todo_or_404(todo_id)

# Create a new To Do List item validating the data provided in the request via Pydantic model. If the id is not provided, it will be generated automatically.
@router.post("/create_to_do", response_model=TodoI, name="Create To Do List",
             summary="Create a new To Do List item",
             description="This endpoint allows you to create a new To Do List item by providing the necessary information.",
             status_code=201)
async def create_todo_list(data: TodoI):
    if data.id is None:
        data.id = _next_id()
    TODO_LIST.append(data)
    return data

# Path operation decorator for the to_do/{todo_id}/attach-file-upload endpoint
# It attaches a file to the specified To Do item using file upload. It does not create a new To Do item.
@router.post("/todo/{todo_id}/attach-file-upload", response_model=TodoI)
async def attach_file_upload(todo_id: Annotated[int, Path()], file: UploadFile):
    todo_item = _get_todo_or_404(todo_id)
    todo_item.file_name = file.filename
    file_content = await file.read()
    print(file_content)
    todo_item.file_size = len(file_content)
    return todo_item

@router.get("/async-endpoint")
async def async_endpoint():
    print(f"Processing request in async endpoint... at {datetime.datetime.now()}",flush=True)
    # Simulate some processing before the long-running task with asynchronous sleep. time.sleep() would block the thread, so we use asyncio.sleep() instead.
    await asyncio.sleep(2)  # Simulate a long-running task
    return {"message": "This is an asynchronous endpoint."}
