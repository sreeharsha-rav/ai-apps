from fastapi import APIRouter, status, Path, UploadFile, File, HTTPException, Depends, BackgroundTasks, Form
from typing import Annotated, List

from .schemas import FileResponse, MultipleFileResponse
from .models import FileSource
from .service import FileService
from .dependencies import get_file_service
from .utils import validate_filename, validate_file_size


file_router = APIRouter(
    prefix="/file",
    tags=["file"],
)

@file_router.post("/upload", status_code=status.HTTP_201_CREATED, response_model=FileResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    source: Annotated[FileSource, Form()] = FileSource.SYSTEM,
    file: UploadFile = File(..., description="The file to upload for chat processing (max 50MB)"),
    file_service: FileService = Depends(get_file_service)
):
    """
    Endpoint to upload a file for chat processing.
    """
    try:
        filename, file_type = validate_filename(filename=file.filename)
        size = await validate_file_size(upload_file=file)

        uploaded_file = await file_service.upload_file_stream(
            source=source,
            filename=filename,
            file_type=file_type,
            size=size,
            file_stream=file.file
        )

        file.file.seek(0)  # Reset file pointer to the beginning
        content = await file.read()
        background_tasks.add_task(
            file_service.process_file_background,
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

@file_router.get("/{file_id}/metadata", status_code=status.HTTP_200_OK, response_model=FileResponse)
async def get_file_metadata(
    file_id: str = Path(
        min_length=41,
        max_length=41,
        pattern=r"^file_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="The ID of the file to check metadata",
        example="file_123e4567-e89b-12d3-a456-426614174000"
    ),
    file_service: FileService = Depends(get_file_service)
):
    """
    Endpoint to get the processing status of an uploaded file.
    """
    try:
        file = await file_service.get_file_metadata(file_id=file_id)
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


@file_router.post("/upload/multiple", status_code=status.HTTP_201_CREATED, response_model=MultipleFileResponse)
async def upload_multiple_files(
        background_tasks: BackgroundTasks,
        source: Annotated[FileSource, Form()] = FileSource.SYSTEM,
        files: List[UploadFile] = File(..., description="Multiple files to upload for chat processing (max 50MB each)"),
        file_service: FileService = Depends(get_file_service)
):
    """
    Endpoint to upload multiple files for chat processing.
    """
    try:
        validated_files = []
        failed_files = []

        # Validate all files first
        for file in files:
            try:
                filename, file_type = validate_filename(filename=file.filename)
                size = await validate_file_size(upload_file=file)
                validated_files.append((filename, file_type, size, file.file))
            except Exception as e:
                failed_files.append(file.filename or "unknown")
                continue

        # Upload validated files
        uploaded_files, upload_failed = await file_service.upload_multiple_files(
            source=source,
            files_data=validated_files
        )

        failed_files.extend(upload_failed)

        # Process files in background
        for i, uploaded_file in enumerate(uploaded_files):
            files[i].file.seek(0)  # Reset file pointer
            content = await files[i].read()
            background_tasks.add_task(
                file_service.process_file_background,
                uploaded_file, content
            )

        file_responses = [
            FileResponse(
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
            for file in uploaded_files
        ]

        return MultipleFileResponse(
            files=file_responses,
            total_count=len(files),
            success_count=len(uploaded_files),
            failed_files=failed_files
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading files: {str(e)}")