from dataclasses import dataclass
from typing import AsyncGenerator, List, Dict, Optional, Any
from datetime import datetime, timedelta
from ulid import ULID
from fastapi import HTTPException
import httpx
import json
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
    ResponseFailedEvent,
    ResponseReasoningTextDeltaEvent
)
import traceback

from config.settings import AZURE_OPENAI_DEPLOYMENT, SHOPIFY_CATALOG_CLIENT_ID, SHOPIFY_CATALOG_CLIENT_SECRET
from config.loggers import logger
from .prompt import CURRENT_SYSTEM_PROMPT
from .models import ChatRequest, Item, CanvasData, ChatHistory, CanvasItem
from .storage import ChatStore

# --------------------
# Helper Functions
# --------------------

def _format_sse(event_type: str, data: any, event_id: str = None) -> str:
    """Formats data as a Server-Sent Event (SSE) string."""
    if event_id is None:
        event_id = str(ULID())
    
    # Pre-process data to handle Pydantic serialization issues
    try:
        if hasattr(data, "type") and data.type == "mcp_call" and hasattr(data, "error"):
            # McpCall error field expects str but sometimes gets dict from backend
            if data.error and not isinstance(data.error, str):
                import json
                try:
                     # If it's a dict or other object, stringify it to satisfy Pydantic schema
                    if isinstance(data.error, dict):
                         data.error = json.dumps(data.error)
                    else:
                         data.error = str(data.error)
                except Exception:
                    data.error = str(data.error)
    except Exception as e:
        logger.warning(f"Failed to normalize MCP error field: {e}")

    # SSE format:
    # id: <id>\n
    # event: <event_type>\n
    # data: <data>\n\n
    return f"id: {event_id}\nevent: {event_type}\ndata: {data}\n\n"

# ---------------------
# Shopify Auth
# ---------------------

