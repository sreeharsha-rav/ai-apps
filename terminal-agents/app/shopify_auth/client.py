"""
Core service for Shopify Auth flow.
"""
import requests
from app.config.utils import logger
from app.shopify_auth.models import TokenResponse
from app.config.settings import SHOPIFY_TOKEN_URL, SHOPIFY_USER_AGENT, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET

def exchange_credentials_for_token(client_id: str | None = None, client_secret: str | None = None) -> TokenResponse:
    """
    Calls Shopify's token endpoint to mint a new access token using client credentials.
    Uses SHOPIFY_CLIENT_ID and SHOPIFY_CLIENT_SECRET from config if not provided.
    """
    cid = client_id or SHOPIFY_CLIENT_ID
    secret = client_secret or SHOPIFY_CLIENT_SECRET

    if not cid or not secret:
        raise ValueError("Shopify Client ID and Secret must be provided or set in environment variables.")

    payload = {
        "client_id": cid,
        "client_secret": secret,
        "grant_type": "client_credentials"
    }

    logger.debug("Requesting Shopify token via client_credentials")
    
    response = requests.post(
        url=SHOPIFY_TOKEN_URL,
        headers={
            "Content-Type": "application/json",
            "User-Agent": SHOPIFY_USER_AGENT
        },
        json=payload,
    )
    
    if not response.ok:
        logger.error(f"Shopify token request failed: {response.status_code} - {response.text}")
        response.raise_for_status()
        
    data = response.json()
    if "access_token" not in data:
        raise ValueError(f"Unexpected token response: {data}")
        
    logger.debug("Successfully obtained Shopify access token")
    return TokenResponse(**data)
