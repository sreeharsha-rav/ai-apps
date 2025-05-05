import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import app_settings
from src.api import api_router

def is_production() -> bool:
    """Check if the application is running in production mode"""
    return app_settings.ENVIRONMENT == "production"

def get_cors_origins() -> list:
    """Get the list of allowed CORS origins based on environment"""
    if is_production():
        return [
            "https://your-production-domain.com"
            # Add other production-specific origins here
        ]
    else:
        return ["*"]    # Allow all origins in development

def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    is_env_production: bool = is_production()
    fastapi_app = FastAPI(
        title="LLM Chat API",
        description="API for LLM Chat application",
        version="1.0.0",
        # disable docs in production
        docs_url=None if is_env_production else "/docs",
        redoc_url=None if is_env_production else "/redoc",
        # disable openapi in production
        openapi_url=None if is_env_production else "/openapi.json",
        # disable debug mode in production
        debug=False if is_env_production else True
    )

    # configure CORS
    fastapi_app.add_middleware(
        CORSMiddleware,         # type: ignore
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add health check endpoint if needed
    @fastapi_app.get("/health", status_code=200)
    async def health_check():
        return {"status": "OK"}

    # register api router
    fastapi_app.include_router(api_router)

    return fastapi_app

def get_server_config() -> dict:
    """Get the uvicorn src configuration based on environment"""
    if is_production():
        return {
            "host": "0.0.0.0",
            "port": app_settings.PORT,
            "workers": 4,
            "reload": False,
            "log_level": "info",
            "proxy_headers": True,
            "forwarded_allow_ips": "*",
        }
    else:
        return {
            "host": app_settings.HOST,
            "port": app_settings.PORT,
            "reload": True,
            "workers": 1,
            "log_level": "debug",
        }

# create the FastAPI application instance
app = create_app()

def main():
    """Main entry point for the application"""
    config = get_server_config()
    uvicorn.run("src.main:app", **config)

if __name__ == "__main__":
    main()