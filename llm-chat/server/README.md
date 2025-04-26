# LLM Chat Server

This is the server component of the LLM Chat application. It provides the backend API for the chat functionality.

## Prerequisites

- Python 3.12
- `uv` for dependency management and package installation (optional but recommended for faster development)
  - [Installation instructions for `uv`](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
- `pip` for package installation

## Project Structure

The project is structured as follows:

- `src/`: Contains the source code for the server.
   ```
   src/
   ├── api/                  # API endpoints
   │   └── v1/               # Version 1 of the API
   │       ├── chat.py       # Chat API endpoints
   │       └── models.py     # Models API endpoints
   ├── core/                 # Core components
   │   ├── config/           # Configuration settings
   │   ├── exceptions/       # Custom exceptions (can be omitted if not needed or just to keep project simple)
   │   ├── llm/              # LLM components
   │   ├── prompts/          # Prompts for LLM
   │   └── search/           # Search components
   ├── models/               # Data models for repositories
   │   ├── chat.py           # Chat model
   │   └── llm.py            # LLM model
   ├── repositories/         # Data repositories
   │   └── chat.py           # Chat repository
   ├── schemas/              # Schemas for data validation
   │   ├── chat.py           # Chat schema
   │   └── llm.py            # LLM schema
   ├── services/             # Business logic services
   │   └── chat.py           # Chat service
   ├── utils/                # Utility functions
   │   ├── decorators.py     # Decorators
   │   └── loggers.py        # Loggers
   ├── main.py               # Main entry point
   └── __init__.py           # Initialization file
   ```
- `tests/`: Contains the test suite for the server.
   ```
   tests/
   ├── api/                  # API tests
   │   └── v1/               # Version 1 of the API
   │       ├── chat.py       # Chat API tests
   │       └── models.py     # Models API tests
   ├── others/               # Other tests to be added
   ```
- `uv.lock`: Lock file for `uv` dependency management.
- `pyproject.toml`: Configuration file for `uv` and `pip`.

This project structure is based on the [FastAPI Clean Architecture](https://github.com/jujumilk3/fastapi-clean-architecture/tree/main) template.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sreeharsa-rav/ai-apps/tree/main/llm-chat
    cd llm-chat/server
    ```
2. Create a virtual environment if not using uv (uv automatically creates a virtual environment):
    ```bash
    python -m venv .venv
    ```
3. Activate the virtual environment:
    ```bash
    # on Windows
    .venv\Scripts\activate

    # on Unix or MacOS
    source .venv/bin/activate
    ```
4. Install the dependencies from `pyproject.toml` into the virtual environment:
    ```bash
    # if you have uv installed
    uv sync
   
   # if you don't have uv installed
    pip install -e .
    ```
5. Setup environment variables using `.env.example` as a template:
   ```bash
   cp .env.example .env
   ```
6. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```
7. View swagger docs (only available in development mode):
   ```bash
   http://localhost:8000/docs
   ```