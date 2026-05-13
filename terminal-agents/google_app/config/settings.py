import os
from dotenv import load_dotenv


load_dotenv()

if not (GEMINI_API_KEY := os.getenv("GEMINI_API_KEY")):
    raise ValueError("GEMINI_API_KEY is not set in environment variables.")
