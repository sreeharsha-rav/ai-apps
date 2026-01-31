# ACP Terminal Chat

An LLM chat experience demonstrating the Agentic Commerce Protocol [ACP](https://www.agenticcommerce.dev/) in terminal using shopify catalog MCP and mock checkout tools.

*Capabilities*:
- Chat with LLM
- Chat History
- Chat with Agents
- Streaming
- MCP
- Web Search
- Tool Calling

## Requirements

- Python 3.11
- OpenAI API Key
- Azure OpenAI Deployment
- Shopify Catalog API
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