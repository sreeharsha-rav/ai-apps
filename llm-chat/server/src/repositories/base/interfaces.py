from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List

T = TypeVar('T')

class BaseRepository(ABC, Generic[T]):
    """Base repository interface defining common operations"""
    
    @abstractmethod
    async def create(self, item: T) -> T:
        """Create a new item"""
        pass

    @abstractmethod
    async def get(self, id: str) -> Optional[T]:
        """Get an item by id"""
        pass

    @abstractmethod
    async def list(self) -> List[T]:
        """List all items"""
        pass

    @abstractmethod
    async def delete(self, id: str) -> None:
        """Delete an item by id"""
        pass

    @abstractmethod
    async def exists(self, id: str) -> bool:
        """Check if an item exists"""
        pass