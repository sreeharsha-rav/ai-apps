from typing import List
from fastapi import FastAPI, status, Depends, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from fastapi.middleware.cors import CORSMiddleware
from jose import jwt, JWTError
from sqlalchemy.exc import SQLAlchemyError
import logging
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
from app.config import settings


logger = logging.getLogger(__name__)

# Constants
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.JWT_ALGORITHM


api = FastAPI(
    title="Todos API",
    description="A simple API to manage todos with validation and error handling.",
    version="1.0.0"
)

# Exception Handlers
@api.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    logger.error(f"Database error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred. Please try again later."},
    )

@api.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An unexpected error occurred. Internal server error."},
    )



# Security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

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

# ----------------------------------
# Auth Endpoints
# ----------------------------------
@api.post("/auth/register", status_code=status.HTTP_201_CREATED)
async def register(register_request: RegisterRequest, auth_service: AuthService = Depends(get_auth_service)) -> dict:
    """
    Register a new user.
    """
    return auth_service.register_user(register_request.username, register_request.password)

@api.post("/auth/login", status_code=status.HTTP_200_OK)
async def login(login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)) -> dict:
    """
    Login a user.
    """
    auth_service.authenticate_user(login_request.username, login_request.password)
    return {"message": "Login successful."}

@api.post("/auth/token", status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def token(form_data: OAuth2PasswordRequestForm = Depends(), auth_service: AuthService = Depends(get_auth_service)) -> TokenResponse:
    """
    Get JWT token for a user.
    """
    user = auth_service.authenticate_user(form_data.username, form_data.password)
    access_token = auth_service.create_jwt_token(user.username)
    return TokenResponse(access_token=access_token, token_type="bearer")

@api.get("/auth/me", status_code=status.HTTP_200_OK)
async def me(user = Depends(get_current_user)) -> dict:
    """
    Get the current user.
    """
    return { "username": user.username, "id": user.id, "is_active": user.is_active }

# ----------------------------------
# Todos Endpoints
# ----------------------------------
@api.get("/todos", status_code=status.HTTP_200_OK, response_model=List[TodoResponse])
async def read_all_todos(user = Depends(get_current_user), todo_service: TodoService = Depends(get_todo_service)) -> List[TodoResponse]:
    """
    Get all todos for the authenticated user.
    """
    return todo_service.get_all_todos(user.id)

@api.get("/todos/{todo_id}", status_code=status.HTTP_200_OK, response_model=TodoResponse)
async def read_todo_by_id(todo_id: str = Path(...), 
                          user = Depends(get_current_user), 
                          todo_service: TodoService = Depends(get_todo_service)) -> TodoResponse:
    """
    Get a specific todo by ID for the authenticated user.
    """
    return todo_service.get_todo_by_id(todo_id, user.id)

@api.post("/todos", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest, 
                      user = Depends(get_current_user), 
                      todo_service: TodoService = Depends(get_todo_service)) -> dict:
    """
    Create a new todo for the authenticated user.
    """
    return todo_service.create_todo(todo_request.model_dump(), user.id)

@api.put("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(todo_request: TodoRequest, 
                      todo_id: str = Path(...), 
                      user = Depends(get_current_user), 
                      todo_service: TodoService = Depends(get_todo_service)) -> None:
    """
    Update an existing todo for the authenticated user.
    """
    todo_service.update_todo(todo_id, todo_request.model_dump(), user.id)

@api.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(todo_id: str = Path(...), 
                      user = Depends(get_current_user), 
                      todo_service: TodoService = Depends(get_todo_service)) -> None:
    """
    Delete a specific todo by ID for the authenticated user.
    """ 
    todo_service.delete_todo(todo_id, user.id)
