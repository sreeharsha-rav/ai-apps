from fastapi import APIRouter, UploadFile, File as FastAPIFile, Depends, HTTPException, status, Path
from ulid import ULID
from src.schemas.file import FileUploadRequest, FileResponse
from src.services.file import FileService
from src.core.exceptions.space import SpaceError
from typing import List
from src.api.v1.dependencies import validate_space_name

file_router = APIRouter(
    prefix="/spaces/{space_name}/files",
    tags=["files"],
)

file_service = FileService()

@file_router.post("", response_model=FileResponse, status_code=status.HTTP_201_CREATED)
async def upload_file(
    space_name: str = Depends(validate_space_name),
    file_data: FileUploadRequest = None,
    file: UploadFile = FastAPIFile(...),
) -> FileResponse:
    """Upload a file to a space"""
    try:
        return await file_service.upload_file(space_name, file_data, file)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")

@file_router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: ULID = Path(description="The file ID to get"),
    space_name: str = Depends(validate_space_name)
) -> FileResponse:
    """Get file metadata"""
    try:
        return await file_service.get_file(space_name, file_id)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting file: {str(e)}")

@file_router.get("", response_model=List[FileResponse])
async def list_files(
    space_name: str = Depends(validate_space_name)
) -> List[FileResponse]:
    """List all files metadata in a space"""
    try:
        return await file_service.list_files(space_name)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")

@file_router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_file(
    file_id: ULID = Path(description="The file ID to delete"),
    space_name: str = Depends(validate_space_name)
) -> None:
    """Delete a file from a space"""
    try:
        await file_service.delete_file(space_name, file_id)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")