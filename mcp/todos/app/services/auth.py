from datetime import datetime, timezone, timedelta
from typing import Optional
from jose import jwt
from fastapi import HTTPException, status
from app.database.repository import UserRepository
from app.database.models import User
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register_user(self, username: str, password_raw: str) -> dict:
        if self.user_repo.get_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already registered"
            )
        self.user_repo.create(username, password_raw)
        return {"message": "User created successfully."}

    def authenticate_user(self, username: str, password_raw: str) -> User:
        user = self.user_repo.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        if not user.verify_password(password_raw):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid password."
            )
        return user

    def create_jwt_token(self, username: str) -> str:
        payload = {"sub": username}
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.user_repo.get_by_username(username)
