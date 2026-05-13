import os
from dotenv import load_dotenv


load_dotenv()

if not (ANTHROPIC_API_KEY := os.getenv("ANTHROPIC_API_KEY")):
    raise ValueError("ANTHROPIC_API_KEY is not set in environment variables.")
