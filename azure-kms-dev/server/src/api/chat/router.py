from fastapi import APIRouter, status, Path
from uuid import uuid4


chat_router = APIRouter(
    prefix="/chat",
    tags=["chat"],
)

@chat_router.get("/{chat_id}", status_code=status.HTTP_200_OK)
async def get_chat(
    chat_id: str = Path(
        min_length=41,
        max_length=41,
        pattern=r"^chat_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="The ID of the chat to retrieve",
        example="chat_123e4567-e89b-12d3-a456-426614174000"
    )
):
    """
    Endpoint to retrieve chat information.
    """
    return {"message": f"Chat {chat_id} retrieved successfully!"}

@chat_router.post("", status_code=status.HTTP_201_CREATED)
async def create_chat():
    """
    Endpoint to create a new chat.
    """
    new_chat_id = f"chat_{uuid4()}"
    return {"message": "Chat created successfully!", "chat_id": new_chat_id}