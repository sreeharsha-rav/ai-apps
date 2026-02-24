from sqlalchemy.orm import Session
from typing import List, Optional
from app.database.models import User, Todo

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, username: str, password_raw: str) -> User:
        user = User(username=username)
        user.password = password_raw
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

class TodoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all_by_user(self, user_id: str) -> List[Todo]:
        return self.db.query(Todo).filter(Todo.owner == user_id).all()

    def get_by_id_and_owner(self, todo_id: str, user_id: str) -> Optional[Todo]:
        return self.db.query(Todo).filter(Todo.id == todo_id, Todo.owner == user_id).first()

    def create(self, todo_data: dict, user_id: str) -> Todo:
        todo = Todo(**todo_data, owner=user_id)
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def update(self, todo: Todo) -> Todo:
        self.db.add(todo)
        self.db.commit()
        self.db.refresh(todo)
        return todo

    def delete(self, todo: Todo) -> None:
        self.db.delete(todo)
        self.db.commit()
