from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from enum import Enum


class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class Message:
    role: Role
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "role": self.role.value,
            "content": self.content,
            "timestamp": self.timestamp.isoformat(),
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        return cls(
            role=Role(data["role"]),
            content=data["content"],
            timestamp=datetime.fromisoformat(data.get("timestamp", datetime.now().isoformat())),
            metadata=data.get("metadata", {})
        )

@dataclass
class Thread:
    thread_id: str
    name: str
    messages: list[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def add_message(self, role: Role, content: str, metadata: Optional[dict] = None) -> Message:
        message = Message(role=role, content=content, metadata=metadata or {})
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message

    def to_dict(self) -> dict:
        return {
            "thread_id": self.thread_id,
            "name": self.name,
            "messages": [msg.to_dict() for msg in self.messages],
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Thread":
        messages = [Message.from_dict(msg) for msg in data.get("messages", [])]
        return cls(
            thread_id=data["thread_id"],
            name=data["name"],
            messages=messages,
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat()))
        )
