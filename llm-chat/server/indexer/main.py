from indexer.core.embedding import AzureOpenAIAda002
from indexer.core.storage import AzureStorageContainer
from indexer.core.vector_store import AzureAISearch
from indexer.services.document_service import DocumentService
from indexer.services.index_manager import IndexManager
from indexer.schemas.document import VectorizedChunk
from indexer.schemas.metadata import IndexingStatus
from indexer.utils.logging import setup_logger
from datetime import datetime

class Indexer:
    """Main entry point for the indexer application."""

    def __init__(self, user_id: str = "sreeharsha-dev"):
        """
        Initialize the indexer application for a user.

        Args:
            user_id: Unique user identifier for container
        """
        # Set up logger
        self.logger = setup_logger(name="Indexer: main")
        self.logger.info(f"Initializing indexer for user: {user_id}")

        # Initialize clients
        # TODO: get user_id from auth and validate
        self.storage_client = AzureStorageContainer(user_id=user_id)
        self.embedding_client = AzureOpenAIAda002()
        self.vector_store_client = AzureAISearch()
        self.logger.debug("Initialized all clients")

        # Initialize services
        self.document_service = DocumentService(
            storage_client=self.storage_client,
            embedding_client=self.embedding_client,
            vectorize_batch_size=10                    # batch size for vectorizing, TODO: research for optimal batch size and set based on embedding model context length
        )
        self.index_manager = IndexManager(
            vector_store_client=self.vector_store_client
        )
        self.logger.debug("Initialized all services")

        # Initialize other variables
        self.index_batch_size = 100
        self.logger.info("Indexer initialization complete")

    async def run(self, space_name: str):
        """
        Run the indexer application for a user and space.

        NOTE: assume index already exists and is created with correct schema

        Args:
            space_name: Unique space identifier
        """
        try:
            self.logger.info(f"Starting indexing for space: {space_name}")
            
            # Initialize indexing status
            self.logger.debug("Updating space metadata status to IN_PROGRESS")
            space_metadata = await self.storage_client.get_space_metadata(space_name)
            space_metadata.indexing_status = IndexingStatus.IN_PROGRESS
            await self.storage_client.update_space_metadata(space_name, space_metadata)

            # Process documents in batches
            document_queue: list[VectorizedChunk] = []
            document_generator = self.document_service.process_documents(space_name)
            
            self.logger.info("Processing documents...")
            async for vectorized_chunk in document_generator:
                document_queue.append(vectorized_chunk)

                # Index documents batch
                if len(document_queue) >= self.index_batch_size:
                    self.logger.debug(f"Indexing batch of {len(document_queue)} documents")
                    await self.index_manager.index_documents(document_queue)
                    document_queue = []

            # Upload any remaining documents from the queue
            if document_queue:
                self.logger.debug(f"Indexing remaining {len(document_queue)} documents")
                await self.index_manager.index_documents(document_queue)
                document_queue = []

            # Update indexing status
            self.logger.debug("Updating space metadata status to COMPLETE")
            space_metadata.indexing_status = IndexingStatus.COMPLETE
            space_metadata.last_indexed = datetime.now().isoformat()
            await self.storage_client.update_space_metadata(space_name, space_metadata)
            
            self.logger.info(f"Indexing completed successfully for space: {space_name}")
        except Exception as e:
            self.logger.error(f"Error running indexer: {str(e)}")
            raise e

    def stop(self):
        """Stop the indexer application."""
        # TODO: not required in current implementation
        self.logger.info("Stopping indexer")
        pass
