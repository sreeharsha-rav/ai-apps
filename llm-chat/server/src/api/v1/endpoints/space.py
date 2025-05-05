from fastapi import APIRouter, status, HTTPException, Depends
from src.schemas.space import SpaceRequest, SpaceResponse
from src.api.v1.dependencies import validate_space_name
from src.services.space import SpaceService
from src.core.exceptions.space import SpaceError
from src.utils.loggers import setup_logger

space_router = APIRouter(
    prefix="/spaces",
    tags=["spaces"],
)

space_service = SpaceService()
logger = setup_logger(name="space_endpoint")

@space_router.post("", response_model=SpaceResponse, status_code=status.HTTP_201_CREATED)
async def create_space(space_request: SpaceRequest) -> SpaceResponse:
    """Create a space"""
    try:
        logger.info(f"Creating new space with name: {space_request.name}")
        response = await space_service.create_new_space(space_request)
        logger.info(f"Successfully created space: {space_request.name}")
        return response
    except SpaceError as e:
        logger.error(f"Space error while creating space '{space_request.name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while creating space '{space_request.name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error creating space: {str(e)}")

@space_router.get("/{space_name}", response_model=SpaceResponse, status_code=status.HTTP_200_OK)
async def get_space(space_name: str = Depends(validate_space_name)) -> SpaceResponse:
    """Get a space by name"""
    try:
        logger.info(f"Getting space with name: {space_name}")
        response = await space_service.get_space_by_name(space_name)
        logger.info(f"Successfully retrieved space: {space_name}")
        return response
    except SpaceError as e:
        logger.error(f"Space error while getting space '{space_name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while getting space '{space_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting space: {str(e)}")

@space_router.get("", response_model=list[SpaceResponse], status_code=status.HTTP_200_OK)
async def list_spaces() -> list[SpaceResponse]:
    """List all spaces"""
    try:
        logger.info("Listing all spaces")
        response = await space_service.list_all_spaces()
        logger.info(f"Successfully listed {len(response)} spaces")
        return response
    except SpaceError as e:
        logger.error(f"Space error while listing spaces: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while listing spaces: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error listing spaces: {str(e)}")

@space_router.delete("/{space_name}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_space(space_name: str = Depends(validate_space_name)) -> None:
    """Delete a space by name"""
    try:
        logger.info(f"Deleting space with name: {space_name}")
        await space_service.delete_space_by_name(space_name)
        logger.info(f"Successfully deleted space: {space_name}")
    except SpaceError as e:
        logger.error(f"Space error while deleting space '{space_name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while deleting space '{space_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error deleting space: {str(e)}")

@space_router.post("/{space_name}/index", status_code=status.HTTP_200_OK)
async def index_space(space_name: str = Depends(validate_space_name)) -> None:
    """Index all files in a space"""
    try:
        logger.info(f"Indexing space with name: {space_name}")
        await space_service.index_space(space_name)
        logger.info(f"Successfully indexed space: {space_name}")
    except SpaceError as e:
        logger.error(f"Space error while indexing space '{space_name}': {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error while indexing space '{space_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error indexing space: {str(e)}")