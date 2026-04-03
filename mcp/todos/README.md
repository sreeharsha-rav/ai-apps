# Todos — REST API + MCP Server

A personal todo manager exposed as both a REST API (FastAPI) and an MCP server (FastMCP), with JWT authentication.

## Stack

| Layer | Technology |
|---|---|
| REST API | FastAPI, mounted at `/api` |
| MCP Server | FastMCP 3.x (Streamable HTTP), mounted at `/mcp` |
| Auth | JWT (HS256) via `python-jose` |
| Database | SQLite via SQLAlchemy |
| Runtime | Python 3.11, `uv` |

## Project Structure

```
app/
  main.py      # Root FastAPI app — mounts API + MCP, CORS, well-known routes
  api.py       # REST API (register, login, CRUD todos)
  mcp.py       # FastMCP server (5 tools, JWT-authenticated)
  config.py    # Settings loaded from .env
  schemas.py   # Pydantic models
  services/    # AuthService, TodoService
  database/    # SQLAlchemy models, repositories, session
Dockerfile
docker-compose.yml
```

---

## Running Locally

**1. Install dependencies**
```bash
uv sync
```

**2. Create a `.env` file**
```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=120
SQLALCHEMY_DATABASE_URL=sqlite:///./todos.db
ROOT_URL=http://localhost:8000
MCP_MOUNT_PREFIX=/mcp
```

**3. Run the server**
```bash
uv run uvicorn app.main:app --reload
```

The server starts at `http://localhost:8000`. Database tables are created automatically on first run.

---

## Running with Docker

**1. Copy and fill in your `.env`**
```bash
cp .env.sample .env
# Edit .env — set a real SECRET_KEY
```

**2. Build and start**
```bash
docker compose up --build
```

The SQLite database is stored in a named Docker volume (`todos-data`) and persists across restarts and rebuilds.

**3. Stop**
```bash
docker compose down           # Keeps data
docker compose down -v        # Also deletes the database volume
```

---

## REST API

Open **[http://localhost:8000/api/docs](http://localhost:8000/api/docs)** for interactive Swagger UI.

### Auth flow

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'

# Get a token
curl -X POST http://localhost:8000/api/auth/token \
  -d "username=alice&password=secret"
```

### Todo endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/api/todos` | List all todos |
| `POST` | `/api/todos` | Create a todo |
| `GET` | `/api/todos/{id}` | Get one |
| `PUT` | `/api/todos/{id}` | Update |
| `DELETE` | `/api/todos/{id}` | Delete |

---

## MCP Server

### Connect with MCP Inspector

```bash
npx @modelcontextprotocol/inspector
```

| Field | Value |
|---|---|
| **Transport** | Streamable HTTP |
| **URL** | `http://localhost:8000/mcp/` |
| **Auth header** | `Authorization: Bearer <your-token>` |

> ⚠️ Use the trailing slash: `http://localhost:8000/mcp/`

### Available Tools

| Tool | Description |
|---|---|
| `get_all_todos` | List all todos for the authenticated user |
| `get_todo_by_id` | Fetch a specific todo by UUID |
| `create_todo` | Create a todo (title, description, priority 1–5) |
| `update_todo` | Update all fields of an existing todo |
| `delete_todo` | Permanently delete a todo by UUID |

### Discovery endpoints

```
GET /.well-known/oauth-protected-resource/mcp
GET /.well-known/oauth-authorization-server/mcp
```

---

## Health Check

```bash
curl http://localhost:8000/health
# {"status": "ok"}
```
