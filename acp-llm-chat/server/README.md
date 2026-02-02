# LLM Chat API

This is a FastAPI application that provides a streaming chat interface using OpenAI's GPT-5 model.


## Requirements

- Python 3.11
- UV
- OpenAI API Key
- Azure OpenAI Deployment

## Setup

1. Install dependencies:
```bash
uv sync
```

2. Set up environment variables:
```bash
cp .env.example .env
```

4. Activate virtual environment:
```bash
uv venv
```

5. Run the application:
```bash
uv run uvicorn main:app --app-dir . --reload --log-level debug
```

The API will be available at `http://localhost:8000`.
