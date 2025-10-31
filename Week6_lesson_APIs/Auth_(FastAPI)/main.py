from fastapi import FastAPI, HTTPException, Header, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="To-Do List API with Authentication")

# In-memory storage
todos = []
next_id = 1

# Secret API Key
API_KEY = "secret"

# Pydantic models
class TodoCreate(BaseModel):
    task: str

class Todo(BaseModel):
    id: int
    task: str


# API key validation
def verify_api_key(x_api_key: Optional[str]):
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key"
        )

# Root endpoint
@app.get("/")
def root():
    return {"detail": "Todo FastAPI with Auth"}

# GET /todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos


# POST /todos
@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(todo_data: TodoCreate):
    global next_id
    todo = {"id": next_id, "task": todo_data.task}
    todos.append(todo)
    next_id += 1
    return todo


# DELETE /todos/{id}
@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, x_api_key: Optional[str] = Header(None)):
    verify_api_key(x_api_key)

    for todo in todos:
        if todo["id"] == todo_id:
            todos.remove(todo)
            return  # 204 No Content

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with ID {todo_id} not found"
    )
