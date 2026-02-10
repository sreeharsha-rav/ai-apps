import os
from dotenv import load_dotenv


load_dotenv()

if not (OPENAI_API_KEY := os.getenv("OPENAI_API_KEY")):
    raise ValueError("OPENAI_API_KEY is not set in environment variables.")
# if not (AZURE_OPENAI_KEY := os.getenv("AZURE_OPENAI_KEY")):
#     raise ValueError("AZURE_OPENAI_KEY is not set in environment variables.")
# if not (AZURE_OPENAI_ENDPOINT := os.getenv("AZURE_OPENAI_ENDPOINT")):
#     raise ValueError("AZURE_OPENAI_ENDPOINT is not set in environment variables.")
# if not (AZURE_OPENAI_DEPLOYMENT := os.getenv("AZURE_OPENAI_DEPLOYMENT")):
#     raise ValueError("AZURE_OPENAI_DEPLOYMENT is not set in environment variables.")
