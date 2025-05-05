from .base_embedding import BaseEmbedding
from indexer.config import azure_openai_embedding_settings
from indexer.utils.logging import setup_logger
from langchain_openai.embeddings import AzureOpenAIEmbeddings

class AzureOpenAIAda002(BaseEmbedding):
    """Azure OpenAI Ada 002 embedding implementation."""

    def __init__(self):
        """Initialize Azure OpenAI Ada 002 embedding model."""
        try:
            self.logger = setup_logger(name="Indexer: azure_openai_embedding")
            self.logger.info("Initializing Azure OpenAI Ada 002 embedding model")
            
            self.embedding_model = AzureOpenAIEmbeddings(
                azure_endpoint=azure_openai_embedding_settings.AZURE_OPENAI_EMBEDDINGS_ENDPOINT,
                azure_deployment=azure_openai_embedding_settings.AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT,
                api_key=azure_openai_embedding_settings.AZURE_OPENAI_EMBEDDINGS_API_KEY,
                api_version=azure_openai_embedding_settings.AZURE_OPENAI_API_VERSION,
                model=azure_openai_embedding_settings.AZURE_OPENAI_EMBEDDINGS_MODEL,
                # dimensions=1536               # default value
            )
            self.logger.debug("Azure OpenAI Ada 002 embedding model initialized successfully")
        except Exception as e:
            self.logger.error(f"Error initializing Azure OpenAI Ada 002 embedding model: {str(e)}")
            raise e

    async def create_single_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            list[float]: generated embedding vector
        """
        try:
            self.logger.debug("Creating single embedding")
            embedding = await self.embedding_model.aembed_query(text)
            self.logger.debug(f"Created embedding with {len(embedding)} dimensions")
            return embedding
        except Exception as e:
            self.logger.error(f"Error creating embedding: {str(e)}")
            raise e

    async def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to embed

        Returns:
            list[list[float]]: List of generated embedding vectors
        """
        try:
            self.logger.debug(f"Creating embeddings for {len(texts)} texts")
            embeddings = await self.embedding_model.aembed_documents(texts)
            self.logger.debug(f"Created {len(embeddings)} embeddings")
            return embeddings
        except Exception as e:
            self.logger.error(f"Error creating embeddings: {str(e)}")
            raise e