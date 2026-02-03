from dataclasses import dataclass
from typing import AsyncGenerator, List, Dict, Optional, Any
import json
from datetime import datetime, timedelta
from ulid import ULID
from fastapi import HTTPException
import httpx
from openai import AsyncOpenAI
from openai.types.responses import (
    ResponseCreatedEvent,
    ResponseTextDeltaEvent,
    ResponseMcpListToolsInProgressEvent,
    ResponseMcpListToolsCompletedEvent,
    ResponseMcpListToolsFailedEvent,
    ResponseMcpCallArgumentsDeltaEvent,
    ResponseMcpCallArgumentsDoneEvent,
    ResponseMcpCallInProgressEvent,
    ResponseMcpCallCompletedEvent,
    ResponseMcpCallFailedEvent,
    ResponseErrorEvent, 
    ResponseOutputItemAddedEvent,
    ResponseOutputItemDoneEvent,
    ResponseCompletedEvent,
    ResponseFailedEvent
)

from config.settings import SHOPIFY_CATALOG_CLIENT_ID, SHOPIFY_CATALOG_CLIENT_SECRET
from config.loggers import logger
from .prompt import CURRENT_SYSTEM_PROMPT
from .models import ChatRequest, Item, CanvasData, ChatHistory
from .storage import ChatStore

# --------------------
# Helper Functions
# --------------------

def _format_sse(event_type: str, data: any, event_id: str = None) -> str:
    """Formats data as a Server-Sent Event (SSE) string."""
    if event_id is None:
        event_id = str(ULID())
    
    # Ensure data is a JSON string
    if not isinstance(data, str):
        data = json.dumps(data)
    
    # SSE format:
    # id: <id>\n
    # event: <event_type>\n
    # data: <data>\n\n
    return f"id: {event_id}\nevent: {event_type}\ndata: {data}\n\n"

# ---------------------
# Shopify Auth
# ---------------------

SHOPIFY_TOKEN_URL = "https://api.shopify.com/auth/authorize"
SHOPIFY_CATALOG_MCP_URL="https://discover.shopifyapps.com/global/mcp"
# SHOPIFY_CHECKOUT_MCP_URL="https://{shop-domain}/api/ucp/mcp"

@dataclass
class ShopifyAccessToken:
    token: str
    expires_at: datetime

class ShopifyAuth:
    """Fetches and caches Shopify access token (JWT)"""

    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._cached: Optional[ShopifyAccessToken] = None
    
    async def _request_new_token(self) -> ShopifyAccessToken:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    SHOPIFY_TOKEN_URL,
                    headers={
                        "Content-Type": "application/json",
                        "User-Agent": "acp-llm-chat"
                    },
                    json={
                        "client_id": self.client_id,
                        "client_secret": self.client_secret,
                        "grant_type": "client_credentials"
                    }
                )
                response.raise_for_status()

                if response.status_code != 200:
                    logger.error(f"Failed to fetch access token: {response.text}")
                    raise HTTPException(status_code=response.status_code, detail=response.text)
                
                data = response.json()

                access_token = data.get("access_token")
                expires_in = data.get("expires_in", 2 * 60 * 60)

                if not access_token:
                    logger.error("Failed to fetch access token: Invalid response")
                    raise RuntimeError("Failed to fetch access token: Invalid response")
                
                return ShopifyAccessToken(
                    token=access_token,
                    expires_at=datetime.now() + timedelta(seconds=expires_in)
                )

        except Exception as e:
            logger.error(f"Failed to fetch access token: {e}")
            raise e

    async def get_valid_token(self) -> str:
        if not self._cached or datetime.now() > self._cached.expires_at:
            self._cached = await self._request_new_token()
        return self._cached.token
    
