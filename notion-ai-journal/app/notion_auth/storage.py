"""Token storage using JSON file."""
import json
from pathlib import Path
from app.utils import logger
from app.notion_auth.models import StoredTokens, TokenResponse
from app.config import NOTION_TOKEN_STORAGE_FILE

STORAGE_FILE = NOTION_TOKEN_STORAGE_FILE


def save_tokens(tokens: TokenResponse, client_id: str | None = None, client_secret: str | None = None) -> None:
    """
    Save tokens to JSON file.
    
    Args:
        tokens: Token response from OAuth server
        client_id: Optional client ID to store for refresh
        client_secret: Optional client secret to store for refresh
    """
    import time
    
    stored_tokens = StoredTokens(
        **tokens.model_dump(),
        client_id=client_id,
        client_secret=client_secret,
        updated_at=int(time.time() * 1000)  # Milliseconds timestamp
    )
    
    storage_path = Path.cwd() / STORAGE_FILE
    storage_path.write_text(stored_tokens.model_dump_json(indent=2))
    
    logger.info(f"Saved tokens to {storage_path}")


def load_tokens() -> StoredTokens | None:
    """
    Load tokens from JSON file.
    
    Returns:
        StoredTokens if file exists, None otherwise
    """
    storage_path = Path.cwd() / STORAGE_FILE
    
    if not storage_path.exists():
        return None
    
    try:
        data = json.loads(storage_path.read_text())
        return StoredTokens(**data)
    except Exception as e:
        logger.error(f"Failed to load tokens: {e}")
        return None


def delete_tokens() -> None:
    """Delete the tokens file if it exists."""
    storage_path = Path.cwd() / STORAGE_FILE
    
    if storage_path.exists():
        storage_path.unlink()
        logger.info(f"Deleted tokens file: {storage_path}")
