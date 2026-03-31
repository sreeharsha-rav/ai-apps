from typing import Dict, Any, Generator
from openai import OpenAI
from openai.types.responses import (
    Response,
    ResponseCreatedEvent,
    ResponseReasoningSummaryPartAddedEvent,
    ResponseReasoningSummaryPartDoneEvent,
    ResponseReasoningTextDeltaEvent,
    ResponseReasoningTextDoneEvent,
    ResponseWebSearchCallInProgressEvent,
    ResponseWebSearchCallCompletedEvent,
    ResponseFunctionCallArgumentsDoneEvent,
    ResponseOutputItemAddedEvent,
    ResponseOutputItemDoneEvent,
    ResponseMcpListToolsCompletedEvent,
    ResponseMcpListToolsFailedEvent,
    ResponseMcpCallArgumentsDoneEvent,
    ResponseMcpCallCompletedEvent,
    ResponseMcpCallFailedEvent,
    ResponseTextDeltaEvent, 
    ResponseCompletedEvent,
    ResponseFailedEvent,
    ResponseErrorEvent,
)
from app.config.settings import OPENAI_API_KEY
from app.config.utils import logger
from app.notion_auth.storage import load_tokens
import time


class BaseQueryHandler:
    """Base class for LLM query handlers."""

    def __init__(self, system_instruction: str):
        self.system_instruction = system_instruction
    
    # def get_completion(self, history: list[dict]) -> str:
    #     """Get a completion from the LLM."""
    #     raise NotImplementedError
    
    def get_streaming_response(self, history: list[dict]) -> Generator[str, None, None]:
        """Get a streaming response from the LLM."""
        raise NotImplementedError


class OpenAIQueryHandler(BaseQueryHandler):
    """Handler for OpenAI LLM queries with Shopify MCP support."""
    
    def __init__(self, system_instruction: str):
        """Initialize the OpenAI client and Shopify Auth."""
        super().__init__(system_instruction)
        self.openai_client = OpenAI(
            api_key=OPENAI_API_KEY
        )
        self.model = "gpt-5-mini"

    def _build_tools(self) -> list[Dict[str, Any]]:
        """
        Build tools config dynamically so the Bearer token is always fresh.
        """
        tokens = load_tokens()
        if not tokens or not tokens.access_token:
            raise ValueError("Notion authentication required. Please type 'notion-login' to authenticate.")
            
        token_age_ms = int(time.time() * 1000) - tokens.updated_at
        expires_in_ms = (tokens.expires_in or 3600) * 1000
        remaining_seconds = (expires_in_ms - token_age_ms) // 1000
        
        if remaining_seconds <= 0:
            raise ValueError("Notion token expired. Please type 'notion-refresh' or 'notion-login' to re-authenticate.")

        NOTION_ACCESS_TOKEN = tokens.access_token
        
        try:
            return [
                {
                    "type": "mcp",
                    "server_label": "notion-mcp",
                    "server_description": "A Notion MCP server to assist with notion tasks.",
                    "server_url": "https://mcp.notion.com/mcp",
                    "headers": {
                        "Authorization": f"Bearer {NOTION_ACCESS_TOKEN}",
                    },
                    "require_approval": "never",
                }
            ]
        except Exception as e:
            logger.error(f"Failed to build tools: {e}")
            return []
        
    def get_streaming_response(self, history: list[dict]) -> Generator[Any, None, None]:
        """Get a streaming response from OpenAI."""
        try:
            tools = self._build_tools()
            
            response_stream = self.openai_client.responses.create(
                model=self.model,
                instructions=self.system_instruction,
                input=history,
                tools=tools,
                stream=True,
                store=False
            )
            for event in response_stream:
                # Log events for debugging (optional, keeping previous logs)
                if isinstance(event, ResponseCreatedEvent):
                    logger.debug(f"--- Response created (ID: {event.response.id}) ---")
                elif isinstance(event, ResponseOutputItemAddedEvent):
                    logger.debug(f"[{event.output_index}] - {event.type} - Output item added:\n {event.item.type}")
                

                # Reasoning Events - TODO: Handle reasoning events by storing them in the history
                # elif isinstance(event, ResponseReasoningSummaryPartAddedEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning summary part added")
                # elif isinstance(event, ResponseReasoningSummaryPartDoneEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning summary part done")
                # # elif isinstance(event, ResponseReasoningTextDeltaEvent):
                # #     logger.debug(f"[{event.output_index}] Reasoning text delta: {event.delta}")
                # elif isinstance(event, ResponseReasoningTextDoneEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning text done - {event.reasoning_text}")

                # FUTURE: Web Search Events
                # elif isinstance(event, ResponseWebSearchCallInProgressEvent):
                #     logger.debug(f"[{event.output_index}] Web search in progress...")
                # elif isinstance(event, ResponseWebSearchCallCompletedEvent):
                #     logger.info(f"[{event.output_index}] Web search completed")

                # Function Call Events
                elif isinstance(event, ResponseFunctionCallArgumentsDoneEvent):
                    logger.info(f"[{event.output_index}] - {event.type} - Function call arguments generated:\n {event.arguments}")
                
                # MCP Events
                elif isinstance(event, ResponseMcpListToolsCompletedEvent):
                    logger.debug(f"[{event.output_index}] - {event.type} - MCP tools listed")
                elif isinstance(event, ResponseMcpListToolsFailedEvent):
                    logger.error(f"[{event.output_index}] - {event.type} - MCP tool listing failed")
                elif isinstance(event, ResponseMcpCallArgumentsDoneEvent):
                    logger.info(f"[{event.output_index}] - {event.type} - MCP tool called, Arguments:\n {event.arguments}")
                elif isinstance(event, ResponseMcpCallCompletedEvent):
                    logger.info(f"[{event.output_index}] - {event.type} - MCP call completed")
                elif isinstance(event, ResponseMcpCallFailedEvent):
                    logger.error(f"[{event.output_index}] - {event.type} - MCP call failed")

                # Response Events
                elif isinstance(event, ResponseOutputItemDoneEvent):
                    logger.debug(f"[{event.output_index}] - {event.type} - Output item done: {event.item.type}")
                elif isinstance(event, ResponseCompletedEvent):
                    logger.debug(f" --- {event.type} - {event.response.usage} ---")
                elif isinstance(event, ResponseFailedEvent):
                    logger.error(f" --- {event.type} - {event.response.error} ---")
                elif isinstance(event, ResponseErrorEvent):
                    logger.error(f" --- {event.type} - {event.code} - {event.message} ---")

                yield event
                    
        except Exception as e:
            logger.error(f"Error getting streaming response: {e}")
            raise e
