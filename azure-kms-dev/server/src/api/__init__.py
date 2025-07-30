from fastapi import APIRouter

from .chat.router import chat_router


api_router = APIRouter(
    prefix="/api",
)

api_router.include_router(chat_router)

__all__ = [
    "api_router",
]