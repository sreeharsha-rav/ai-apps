from typing import Any, Dict, List, Optional
from app.core.config import (
    SHOPIFY_CATALOG_CLIENT_ID,
    SHOPIFY_CATALOG_CLIENT_SECRET
)
from app.services.shopify import ShopifyAuth, SHOPIFY_CATALOG_MCP_URL


# -------------------------------------------------------------------------
# Tool Implementations
# -------------------------------------------------------------------------

# TODO: Implement the tools

# -------------------------------------------------------------------------
# Tool Execution
# -------------------------------------------------------------------------

# TODO: Execute Tools

# -------------------------------------------------------------------------
# Tool Definitions
# -------------------------------------------------------------------------

shopify_auth = ShopifyAuth(
    client_id=SHOPIFY_CATALOG_CLIENT_ID,
    client_secret=SHOPIFY_CATALOG_CLIENT_SECRET,
)

def get_tool_definitions(shopify_access_token: Optional[str] = None, checkout_enabled: Optional[bool] = False) -> List[Dict[str, Any]]:
    """
    Returns the list of tool definitions for the OpenAI model.
    """
    tools = []
    
    if shopify_access_token:
        tools.append({
            "type": "mcp",
            "server_label": "shopify-catalog-mcp",
            "server_url": SHOPIFY_CATALOG_MCP_URL,
            "headers": {
                "Authorization": f"Bearer {shopify_access_token}"
            },
            "require_approval": "never",
            "allowed_tools": ["search_global_products", "get_global_product_details"],
        })
    
    # Checkout Tools
    if checkout_enabled:
        tools.append({
            "type": "function",
            "name": "create_checkout_session",
            "description": "[STEP 1] Initialize a new checkout session. ONLY call this when the user EXPLICITLY expresses intent to purchase (e.g., 'I want to buy', 'Add to cart'). PREREQUISITE: You must have product variant ID(s) from search results. Returns a session_id that you MUST store and use for all subsequent checkout operations. DO NOT call this multiple times for the same purchase.",
            "parameters": {
                "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "description": "Array of items to add to the checkout session.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string", "description": "The unique identifier of the product (specifically the variant ID if available, or product ID)."},
                            "quantity": {"type": "integer", "description": "Quantity of the item to purchase."},
                            "title": {"type": "string", "description": "The title of the product or variant."},
                            "image_url": {"type": "string", "description": "The URL of the product image."}
                        },
                        "required": ["id", "quantity"]
                    }
                }
            },
            "required": ["items"]
        }
        })

        tools.append({
            "type": "function",
            "name": "get_checkout_session",
            "description": "[OPTIONAL] Retrieve an EXISTING checkout session. PREREQUISITE: You must have a valid session_id from a previous create_checkout_session call. DO NOT call this if you haven't created a session yet. Use this only to verify the current state of an active session.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "The ID of the checkout session to retrieve."}
                },
                "required": ["session_id"]
            }
        })

        tools.append({
            "type": "function",
            "name": "update_checkout_session",
            "description": "[STEP 2-3] Update an EXISTING checkout session with buyer information, shipping address, or shipping option selection. PREREQUISITE: You MUST have a valid session_id from create_checkout_session. Call this ONLY when the user provides new information (name, email, address, or selects shipping). DO NOT call this before creating a session or repeatedly with the same data.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "The ID of the checkout session to update."},
                    "buyer": {
                        "type": "object",
                        "description": "Buyer's personal information.",
                        "properties": {
                            "first_name": {"type": "string"},
                            "last_name": {"type": "string"},
                            "email": {"type": "string"}
                        }
                    },
                    "fulfillment_address": {
                        "type": "object",
                        "description": "Shipping address for the order. Providing this will generate fulfillment options.",
                        "properties": {
                            "name": {"type": "string"},
                            "line_one": {"type": "string"},
                            "city": {"type": "string"},
                            "state": {"type": "string"},
                            "postal_code": {"type": "string"},
                            "country": {"type": "string"}
                        }
                    },
                    "fulfillment_option_id": {"type": "string", "description": "The ID of the selected fulfillment option (e.g., 'ship_std')."}
                },
                "required": ["session_id"]
            }
        })

        tools.append({
            "type": "function",
            "name": "complete_checkout_session",
            "description": "[STEP 4 - FINAL] Complete and finalize the checkout. PREREQUISITES: (1) Valid session_id, (2) Session status must be 'ready_for_payment' (buyer info, address, and shipping option all set), (3) User has confirmed they want to complete the purchase. DO NOT call this before all information is collected.",
            "parameters": {
                "type": "object",
                "properties": {
                    "session_id": {"type": "string", "description": "The ID of the checkout session to complete."},
                    "payment_token": {"type": "string", "description": "A token representing the payment method (mock value)."}
                },
                "required": ["session_id", "payment_token"]
            }
        })
    
    return tools
