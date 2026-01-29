import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from .models import Thread


class Storage(ABC):
    """Base storage interface."""

    @abstractmethod
    def save(self, thread: Thread) -> None:
        pass

    @abstractmethod
    def load(self, thread_id: str) -> Optional[Thread]:
        pass

    @abstractmethod
    def delete(self, thread_id: str) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> list[Thread]:
        pass


class MemoryStorage(Storage):
    """In-memory storage (data lost on restart)."""

    def __init__(self):
        self._data: dict[str, Thread] = {}

    def save(self, thread: Thread) -> None:
        self._data[thread.thread_id] = thread

    def load(self, thread_id: str) -> Optional[Thread]:
        return self._data.get(thread_id)

    def delete(self, thread_id: str) -> bool:
        return self._data.pop(thread_id, None) is not None

    def list_all(self) -> list[Thread]:
        return list(self._data.values())


class JSONStorage(Storage):
    """JSON file storage."""

    def __init__(self, file_path: str = "data/threads.json"):
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self._data = self._load_file()

    def _load_file(self) -> dict[str, Thread]:
        if not self.file_path.exists():
            return {}
        with open(self.file_path, 'r') as f:
            data = json.load(f)
            return {tid: Thread.from_dict(t) for tid, t in data.items()}

    def _save_file(self) -> None:
        with open(self.file_path, 'w') as f:
            json.dump(
                {tid: t.to_dict() for tid, t in self._data.items()},
                f,
                indent=2
            )

    def save(self, thread: Thread) -> None:
        self._data[thread.thread_id] = thread
        self._save_file()

    def load(self, thread_id: str) -> Optional[Thread]:
        return self._data.get(thread_id)

    def delete(self, thread_id: str) -> bool:
        if thread_id in self._data:
            del self._data[thread_id]
            self._save_file()
            return True
        return False

    def list_all(self) -> list[Thread]:
        return list(self._data.values())
