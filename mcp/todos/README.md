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
```

---

## Setup

**1. Install dependencies**
```bash
uv sync
```

**2. Create a `.env` file**
```env
SECRET_KEY=your-secret-key-here
ACCESS_TOKEN_EXPIRE_MINUTES=30
SQLALCHEMY_DATABASE_URL=sqlite:///./todos.db
ROOT_URL=http://localhost:8000
```

**3. Run the server**
```bash
uv run uvicorn app.main:app --reload
```

The server starts at `http://localhost:8000`. The database tables are created automatically on first run.

---

## Testing the REST API with Swagger

Open **[http://localhost:8000/api/docs](http://localhost:8000/api/docs)**

### Flow

**1. Register a user**
- `POST /api/auth/register` → `{ "username": "alice", "password": "secret" }`

**2. Log in and copy the token**
- `POST /api/auth/login` → returns `{ "access_token": "...", "token_type": "bearer" }`

**3. Authorize in Swagger**
- Click **Authorize** (🔒) → paste your token → **Authorize**

**4. Use the todo endpoints**
- `GET /api/todos` — list todos
- `POST /api/todos` — create a todo
- `GET /api/todos/{id}` — get one
- `PUT /api/todos/{id}` — update
- `DELETE /api/todos/{id}` — delete

---

## Testing the MCP Server with MCP Inspector

### Prerequisites
```bash
npx @modelcontextprotocol/inspector
```

### Get a JWT token first

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "secret"}'
```

Copy the `access_token` from the response.

### Connect in MCP Inspector

| Field | Value |
|---|---|
| **Transport** | Streamable HTTP |
| **URL** | `http://localhost:8000/mcp/` |
| **Auth header** | `Authorization: Bearer <your-token>` |

> ⚠️ Use the trailing slash: `http://localhost:8000/mcp/` — the server redirects `POST /mcp` → `/mcp/`.

### Available MCP Tools

| Tool | Description |
|---|---|
| `get_all_todos` | List all todos for the authenticated user |
| `get_todo_by_id` | Fetch a specific todo by UUID |
| `create_todo` | Create a todo (title, description, priority 1–5) |
| `update_todo` | Update all fields of an existing todo |
| `delete_todo` | Permanently delete a todo by UUID |

### Discovery endpoints (OAuth/auth metadata)

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
