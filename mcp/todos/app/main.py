from fastapi import FastAPI
from app.api import api

# Create the root application
app = FastAPI(
    title="Main App",
    description="Root application mounting the Todos API."
)

# Mount the 'api' application at the '/api' prefix
app.mount("/api", api)

@app.get("/health")
async def health():
    return {"status": "ok"}