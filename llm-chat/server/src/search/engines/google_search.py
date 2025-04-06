import requests
import logging
from typing import ClassVar, List
from src.search.engines.base_search import BaseSearch
from src.schemas.search import SearchEngineInfo, SearchEngineID, SearchResult
from src.config.settings import settings
from src.utils.decorators import singleton
from src.exceptions.search import SearchEngineConfigError, SearchQueryError


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

            # Set up logging
            self.logger = logging.getLogger(__name__)

            # Get credentials from settings
            self.api_key = settings.GOOGLE_CSE_API_KEY
            self.search_engine_id = settings.GOOGLE_CSE_ID
            self.base_url = "https://www.googleapis.com/customsearch/v1"

            # Validate required environment variables
            if not self.api_key:
                raise SearchEngineConfigError("GOOGLE_CSE_API_KEY environment variable is not set")
            if not self.search_engine_id:
                raise SearchEngineConfigError("GOOGLE_CSE_ID environment variable is not set")

            self.logger.info("Google Search API initialized successfully")
            self._initialized = True

    def search(self, query: str, num_results: int = 5) -> List[SearchResult]:
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
        self.logger.info(f"Performing Google search for query: {query[:100]}...")

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
            self.logger.info("Making request to Google Custom Search API")
            response = requests.get(self.base_url, params=params, timeout=5)

            if response.status_code in (401, 403):
                raise SearchQueryError(f"Authentication error: {response.status_code}")
            elif response.status_code == 429:
                raise SearchQueryError("Rate limit exceeded for Google Search API")

            response.raise_for_status()
            results = response.json()

            # Check if 'items' exists in the results
            if 'items' not in results:
                self.logger.warning("No search results found")
                return []

            items = results['items']
            self.logger.info(f"Successfully received {len(items)} results from Google API")

            # Format the results
            formatted_results: List[SearchResult] = [
                SearchResult(
                    title=item.get('title', ''),
                    link=item.get('link', ''),
                    snippet=item.get('snippet', '')
                ) for item in items if 'title' in item and 'link' in item and 'snippet' in item
                ## Can add CSE image and other fields if needed
            ]

            return formatted_results

        except requests.Timeout:
            self.logger.error("Google search request timed out")
            raise SearchQueryError("Search request timed out")
        except requests.ConnectionError:
            self.logger.error("Connection error during Google search")
            raise SearchQueryError("Connection error during search")
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Google search failed: {str(e)}")
            raise SearchQueryError(f"Search query failed: {str(e)}")