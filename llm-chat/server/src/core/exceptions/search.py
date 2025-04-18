class SearchError(Exception):
    """Base exception for search errors"""
    pass

class SearchEngineConfigError(SearchError):
    """Exception raised when search engine configuration is invalid"""
    pass

class SearchEngineNotFoundError(SearchError):
    """Exception raised when a search engine is not found"""
    pass

class SearchQueryError(SearchError):
    """Exception raised when a search query fails"""
    pass