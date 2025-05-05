from azure.search.documents.aio import SearchClient
from azure.search.documents.models import IndexingResult
from azure.search.documents.indexes.aio import SearchIndexClient
from azure.search.documents.indexes.models import SearchIndex
from azure.core.credentials import AzureKeyCredential
from indexer.schemas.vector_store import IndexFields, IndexVectorSearch, IndexDocument, IndexResult
from indexer.config import azure_search_settings
from indexer.utils.logging import setup_logger
from .base_vector_store import BaseVectorStore

class AzureAISearch(BaseVectorStore):
    """Class for interacting with Azure AI Search."""

    def __init__(self):
        """Initialize the Azure AI Search client."""
        try:
            self.logger = setup_logger(name="Indexer: azure_ai_search")
            self.logger.info("Initializing Azure AI Search client")
            
            # define index
            self.search_index = SearchIndex(
                name=azure_search_settings.AZURE_AI_SEARCH_INDEX_NAME,
                fields=IndexFields,
                vector_search=IndexVectorSearch
            )

            # define credential for Azure AI Search
            self.azure_search_credential = AzureKeyCredential(
                key=azure_search_settings.AZURE_AI_SEARCH_API_KEY,
            )

            # initialize index client
            self.index_client = SearchIndexClient(
                endpoint=azure_search_settings.AZURE_AI_SEARCH_ENDPOINT,
                credential=self.azure_search_credential
            )

            # initialize search client for retrieving documents
            self.search_client = SearchClient(
                endpoint=azure_search_settings.AZURE_AI_SEARCH_ENDPOINT,
                index_name=self.search_index.name,
                credential=self.azure_search_credential
            )
            
            self.logger.debug("Azure AI Search client initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing Azure AI Search client: {str(e)}")
            raise e
            
    async def close(self):
        """Close all clients and release resources."""
        try:
            self.logger.debug("Closing Azure AI Search clients")
            await self.index_client.close()
            await self.search_client.close()
            self.logger.debug("Azure AI Search clients closed successfully")
        except Exception as e:
            self.logger.error(f"Error closing Azure AI Search clients: {str(e)}")

    async def does_index_exist(self) -> bool:
        """Check if the index exists."""
        try:
            self.logger.debug(f"Checking if index '{self.search_index.name}' exists")
            if await self.index_client.get_index(self.search_index.name):
                self.logger.debug(f"Index '{self.search_index.name}' exists")
                return True
            else:
                self.logger.debug(f"Index '{self.search_index.name}' does not exist")
                return False
        except Exception as e:
            self.logger.error(f"Error checking index existence: {str(e)}")
            raise e

    async def create_index(self):
        """Create the index from index schema definition."""
        try:
            self.logger.info(f"Creating index '{self.search_index.name}'")
            await self.index_client.create_or_update_index(self.search_index)
            self.logger.info(f"Index '{self.search_index.name}' created successfully")
        except Exception as e:
            self.logger.error(f"Error creating index: {str(e)}")
            raise e

    async def delete_index(self):
        """Delete the search index and all documents it contains."""
        try:
            self.logger.info(f"Deleting index '{self.search_index.name}'")
            await self.index_client.delete_index(self.search_index)
            self.logger.info(f"Index '{self.search_index.name}' deleted successfully")
        except Exception as e:
            self.logger.error(f"Error deleting index: {str(e)}")
            raise e

    async def index_documents(self, documents: list[IndexDocument]) -> list[IndexResult]:
        """
        Index documents in Azure AI Search.

        Args:
            documents(list[IndexDocument]): List of documents to index

        Returns:
            list[IndexResult]: List of indexing results
        """
        try:
            self.logger.info(f"Indexing {len(documents)} documents")
            dict_documents = [doc.model_dump() for doc in documents]
            results: list[IndexingResult] = await self.search_client.upload_documents(documents=dict_documents)
            self.logger.info(f"Documents indexed successfully: {sum(1 for r in results if r.succeeded)}/{len(results)} succeeded")
            return [
                IndexResult(success=r.succeeded)
                for r in results
            ]
        except Exception as e:
            self.logger.error(f"Error indexing documents: {str(e)}")
            raise e

    async def delete_documents(self, user_id: str, space_name: str):
        """
        Delete all documents of space_name and user_id in index.

        Args:
            user_id: User ID
            space_name: Space name
        """
        try:
            self.logger.info(f"Deleting documents for user '{user_id}' in space '{space_name}'")
            
            # get all existing documents of space_name and user_id
            self.logger.debug("Searching for documents to delete")
            existing_documents = await self.search_client.search(
                search_text="*",
                filter=f"user_id eq '{user_id}' and space_name eq '{space_name}'",
                select="chunk_id"           # only select chunk_id as key to delete
            )

            # delete all existing documents of space_name and user_id
            if existing_documents:
                doc_count = sum(1 for _ in existing_documents)
                self.logger.debug(f"Found {doc_count} documents to delete")
                await self.search_client.delete_documents(documents=existing_documents)
                self.logger.info(f"Documents deleted successfully")
            else:
                self.logger.info(f"No documents found to delete")
        except Exception as e:
            self.logger.error(f"Error deleting documents: {str(e)}")
            raise e

    # async def search_index_documents(self, user_id: str, space_name: str, query: str, top: int, query_embedding: list[float]):
    #     """
    #     Search the index for documents.
    #
    #     Args:
    #         user_id: User ID
    #         space_name: Space name
    #         query: Search query
    #         top: Number of top results to return
    #         query_embedding: Query embedding
    #
    #     Returns:
    #         List of search results
    #     """
    #     try:
    #         query_vector = VectorizedQuery(
    #             vector=query_embedding,
    #             k_nearest_neighbors=50,             # TODO: research for optimal value
    #             fields="chunk_vector",
    #         )
    #         results = await self.search_client.search(
    #             search_text=query,
    #             top=top,                            # TODO: research for optimal value
    #             vector_queries=[query_vector],
    #             filter=f"user_id eq '{user_id}' and space_name eq '{space_name}'"
    #         )
    #         return results
    #     except Exception as e:
    #         print(f"Error searching index: {str(e)}")
    #         raise e

