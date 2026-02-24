from typing import List
from fastapi import HTTPException, status, Path
from fastmcp import FastMCP
from fastmcp.dependencies import Depends, CurrentAccessToken
from fastmcp.server.auth.providers.jwt import JWTVerifier
from app.services import (
    AuthService,
    TodoService,
    get_auth_service,
    get_todo_service
)
from app.schemas import (
    TodoRequest,
    TodoResponse
)
from app.config import settings


# Constants
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM

# Initialize FastMCP server with JWT authentication
mcp = FastMCP(
    name="todos-mcp",
    instructions="Todos manager with authentication. Use tools: ",
    version="1.0.0",
    auth=JWTVerifier(
        public_key=SECRET_KEY,
        algorithm=ALGORITHM,
        base_url=f"{settings.ROOT_URL}{settings.MCP_MOUNT_PREFIX}"
    )
)

# Security
async def get_current_user(
    access_token: CurrentAccessToken,
    auth_service: AuthService = Depends(get_auth_service)
):
    """
    Dependency to get the current authenticated user using FastMCP's CurrentAccessToken.
    """
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    username = access_token.claims.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: missing subject.")

    user = auth_service.get_user_by_username(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

# MCP Tools
@mcp.tool
async def create_todo(todo_request: TodoRequest, user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> dict:
    """
    Create a new todo for the authenticated user.
    """
    return todo_service.create_todo(todo_request.model_dump(), user.id)

@mcp.tool
async def update_todo(todo_request: TodoRequest, todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> None:
    """
    Update a specific todo by ID for the authenticated user.
    """
    return todo_service.update_todo(todo_id, todo_request.model_dump(), user.id)

@mcp.tool
async def delete_todo(todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> None:
    """
    Delete a specific todo by ID for the authenticated user.
    """
    return todo_service.delete_todo(todo_id, user.id)

@mcp.tool
async def get_all_todos(user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> List[TodoResponse]:
    """
    Get all todos for the authenticated user.
    """
    return todo_service.get_all_todos(user.id)

@mcp.tool
async def get_todo_by_id(todo_id: str = Path(...), user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> TodoResponse:
    """
    Get a specific todo by ID for the authenticated user.
    """
    return todo_service.get_todo_by_id(todo_id, user.id)
