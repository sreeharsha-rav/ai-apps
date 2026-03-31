from typing import Optional, List
from pydantic import BaseModel, Field


class OAuthMetadata(BaseModel):
    """OAuth Authorization Server Metadata (RFC 8414)."""
    issuer: str
    authorization_endpoint: str
    token_endpoint: str
    registration_endpoint: Optional[str] = None
    code_challenge_methods_supported: Optional[List[str]] = None
    grant_types_supported: Optional[List[str]] = None
    response_types_supported: Optional[List[str]] = None
    scopes_supported: Optional[List[str]] = None


class ProtectedResourceMetadata(BaseModel):
    """Protected Resource Metadata (RFC 9470)."""
    authorization_servers: List[str]


class ClientRegistration(BaseModel):
    """Dynamic Client Registration request (RFC 7591)."""
    client_name: str
    client_uri: Optional[str] = None
    redirect_uris: List[str]
    grant_types: List[str]
    response_types: List[str]
    token_endpoint_auth_method: str
    scope: Optional[str] = None


class ClientCredentials(BaseModel):
    """Dynamic Client Registration response."""
    client_id: str
    client_secret: Optional[str] = None
    client_id_issued_at: Optional[int] = None
    client_secret_expires_at: Optional[int] = None


class TokenResponse(BaseModel):
    """OAuth token endpoint response."""
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


class StoredTokens(TokenResponse):
    """Extended token storage with client credentials and timestamp."""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    updated_at: int = Field(default_factory=lambda: int(__import__('time').time() * 1000))
