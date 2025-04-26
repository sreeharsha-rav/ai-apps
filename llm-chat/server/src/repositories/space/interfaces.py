from abc import ABC, abstractmethod
from src.models.space import Space
from src.repositories.base import BaseRepository

class ISpaceRepository(BaseRepository[Space], ABC):
    """Interface for space repository operations"""
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Space:
        """Get a space by name"""
        pass

    @abstractmethod
    async def delete_by_name(self, name: str) -> None:
        """Delete a space by name"""
        pass

class ISpaceDirectoryManager(ABC):
    """Interface for space directory operations"""
    
    @abstractmethod
    async def ensure_directory_exists(self) -> None:
        """Ensure spaces directory exists"""
        pass

    @abstractmethod
    async def add_space(self, space: Space) -> None:
        """Add space to directory"""
        pass

    @abstractmethod
    async def remove_space(self, space_name: str) -> None:
        """Remove space from directory"""
        pass