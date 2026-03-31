import os
from dotenv import load_dotenv


load_dotenv()

if not (OPENAI_API_KEY := os.getenv("OPENAI_API_KEY")):
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")

# Notion OAuth Configuration
NOTION_MCP_SERVER_URL = os.getenv("NOTION_MCP_SERVER_URL", "https://mcp.notion.com")
NOTION_CALLBACK_PORT = int(os.getenv("NOTION_CALLBACK_PORT", "3456"))
NOTION_CALLBACK_URI = os.getenv("NOTION_CALLBACK_URI", f"http://localhost:{NOTION_CALLBACK_PORT}/callback")
NOTION_TOKEN_STORAGE_FILE = os.getenv("NOTION_TOKEN_STORAGE_FILE", ".notion-tokens.json")
NOTION_OAUTH_CLIENT_NAME = os.getenv("NOTION_OAUTH_CLIENT_NAME", "notion-oauth Agentic Journal Client")
NOTION_OAUTH_CLIENT_URI = os.getenv("NOTION_OAUTH_CLIENT_URI", "https://github.com/sreeharsha-rav/ai-apps/notion-ai-journal")

# Shopify Auth Configuration
SHOPIFY_CLIENT_ID = os.getenv("SHOPIFY_CLIENT_ID")
SHOPIFY_CLIENT_SECRET = os.getenv("SHOPIFY_CLIENT_SECRET")
SHOPIFY_TOKEN_URL = os.getenv("SHOPIFY_TOKEN_URL", "https://api.shopify.com/auth/access_token")
SHOPIFY_TOKEN_STORAGE_FILE = os.getenv("SHOPIFY_TOKEN_STORAGE_FILE", ".shopify-tokens.json")
SHOPIFY_CATALOG_MCP_URL = os.getenv("SHOPIFY_CATALOG_MCP_URL", "https://discover.shopifyapps.com/global/mcp")
SHOPIFY_USER_AGENT = os.getenv("SHOPIFY_USER_AGENT", "Terminal Chat")
