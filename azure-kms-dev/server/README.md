# Azure KMS Server

## Prerequisites

- Python 3.12
- `uv` for dependency management and package installation (optional but recommended for faster development)
  - [Installation instructions for `uv`](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
- `pip` for package installation

## Installation

1. Clone the repository:
    ```bash
    git clone
   ```
   
2. Navigate to the project directory:
    ```bash
    cd server
    ```

3. Create a virtual environment if not using uv (uv automatically creates a virtual environment):
    ```bash
    python -m venv .venv
   
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

## Running the Application

### Development Setup

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug
```

View swagger docs (only available in development mode):
```bash
http://localhost:8000/docs
```

### Production Setup

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4 --log-level info
```