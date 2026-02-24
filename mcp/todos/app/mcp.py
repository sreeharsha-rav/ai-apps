from contextlib import contextmanager
from typing import Annotated, List

from fastmcp import FastMCP, Context
from fastmcp.dependencies import Depends
from fastmcp.exceptions import ToolError
from fastmcp.server.auth.providers.jwt import JWTVerifier
from fastmcp.server.dependencies import get_access_token
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.config import settings
from app.database.db import SessionLocal
from app.database.repository import TodoRepository, UserRepository
from app.schemas import TodoRequest, TodoResponse
from app.services.auth import AuthService
from app.services.todo import TodoService


# ---------------------------------------------------------------------------
# FastMCP server
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="todos-mcp",
    instructions=(
        "You are a personal todo manager. Users must be authenticated with a "
        "JWT bearer token before calling any tool. Available operations: "
        "list all todos, get a specific todo by ID, create a todo, update a todo, "
        "and delete a todo. Always use the user's verified identity from the token."
    ),
    version="1.0.0",
    auth=JWTVerifier(
        public_key=settings.SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
        base_url=f"{settings.ROOT_URL}/",
    ),
)


# ---------------------------------------------------------------------------
# Dependency providers (FastMCP-native, using fastmcp.dependencies.Depends)
# ---------------------------------------------------------------------------

@contextmanager
def get_db_session():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_auth_service(db: Session = Depends(get_db_session)) -> AuthService:
    return AuthService(UserRepository(db))


def get_todo_service(db: Session = Depends(get_db_session)) -> TodoService:
    return TodoService(TodoRepository(db))


# ---------------------------------------------------------------------------
# Auth helper
# ---------------------------------------------------------------------------

def _require_user(auth_service: AuthService):
    """Read the verified JWT from the HTTP request scope and return the DB user."""
    token = get_access_token()
    if not token:
        raise ToolError("Not authenticated. Provide a valid JWT bearer token.")
    username = token.claims.get("sub")
    if not username:
        raise ToolError("Invalid token: missing 'sub' claim.")
    user = auth_service.get_user_by_username(username)
    if user is None:
        raise ToolError(f"Authenticated user '{username}' not found in the database.")
    return user


# ---------------------------------------------------------------------------
# Output wrapper — lists must be returned as an object (dict) for MCP
# structured output compatibility.
# ---------------------------------------------------------------------------

class TodoListResult(BaseModel):
    """Container for a list of todo items."""
    todos: List[TodoResponse]
    count: int


# ---------------------------------------------------------------------------
# MCP Tools
# ---------------------------------------------------------------------------

@mcp.tool(
    name="get_all_todos",
    description=(
        "Retrieve all todo items that belong to the currently authenticated user. "
        "Returns a list of todos with their IDs, titles, descriptions, priorities, "
        "and completion status. Use this to give the user an overview of their tasks."
    ),
)
async def get_all_todos(
    ctx: Context,
    auth_service: AuthService = Depends(get_auth_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> TodoListResult:
    """Returns all todos for the authenticated user, sorted by priority."""
    user = _require_user(auth_service)
    await ctx.info(f"Fetching all todos for '{user.username}'")
    todos = todo_service.get_all_todos(user.id)
    validated = [TodoResponse.model_validate(t) for t in todos]
    return TodoListResult(todos=validated, count=len(validated))


@mcp.tool(
    name="get_todo_by_id",
    description=(
        "Retrieve a single todo item by its unique ID. "
        "Use this when the user refers to a specific task by ID, or to verify "
        "the current state of a todo before updating it."
    ),
)
async def get_todo_by_id(
    todo_id: Annotated[str, Field(description="The UUID of the todo to retrieve")],
    ctx: Context,
    auth_service: AuthService = Depends(get_auth_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Returns full details of a single todo item owned by the authenticated user."""
    user = _require_user(auth_service)
    await ctx.info(f"Fetching todo '{todo_id}' for '{user.username}'")
    try:
        todo = todo_service.get_todo_by_id(todo_id, user.id)
    except Exception:
        raise ToolError(f"Todo with ID '{todo_id}' was not found or does not belong to you.")
    return TodoResponse.model_validate(todo)


@mcp.tool(
    name="create_todo",
    description=(
        "Create a new todo item for the authenticated user. "
        "Requires a title, description, and a priority from 1 (lowest) to 5 (highest). "
        "Returns the newly created todo including its assigned ID."
    ),
)
async def create_todo(
    title: Annotated[str, Field(description="Short, descriptive title for the task", min_length=3, max_length=100)],
    description: Annotated[str, Field(description="Detailed notes or context for the task", min_length=1, max_length=100)],
    priority: Annotated[int, Field(description="Importance level: 1 = lowest, 5 = highest", ge=1, le=5)],
    ctx: Context,
    auth_service: AuthService = Depends(get_auth_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> TodoResponse:
    """Creates a new todo and returns it with its assigned ID."""
    user = _require_user(auth_service)
    await ctx.info(f"Creating todo '{title}' for '{user.username}'")
    todo_data = TodoRequest(title=title, description=description, priority=priority)
    result = todo_service.create_todo(todo_data.model_dump(), user.id)
    # result["todo"] is a SQLAlchemy model — validate through Pydantic before returning
    created_todo = result.get("todo") if isinstance(result, dict) else result
    return TodoResponse.model_validate(created_todo)


@mcp.tool(
    name="update_todo",
    description=(
        "Update the title, description, priority, or completion status of an existing todo. "
        "All fields are required — provide current values for fields you do not want to change. "
        "Use get_todo_by_id first to fetch the current values before updating."
    ),
)
async def update_todo(
    todo_id: Annotated[str, Field(description="UUID of the todo to update")],
    title: Annotated[str, Field(description="Updated title (3–100 characters)", min_length=3, max_length=100)],
    description: Annotated[str, Field(description="Updated description (1–100 characters)", min_length=1, max_length=100)],
    priority: Annotated[int, Field(description="Updated priority: 1 = lowest, 5 = highest", ge=1, le=5)],
    completed: Annotated[bool, Field(description="True if the task is done, False if still in progress")] = False,
    ctx: Context = None,
    auth_service: AuthService = Depends(get_auth_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> str:
    """Updates a todo item and returns a confirmation message."""
    user = _require_user(auth_service)
    if ctx:
        await ctx.info(f"Updating todo '{todo_id}' for '{user.username}'")
    try:
        todo_service.update_todo(
            todo_id,
            {"title": title, "description": description, "priority": priority, "completed": completed},
            user.id,
        )
    except Exception:
        raise ToolError(f"Todo '{todo_id}' was not found or does not belong to you.")
    return f"Todo '{todo_id}' updated successfully."


@mcp.tool(
    name="delete_todo",
    description=(
        "Permanently delete a todo item by its ID. "
        "This action cannot be undone — confirm with the user before calling this tool. "
        "Returns a confirmation message on success."
    ),
)
async def delete_todo(
    todo_id: Annotated[str, Field(description="UUID of the todo to permanently delete")],
    ctx: Context,
    auth_service: AuthService = Depends(get_auth_service),
    todo_service: TodoService = Depends(get_todo_service),
) -> str:
    """Deletes a todo item permanently."""
    user = _require_user(auth_service)
    await ctx.info(f"Deleting todo '{todo_id}' for '{user.username}'")
    try:
        todo_service.delete_todo(todo_id, user.id)
    except Exception:
        raise ToolError(f"Todo '{todo_id}' was not found or does not belong to you.")
    return f"Todo '{todo_id}' deleted successfully."
