import json
import os
from abc import ABC, abstractmethod
from typing import List
from openai.types.responses import ResponseInputItemParam
from core.utils import logger
from core.models import Context

class ChatStore(ABC):
    """
    Abstract base class for chat history storage.
    """
    @abstractmethod
    def add_item(self, item: ResponseInputItemParam) -> None:
        """Add a single item to the history."""
        pass

    @abstractmethod
    def get_history(self) -> List[ResponseInputItemParam]:
        """Retrieve the full chat history."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear the history."""
        pass


class InMemoryChatStore(ChatStore):
    """
    Simples in-memory list storage.
    """
    def __init__(self):
        self._history: List[ResponseInputItemParam] = []

    def add_item(self, item: ResponseInputItemParam) -> None:
        self._history.append(item)

    def get_history(self) -> List[ResponseInputItemParam]:
        return self._history

    def clear(self) -> None:
        self._history = []


class LocalJSONChatStore(ChatStore):
    """
    File-based JSON storage for persistence.
    """
    def __init__(self, file_path: str = "_history.json"):
        self.file_path = file_path
        self._history: List[ResponseInputItemParam] = self._load()

    def _load(self) -> List[ResponseInputItemParam]:
        if not os.path.exists(self.file_path):
            logger.debug(f"History file {self.file_path} not found. Starting with empty history.")
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                history = json.load(f)
                logger.debug(f"Loaded {len(history)} items from {self.file_path}")
                return history
        except Exception as e:
            logger.error(f"Failed to load history from {self.file_path}: {e}")
            return []

    def _save(self) -> None:
        try:
            def default_serializer(obj):
                if hasattr(obj, "model_dump"):
                    return obj.model_dump()
                raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._history, f, indent=2, default=default_serializer)
                logger.debug(f"Saved history to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def add_item(self, item: ResponseInputItemParam) -> None:
        if isinstance(item, dict):
             # Handle dict items (like user messages created manually)
             item_type = item.get("type", "unknown")
             if "role" in item:
                 item_type = "message"
        else:
            # Handle objects (like Pydantic models)
            item_type = getattr(item, "type", "unknown")
            
        logger.debug(f"Adding item to store: {item_type}")
        self._history.append(item)
        self._save()

    def get_history(self) -> List[ResponseInputItemParam]:
        return self._history

    def clear(self) -> None:
        logger.info("Clearing chat history")
        self._history = []
        self._save()


class LocalJSONContextStore:
    """
    File-based JSON storage for Context.
    """
    def __init__(self, file_path: str = "_context.json"):
        self.file_path = file_path
        self._context: Context = self._load()

    def _load(self) -> Context:
        if not os.path.exists(self.file_path):
            logger.debug(f"Context file {self.file_path} not found. Starting with empty context.")
            return Context()
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                logger.debug(f"Loaded context from {self.file_path}")
                return Context(**data)
        except Exception as e:
            logger.error(f"Failed to load context from {self.file_path}: {e}")
            return Context()

    def save(self, context: Context) -> None:
        try:
            self._context = context
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(self._context.model_dump(), f, indent=2)
                logger.debug(f"Saved context to {self.file_path}")
        except Exception as e:
            logger.error(f"Failed to save context: {e}")

    def get_context(self) -> Context:
        return self._context

    def clear(self) -> None:
        logger.info("Clearing context")
        self._context = Context()
        self.save(self._context)
