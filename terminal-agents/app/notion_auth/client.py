"""
Core service for Notion OAuth flow.
Consolidates discovery, registration, and authorization logic.
"""
from urllib.parse import urljoin
from typing import Tuple

import requests
from authlib.integrations.requests_client import OAuth2Session
from authlib.common.security import generate_token

from app.config.utils import logger
from app.notion_auth.models import (
    OAuthMetadata, 
    ProtectedResourceMetadata, 
    ClientRegistration, 
    ClientCredentials, 
    TokenResponse
)
from app.config.settings import NOTION_OAUTH_CLIENT_NAME, NOTION_OAUTH_CLIENT_URI


def discover_oauth_metadata(mcp_server_url: str) -> OAuthMetadata:
    """
    Discover OAuth configuration from MCP server.
    
    Step 1: RFC 9470 - Get Protected Resource Metadata
    Step 2: RFC 8414 - Get Authorization Server Metadata
    """
    # Step 1: RFC 9470 - Get Protected Resource Metadata
    protected_resource_url = urljoin(mcp_server_url, "/.well-known/oauth-protected-resource")
    logger.debug(f"Discovering OAuth metadata for {protected_resource_url}")
    
    response = requests.get(protected_resource_url)
    response.raise_for_status()
    
    protected_resource = ProtectedResourceMetadata(**response.json())
    logger.debug(f"Protected resource metadata: {protected_resource.model_dump_json()}")
    
    if not protected_resource.authorization_servers:
        raise ValueError("No authorization servers found in protected resource metadata")
    
    # Use the first authorization server
    auth_server_url = protected_resource.authorization_servers[0]
    
    # Step 2: RFC 8414 - Get Authorization Server Metadata
    metadata_url = urljoin(auth_server_url, "/.well-known/oauth-authorization-server")
    logger.debug(f"Discovering OAuth metadata for authorization server: {metadata_url}")
    
    metadata_response = requests.get(metadata_url)
    metadata_response.raise_for_status()
    
    metadata = OAuthMetadata(**metadata_response.json())
    logger.debug(f"OAuth metadata: {metadata.model_dump_json()}")
    
    # Validate required fields
    if not metadata.authorization_endpoint or not metadata.token_endpoint:
        raise ValueError("Missing required OAuth endpoints in metadata")
    
    return metadata


def register_client(metadata: OAuthMetadata, redirect_uri: str) -> ClientCredentials:
    """
    Register a dynamic OAuth client with the authorization server (RFC 7591).
    """
    if not metadata.registration_endpoint:
        raise ValueError("Server does not support dynamic client registration")
    
    registration_request = ClientRegistration(
        client_name=NOTION_OAUTH_CLIENT_NAME,
        client_uri=NOTION_OAUTH_CLIENT_URI,
        redirect_uris=[redirect_uri],
        grant_types=["authorization_code", "refresh_token"],
        response_types=["code"],
        token_endpoint_auth_method="none",  # Public client - PKCE provides security
    )
    
    logger.debug(f"Registering client: {registration_request.model_dump_json()}")
    
    response = requests.post(
        metadata.registration_endpoint,
        json=registration_request.model_dump(),
        headers={
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
    )
    response.raise_for_status()
    
    credentials = ClientCredentials(**response.json())
    logger.debug(f"Registered client successfully! Client ID: {credentials.client_id}")
    
    return credentials


def create_authorization_url(
    metadata: OAuthMetadata,
    client_id: str,
    redirect_uri: str,
    state: str,
    scopes: list[str] | None = None
) -> Tuple[str, str]:
    """
    Build authorization URL with PKCE.
    Returns (authorization_url, code_verifier).
    """
    session = OAuth2Session(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=" ".join(scopes or []),
        state=state,
        code_challenge_method='S256'  # Enable PKCE with SHA-256
    )
    
    # Generate code_verifier (Authlib generates it automatically if not provided)
    code_verifier = generate_token(48)
    
    # create_authorization_url will generate code_challenge from code_verifier
    url, _ = session.create_authorization_url(
        metadata.authorization_endpoint,
        state=state,
        code_verifier=code_verifier,
        prompt='consent'
    )
    
    logger.debug(f"Created authorization URL (state: {state[:8]}...)")
    
    return url, code_verifier


def exchange_code_for_tokens(
    code: str,
    code_verifier: str,
    metadata: OAuthMetadata,
    client_id: str,
    client_secret: str | None,
    redirect_uri: str
) -> TokenResponse:
    """
    Exchange authorization code for access tokens.
    """
    session = OAuth2Session(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        code_challenge_method='S256'
    )
    
    token = session.fetch_token(
        metadata.token_endpoint,
        grant_type='authorization_code',
        code=code,
        code_verifier=code_verifier
    )
    
    logger.debug("Token exchange successful")
    
    return TokenResponse(**token)


def refresh_access_token(
    refresh_token: str,
    metadata: OAuthMetadata,
    client_id: str,
    client_secret: str | None
) -> TokenResponse:
    """
    Refresh an expired access token.
    """
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
    }
    
    if client_secret:
        data['client_secret'] = client_secret
    
    response = requests.post(
        metadata.token_endpoint,
        data=data,
        headers={
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
        }
    )
    
    if not response.ok:
        error_body = response.text
        try:
            error = response.json()
            if error.get('error') == 'invalid_grant':
                raise ValueError("REAUTH_REQUIRED: Refresh token expired or revoked")
            if error.get('error') == 'invalid_client':
                raise ValueError("INVALID_CLIENT: Client credentials no longer valid")
        except Exception:
            pass
        
        response.raise_for_status()
    
    logger.debug("Token refresh successful")
    
    return TokenResponse(**response.json())
