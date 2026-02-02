from fastapi import APIRouter, Request, Depends
from fastapi.responses import StreamingResponse

from .models import ChatRequest
from .storage import storage
from .service import ChatService

router = APIRouter()

def get_chat_service(request: Request) -> ChatService:
    """Dependency to get ChatService instance"""
    return ChatService(storage=storage, openai_client=request.app.state.openai_client)

@router.get("/history")
async def get_history(service: ChatService = Depends(get_chat_service)):
    """Get all chat histories"""
    return await service.get_all_chats()

@router.get("/history/{chat_id}")
async def get_chat(chat_id: str, service: ChatService = Depends(get_chat_service)):
    """Get a specific chat history"""
    return await service.get_chat(chat_id)

@router.delete("/history")
async def clear_history(service: ChatService = Depends(get_chat_service)):
    """Clear all chat history"""
    return await service.clear_all_chats()

@router.delete("/history/{chat_id}")
async def delete_chat(chat_id: str, service: ChatService = Depends(get_chat_service)):
    """Delete a specific chat"""
    return await service.delete_chat(chat_id)

@router.post("/history")
async def create_chat(service: ChatService = Depends(get_chat_service)):
    """Create a new chat session"""
    return await service.create_chat()

@router.patch("/history/{chat_id}/title")
async def update_title(chat_id: str, request: dict, service: ChatService = Depends(get_chat_service)):
    """Update chat title"""
    return await service.update_chat_title(chat_id, request.get("title"))

@router.post("/stream")
async def chat_stream(request: ChatRequest, service: ChatService = Depends(get_chat_service)):
    """Stream chat response"""
    return StreamingResponse(service.stream_chat(request), media_type="text/event-stream")