SHOPIFY_TOKEN_URL = "https://api.shopify.com/auth/access_token"
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
            logger.error(f"Failed to fetch access token: {e}", exc_info=True)
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

    async def _build_tools(self) -> List[Dict[str, Any]]:
        tools = []
        if self.shopify_auth:
            access_token = await self.shopify_auth.get_valid_token()
            shopify_tools = [
                {
                    "type": "mcp",
                    "server_label": "shopify-catalog-mcp",
                    "server_url": SHOPIFY_CATALOG_MCP_URL,
                    "headers": {
                        "Authorization": f"Bearer {access_token}"
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
            logger.error(f"Failed to fetch history: {e}", exc_info=True)
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
            logger.error(f"Failed to fetch chat {chat_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Internal server error")

    async def clear_all_chats(self) -> Dict[str, str]:
        try:
            self.storage.clear()
            return {"message": "All history cleared"}
        except Exception as e:
            logger.error(f"Failed to clear history: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to clear history")

    async def delete_chat(self, chat_id: str) -> Dict[str, str]:
        try:
            self.storage.delete_chat(chat_id)
            return {"message": f"Chat {chat_id} deleted"}
        except Exception as e:
            logger.error(f"Failed to delete chat {chat_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to delete chat")

    async def create_chat(self) -> ChatHistory:
        try:
            chat = self.storage.get_or_create_chat()
            return chat
        except Exception as e:
            logger.error(f"Failed to create chat: {e}", exc_info=True)
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
            logger.error(f"Failed to update title for chat {chat_id}: {e}", exc_info=True)
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
            logger.error(f"Storage error before streaming: {e}", exc_info=True)
            # Proceeding to try and get AI response at least

        total_tokens = 0
        
        try:
            history_input = []
            for item in chat.items:
                history_input.append(item.data)

            # inject context about product with id extracted UPID, title, variant["shop"]["id"], variant["shop"]["name"], variant["shop"]["onlineStoreUrl"]
            context = ""
            if chat.canvas and chat.canvas.items:
                products = ""
                for canvas_item in chat.canvas.items:
                    if canvas_item.type == "product_list":
                        product_list = canvas_item.content
                        for product in product_list:
                            product_upid = product.get("id", "").split("/")[-1] if product.get("id") else "unknown"
                            product_title = product.get("title", "Unknown Product")
                            
                            # Shop info is in variants, not at product level
                            variants = product.get("variants", [])
                            if variants and len(variants) > 0:
                                first_variant = variants[0]
                                shop = first_variant.get("shop", {})
                                product_shop_name = shop.get("name", "Unknown Shop")
                                product_shop_domain = shop.get("onlineStoreUrl", "")
                            else:
                                product_shop_name = "Unknown Shop"
                                product_shop_domain = ""
                            
                            products += f"<product id=\"{product.get('id', '')}\"><upid>{product_upid}</upid><title>{product_title}</title><shop_name>{product_shop_name}</shop_name><shop_domain>{product_shop_domain}</shop_domain></product>"
                context = f"<products_context>{products}</products_context>"
            logger.debug(f"\n-- Plugging in context --\n{context}\n-- End of context --\n")

            user_message.data["content"][0]["text"] = user_message.data["content"][0]["text"] + "\n\n" + context
            history_input.append(user_message.data)

            kwargs = {
                # "model": AZURE_OPENAI_DEPLOYMENT,
                "model": "gpt-5-mini",
                "instructions": CURRENT_SYSTEM_PROMPT,
                "input": history_input,
                "stream": True,
                "store": False
            }

            tools = await self._build_tools()
            if tools:
                tools_str = ""
                for tool in tools:
                    if tool["type"] == "mcp":
                        tools_str += f"{tool['type']}"
                        tools_str += f": {tool['server_label']}\n"

                logger.debug(f"Adding tools to kwargs:\n{tools_str}")
                kwargs["tools"] = tools
            
            response_stream = await self.client.responses.create(**kwargs)
            
            async for event in response_stream:
                if isinstance(event, ResponseCreatedEvent):
                    logger.debug(f"{event.type}")
                    yield _format_sse(event_type=event.type, data=event)

                # Output Item Added events
                elif isinstance(event, ResponseOutputItemAddedEvent):
                    logger.debug(f"{event.type}: index {event.output_index} - item={event.item.type}")
                    yield _format_sse(event_type=event.type, data=event)

                # MCP events
                elif isinstance(event, ResponseMcpListToolsInProgressEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)
                elif isinstance(event, ResponseMcpListToolsCompletedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)
                elif isinstance(event, ResponseMcpListToolsFailedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)

                elif isinstance(event, ResponseMcpCallArgumentsDoneEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)

                elif isinstance(event, ResponseMcpCallInProgressEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)
                elif isinstance(event, ResponseMcpCallCompletedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)
                elif isinstance(event, ResponseMcpCallFailedEvent):
                    logger.debug(f"{event.type}: index {event.output_index}")
                    yield _format_sse(event_type=event.type, data=event)
                
                # Text Delta events
                elif isinstance(event, ResponseTextDeltaEvent):
                    # logger.debug(f"{event.type}[{event.output_index}] seq_idx={event.sequence_number} content_idx={event.content_index}")
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
                
                # Reasoning Delta events
                elif isinstance(event, ResponseReasoningTextDeltaEvent):
                     reasoning_data = {
                        "type": "reasoning",
                        "index": event.output_index,
                        "delta": event.delta
                     }
                     yield _format_sse(event_type="response.reasoning_text.delta", data=reasoning_data)
                
                # Output Item Done events
                elif isinstance(event, ResponseOutputItemDoneEvent):
                    logger.debug(f"{event.type}: index {event.output_index} - item={event.item.type}")
                    
                    # MCP items
                    if event.item.type == "mcp_list_tools":
                        storage_item = Item(data=event.item.model_dump())
                        self.storage.save_item(chat_id, storage_item)
                    elif event.item.type == "mcp_call":
                        storage_item = Item(data=event.item.model_dump())
                        self.storage.save_item(chat_id, storage_item)

                        # --- CANVAS events ---
                        if event.item.status == "completed" and event.item.output:

                            if chat.canvas:
                                current_items = chat.canvas.items
                            else:
                                current_items = []
                            
                            try:
                                output_data = json.loads(event.item.output)
                                
                                if event.item.name == "search_global_products":
                                    if "offers" in output_data and isinstance(output_data["offers"], list):
                                        logger.debug(f"- adding {event.item.name} results to canvas")
                                        products = output_data["offers"]

                                        # replace existing product list if exists, else append
                                        found = False
                                        for item in current_items:
                                            if item.type == "product_list":
                                                item.content = products
                                                found = True
                                                break
                                        
                                        if not found:
                                            current_items.append(
                                                CanvasItem(
                                                    type="product_list",
                                                    content=products
                                                )
                                            )
                                
                                elif event.item.name == "get_global_product_details":
                                    if output_data and output_data.get("product"):
                                        logger.debug(f"- adding {event.item.name} results to canvas")
                                        product_detail = output_data["product"]

                                        # replace existing product detail if exists, else append
                                        found = False
                                        for item in current_items:
                                            if item.type == "product_detail":
                                                item.content = product_detail
                                                found = True
                                                break
                                        
                                        if not found:
                                            current_items.append(
                                                CanvasItem(
                                                    type="product_detail",
                                                    content=product_detail
                                                )
                                            )
                                
                                canvas_data = CanvasData(items=current_items)
                                self.storage.update_chat_canvas(
                                    chat_id=chat_id,
                                    canvas_data=canvas_data
                                )
                                yield _format_sse("canvas.update", canvas_data.model_dump())
                        
                            except Exception as e:
                                logger.warning(f"Failed to parse MCP output for canvas update: {e} - traceback: {traceback.format_exc()}")
                                error_item = CanvasItem(
                                    type="error",
                                    content={
                                        "message": str(e),
                                        "traceback": traceback.format_exc()
                                    }
                                )
                                current_items.append(error_item)
                                canvas_data = CanvasData(items=current_items)           # FUTURE: optimize canvas data update
                                self.storage.update_chat_canvas(
                                    chat_id=chat_id,
                                    canvas_data=canvas_data
                                )
                                yield _format_sse("canvas.update", canvas_data.model_dump())
                        # ---------------------------
                    
                    # Message items
                    elif event.item.type == "message":
                        storage_item = Item(data=event.item.model_dump())
                        self.storage.save_item(chat_id, storage_item)

                    yield _format_sse(event_type=event.type, data=event.item)
                
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

        except GeneratorExit:
            logger.warning(f"Stream interrupted (client disconnected or server shutdown) for chat {chat_id}")
            raise

        except Exception as e:
            error_type = type(e).__name__
            logger.error(f"OpenAI Stream Error [{error_type}]: {str(e)} - traceback: {traceback.format_exc()}", exc_info=True)
            
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
            self.storage.update_chat_tokens(chat_id, total_tokens)
