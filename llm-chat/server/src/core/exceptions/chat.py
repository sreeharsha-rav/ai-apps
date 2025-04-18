class ChatError(Exception):
    """Base exception for chat-related errors"""
    pass

class ChatNotFoundError(ChatError):
    """Raised when chat_id is not found"""
    pass