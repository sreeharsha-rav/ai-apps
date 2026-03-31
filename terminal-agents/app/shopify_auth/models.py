from typing import Optional
from pydantic import BaseModel, Field

class TokenResponse(BaseModel):
    """Shopify token endpoint response."""
    access_token: str
    expires_in: Optional[int] = None
    scope: Optional[str] = None

class StoredTokens(TokenResponse):
    """Extended token storage with client credentials and timestamp."""
    client_id: str
    client_secret: str
    updated_at: int = Field(default_factory=lambda: int(__import__('time').time() * 1000))
