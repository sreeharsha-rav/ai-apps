
from fastapi import status

class SpaceError(Exception):
    """Base exception for space-related errors"""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail: str = "An unexpected error occurred"

class SpaceNotFoundError(SpaceError):
    """Raised when space is not found"""
    status_code = status.HTTP_404_NOT_FOUND
    detail = "Space not found"

class SpaceAlreadyExistsError(SpaceError):
    """Raised when space already exists"""
    status_code = status.HTTP_409_CONFLICT
    detail = "Space already exists"

class SpaceValidationError(SpaceError):
    """Raised when space validation fails"""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = "Space validation failed"
