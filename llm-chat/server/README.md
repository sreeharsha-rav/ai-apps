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
   ├── api/                                         # API endpoints
   │   ├── __init__.py                                  # Initialization file containing api_router
   │   └── v1/                                          # Version 1 of the API
   │       ├── __init__.py                                  # Initialization file containing v1_router
   │       ├── endpoints/                                   # API endpoint implementations
   │       │   ├── __init__.py                                  # Initialization file
   │       │   ├── chat.py                                      # Chat API endpoints
   │       │   ├── models.py                                    # Models API endpoints
   │       │   └── space.py                                     # Space API endpoints
   │       └── dependencies.py                          # Dependencies for the API
   ├── core/                                        # Core components
   │   ├── config/                                      # Configuration settings
   │   ├── exceptions/                                  # Custom exceptions (can be omitted if not needed or just to keep project simple)
   │   ├── llm/                                         # LLM components
   │   ├── prompts/                                     # Prompts for LLM
   │   ├── retriever/                                   # Retriever components
   │   └── search/                                      # Search components
   ├── models/                                      # Data models for storage representation
   │   ├── chat.py                                      # Chat model
   │   └── space.py                                     # Space model
   ├── repositories/                                # Data repositories
   │   ├── chat.py                                      # Chat repository
   │   └── spaces.py                                    # Space repository
   ├── schemas/                                     # Schemas for data validation
   │   ├── chat.py                                      # Chat schema
   │   ├── llm.py                                       # LLM schema
   │   ├── search.py                                    # Search schema
   │   └── space.py                                     # Space schema
   ├── services/                                    # Business logic services
   │   ├── chat.py                                      # Chat service
   │   └── space.py                                     # Space service
   ├── utils/                                       # Utility functions
   │   ├── decorators.py                                # Decorators
   │   └── loggers.py                                   # Loggers
   ├── main.py                                      # Main entry point
   └── __init__.py                                  # Initialization file
   ```
- `tests/`: Contains the test suite for the server.
   ```
   tests/
   ├── api/                  # API tests
   │   └── v1/               # Version 1 of the API
   ├── others/               # Other tests to be added
   ```
- `indexer/`: Contains the indexer function application.
    ```
   indexer/
   ├── config/                                      # Configuration settings
   │   ├── settings.py                                  # Settings for Azure Storage, Azure AI Search, and Azure OpenAI Embedding
   │   └── constants.py                                 # Constants for the indexer application
   ├── core/                                        # Core components
   │   ├── embedding/                                   # Embedding components
   │   ├── processors/                                  # Processor components
   │   ├── storage/                                     # Storage components
   │   └── vector_store/                                # Vector store components
   ├── schemas/                                      # Data models for schema representation
   │   ├── document.py                                  # Document schemas
   │   ├── metadata.py                                  # Metadata schemas
   │   └── vector_store.py                              # Vector store schemas
   ├── services/                                     # Business logic services
   │   ├── document_service.py                          # Document service
   │   └── index_manager.py                             # Index manager service
   ├── main.py                                      # Main entry point
   └── __init__.py                                  # Initialization file
    ```
- `uv.lock`: Lock file for `uv` dependency management.
- `pyproject.toml`: Configuration file for `uv` and `pip`.

This project structure is based on the [FastAPI Clean Architecture](https://github.com/jujumilk3/fastapi-clean-architecture/tree/main) template.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/sreeharsa-rav/ai-apps/tree/main/llm-chat
    cd llm-chat/src
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