import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.routers.v1 import chat, models

def is_production() -> bool:
    """Check if the application is running in production mode"""
    return settings.ENVIRONMENT.lower() == "production"

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
    app = FastAPI(
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
    app.add_middleware(
        CORSMiddleware,
        allow_origins=get_cors_origins(),
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # add health check endpoint if needed
    @app.get("/health", status_code=200)
    async def health_check():
        return {"status": "OK"}

    # register routers
    app.include_router(chat.router)
    app.include_router(models.router)

    return app

def get_server_config() -> dict:
    """Get the uvicorn server configuration based on environment"""
    if is_production():
        return {
            "host": "0.0.0.0",
            "port": 8000,
            "workers": 4,
            "reload": False,
            "log_level": "info",
            "proxy_headers": True,
            "forwarded_allow_ips": "*",
        }
    else:
        return {
            "host": "127.0.0.1",
            "port": 8000,
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