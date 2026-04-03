from typing import List, Optional
from fastapi import HTTPException, status
from app.database.repository import TodoRepository
from app.database.models import Todo

class TodoService:
    def __init__(self, todo_repo: TodoRepository):
        self.todo_repo = todo_repo

    def get_all_todos(self, user_id: str) -> List[Todo]:
        return self.todo_repo.get_all_by_user(user_id)

    def get_todo_by_id(self, todo_id: str, user_id: str) -> Todo:
        todo = self.todo_repo.get_by_id_and_owner(todo_id, user_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found."
            )
        return todo

    def create_todo(self, todo_data: dict, user_id: str) -> dict:
        todo = self.todo_repo.create(todo_data, user_id)
        return {"message": "Todo created successfully.", "todo": todo}

    def update_todo(self, todo_id: str, todo_data: dict, user_id: str) -> None:
        todo = self.get_todo_by_id(todo_id, user_id)
        for key, value in todo_data.items():
            setattr(todo, key, value)
        self.todo_repo.update(todo)

    def delete_todo(self, todo_id: str, user_id: str) -> None:
        todo = self.get_todo_by_id(todo_id, user_id)
        self.todo_repo.delete(todo)
