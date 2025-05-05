from abc import ABC, abstractmethod

class BaseEmbedding(ABC):
    """Base class for all embedding implementations"""

    @abstractmethod
    async def create_embeddings(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for a list of texts as an asynchronous generator.

        Args:
            texts: List of texts to embed

        Returns:
            list[list[float]]: List of generated embedding vectors
        """
        pass

    @abstractmethod
    async def create_single_embedding(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            list[float]: generated embedding vector
        """
        pass