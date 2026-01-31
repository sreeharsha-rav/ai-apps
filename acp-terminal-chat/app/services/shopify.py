import requests
from dataclasses import dataclass
from typing import Optional
from app.core.config import (
    SHOPIFY_CATALOG_CLIENT_ID,
    SHOPIFY_CATALOG_CLIENT_SECRET
)
from app.core.utils import logger


# -----------------------------
# Shopify Catalog Auth Client
# -----------------------------

SHOPIFY_TOKEN_URL = "https://api.shopify.com/auth/access_token"
SHOPIFY_CATALOG_MCP_URL = "https://discover.shopifyapps.com/global/mcp"

@dataclass
class ShopifyAccessToken:
    token: str

class ShopifyAuth:
    """
    Fetches and caches Shopify access tokens (JWT).
    """
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self._cached: Optional[ShopifyAccessToken] = None

    def _request_new_token(self) -> ShopifyAccessToken:
        """
        Calls Shopify's token endpoint to mint a new access token.
        """
        try:
            payload = {
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials"
            }

            resp = requests.post(
                url=SHOPIFY_TOKEN_URL,
                headers={
                    "Content-Type": "application/json",
                    "User-Agent": "Terminal Chat"
                },
                json=payload,
            )

            if resp.status_code != 200:
                raise RuntimeError(
                    f"Shopify token request failed: {resp.status_code} - {resp.text}"
                )

            data = resp.json()
            access_token = data.get("access_token")
            
            if not access_token:
                raise RuntimeError(f"Unexpected token response: {data}")

            return ShopifyAccessToken(token=access_token)
            
        except Exception as e:
            logger.error(f"Failed to refresh Shopify token: {e}")
            raise

    def get_valid_token(self) -> str:
        """
        Returns a valid token, refreshing if necessary.
        """
        if self._cached is None:
            logger.info("Refreshing Shopify access token...")
            self._cached = self._request_new_token()
        return self._cached.token
