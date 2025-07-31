from fastapi import APIRouter, status, Path, UploadFile, File, HTTPException, Depends, BackgroundTasks, Form
from uuid import uuid4
from typing import Annotated

from .schemas import FileResponse
from .models import FileSource
from .service import ChatService
from .dependencies import get_chat_service
from .utils import validate_filename, validate_file_size


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

@chat_router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=FileResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    source: Annotated[FileSource, Form()] = FileSource.SYSTEM,
    file: UploadFile = File(..., description="The file to upload for chat processing (max 50MB)"),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Endpoint to upload a file for chat processing.
    """
    try:
        filename, file_type = validate_filename(filename=file.filename)
        size = await validate_file_size(upload_file=file)

        uploaded_file = await chat_service.upload_file_stream(
            source=source,
            filename=filename,
            file_type=file_type,
            size=size,
            file_stream=file.file
        )

        file.file.seek(0)  # Reset file pointer to the beginning
        content = await file.read()
        background_tasks.add_task(
            chat_service.process_file_background,
            uploaded_file, content
        )

        return FileResponse(
            id=uploaded_file.id,
            name=uploaded_file.name,
            type=uploaded_file.type,
            size=uploaded_file.size,
            source=uploaded_file.source,
            uploaded_at=uploaded_file.uploaded_at,
            url=uploaded_file.url,
            extracted_content_url=uploaded_file.extracted_content_url,
            processing_status=uploaded_file.processing_status
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@chat_router.get("/file/{file_id}/metadata", status_code=status.HTTP_200_OK, response_model=FileResponse)
async def get_file_metadata(
    file_id: str = Path(
        min_length=41,
        max_length=41,
        pattern=r"^file_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="The ID of the file to check metadata",
        example="file_123e4567-e89b-12d3-a456-426614174000"
    ),
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Endpoint to get the processing status of an uploaded file.
    """
    try:
        file = await chat_service.get_file_metadata(file_id=file_id)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")

        return FileResponse(
            id=file.id,
            name=file.name,
            type=file.type,
            size=file.size,
            source=file.source,
            uploaded_at=file.uploaded_at,
            url=file.url,
            extracted_content_url=file.extracted_content_url,
            processing_status=file.processing_status
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file status: {str(e)}")