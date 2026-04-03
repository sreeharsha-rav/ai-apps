from fastapi import Depends
from sqlalchemy.orm import Session
from app.database.db import get_db
from app.database.repository import UserRepository
from app.services.auth import AuthService
from app.services.todo import TodoService
from app.database.repository import TodoRepository

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(UserRepository(db))

def get_todo_service(db: Session = Depends(get_db)) -> TodoService:
    return TodoService(TodoRepository(db))

__all__ = [
    "AuthService",
    "TodoService",
    "get_auth_service",
    "get_todo_service"
]
