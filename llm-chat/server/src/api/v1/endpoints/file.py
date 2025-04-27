from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends, HTTPException, status, Path, Form
from src.schemas.file import FileRequest, FileResponse
from src.models.file import FileExtension
from src.services.file import FileService
from src.core.exceptions.space import SpaceError
from src.core.exceptions.file import FileError
from typing import List
from src.api.v1.dependencies import validate_space_name, validate_file_name
from src.utils.loggers import setup_logger
import json

file_router = APIRouter(
    prefix="/spaces/{space_name}/files",
    tags=["files"],
)

file_service = FileService()
logger = setup_logger(name="file_endpoint")

@file_router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    space_name: str = Depends(validate_space_name),
    file_data: UploadFile = FastAPIFile(...),
) -> FileResponse:
    """Upload a file to a space"""
    try:
        logger.info(f"Uploading file '{file_data.filename}' to space: {space_name}")
        # todo validate file_data via dependency injection
        response = await file_service.upload_file(
            space_name=space_name,
            file_data=file_data,
        )
        logger.info(f"Successfully uploaded file '{file_data.filename}' to space: {space_name}")
        return response
    except (SpaceError, FileError) as e:
        logger.error(f"Error uploading file '{file_data.filename}' to space '{space_name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error uploading file '{file_data.filename}' to space '{space_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@file_router.get("{file_name}", response_model=FileResponse)
async def get_file(
    file_name: str = Depends(validate_file_name),
    space_name: str = Depends(validate_space_name)
) -> FileResponse:
    """Get file metadata"""
    try:
        base_name, extension = file_name.rsplit('.', 1)
        file_request = FileRequest(
            base_name=base_name,
            extension=FileExtension(extension)
        )
        return await file_service.get_file(
            space_name=space_name,
            file=file_request
        )
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")

@file_router.get("/all", response_model=List[FileResponse])
async def list_files(
    space_name: str = Depends(validate_space_name)
) -> List[FileResponse]:
    """List all files metadata in a space"""
    try:
        logger.info(f"Listing all files in space: {space_name}")
        response = await file_service.list_all_files(space_name)
        logger.info(f"Successfully listed {len(response)} files in space: {space_name}")
        return response
    except (SpaceError, FileError) as e:
        logger.error(f"Error listing files in space '{space_name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error listing files in space '{space_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@file_router.delete("/{file_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_name: str = Depends(validate_file_name),
    space_name: str = Depends(validate_space_name)
) -> None:
    """Delete a file from a space"""
    try:
        base_name, extension = file_name.rsplit('.', 1)
        await file_service.delete_file(
            space_name=space_name,
            file=FileRequest(
                base_name=base_name,
                extension=FileExtension(extension)
            )
        )
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")