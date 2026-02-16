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
