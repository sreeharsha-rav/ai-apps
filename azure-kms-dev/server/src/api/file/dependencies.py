from functools import lru_cache

from .service import FileService
from .repository import FileRepository


@lru_cache()
def get_file_repository() -> FileRepository:
    """
    Dependency to get a singleton instance of FileRepository.
    This ensures that the repository is reused across requests.
    """
    return FileRepository()

@lru_cache()
def get_file_service() -> FileService:
    """
    Dependency to get a singleton instance of FileService.
    This ensures that the service is reused across requests.
    """
    return FileService(file_repository=get_file_repository())