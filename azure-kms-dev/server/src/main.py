from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import get_app_config
from src.middleware.logging import LoggingMiddleware

app_config = get_app_config()
is_env_production: bool = app_config.environment.lower() == "production"

app = FastAPI(
    title="Azure KMS Server",
    description="A FastAPI server for Knowledge Management System (KMS) using Azure services",
    version=app_config.version,
    docs_url=None if is_env_production else "/docs",
    redoc_url=None if is_env_production else "/redoc",
    openapi_url=None if is_env_production else "/openapi.json",
    debug=not is_env_production
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=app_config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LoggingMiddleware)   # type: ignore

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Azure KMS Server is running"}

@app.get("/health", status_code=200)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "OK",
        "timestamp": datetime.now().isoformat(),
        "service": "azure-kms-server",
        "version": app_config.version,
        "environment": app_config.environment,
        "debug": app_config.log_level
    }