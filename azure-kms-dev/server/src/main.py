from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config.settings import get_app_config
from src.middleware.logging import LoggingMiddleware
from src.api import api_router

app_config = get_app_config()
is_env_production: bool = app_config.ENVIRONMENT.lower() == "production"

app = FastAPI(
    title="Azure KMS Server",
    description="A FastAPI server for Knowledge Management System (KMS) using Azure services",
    version=app_config.VERSION,
    docs_url=None if is_env_production else "/docs",
    redoc_url=None if is_env_production else "/redoc",
    openapi_url=None if is_env_production else "/openapi.json",
    debug=not is_env_production
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=app_config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)   # type: ignore

@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "service": "azure-kms-server",
        "version": app_config.VERSION,
        "environment": app_config.ENVIRONMENT,
        "debug": app_config.SERVER_LOG_LEVEL
    }

app.include_router(api_router)