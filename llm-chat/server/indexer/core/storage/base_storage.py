from abc import ABC, abstractmethod
from indexer.schemas.document import RawDocument
from indexer.schemas.metadata import SpaceMetadata
from typing import AsyncGenerator

class BaseStorage(ABC):
    """Base class for all storage implementations"""

    @abstractmethod
    async def does_space_exist(self, space_name: str) -> bool:
        """Check if a space exists.

        Args:
            space_name: Space name

        Returns:
            True if the space exists, False otherwise
        """
        pass

    @abstractmethod
    async def get_space_metadata(self, space_name: str) -> SpaceMetadata:
        """Get metadata for a space.

        Args:
            space_name: Space name

        Returns:
            Space metadata object
        """
        pass

    @abstractmethod
    async def update_space_metadata(self, space_name: str, metadata: SpaceMetadata):
        """Update metadata for a space.

        Args:
            space_name: Space name
            metadata: Space metadata object
        """
        pass

    @abstractmethod
    async def list_all_files(self, space_name: str) -> list[str]:
        """List all files in a space.

        Args:
            space_name: Space name

        Returns:
            List of file names in the space
        """
        pass

    @abstractmethod
    def load_all_files(self, space_name: str, files: list[str]) -> AsyncGenerator[RawDocument, None]:
        """Load all files in a space.

        Args:
            space_name: Space name
            files: List of file names to load
        """
        pass
