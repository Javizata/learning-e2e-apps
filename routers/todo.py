
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
@router.get("/to_do", response_model=list[TodoI])
async def read_to_do(completed: Optional[bool] = None):
    if completed is not None:
        return [todo for todo in TODO_LIST if todo.completed == completed]
    return TODO_LIST


# Path operation decorator for the to_do/{todo_id} endpoint
@router.get("/to_do/{todo_id}", response_model=TodoI)
async def read_todo_by_id(todo_id: int):
    return _get_todo_or_404(todo_id)


# Path operation decorator for the to_do endpoint with POST method
@router.post("/to_do", response_model=list[TodoI])
async def create_todo(id: int = Body(), description: str = Body(), completed: bool = Body()):
    TODO_LIST.append(TodoI(id=id, description=description, completed=completed))
    return TODO_LIST


@router.post("/create_to_do", response_model=TodoI, name="Create To Do List",
             summary="Create a new To Do List item",
             description="This endpoint allows you to create a new To Do List item by providing the necessary information.",
             status_code=201)
async def create_todo_list(data: TodoI):
    if data.id is None:
        data.id = _next_id()
    TODO_LIST.append(data)
    return data

@router.get("/async-endpoint")
async def async_endpoint():
    print(f"Processing request in async endpoint... at {datetime.datetime.now()}",flush=True)
    await asyncio.sleep(2)  # Simulate a long-running task
    return {"message": "This is an asynchronous endpoint."}

# Path operation decorator for the to_do/{todo_id}/attach-file endpoint
@router.post("/todo/{todo_id}/attach-file", response_model=TodoI)
async def attach_file(todo_id: Annotated[int, Path()], file: Annotated[bytes, File()]):
    todo_item = _get_todo_or_404(todo_id)
    todo_item.file_size = len(file)
    return todo_item


# Path operation decorator for the to_do/{todo_id}/attach-file-upload endpoint
@router.post("/todo/{todo_id}/attach-file-upload", response_model=TodoI)
async def attach_file_upload(todo_id: Annotated[int, Path()], file: UploadFile):
    todo_item = _get_todo_or_404(todo_id)
    todo_item.file_name = file.filename
    file_content = await file.read()
    todo_item.file_size = len(file_content)
    return todo_item