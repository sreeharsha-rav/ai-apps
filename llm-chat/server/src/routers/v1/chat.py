from fastapi import APIRouter, status, HTTPException, Path
from typing import List
import logging
from src.services.chat import ChatService
from src.schemas.chat import Chat, ChatRequest, ChatResponse
from src.exceptions.chat import ChatNotFoundError
from ulid import ULID

router = APIRouter(
    prefix="/v1/chat",
    tags=["chat"],
)

chat_service = ChatService()

@router.post("", response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(chat_request: ChatRequest) -> ChatResponse:
    """Create a chat from a user message"""
    
    try:
        response = await chat_service.generate_chat_completion(chat_request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@router.get("/{chat_id}", response_model=Chat, status_code=status.HTTP_200_OK)
async def get_chat(chat_id: ULID = Path(description="The chat ID to get")) -> Chat:
    """Get a chat by ID"""
    try:
        return await chat_service.get_chat(chat_id)
    except ChatNotFoundError:
        raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found")

@router.get("", response_model=List[Chat], status_code=status.HTTP_200_OK)
async def list_chats() -> List[Chat]:
    """List all chats"""
    return await chat_service.list_chats()

@router.delete("/{chat_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(chat_id: ULID = Path(description="The chat ID to delete")) -> None:
    """Delete a chat"""
    await chat_service.delete_chat(chat_id)