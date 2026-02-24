from sqlalchemy.orm import Session
from typing import List, Optional, Type, TypeVar, Generic
from app.database.models import User, Todo

T = TypeVar("T")

class BaseRepository(Generic[T]):
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_by_id(self, id: str) -> Optional[T]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def delete(self, entity: T) -> None:
        self.db.delete(entity)
        self.db.commit()

    def save(self, entity: T) -> T:
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

class UserRepository(BaseRepository[User]):
    def __init__(self, db: Session):
        super().__init__(db, User)

    def get_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, username: str, password_raw: str) -> User:
        user = User(username=username)
        user.password = password_raw
        return self.save(user)

class TodoRepository(BaseRepository[Todo]):
    def __init__(self, db: Session):
        super().__init__(db, Todo)

    def get_all_by_user(self, user_id: str) -> List[Todo]:
        return self.db.query(Todo).filter(Todo.owner == user_id).all()

    def get_by_id_and_owner(self, todo_id: str, user_id: str) -> Optional[Todo]:
        return self.db.query(Todo).filter(Todo.id == todo_id, Todo.owner == user_id).first()

    def create(self, todo_data: dict, user_id: str) -> Todo:
        todo = Todo(**todo_data, owner=user_id)
        return self.save(todo)

    def update(self, todo: Todo) -> Todo:
        return self.save(todo)
