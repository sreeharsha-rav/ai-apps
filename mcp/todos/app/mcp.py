from typing import List
from fastmcp import FastMCP
from jose import jwt, JWTError
from app.services import (
    AuthService,
    TodoService,
    get_auth_service,
    get_todo_service
)
from app.schemas import (
    RegisterRequest,
    LoginRequest,
    TokenResponse,
    TodoRequest,
    TodoResponse
)
from app.database.models import Base
from app.database.db import engine
from app.config import settings

# TODO: setup logging for FastMCP

# Constants
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"

# Initialize FastAPI app
mcp = FastMCP(
    name="todos-mcp",
    instructions="Todos manager with authentication. Use tools: ",
    version="1.0.0"
)

# TODO: CORS Middleware for MCP

# FUTURE: Exception Handlers

# Database Setup
Base.metadata.create_all(bind=engine)

# Security
async def get_current_user(token: str = Depends(oauth2_scheme), auth_service: AuthService = Depends(get_auth_service)):
    """
    Dependency to get the current authenticated user.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token.")

    user = auth_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

@mcp.tool
async def create_todo(todo_request: TodoRequest, user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)):
    """
    Create a new todo for the authenticated user.
    """
    return todo_service.create_todo(todo_request.model_dump(), user.id)

@mcp.tool
async def update_todo(todo_request: TodoRequest, todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)):
    """
    Update a specific todo by ID for the authenticated user.
    """
    return todo_service.update_todo(todo_id, todo_request.model_dump(), user.id)

@mcp.tool
async def delete_todo(todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)):
    """
    Delete a specific todo by ID for the authenticated user.
    """
    return todo_service.delete_todo(todo_id, user.id)

@mcp.tool
async def get_all_todos(user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)):
    """
    Get all todos for the authenticated user.
    """
    return todo_service.get_all_todos(user.id)

@mcp.tool
async def get_todo_by_id(todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)):
    """
    Get a specific todo by ID for the authenticated user.
    """
    return todo_service.get_todo_by_id(todo_id, user.id)
