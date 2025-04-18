from enum import Enum
from pydantic import BaseModel, Field

class SearchEngineID(str, Enum):
    """Enum for supported search engine IDs"""
    GOOGLE = "google"
    # Add more search engines as you implement them
    # DUCKDUCKGO = "duckduckgo"
    # BING = "bing"

class SearchEngineInfo(BaseModel):
    """Information about the search engine"""
    engine_id: SearchEngineID = Field(description="Unique identifier for the search engine")
    name: str = Field(description="Display name for the search engine")
    max_results_per_query: int = Field(gt=0, description="Maximum number of results per query")

class SearchResult(BaseModel):
    """A single search result item from the search engine"""
    title: str = Field(description="Title of the search result")
    link: str = Field(description="URL of the search result")
    snippet: str = Field(description="Snippet or description of the search result")
    ## Add more fields as needed, like image URL, etc.