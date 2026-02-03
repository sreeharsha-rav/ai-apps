SHOPIFY_CATALOG_MCP_URL="https://discover.shopifyapps.com/global/mcp"
SHOPIFY_CHECKOUT_MCP_URL="https://{shop-domain}/api/ucp/mcp"

tools = [
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