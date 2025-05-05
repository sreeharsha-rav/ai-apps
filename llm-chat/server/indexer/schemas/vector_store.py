from pydantic import BaseModel
from typing import Optional
from azure.search.documents.indexes.models import (
    SimpleField,
    SearchField,
    SearchableField,
    VectorSearch,
    HnswAlgorithmConfiguration,
    HnswParameters,
    VectorSearchProfile
)

# Define vector search config , TODO: Research for optimization using vector quantization
IndexVectorSearch = VectorSearch(
    algorithms=[
        HnswAlgorithmConfiguration(
            name="myHnswConfig",
            kind="hnsw",
            parameters=HnswParameters(
                m=4,
                ef_construction=400,
                ef_search=500,
                metric="cosine"
            )
        )
    ],
    profiles=[
        VectorSearchProfile(
            name="myHnswProfile",
            algorithm_configuration_name="myHnswConfig"
        )
    ]
)

# Define fields for Index Store
IndexFields = [
    # Primary key (chunk identifier)
    SimpleField(name="chunk_id", type="Edm.String", key=True, filterable=False),

    # Security & multi-tenancy fields
    SimpleField(name="user_id", type="Edm.String", filterable=True, retrievable=True),

    # Document relationship fields
    SimpleField(name="doc_id", type="Edm.String", filterable=True, retrievable=True),
    SimpleField(name="space_name", type="Edm.String", filterable=True, retrievable=True),  # Folder equivalent
    SimpleField(name="file_name", type="Edm.String", filterable=True, retrievable=True),

    # Content fields
    SearchableField(name="chunk_content", type="Edm.String", searchable=True, retrievable=True),

    # Vector field (1536 dimensions for text-embedding-ada-002)
    SearchField(
        name="chunk_vector",
        type="Collection(Edm.Single)",
        vector_search_dimensions=1536,  # default, can be configurable based on embedding model
        vector_search_profile_name="myHnswProfile"
        # can be configured based on needs and optimized for efficieny using custom vector profiles
    ),

    # Metadata (optional)
    SimpleField(name="blob_path", type="Edm.String", retrievable=True)
]


class IndexDocument(BaseModel):
    """Represents a document ready for Azure AI Search indexing."""
    chunk_id: str  # key
    user_id: str
    doc_id: str
    space_name: str
    file_name: str
    chunk_content: str
    chunk_vector: list[float]
    blob_path: str

class IndexResult(BaseModel):
    """Represents the result of indexing a document."""
    success: bool
