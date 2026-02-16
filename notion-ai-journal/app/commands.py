from typing import Callable, Dict
from rich.console import Console
from app.notion_auth.cli import (
    handle_login,
    handle_status,
    handle_logout,
    handle_refresh
)

# Command Registry
# Maps command strings to handler functions that accept a Console object
COMMANDS: Dict[str, Callable[[Console], None]] = {
    "notion-login": handle_login,
    "notion-status": handle_status,
    "notion-logout": handle_logout,
    "notion-refresh": handle_refresh,
}
