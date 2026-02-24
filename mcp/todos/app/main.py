from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp.utilities.lifespan import combine_lifespans
from app.api import api
from app.mcp import mcp
from app.config import settings
from app.database.db import engine
from app.database.models import Base
from app.middleware import LogRequestsMiddleware, configure_logging
import logging


configure_logging()
logger = logging.getLogger(__name__)

# --- MCP ASGI App ---
mcp_app = mcp.http_app(path="/")

# --- Lifespan ---
@asynccontextmanager
async def app_lifespan(app: FastAPI):
    """Application startup: initialize database tables."""
    logger.info("Initializing database...")
    Base.metadata.create_all(bind=engine)
    yield

# --- Root FastAPI Application ---
app = FastAPI(
    title="Todos App",
    description="Root application mounting the Todos REST API and FastMCP server.",
    version="1.0.0",
    lifespan=combine_lifespans(app_lifespan, mcp_app.lifespan),
)

# --- Middleware (root-level, applies to ALL sub-apps) ---
app.add_middleware(LogRequestsMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=[
        "mcp-protocol-version",
        "mcp-session-id",
        "Authorization",
        "Content-Type",
    ],
    expose_headers=["mcp-session-id"],
)

# --- Well-Known Discovery Routes (required at root level for OAuth auth providers) ---
well_known_routes = mcp.auth.get_well_known_routes(
    mcp_path="/mcp"
)
if well_known_routes:
    for route in well_known_routes:
        app.routes.append(route)
    logger.info(f"Registered {len(well_known_routes)} well-known discovery route(s)")
else:
    logger.info("No well-known discovery routes required for current auth provider")

# --- Health Check ---
@app.get("/health")
async def health():
    return {"status": "ok"}

# --- Mount Sub-Applications ---
app.mount("/api", api)
app.mount("/mcp", mcp_app)
