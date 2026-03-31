from typing import Callable, Dict
from rich.console import Console
from app.notion_auth.cli import (
    handle_login,
    handle_status,
    handle_logout,
    handle_refresh
)
from app.shopify_auth.cli import (
    handle_login as shopify_handle_login,
    handle_status as shopify_handle_status,
    handle_logout as shopify_handle_logout,
    handle_refresh as shopify_handle_refresh
)

# Command Registry
# Maps command strings to handler functions that accept a Console object
COMMANDS: Dict[str, Callable[[Console], None]] = {
    "notion-login": handle_login,
    "notion-status": handle_status,
    "notion-logout": handle_logout,
    "notion-refresh": handle_refresh,
    "shopify-login": shopify_handle_login,
    "shopify-status": shopify_handle_status,
    "shopify-logout": shopify_handle_logout,
    "shopify-refresh": shopify_handle_refresh,
}
