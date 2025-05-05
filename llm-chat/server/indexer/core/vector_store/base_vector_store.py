from abc import ABC, abstractmethod
from indexer.schemas.vector_store import IndexDocument, IndexResult

class BaseVectorStore(ABC):
    """Base class for all vector store implementations"""

    @abstractmethod
    async def does_index_exist(self) -> bool:
        """Check if the index exists.

        Returns:
            True if the index exists, False otherwise
        """
        pass

    @abstractmethod
    async def create_index(self):
        """Create the index."""
        pass

    @abstractmethod
    async def delete_index(self):
        """Delete the index."""
        pass

    @abstractmethod
    async def index_documents(self, documents: list[IndexDocument]) -> list[IndexResult]:
        """
        Index documents.

        Args:
            documents(list[IndexDocument]): List of documents to index

        Returns:
            list[IndexResult]: List of indexing results
        """
        pass

    # TODO: future update only selected documents

    @abstractmethod
    async def delete_documents(self, user_id: str, space_name: str):
        """
        Delete all documents of space_name in index.

        Args:
            user_id: User ID
            space_name: Space name
        """
        pass

    # TODO: future delete only selected documents

    @abstractmethod
    async def close(self):
        """Close all clients and release resources."""
        pass
