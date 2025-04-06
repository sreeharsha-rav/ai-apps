from typing import Dict, List
from src.search.engines.base_search import BaseSearch
from src.search.engines.google_search import GoogleSearch
from src.schemas.search import SearchEngineID, SearchEngineInfo
from src.utils.decorators import singleton
from src.exceptions.search import SearchEngineNotFoundError

@singleton
class SearchRegistry:
    """Registry for managing search engines"""

    # Initialize the engines dictionary
    _engines: Dict[SearchEngineID, BaseSearch] = {
        SearchEngineID.GOOGLE: GoogleSearch(),
        # Add more engines as they're implemented
    }

    def list_engines(self) -> List[SearchEngineInfo]:
        """List all available search engines"""
        return [engine.ENGINE_INFO for engine in self._engines.values()]

    def get_engine_info(self, engine_id: str) -> SearchEngineInfo:
        """Get engine information for a specific search engine"""
        try:
            engine_enum = SearchEngineID(engine_id)
            return self._engines[engine_enum].ENGINE_INFO
        except (ValueError, KeyError):
            raise SearchEngineNotFoundError(
                f"Invalid engine_id: {engine_id}. "
                f"Supported engines: {[e.value for e in SearchEngineID]}"
            )

    def get_engine(self, engine_id: SearchEngineID) -> BaseSearch:
        """Get the search engine instance for the specified engine_id"""
        try:
            engine_enum = SearchEngineID(engine_id)
            return self._engines[engine_enum]
        except (ValueError, KeyError):
            raise SearchEngineNotFoundError(
                f"Invalid engine_id: {engine_id}. "
                f"Supported engines: {[e.value for e in SearchEngineID]}"
            )