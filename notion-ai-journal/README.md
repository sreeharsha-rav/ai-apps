# Notion AI Journal

Agentic notion journal workflow.

- Write daily entries (fleeting thoughts, daily affirmations, reflections)

## Requirements

- Python 3.11
- Notion Account
- OpenAI API Key
- uv

## Getting Started

1. Install dependencies:
```bash
uv sync
```

2. Set environment variables:
```bash
cp .env.sample .env
```

3. Activate virtual environment:
```bash

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

4. Run the chat:
```bash
uv run python -m app.main
```