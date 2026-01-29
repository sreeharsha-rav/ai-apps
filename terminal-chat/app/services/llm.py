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
from app.core.config import (
    OPENAI_API_KEY, 
    AZURE_OPENAI_KEY, 
    AZURE_OPENAI_ENDPOINT, 
    AZURE_OPENAI_DEPLOYMENT, 
    SHOPIFY_CATALOG_CLIENT_ID,
    SHOPIFY_CATALOG_CLIENT_SECRET
)
from app.core.utils import logger
from app.services.shopify import ShopifyCatalogAuth, SHOPIFY_CATALOG_MCP_URL


class BaseQueryHandler:
    """Base class for LLM query handlers."""
    
    def get_completion(self, system_instruction: str, history: list[dict]) -> str:
        """Get a completion from the LLM."""
        raise NotImplementedError
    
    def get_streaming_response(self, system_instruction: str, history: list[dict]) -> Generator[str, None, None]:
        """Get a streaming response from the LLM."""
        raise NotImplementedError

class AzureOpenAIQueryHandler(BaseQueryHandler):
    """Handler for Azure OpenAI LLM queries."""
    
    def __init__(self):
        """Initialize the Azure OpenAI client."""
        self.openai_client = OpenAI(
            base_url=AZURE_OPENAI_ENDPOINT,
            api_key=AZURE_OPENAI_KEY
        )
        self.model = AZURE_OPENAI_DEPLOYMENT
        
    def get_completion(self, system_instruction: str, history: list[dict]) -> str:
        """Get a completion from OpenAI."""
        try:
            response: Response = self.openai_client.responses.create(
                model=self.model,
                instructions=system_instruction,
                input=history,
                store=False
            )
            if response.usage:
                logger.debug(f"Token usage: {response.usage}")
            return response.output_text
        except Exception as e:
            logger.error(f"Error getting completion: {e}")
            return "Error: Unable to get response from OpenAI."
        
    def get_streaming_response(self, system_instruction: str, history: list[dict]) -> Generator[str, None, None]:
        """Get a streaming response from OpenAI."""
        try:
            response_stream = self.openai_client.responses.create(
                model=self.model,
                instructions=system_instruction,
                input=history,
                reasoning={"effort": "minimal"},
                stream=True,
                store=False
            )
            for event in response_stream:
                if isinstance(event, ResponseTextDeltaEvent):
                    yield event.delta
        except Exception as e:
            logger.error(f"Error getting streaming response: {e}")
            yield "Error: Unable to get response from OpenAI."


class OpenAIQueryHandler(BaseQueryHandler):
    """Handler for OpenAI LLM queries with Shopify MCP support."""
    
    def __init__(self):
        """Initialize the OpenAI client and Shopify Auth."""
        self.openai_client = OpenAI(
            api_key=OPENAI_API_KEY
        )
        self.model = "gpt-5-mini"
        
        # Shopify token manager
        self.shopify_auth = ShopifyCatalogAuth(
            client_id=SHOPIFY_CATALOG_CLIENT_ID,
            client_secret=SHOPIFY_CATALOG_CLIENT_SECRET,
        )

    def _build_tools(self) -> list[Dict[str, Any]]:
        """
        Build tools config dynamically so the Bearer token is always fresh.
        """
        try:
            shopify_access_token = self.shopify_auth.get_valid_token()
            shopify_access_token = shopify_access_token.replace('"', '')

            return [
                {
                    "type": "mcp",
                    "server_label": "shopify-catalog-mcp",
                    "server_url": SHOPIFY_CATALOG_MCP_URL,
                    "headers": {
                        "Authorization": f"Bearer {shopify_access_token}"
                    },
                    "require_approval": "never",
                    "allowed_tools": ["search_global_products"],
                },
            ]
        except Exception as e:
            logger.error(f"Failed to build tools: {e}")
            return []
        
    def get_streaming_response(self, system_instruction: str, history: list[dict]) -> Generator[Any, None, None]:
        """Get a streaming response from OpenAI."""
        try:
            tools = self._build_tools()
            
            response_stream = self.openai_client.responses.create(
                model=self.model,
                instructions=system_instruction,
                input=history,
                tools=tools,
                tool_choice="auto",
                stream=True,
                store=False
            )
            for event in response_stream:
                # Log events for debugging (optional, keeping previous logs)
                if isinstance(event, ResponseCreatedEvent):
                    logger.debug(f"Response created (ID: {event.response.id})")

                # Reasoning Events - TODO: Handle reasoning events by storing them in the history
                # elif isinstance(event, ResponseReasoningSummaryPartAddedEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning summary part added")
                # elif isinstance(event, ResponseReasoningSummaryPartDoneEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning summary part done")
                # # elif isinstance(event, ResponseReasoningTextDeltaEvent):
                # #     logger.debug(f"[{event.output_index}] Reasoning text delta: {event.delta}")
                # elif isinstance(event, ResponseReasoningTextDoneEvent):
                #     logger.debug(f"[{event.output_index}] Reasoning text done - {event.reasoning_text}")

                # Web Search Events
                elif isinstance(event, ResponseWebSearchCallInProgressEvent):
                    logger.debug(f"[{event.output_index}] Web search in progress...")
                elif isinstance(event, ResponseWebSearchCallCompletedEvent):
                    logger.info(f"[{event.output_index}] Web search completed")
                
                # MCP Events
                elif isinstance(event, ResponseMcpListToolsCompletedEvent):
                    logger.debug(f"[{event.output_index}] MCP tools listed")
                elif isinstance(event, ResponseMcpListToolsFailedEvent):
                    logger.error(f"[{event.output_index}] MCP tool listing failed")
                elif isinstance(event, ResponseMcpCallArgumentsDoneEvent):
                    logger.info(f"[{event.output_index}] MCP tool called: {event.arguments}")
                elif isinstance(event, ResponseMcpCallCompletedEvent):
                    logger.info(f"[{event.output_index}] MCP call completed")
                elif isinstance(event, ResponseMcpCallFailedEvent):
                    logger.error(f"[{event.output_index}] MCP call failed")

                # Response Events
                elif isinstance(event, ResponseOutputItemAddedEvent):
                    logger.debug(f"[{event.output_index}] Output item added: {event.item.type}")
                elif isinstance(event, ResponseOutputItemDoneEvent):
                    logger.debug(f"[{event.output_index}] Output item done: {event.item.type}")
                elif isinstance(event, ResponseCompletedEvent):
                    logger.debug(f"Response completed. Usage: {event.response.usage}")
                elif isinstance(event, ResponseFailedEvent):
                    logger.error(f"Response failed: {event.response.error}")
                elif isinstance(event, ResponseErrorEvent):
                    logger.error(f"Error event - Code: {event.code}, Message: {event.message}")

                yield event
                    
        except Exception as e:
            logger.error(f"Error getting streaming response: {e}")
            # Yield nothing or raise error depending on desired behavior.
            # Here we just log and stop.
