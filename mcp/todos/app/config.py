import os
from dotenv import load_dotenv


class Settings:
    def __init__(self):
        load_dotenv()
        
        self.SECRET_KEY = os.getenv("SECRET_KEY")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        self.SQLALCHEMY_DATABASE_URL = os.getenv("SQLALCHEMY_DATABASE_URL")
        self.ROOT_URL = os.getenv("ROOT_URL", "http://localhost:8000")
        self.MCP_MOUNT_PREFIX = os.getenv("MCP_MOUNT_PREFIX", "/mcp")
        self.JWT_ALGORITHM = "HS256"
        
        if not self.SECRET_KEY:
            raise ValueError("SECRET_KEY is not set in environment variables.")
        if not self.ACCESS_TOKEN_EXPIRE_MINUTES:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES is not set in environment variables.")
        if not self.SQLALCHEMY_DATABASE_URL:
            raise ValueError("SQLALCHEMY_DATABASE_URL is not set in environment variables.")
        
settings = Settings()
