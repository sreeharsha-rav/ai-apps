import os
from dotenv import load_dotenv
from typing import AsyncGenerator, Sequence
from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk, ChatCompletionStreamOptionsParam

from .logger import logger

load_dotenv()


class OpenAIResponseGen:
    """
    A class to handle streaming responses from OpenAI's LLM.
    """

    def __init__(self, model: str = "gpt-4.1-mini"):
        """
        Initialize the OpenAI response generator.

        Args:
            model (str): The model to use for completions. Defaults to "gpt-4.1-mini".

        Raises:
            ValueError: If API key is not provided and not found in environment variables.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables.")

        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)

    async def get_response(self, system_instruction: str, history: list[dict[str, str]]) -> str:
        """
        Generate a complete response from the LLM based on the system instruction and chat history.

        Args:
            system_instruction (str): The system instruction to guide the LLM's behavior.
            history (list[dict[str, str]]): The chat history containing previous messages.
        Returns:
            str: The complete LLM response.
        """
        try:
            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {"role": "system", "content": system_instruction},
                    *history,
                ],
            )
            return response.output_text
        except Exception as e:
            logger.error(f"Error during LLM response: {str(e)}", exc_info=True)
            return f"\n[Error]: {str(e)}\n"

    async def get_streaming_response(self, system_instruction: str, history: list[dict[str, str]]) -> AsyncGenerator[Sequence[str], None]:
        """
        Generate a streaming response from the LLM based on the system instruction and chat history.

        Args:
            system_instruction (str): The system instruction to guide the LLM's behavior.
            history (list[dict[str, str]]): The chat history containing previous messages.
        Yields:
            str: Chunks of the LLM's response as they are generated.
        """
        try:
            response: AsyncStream[ChatCompletionChunk] = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_instruction},
                    *history,
                ],
                stream=True,
                stream_options=ChatCompletionStreamOptionsParam(include_usage=True),
            )

            async for chunk in response:
                if chunk.choices and len(chunk.choices) > 0:
                    delta = chunk.choices[0].delta
                    if delta and delta.content:
                        yield delta.content

                if chunk.usage:
                    logger.info(f"Token usage - Prompt: {chunk.usage.prompt_tokens}, "
                                f"Completion: {chunk.usage.completion_tokens}, "
                                f"Total: {chunk.usage.total_tokens}")

        except Exception as e:
            logger.error(f"Error during LLM streaming response: {str(e)}", exc_info=True)
            yield f"\n[Error]: {str(e)}\n"
