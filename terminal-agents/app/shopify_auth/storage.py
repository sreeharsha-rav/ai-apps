"""Token storage using JSON file."""
import json
from pathlib import Path
from app.config.utils import logger
from app.shopify_auth.models import StoredTokens, TokenResponse
from app.config.settings import SHOPIFY_TOKEN_STORAGE_FILE

STORAGE_FILE = SHOPIFY_TOKEN_STORAGE_FILE

def save_tokens(tokens: TokenResponse, client_id: str, client_secret: str) -> None:
    import time
    
    stored_tokens = StoredTokens(
        **tokens.model_dump(),
        client_id=client_id,
        client_secret=client_secret,
        updated_at=int(time.time() * 1000)
    )
    
    storage_path = Path.cwd() / STORAGE_FILE
    storage_path.write_text(stored_tokens.model_dump_json(indent=2))
    
    logger.info(f"Saved Shopify tokens to {storage_path}")

def load_tokens() -> StoredTokens | None:
    storage_path = Path.cwd() / STORAGE_FILE
    
    if not storage_path.exists():
        return None
    
    try:
        data = json.loads(storage_path.read_text())
        return StoredTokens(**data)
    except Exception as e:
        logger.error(f"Failed to load Shopify tokens: {e}")
        return None

def delete_tokens() -> None:
    storage_path = Path.cwd() / STORAGE_FILE
    
    if storage_path.exists():
        storage_path.unlink()
        logger.info(f"Deleted Shopify tokens file: {storage_path}")
