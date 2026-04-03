# Use uv's official Python 3.11 image (includes uv pre-installed)
FROM ghcr.io/astral-sh/uv:python3.11-trixie-slim

WORKDIR /app

# Install dependencies first (separate layer — cached unless lockfile changes)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Copy source code
COPY . /app

# Install the project itself into the venv
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Put the venv on PATH so uvicorn is available directly
ENV PATH="/app/.venv/bin:$PATH"

# Dedicated directory for the SQLite volume mount
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
