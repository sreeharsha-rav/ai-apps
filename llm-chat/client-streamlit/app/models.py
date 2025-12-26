from pydantic import BaseModel

class Message(BaseModel):
    role: str
    content: str
    
class ChatHistory(BaseModel):
    messages: list[Message] = []

class CompletionChunk(BaseModel):
    content: str
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int