# ---------------------
# Main Service Class
# ---------------------
class ChatService:
    def __init__(self, storage: ChatStore, openai_client: AsyncOpenAI):
        self.storage = storage
        self.client = openai_client

        if SHOPIFY_CATALOG_CLIENT_ID and SHOPIFY_CATALOG_CLIENT_SECRET:
            self.shopify_auth = ShopifyAuth(SHOPIFY_CATALOG_CLIENT_ID, SHOPIFY_CATALOG_CLIENT_SECRET)
        else:
            self.shopify_auth = None
            logger.warning("Shopify authentication not configured. Shopify catalog, checkout features will not be available.")

    def _build_tools(self) -> List[Dict[str, Any]]:
        tools = []
        if self.shopify_auth:
            shopify_tools = [
                {
                    "type": "mcp",
                    "server_label": "shopify-catalog-mcp",
                    "server_url": SHOPIFY_CATALOG_MCP_URL,
                    "headers": {
                        "Authorization": "Bearer {access_token}"
                    },
                    "require_approval": "never",
                    "allowed_tools": ["search_global_products", "get_global_product_details"]
                }
                # },
                # {
                #     "type": "mcp",
                #     "server_label": "shopify-checkout-mcp",
                #     "server_url": SHOPIFY_CHECKOUT_MCP_URL,             # TODO: add shop domain dynamically
                #     "headers": {
                #         "Authorization": "Bearer {access_token}"
                #     },
                #     "require_approval": "never",        # FUTURE: Add approval
                #     "allowed_tools": ["create_checkout", "get_checkout", "update_checkout", "complete_checkout", "cancel_checkout", "get_order"]
                # }
            ]
            tools.extend(shopify_tools)
        return tools

    async def get_all_chats(self) -> List[ChatHistory]:
        try:
            return self.storage.get_all_chats()
        except Exception as e:
            logger.error(f"Failed to fetch history: {e}")
            raise HTTPException(status_code=500, detail="Internal server error while fetching history")

    async def get_chat(self, chat_id: str) -> ChatHistory:
        try:
            chat = self.storage.backend.load_chat(chat_id)
            if not chat:
                raise HTTPException(status_code=404, detail=f"Chat {chat_id} not found")
            return chat
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Failed to fetch chat {chat_id}: {e}")
            raise HTTPException(status_code=500, detail="Internal server error")

    async def clear_all_chats(self) -> Dict[str, str]:
        try:
            self.storage.clear()
            return {"message": "All history cleared"}
        except Exception as e:
            logger.error(f"Failed to clear history: {e}")
            raise HTTPException(status_code=500, detail="Failed to clear history")

    async def delete_chat(self, chat_id: str) -> Dict[str, str]:
        try:
            self.storage.delete_chat(chat_id)
            return {"message": f"Chat {chat_id} deleted"}
        except Exception as e:
            logger.error(f"Failed to delete chat {chat_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to delete chat")

    async def create_chat(self) -> ChatHistory:
        try:
            chat = self.storage.get_or_create_chat()
            return chat
        except Exception as e:
            logger.error(f"Failed to create chat: {e}")
            raise HTTPException(status_code=500, detail="Failed to create chat")

    async def update_chat_title(self, chat_id: str, title: str) -> ChatHistory:
        if not title:
            raise HTTPException(status_code=400, detail="Title is required")
        
        try:
            updated_chat = self.storage.update_chat_title(chat_id, title)
            if not updated_chat:
                raise HTTPException(status_code=404, detail="Chat not found")
            return updated_chat
        except Exception as e:
            logger.error(f"Failed to update title for chat {chat_id}: {e}")
            raise HTTPException(status_code=500, detail="Failed to update title")

    async def stream_chat(self, request: ChatRequest) -> AsyncGenerator[str, None]:
        logger.info(f"Chat stream request received for chat_id: {request.chat_id}")
        
        try:
            # Get or create chat session
            chat_id = request.chat_id
            chat = self.storage.get_or_create_chat(chat_id)
            chat_id = chat.id

            # Save prompt as user message
            user_message = Item(
                data={
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": request.prompt
                        }
                    ],
                    "type": "message"
                }
            )
            self.storage.save_item(chat_id, user_message)

            # Auto-generate title if it's the first message
            if len(chat.items) == 0:  # It was empty before we saved the first message
                new_title = request.prompt[:40].strip() + ("..." if len(request.prompt) > 40 else "")
                self.storage.update_chat_title(chat_id, new_title)

        except Exception as e:
            logger.error(f"Storage error before streaming: {e}")
            # Proceeding to try and get AI response at least

        total_tokens = 0
        
        try:
            history_input = []
            for item in chat.items:
                history_input.append(item.data)
            history_input.append(user_message.data)

            kwargs = {
                "model": "gpt-5-mini",
                "instructions": CURRENT_SYSTEM_PROMPT,
                "input": history_input,
                "stream": True,
                "store": False
            }

            tools = self._build_tools()
            if tools:
                logger.debug(f"Adding tools to kwargs: {tools}")
                kwargs["tools"] = tools
            
            response_stream = await self.client.responses.create(**kwargs)
            
            async for event in response_stream:
                if isinstance(event, ResponseCreatedEvent):
                    logger.debug(f"{event.type}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())

                # Output Item Added events
                elif isinstance(event, ResponseOutputItemAddedEvent):
                    logger.debug(f"{event.type}: index {event.output_index} - item={event.item.type}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())

                # MCP events
                elif isinstance(event, ResponseMcpListToolsInProgressEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                elif isinstance(event, ResponseMcpListToolsCompletedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                elif isinstance(event, ResponseMcpListToolsFailedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())

                elif isinstance(event, ResponseMcpCallArgumentsDoneEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())

                elif isinstance(event, ResponseMcpCallInProgressEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                elif isinstance(event, ResponseMcpCallCompletedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                elif isinstance(event, ResponseMcpCallFailedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                
                # Text Delta events
                elif isinstance(event, ResponseTextDeltaEvent):
                    logger.debug(f"{event.type}[{event.output_index}] seq_idx={event.sequence_number} content_idx={event.content_index}")
                    text_data = {
                        "type": "message",
                        "role": "assistant",
                        "content": [
                            {
                                "type": "output_text",
                                "text": event.delta
                            }
                        ]
                    }
                    yield _format_sse(event_type=event.type, data=text_data)
                
                # Output Item Done events
                elif isinstance(event, ResponseOutputItemDoneEvent):
                    logger.debug(f"{event.type}: index {event.output_index} - item={event.item.type}")
                    item_event = event.item
                    
                    # MCP items
                    if item_event.type == "mcp_list_tools":
                        storage_item = Item(data=item_event.model_dump(exclude=["id"]))
                        self.storage.save_item(chat_id, storage_item)
                    elif item_event.type == "mcp_call":
                        storage_item = Item(data=item_event.model_dump(exclude=["id"]))
                        self.storage.save_item(chat_id, storage_item)
                    
                    # Message items
                    elif item_event.type == "message":
                        storage_item = Item(data=item_event.model_dump(exclude=["id"]))
                        self.storage.save_item(chat_id, storage_item)

                    yield _format_sse(event_type=event.type, data=event.model_dump())
                
                # Completion events
                elif isinstance(event, ResponseCompletedEvent):
                    total_tokens = event.response.usage.total_tokens
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                    logger.info(f"Stream completed. Total tokens: {total_tokens}")
                
                # Error events
                elif isinstance(event, ResponseErrorEvent):
                    yield _format_sse(event_type=event.type, data=event.model_dump())
                
                # Failed events
                elif isinstance(event, ResponseFailedEvent):
                    yield _format_sse(event_type=event.type, data=event.model_dump())

            # TODO: update canvas content with MCP call results, web results, tool results etc..
            test_canvas = CanvasData(
                content="# Hello Canvas\n\nThis is a **test** content sent from the server.\n\n- Item 1\n- Item 2\n\n```python\nprint('Hello World')\n```",
                language="markdown"
            )
            self.storage.update_chat_canvas(chat_id, test_canvas)

        except GeneratorExit:
            logger.warning(f"Stream interrupted (client disconnected or server shutdown) for chat {chat_id}")
            raise

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"OpenAI Stream Error [{error_type}]: {str(e)}")
            
            # Map errors to user friendly messages
            error_msg = "Error: Internal server error."
            if "api_key" in str(e).lower():
                error_msg = "Error: Invalid OpenAI API Key."
            elif "rate_limit" in str(e).lower():
                error_msg = "Error: Rate limit exceeded. Please try again later."
            elif "insufficient_quota" in str(e).lower():
                error_msg = "Error: OpenAI quota exceeded."
            elif "model_not_found" in str(e).lower():
                error_msg = f"Error: Model '{request.model}' not found or no access."
            
            error_payload = f"\n\n🚨 **{error_msg}**\n\n*Details: {str(e)}*"
            yield _format_sse("error", error_payload)
            
        finally:
            # update total tokens
            self.storage.update_chat_tokens(chat_id, total_tokens)
