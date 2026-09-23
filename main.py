
from fastapi import FastAPI

from routers import support, todo

app = FastAPI()


app.include_router(todo.router)
app.include_router(support.router)


# Path operation decorator for the root endpoint
@app.get("/")
async def hello_world():
    return {"message": "Hello World"}
