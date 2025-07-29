from fastapi import APIRouter

from .endpoints.chat import chat_router

v1_router = APIRouter(
    prefix="/v1",
)

# Include feature-specific routers
v1_router.include_router(chat_router)