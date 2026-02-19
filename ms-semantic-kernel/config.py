from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

if (AZURE_OPENAI_ENDPOINT := os.getenv("AZURE_OPENAI_ENDPOINT")) is None:
    raise ValueError("AZURE_OPENAI_ENDPOINT is not set in the environment variables.")
if (AZURE_OPENAI_DEPLOYMENT := os.getenv("AZURE_OPENAI_DEPLOYMENT")) is None:
    raise ValueError("AZURE_OPENAI_DEPLOYMENT is not set in the environment variables.")
if (AZURE_OPENAI_API_KEY := os.getenv("AZURE_OPENAI_API_KEY")) is None:
    raise ValueError("AZURE_OPENAI_API_KEY is not set in the environment variables.")
if (AZURE_OPENAI_API_VERSION := os.getenv("AZURE_OPENAI_API_VERSION")) is None:
    raise ValueError("AZURE_OPENAI_API_VERSION is not set in the environment variables.")
