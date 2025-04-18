from abc import ABC, abstractmethod
from typing import ClassVar
from src.schemas.search import SearchEngineInfo, SearchResult

class BaseSearch(ABC):
    """Base class for search engine implementations"""

    ENGINE_INFO: ClassVar[SearchEngineInfo]     # Static class variable for engine information

    def __init__(self):
        """Initialize the search engine"""
        return

    @abstractmethod
    async def search(self, query: str, num_results: int = 5) -> list[SearchResult]:
        """Perform a search and return results."""
        pass