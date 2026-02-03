from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from openai import AsyncOpenAI

from api.chat.routes import router as chat_router
from config.settings import OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, AZURE_OPENAI_KEY
from config.loggers import logger
from middleware.logging_middleware import LoggingMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create AsyncOpenAI client
    logger.info("Initializing AsyncOpenAI client...")
    app.state.openai_client = AsyncOpenAI(base_url=AZURE_OPENAI_ENDPOINT, api_key=AZURE_OPENAI_KEY)
    yield
    # Shutdown: Close client
    logger.info("Closing AsyncOpenAI client...")
    await app.state.openai_client.close()

app = FastAPI(title="Streaming Chat API", lifespan=lifespan)

# Add logging middleware first to catch everything
app.add_middleware(LoggingMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(chat_router, prefix="/api/chat", tags=["chat"])

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Server is running. Documentation available at /docs"}
