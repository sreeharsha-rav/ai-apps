from fastapi import APIRouter, status, HTTPException, Query, Depends
from src.schemas.space import SpaceRequest, SpaceResponse, RESERVED_SPACE_NAMES
from src.services.space import SpaceService

space_router = APIRouter(
    prefix="/spaces",
    tags=["spaces"],
)

space_service = SpaceService()

# Dependency function to validate space name
def validate_space_name(
    space_name: str = Query(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+$',
        description="The space name",
    )
) -> str:
    """Validate space name from query parameters"""
    if space_name in RESERVED_SPACE_NAMES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Space name '{space_name}' is reserved and cannot be used"
        )
    return space_name

@space_router.post("", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
async def create_space(space_request: SpaceRequest) -> SpaceResponse:
    """Create a space"""
    try:
        return await space_service.create_new_space(space_request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating space: {str(e)}")

@space_router.get("", response_model=SpaceResponse, status_code=status.HTTP_200_OK)
async def get_space(space_name: str = Depends(validate_space_name)) -> SpaceResponse:
    """Get a space by name"""
    try:
        return await space_service.get_space(space_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting space: {str(e)}")

@space_router.get("/all", response_model=list[SpaceResponse], status_code=status.HTTP_200_OK)
async def list_spaces() -> list[SpaceResponse]:
    """List all spaces"""
    try:
        return await space_service.list_spaces()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing spaces: {str(e)}")

@space_router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_space(space_name: str = Depends(validate_space_name)) -> None:
    """Delete a space by name"""
    try:
        await space_service.delete_space(space_name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting space: {str(e)}")