import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the server root directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

if not (OPENAI_API_KEY := os.getenv("OPENAI_API_KEY")):
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
# if not (AZURE_OPENAI_KEY := os.getenv("AZURE_OPENAI_KEY")):
#     raise ValueError("AZURE_OPENAI_KEY is not set in environment variables.")
# if not (AZURE_OPENAI_ENDPOINT := os.getenv("AZURE_OPENAI_ENDPOINT")):
#     raise ValueError("AZURE_OPENAI_ENDPOINT is not set in environment variables.")
# if not (AZURE_OPENAI_DEPLOYMENT := os.getenv("AZURE_OPENAI_DEPLOYMENT")):
#     raise ValueError("AZURE_OPENAI_DEPLOYMENT is not set in environment variables.")
if not (SHOPIFY_CATALOG_CLIENT_ID := os.getenv("SHOPIFY_CATALOG_CLIENT_ID")):
    raise ValueError("SHOPIFY_CATALOG_CLIENT_ID is not set in environment variables.")
if not (SHOPIFY_CATALOG_CLIENT_SECRET := os.getenv("SHOPIFY_CATALOG_CLIENT_SECRET")):
    raise ValueError("SHOPIFY_CATALOG_CLIENT_SECRET is not set in environment variables.")

