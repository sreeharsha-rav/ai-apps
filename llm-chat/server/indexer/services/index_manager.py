from indexer.core.vector_store import BaseVectorStore
from indexer.schemas.document import VectorizedChunk
from indexer.schemas.vector_store import IndexDocument
from indexer.utils.logging import setup_logger

class IndexManager:
    """Manages Search Indexes"""

    def __init__(
            self,
            vector_store_client: BaseVectorStore
    ):
        """
        Initialize the IndexManager.

        Args:
            vector_store_client: Vector store client for indexing documents
        """
        self.vector_store_client = vector_store_client
        self.logger = setup_logger(name="Indexer: index_manager")

    async def create_index(self):
        """Create an index for a user and space."""
        try:
            # check if index exists
            if await self.vector_store_client.does_index_exist():
                self.logger.warning("Index already exists")
                raise Exception("Index already exists")

            # create index
            self.logger.info("Creating new index")
            await self.vector_store_client.create_index()
            self.logger.info("Index created successfully")
        except Exception as e:
            self.logger.error(f"Error creating index: {str(e)}")
            raise e

    async def index_documents(self, vectorized_chunks: list[VectorizedChunk]):
        """Index documents in an index for a user and space."""
        try:
            # check if index exists
            if not await self.vector_store_client.does_index_exist():
                self.logger.error("Index does not exist")
                raise Exception("Index does not exist")
                # self.logger.warning("Index does not exist, creating new index")
                # await self.vector_store_client.create_index()

            # convert vectorized chunks to index documents
            self.logger.info(f"Indexing {len(vectorized_chunks)} documents")
            index_documents = [
                IndexDocument(
                    chunk_id=chunk.chunk_id,
                    user_id=chunk.user_id,
                    doc_id=chunk.doc_id,
                    space_name=chunk.space_name,
                    file_name=chunk.file_name,
                    chunk_content=chunk.chunk_content,
                    chunk_vector=chunk.chunk_vector,
                    blob_path=chunk.blob_path
                )
                for chunk in vectorized_chunks
            ]

            # index documents
            index_results = await self.vector_store_client.index_documents(index_documents)
            self.logger.info(f"Successfully indexed {len(index_results)} documents")
            # TODO: use index_results to update metadata status
        except Exception as e:
            self.logger.error(f"Error indexing documents: {str(e)}")
            raise e

    async def delete_documents(self, user_id: str, space_name: str):
        """Delete all documents in an index for a user and space."""
        try:
            self.logger.info(f"Deleting documents for user '{user_id}' in space '{space_name}'")
            # delete documents
            await self.vector_store_client.delete_documents(user_id, space_name)
            self.logger.info(f"Successfully deleted documents for user '{user_id}' in space '{space_name}'")
        except Exception as e:
            self.logger.error(f"Error deleting documents: {str(e)}")
            raise e
