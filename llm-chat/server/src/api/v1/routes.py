from fastapi import APIRouter
from .endpoints import chat_router, models_router

v1_router = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

# include routers
v1_router.include_router(chat_router)
v1_router.include_router(models_router)