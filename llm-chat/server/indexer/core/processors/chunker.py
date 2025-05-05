from langchain_text_splitters import RecursiveCharacterTextSplitter
from indexer.schemas.document import ParsedDocument, TextChunk
from indexer.utils.logging import setup_logger
from typing import AsyncGenerator

class Chunker:
    """Class for chunking text into smaller pieces."""

    def __init__(self, chunk_size, chunk_overlap):
        """
        Initialize the chunker with the given chunk size and overlap.

        Args:
            chunk_size: Size of each chunk
            chunk_overlap: Overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        # TODO: research and implement text splitters based on chunking strategies
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
        self.logger = setup_logger(name="Indexer: chunker")
        self.logger.debug(f"Initialized chunker with size={chunk_size}, overlap={chunk_overlap}")

    def chunk_document(self, document: ParsedDocument) -> list[TextChunk]:
        """
        Chunk the given document into smaller pieces.

        Args:
            document(ParsedDocument): Document to chunk

        Returns:
            list[TextChunk]: List of chunks
        """
        try:
            self.logger.debug(f"Chunking document: {document.file_name}")
            split_chunks = self.text_splitter.split_text(document.content)
            self.logger.info(f"Split document into {len(split_chunks)} chunks")
            
            chunks = [
                TextChunk(
                    chunk_id=f"chunk-{document.doc_id}-{idx}",
                    doc_id=document.doc_id,
                    user_id=document.user_id,
                    space_name=document.space_name,
                    file_name=document.file_name,
                    blob_path=document.blob_path,
                    chunk_content=chunk,
                    chunk_index=idx
                )
                for idx, chunk in enumerate(split_chunks, 1)
            ]
            return chunks
        except Exception as e:
            self.logger.error(f"Error chunking text: {str(e)}")
            raise e

    async def chunk_document_async(self, document: ParsedDocument) -> AsyncGenerator[TextChunk, None]:
        """
        Chunk the given document into smaller pieces as an asynchronous generator.

        Args:
            document(ParsedDocument): Document to chunk

        Returns:
            AsyncGenerator[TextChunk, None]: Generator of chunks
        """
        try:
            self.logger.debug(f"Async chunking document: {document.file_name}")
            split_chunks = self.text_splitter.split_text(document.content)
            self.logger.info(f"Split document into {len(split_chunks)} chunks")
            
            # TODO: research and implement text splitters based on chunking strategies and async generator
            for idx, chunk in enumerate(split_chunks, 1):
                yield TextChunk(
                    chunk_id=f"chunk-{document.doc_id}-{idx}",
                    doc_id=document.doc_id,
                    user_id=document.user_id,
                    space_name=document.space_name,
                    file_name=document.file_name,
                    blob_path=document.blob_path,
                    chunk_content=chunk,
                    chunk_index=idx
                )
        except Exception as e:
            self.logger.error(f"Error chunking text: {str(e)}")
            raise e