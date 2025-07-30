from functools import lru_cache

from .service import ChatService
from .repository import FileRepository


@lru_cache()
def get_file_repository() -> FileRepository:
    """
    Dependency to get a singleton instance of FileRepository.
    This ensures that the repository is reused across requests.
    """
    return FileRepository()

@lru_cache()
def get_chat_service() -> ChatService:
    """
    Dependency to get a singleton instance of ChatService.
    This ensures that the service is reused across requests.
    """
    return ChatService(file_repository=get_file_repository())