# Terminal Agents

Terminal Agents is a framework for building terminal-based AI agents.

## Features

- **Agent-based architecture**: Agents can be composed of multiple sub-agents.
- **Tool integration**: Agents can use tools to interact with the environment.
- **Streaming responses**: Agents can stream responses to the user.
- **Context management**: Agents can maintain context across multiple turns.

## Requirements

- Python 3.12
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

# TODOS

- File Session [https://github.com/openai/openai-agents-python/blob/main/examples/memory/file_session.py]
- research Agent v0 [https://github.com/openai/openai-agents-python/tree/main/examples/research_bot]