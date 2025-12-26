import os
from dotenv import load_dotenv
from typing import Generator
from openai import OpenAI

from app.config import logger
from app.models import ChatHistory, CompletionChunk

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

llm_client = OpenAI(api_key=OPENAI_API_KEY)


def get_streaming_response(system_instruction: str, history: ChatHistory) -> Generator[str, None, None]:
    """
    Generate a streaming response from the LLM based on the system instruction and chat history.
    
    Args:
        system_instruction (str): The system instruction to guide the LLM's behavior.
        history (ChatHistory): The chat history containing previous messages.
        
    Yields:
        str: Chunks of the LLM's response as they are generated.
    """
    try:
        messages = [{"role": msg.role, "content": msg.content} for msg in history.messages]
        response = llm_client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": system_instruction},
                *messages
            ],
            stream=True,
            stream_options={"include_usage": True}
        )
        
        for chunk in response:
            if chunk.choices and len(chunk.choices) > 0:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    # Yield string content for Streamlit
                    yield delta.content
                    
            # Log usage information when available (final chunk)
            if chunk.usage:
                logger.info(f"Token usage - Prompt: {chunk.usage.prompt_tokens}, "
                           f"Completion: {chunk.usage.completion_tokens}, "
                           f"Total: {chunk.usage.total_tokens}")
    
    except Exception as e:
        logger.error(f"Error during LLM streaming response: {str(e)}", exc_info=True)
        yield f"\n[Error]: {str(e)}\n"
