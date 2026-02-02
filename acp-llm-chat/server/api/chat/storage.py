import json
from pathlib import Path
from typing import Protocol, List, Dict, Optional
from .models import ChatHistory, Item
from datetime import datetime

class StorageBackend(Protocol):
    def save_chat(self, chat: ChatHistory) -> None: ...
    def load_chat(self, chat_id: str) -> Optional[ChatHistory]: ...
    def load_all_chats(self) -> List[ChatHistory]: ...
    def delete_chat(self, chat_id: str) -> None: ...
    def clear_all(self) -> None: ...
    def update_chat_title(self, chat_id: str, title: str) -> Optional[ChatHistory]: ...

class JSONFileStorage:
    def __init__(self, filepath: str = "./chats.json"):
        self.filepath = Path(filepath)
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self._write_file({})

    def _read_file(self) -> Dict[str, dict]:
        try:
            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    # Convert list to dict if someone manually edited it or using old format
                    return {c.get("id", str(i)): c for i, c in enumerate(data)}
                return data if isinstance(data, dict) else {}
        except (json.JSONDecodeError, FileNotFoundError, Exception):
            return {}

    def _write_file(self, data: Dict[str, dict]) -> None:
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_chat(self, chat: ChatHistory) -> None:
        data = self._read_file()
        chat.updated_at = datetime.now()
        data[chat.id] = json.loads(chat.model_dump_json())
        self._write_file(data)

    def load_chat(self, chat_id: str) -> Optional[ChatHistory]:
        data = self._read_file()
        chat_dict = data.get(chat_id)
        return ChatHistory(**chat_dict) if chat_dict else None

    def load_all_chats(self) -> List[ChatHistory]:
        data = self._read_file()
        return [ChatHistory(**c) for c in data.values()]

    def delete_chat(self, chat_id: str) -> None:
        data = self._read_file()
        if chat_id in data:
            del data[chat_id]
            self._write_file(data)

    def clear_all(self) -> None:
        self._write_file({})

    def update_chat_title(self, chat_id: str, title: str) -> Optional[ChatHistory]:
        chat = self.load_chat(chat_id)
        if chat:
            chat.title = title
            self.save_chat(chat)
            return chat
        return None

class ChatStore:
    def __init__(self, backend: StorageBackend):
        self.backend = backend

    def get_or_create_chat(self, chat_id: Optional[str] = None) -> ChatHistory:
        if chat_id:
            chat = self.backend.load_chat(chat_id)
            if chat: return chat
        
        new_chat = ChatHistory()
        self.backend.save_chat(new_chat)
        return new_chat

    def update_chat_tokens(self, chat_id: str, tokens: int) -> None:
        chat = self.backend.load_chat(chat_id)
        if chat:
            chat.total_tokens = tokens
            self.backend.save_chat(chat)

    def save_item(self, chat_id: str, item: Item) -> None:
        chat = self.backend.load_chat(chat_id)
        if not chat:
            chat = ChatHistory(id=chat_id)
        
        chat.items.append(item)
        # Assuming total_tokens might be inside item.data or handled elsewhere, 
        # but for now preserving previous logic if applicable or simplifying.
        # If item has token usage we might want to update it. 
        # checking item.data for usage info if it's a dict
        if isinstance(item.data, dict) and 'usage' in item.data:
             # simplistic total token accumulation if possible, or just ignore for now as per refactor
             pass
        
        self.backend.save_chat(chat)

    def get_all_chats(self) -> List[ChatHistory]:
        return sorted(self.backend.load_all_chats(), key=lambda x: x.updated_at, reverse=True)

    def delete_chat(self, chat_id: str) -> None:
        self.backend.delete_chat(chat_id)

    def clear(self) -> None:
        self.backend.clear_all()

    def update_chat_title(self, chat_id: str, title: str) -> Optional[ChatHistory]:
        return self.backend.update_chat_title(chat_id, title)
    
    def update_chat_canvas(self, chat_id: str, canvas_data: any) -> None:
        chat = self.backend.load_chat(chat_id)
        if chat:
            chat.canvas = canvas_data
            self.backend.save_chat(chat)

storage = ChatStore(JSONFileStorage())
