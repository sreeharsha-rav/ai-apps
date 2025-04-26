from abc import ABC, abstractmethod
from src.models.space import Space

class ISpaceRepository(ABC):
    """Interface for space repository operations"""

    @abstractmethod
    async def space_exists(self, space_name: str) -> bool:
        """Check if a space exists"""
        pass

    @abstractmethod
    async def create_new_space(self, space: Space) -> Space:
        """Create a new space with space info"""
        pass
    
    @abstractmethod
    async def get_by_name(self, name: str) -> Space:
        """Get a space by name"""
        pass

    @abstractmethod
    async def list_all_spaces(self) -> list[Space]:
        """List all spaces with space info"""
        pass

    @abstractmethod
    async def delete_by_name(self, name: str) -> None:
        """Delete a space by name including all files"""
        pass

class ISpaceDirectoryManager(ABC):
    """Interface for space directory operations"""

    @abstractmethod
    async def spaces_dir_exists(self) -> bool:
        """Check if spaces directory exists"""
        pass
    
    @abstractmethod
    async def create_spaces_dir(self) -> None:
        """Create spaces directory with _info.json"""
        pass

    @abstractmethod
    async def add_space_to_spaces_info(self, space: Space) -> None:
        """Add space to spaces/_info.json"""
        pass

    @abstractmethod
    async def remove_space_from_spaces_info(self, space_name: str) -> None:
        """Remove space from spaces/_info.json"""
        pass