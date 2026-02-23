import json
import os
from uuid import uuid4
from datetime import datetime, timezone
from typing import List, Optional
from pydantic import BaseModel, Field
from fastmcp import FastMCP

# -------------------------------
#             Model
# -------------------------------
class TodoItem(BaseModel):
    id: str = Field(default_factory=lambda: f"todo-{uuid4()}", description="Unique identifier for the todo item")
    description: str = Field(..., description="Description of the todo item")
    completed: bool = Field(default=False, description="Completion status of the todo item")
    created_at: str = Field(default_factory=lambda: str(datetime.now(timezone.utc)), description="Creation timestamp of the todo item")
    updated_at: str = Field(default_factory=lambda: str(datetime.now(timezone.utc)), description="Last update timestamp of the todo item")
    
# -------------------------------
#            Storage
# -------------------------------
TODO_FILE = "todos.json"

def load_todos() -> List[TodoItem]:
    """Load todos from JSON file into Pydantic models"""
    if os.path.exists(TODO_FILE):
        with open(TODO_FILE, 'r') as f:
            data = json.load(f)
            return [TodoItem.model_validate(todo) for todo in data]
    return []

def save_todos(todos: List[TodoItem]) -> None:
    """Save todos from Pydantic models to JSON file"""
    data = [todo.model_dump() for todo in todos]
    os.makedirs(os.path.dirname(TODO_FILE) or '.', exist_ok=True)
    with open(TODO_FILE, 'w') as f:
        json.dump(data, f, indent=2)
        
# -------------------------------
#     MCP Tools & Resources
# -------------------------------
mcp = FastMCP(
    name="todo-mcp",
    instructions="""Manage a simple todo list with the following operations: add_todo(), list_todos(), complete_todo(), delete_todo(). 
    Use the provided tools to manipulate the todo items and the resource to get an overview of all todos.""",
)

@mcp.tool
async def add_todo(description: str) -> TodoItem:
    """Add a new todo item with the given description and return the created item"""
    todos = load_todos()
    new_todo = TodoItem(description=description)
    todos.append(new_todo)
    save_todos(todos)
    return new_todo

@mcp.tool
async def list_todos(completed: Optional[bool] = None) -> List[TodoItem]:
    """List all todos, optionally filter by completion status"""
    todos = load_todos()
    if completed is not None:
        todos = [t for t in todos if t.completed == completed]
    
    return todos

@mcp.tool
async def complete_todo(todo_id: str) -> Optional[TodoItem]:
    """Mark a todo as completed by ID, update its timestamp, and return the updated item"""
    todos = load_todos()
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = True
            todo.updated_at = str(datetime.now(timezone.utc))
            save_todos(todos)
            return todo
    return None

@mcp.tool
async def delete_todo(todo_id: str) -> Optional[TodoItem]:
    """Delete a todo by ID and return the deleted item"""
    todos = load_todos()
    for todo in todos:
        if todo.id == todo_id:
            todos.remove(todo)
            save_todos(todos)
            return todo
    return None

@mcp.resource("todos://list")
async def todos_resource() -> str:
    """Get all todos as JSON resource"""
    todos = load_todos()
    return json.dumps([todo.model_dump() for todo in todos])

if __name__ == "__main__":
    mcp.run(transport="http", port=7020)
