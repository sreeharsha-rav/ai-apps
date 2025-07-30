from fastapi import APIRouter, status, Path, Query, UploadFile, File, HTTPException, Depends
from uuid import uuid4
from typing import Optional

from .schemas import FileUploadResponse
from .service import ChatService
from .dependencies import get_chat_service


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

@chat_router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_file(
    # chat_id: Optional[str] = Query(
    #     default=None,
    #     min_length=41,
    #     max_length=41,
    #     pattern=r"^chat_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    #     description="The ID of the chat for file upload",
    #     example="chat_123e4567-e89b-12d3-a456-426614174000"
    # ),
    file: UploadFile = File(..., description="The file to upload for chat processing (max 50MB)"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Endpoint to upload a file for chat processing.
    """
    try:
        # FUTURE: Use chat_id to associate the file with a specific chat if needed

        uploaded_file = await chat_service.upload_file_and_process_stream(file=file)
        return FileUploadResponse(
            id=uploaded_file.id,
            filename=uploaded_file.filename,
            type=uploaded_file.type,
            size=uploaded_file.size,
            uploaded_at=uploaded_file.uploaded_at,
            url=uploaded_file.url,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")