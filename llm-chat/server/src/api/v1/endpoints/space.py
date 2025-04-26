from fastapi import APIRouter, status, HTTPException, Depends
from src.schemas.space import SpaceRequest, SpaceResponse, RESERVED_SPACE_NAMES
from src.api.v1.dependencies import validate_space_name
from src.services.space import SpaceService
from src.core.exceptions.space import SpaceError

space_router = APIRouter(
    prefix="/spaces",
    tags=["spaces"],
)

space_service = SpaceService()

@space_router.post("", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
async def create_space(space_request: SpaceRequest) -> SpaceResponse:
    """Create a space"""
    try:
        return await space_service.create_new_space(space_request)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating space: {str(e)}")

@space_router.get("", response_model=SpaceResponse, status_code=status.HTTP_200_OK)
async def get_space(space_name: str = Depends(validate_space_name)) -> SpaceResponse:
    """Get a space by name"""
    try:
        return await space_service.get_space_by_name(space_name)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting space: {str(e)}")

@space_router.get("/all", response_model=list[SpaceResponse], status_code=status.HTTP_200_OK)
async def list_spaces() -> list[SpaceResponse]:
    """List all spaces"""
    try:
        return await space_service.list_all_spaces()
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing spaces: {str(e)}")

@space_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_space(space_name: str = Depends(validate_space_name)) -> None:
    """Delete a space by name"""
    try:
        await space_service.delete_space_by_name(space_name)
    except SpaceError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting space: {str(e)}")