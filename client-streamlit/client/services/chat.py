from typing import Generator
from openai import OpenAI, Stream
from openai.types.chat import ChatCompletionChunk, ChatCompletionStreamOptionsParam

from core.models import Role
from .thread import ThreadManager

class ChatService:
    """Handles chat interactions with LLM."""

    def __init__(
        self,
        thread_manager: ThreadManager,
        api_key: str,
        model: str = "gpt-4.1-mini",
        system_prompt: str = "You are a helpful assistant."
    ):
        self.thread_manager = thread_manager
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.system_prompt = system_prompt

    def send_message(
        self,
        thread_id: str,
        content: str,
        model: str = "gpt-4.1-mini"
    ) -> Generator[str, None, None]:
        """Send message and stream response."""

        thread = self.thread_manager.add_message(thread_id=thread_id, role=Role.USER, content=content)
        messages = [
            {"role": "system", "content": self.system_prompt},
            *[{"role": m.role.value, "content": m.content} for m in thread.messages]
        ]

        response: Stream[ChatCompletionChunk] = self.client.chat.completions.create(
            messages=messages,
            model=model,
            stream=True,
            stream_options=ChatCompletionStreamOptionsParam(include_usage=True)
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

            if chunk.usage:
                print (f"prompt_tokens: {chunk.usage.prompt_tokens}\n"
                      f"completion_tokens: {chunk.usage.completion_tokens}\n"
                      f"total_tokens: {chunk.usage.total_tokens}")

    def save_response(self, thread_id: str, content: str) -> None:
        """Save assistant response."""
        self.thread_manager.add_message(thread_id=thread_id, role=Role.ASSISTANT, content=content)
