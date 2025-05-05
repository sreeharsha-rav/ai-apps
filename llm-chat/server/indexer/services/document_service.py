from indexer.schemas.document import ParsedDocument, TextChunk, VectorizedChunk
from indexer.core.storage import BaseStorage
from indexer.core.embedding import BaseEmbedding
from indexer.core.processors import ContentParser, Chunker
from indexer.config import CHUNK_SIZE, CHUNK_OVERLAP
from indexer.utils.logging import setup_logger
from typing import AsyncGenerator

class DocumentService:
    """Processes documents and generates embeddings."""

    def __init__(self, storage_client: BaseStorage, embedding_client: BaseEmbedding, vectorize_batch_size: int = 10):
        """
        Initialize the DocumentService.

        Args:
            storage_client: Storage client for managing documents
            embedding_client: Embedding client for generating embeddings
            vectorize_batch_size: Batch size for vectorization
        """
        self.storage_client = storage_client
        self.embedding_client = embedding_client
        self.content_parser = ContentParser()
        self.vectorize_batch_size = vectorize_batch_size
        self.chunker = Chunker(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        self.logger = setup_logger(name="Indexer: document_service")

    async def process_documents(self, space_name: str) -> AsyncGenerator[VectorizedChunk, None]:
        """
        Process documents in a space using batches.

        Args:
            space_name: Space name

        Returns:
            AsyncGenerator[VectorizedChunk, None]: Generator of vectorized chunks
        """
        try:
            # check if space exists
            if not await self.storage_client.does_space_exist(space_name):
                self.logger.warning(f"Space with name '{space_name}' not found")
                raise FileNotFoundError(f"Space with name '{space_name}' not found")

            # list all files in the space
            files = await self.storage_client.list_all_files(space_name)
            self.logger.info(f"Found {len(files)} files in space: {space_name}")

            # load all files in the space
            files_generator = self.storage_client.load_all_files(space_name, files)
            current_batch: list[TextChunk] = []                                     # batch of text chunks to process
            async for raw_document in files_generator:
                # parse document based on file extension
                parsed_document: ParsedDocument = self.content_parser.parse(raw_document)
                self.logger.debug(f"Parsed document: {parsed_document.file_name}")

                # chunk documents as async generator
                chunk_generator = self.chunker.chunk_document_async(parsed_document)
                async for chunk in chunk_generator:
                    current_batch.append(chunk)

                    # process batch if it reaches the batch size
                    if len(current_batch) >= self.vectorize_batch_size:
                        self.logger.debug(f"Processing batch of {len(current_batch)} chunks")
                        async for vectorized_chunk in self._vectorize_batch(current_batch):
                            yield vectorized_chunk

                        # reset batch
                        current_batch = []

            # process any remaining documents in the batch
            if current_batch:
                self.logger.debug(f"Processing remaining batch of {len(current_batch)} chunks")
                async for vectorized_chunk in self._vectorize_batch(current_batch):
                    yield vectorized_chunk

        except Exception as e:
            self.logger.error(f"Error processing documents: {str(e)}")
            raise e

    async def _vectorize_batch(self, text_chunks: list[TextChunk]) -> AsyncGenerator[VectorizedChunk, None]:
        """
        Vectorize a batch of text chunks.

        Args:
            text_chunks: List of text chunks to process

        Returns:
            AsyncGenerator[VectorizedChunk, None]: Generator of vectorized chunks
        """
        if not text_chunks:
            return

        # extract text content for embedding
        texts = [chunk.chunk_content for chunk in text_chunks]

        try:
            # generate embeddings for the batch
            embeddings = await self.embedding_client.create_embeddings(texts)
            self.logger.debug(f"Generated {len(embeddings)} embeddings")

            # create vectorized chunks from the embeddings
            for chunk, embedding in zip(text_chunks, embeddings):
                yield VectorizedChunk(
                    chunk_id=chunk.chunk_id,
                    doc_id=chunk.doc_id,
                    user_id=chunk.user_id,
                    space_name=chunk.space_name,
                    file_name=chunk.file_name,
                    chunk_content=chunk.chunk_content,
                    chunk_vector=embedding,
                    blob_path=chunk.blob_path,
                    chunk_index=chunk.chunk_index
                )
        except Exception as e:
            self.logger.error(f"Error generating embeddings for batch: {str(e)}")
            raise e
