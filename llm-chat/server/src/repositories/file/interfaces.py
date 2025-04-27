from abc import ABC, abstractmethod
from src.models.file import File, FileExtension

class IFileRepository(ABC):
    """Interface for file repository operations"""

    @abstractmethod
    async def file_exists(self, space_name: str, file_name: str, file_extension: FileExtension) -> bool:
        """Check if a file exists in a space"""
        pass

    @abstractmethod
    async def upload_file(self, space_name: str, file: File, content: bytes) -> File:
        """Upload a file to a space"""
        pass

    @abstractmethod
    async def get_file_by_name(self, space_name: str, file_name: str, file_extension: FileExtension) -> File:
        """Get file metadata by name"""
        pass

    @abstractmethod
    async def list_all_files(self, space_name: str) -> list[File]:
        """List all files in a space"""
        pass

    @abstractmethod
    async def delete_file_by_name(self, space_name: str, file_name: str, file_extension: FileExtension) -> None:
        """Delete a space by name"""
        pass


class IFileDirectoryManager(ABC):
    """Interface for file directory operations"""

    @abstractmethod
    async def files_dir_exists(self, space_name: str) -> bool:
        """Check if files directory exists"""
        pass

    @abstractmethod
    async def create_files_dir(self, space_name: str) -> None:
        """Create files/_info.json"""
        pass