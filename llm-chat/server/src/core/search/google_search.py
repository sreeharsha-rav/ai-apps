from .base_search import BaseSearch
import requests
from typing import ClassVar
from src.schemas.search import SearchEngineInfo, SearchEngineID, SearchResult
from src.core.config import search_settings
from src.utils.decorators import singleton
from src.core.exceptions.search import SearchEngineConfigError, SearchQueryError

@singleton
class GoogleSearch(BaseSearch):
    """Implementation of Google Custom Search API."""

    ENGINE_INFO: ClassVar[SearchEngineInfo] = SearchEngineInfo(
        engine_id=SearchEngineID.GOOGLE,
        name="Google Custom Search",
        max_results_per_query=10,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()

            # Get credentials from settings
            self.api_key = search_settings.GOOGLE_CSE_API_KEY
            self.search_engine_id = search_settings.GOOGLE_CSE_ID
            self.base_url = search_settings.GOOGLE_CSE_BASE_URL

            # Validate required environment variables
            if not self.api_key:
                raise SearchEngineConfigError("GOOGLE_CSE_API_KEY environment variable is not set")
            if not self.search_engine_id:
                raise SearchEngineConfigError("GOOGLE_CSE_ID environment variable is not set")
            if not self.base_url:
                raise SearchEngineConfigError("GOOGLE_CSE_BASE_URL environment variable is not set")

            self._initialized = True

    def search(self, query: str, num_results: int = 5) -> list[SearchResult]:
        """
        Fetches search results from Google Custom Search API.

        Args:
            query: The search query string
            num_results: Number of results to return (max 10)

        Returns:
            List[SearchResult]: List of search results

        Raises:
            SearchQueryError: When the search query fails
        """
        if not query:
            raise SearchQueryError("Search query cannot be empty")

        # Ensure num_results doesn't exceed the max allowed
        num_results = min(num_results, self.ENGINE_INFO.max_results_per_query)

        params = {
            'q': query,
            'key': self.api_key,
            'cx': self.search_engine_id,
            'num': num_results
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=5)
            if response.status_code in (401, 403):
                raise SearchQueryError(f"Authentication error: {response.status_code}")
            elif response.status_code == 429:
                raise SearchQueryError("Rate limit exceeded for Google Search API")

            response.raise_for_status()
            results = response.json()

            # Check if 'items' exists in the results
            if 'items' not in results:
                return []

            items = results['items']

            # Format the results
            formatted_results: list[SearchResult] = [
                SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', '')
                ) for item in items if 'title' in item and 'link' in item and 'snippet' in item
                ## Can add CSE image and other fields if needed
            ]

            return formatted_results

        except requests.Timeout:
            raise SearchQueryError("Search request timed out")
        except requests.ConnectionError:
            raise SearchQueryError("Connection error during search")
        except requests.exceptions.RequestException as e:
            raise SearchQueryError(f"Search query failed: {str(e)}")