from typing import Optional
from ulid import ULID

from core.models import Thread, Role
from core.storage import Storage


class ThreadManager:
    """Manages chat threads."""

    def __init__(self, storage: Storage):
        self.storage = storage

    def create(self, name: Optional[str] = None) -> Thread:
        thread_id = f"thread_{ULID()}"
        thread_name = name or f"Chat {len(self.storage.list_all()) + 1}"
        thread = Thread(thread_id=thread_id, name=thread_name)
        self.storage.save(thread)
        return thread

    def get(self, thread_id: str) -> Optional[Thread]:
        return self.storage.load(thread_id)

    def delete(self, thread_id: str) -> bool:
        return self.storage.delete(thread_id)

    def list_all(self, reverse: bool = True) -> list[Thread]:
        threads = self.storage.list_all()
        return sorted(threads, key=lambda t: t.created_at, reverse=reverse)

    def add_message(self, thread_id: str, role: Role, content: str) -> Thread:
        thread = self.get(thread_id)
        if not thread:
            raise ValueError(f"Thread {thread_id} not found")
        thread.add_message(role, content)
        self.storage.save(thread)
        return thread
