from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="To-Do List API")

# In-memory storage
todos = []
next_id = 1

# Pydantic model for input validation
class TodoCreate(BaseModel):
    task: str

# Pydantic model for returning todos
class Todo(BaseModel):
    id: int
    task: str

# Root endpoint
@app.get("/")
def root():
    return {"detail": "Todo FastAPI"}

# Fetch all todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos


# Add a new todo
@app.post("/todos", response_model=Todo, status_code=201)
def add_todo(todo_data: TodoCreate):
    global next_id
    todo = {"id": next_id, "task": todo_data.task}
    todos.append(todo)
    next_id += 1
    return todo
