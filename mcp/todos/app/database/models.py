from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.hybrid import hybrid_property
from passlib.context import CryptContext
from app.database.db import Base
import uuid


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True, default=lambda: f"user_{uuid.uuid4()}")
    username = Column(String, unique=True)
    _password_hash = Column(String)
    is_active = Column(Boolean, default=True)

    @hybrid_property
    def password(self):
        raise ValueError("Password is hashed; use verify_password() instead.")

    @password.setter
    def password(self, password: str) -> None:
        if password:
            self._password_hash = pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        return pwd_context.verify(password, self._password_hash)

class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(String, primary_key=True, index=True, default=lambda: f"todo_{uuid.uuid4()}")
    title = Column(String)
    description = Column(String)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)
    owner = Column(String, ForeignKey("users.id"))
