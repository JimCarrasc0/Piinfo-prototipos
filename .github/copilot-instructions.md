# Piinfo-Prototipos: AI Agent Guidelines

## Project Overview

**Piinfo-prototipos** is a multi-service social media analytics platform consisting of:

1. **Chat-bot** (T-Radar Chatbot Backend): FastAPI service with RAG (Retrieval-Augmented Generation) for querying Instagram analytics via natural language
2. **Prototipo Backend**: RRAMASI inspection management system with FastAPI, Alembic migrations, and machine learning pipelines
3. **Prototipo/proto-tipo**: Vue 3 + TypeScript frontend dashboard (Vite) - **NOW WITH INTEGRATED BANDURRIA CHATBOT**
4. **Prototipo ing 3.2**: Secondary Vue 3 dashboard (t-radar-dashboard)
5. **Scraper**: Instagram data collection utility

## Critical Architecture Patterns

### Chat-Bot Request Pipeline

The chat service follows a strict orchestration pattern. **Every chat request** flows through these sequential stages:

```
chat_endpoint → intent_detector → orchestrator.build_context → prompt_builder → run_llm → response
```

**Key files**: [chat.py](chat-bot/app/api/chat.py), [orchestrator.py](chat-bot/app/services/orchestrator.py), [intent_detector.py](chat-bot/app/services/intent_detector.py)

- **Intent Detection**: Uses sentence-transformers (all-MiniLM-L6-v2) to classify user queries against predefined intents (`listar_posts`, `consultar_metricas`, `analizar_comentarios`, `recomendacion_general`)
- **Context Building**: Based on detected intent and entities (post_scope: "last"/"first"/"all"/"specific"), the orchestrator queries SQLite for posts, metrics, and comments
- **RAG Layer**: Retrieved context is enhanced with semantic search using `sentence_transformers.util.cos_sim` to find most relevant posts by embedding similarity
- **Prompt Assembly**: [prompt_builder.py](chat-bot/app/services/prompt_builder.py) constructs contextual prompts; examine this file to understand what format the LLM expects

### Backend Data Model (Prototipo Backend)

Uses **SQLAlchemy ORM** with **Alembic** for migrations. All models extend `Base` from [base_class.py](Prototipo%20Backend/app/db/base_class.py).

**Key entities**:
- User → has multiple Meta Accounts
- Meta Account → has Posts, Comments, Metrics
- Post → has Post_Comment, Post_Metric, Post_Analysis

**Database operations**: Use declarative models in [models/](Prototipo%20Backend/app/models) + CRUD layer in [crud/](Prototipo%20Backend/app/crud). Never execute raw SQL directly; follow the CRUD pattern.

**Migrations workflow** (Makefile):
```bash
make alembic-rev m="Add new table"  # Generate migration
make alembic-up                      # Apply migrations
```

### Frontend Chat Integration (Prototipo/proto-tipo)

The Vue 3 frontend now integrates with the BandurrIA chatbot via [chatService.ts](Prototipo/proto-tipo/src/lib/chatService.ts).

**Chat Component**: [BandurriaSidebar.vue](Prototipo/proto-tipo/src/components/BandurriaSidebar.vue)

**API Communication Pattern**:
1. **Session Management**: Sessions are persisted in localStorage using unique IDs; retrieved via `getOrCreateSessionId()`
2. **Send Message**: `POST http://localhost:8000/chat/` with `{message, session_id}`
3. **Receive Response**: Backend returns `{session_id, reply}`
4. **Load History**: `GET http://localhost:8000/chat/history/{session_id}` returns array of `{role, content, created_at}`

**Key features**:
- Automatic session persistence across page reloads
- Loading states with spinner animation while waiting for bot response
- Error handling with user-friendly messages
- Quick idea suggestions for new sessions
- Both desktop (sidebar) and mobile (floating button) UI

### Configuration Management

- **Chat-bot**: [config.py](chat-bot/app/utils/config.py) reads from environment variables (`DB_PATH`, `API_PORT`, `EMBEDDING_MODEL_NAME`, `RAG_TOP_K`)
- **Prototipo Backend**: [config.py](Prototipo%20Backend/app/core/config.py) uses Starlette config loader (`.env` file); includes JWT settings, CORS, logging
- **Prototipo Frontend**: [chatService.ts](Prototipo/proto-tipo/src/lib/chatService.ts) communicates with chat backend at `http://localhost:8000/chat`
- **All services**: Deploy docker-compose; check [docker-compose.yml](chat-bot/docker-compose.yml) and Dockerfiles for container setup

## Project-Specific Conventions

### Commit Messages

Strictly follow format: `[Section] [Subject] message`

Examples:
```
[Chat] [fix] Correct intent detection threshold
[Backend] [feat] Add post analysis endpoint
[Front] [refactor] Restructure dashboard components
```

Valid sections: `Chat`, `Backend`, `Front`, `Scraper`, `Infra`

### Data Pipelines

**Chat-bot**: Message → Intent → Entity Extraction → Context Retrieval → Prompt → LLM → DB Save

**Backend**: Data comes from Meta (via OAuth) or manual upload → stored in DB → analyzed via ML models → served via API

**Scraper** [scraper.py](scraper/scraper.py): Instagram account data → `publicaciones.json` (id, description, likes, comments, publication_type, date)

### Database Patterns

**Chat-bot** (SQLite, schema in [schema.sql](chat-bot/app/db/schema.sql)):
- Direct SQL queries via `get_db()` connection
- Row factory: `conn.row_factory = sqlite3.Row` (access columns as dict keys)
- No ORM; keep queries simple and retrieve only needed fields

**Backend** (PostgreSQL via Alembic + SQLAlchemy):
- All changes via Alembic migrations (`alembic-rev`)
- CRUD operations in [crud/](Prototipo%20Backend/app/crud) directory
- Schemas (Pydantic validation) in [schemas/](Prototipo%20Backend/app/schemas)

### API Response Structure

All endpoints return consistent structure:
- Success: HTTP 200 with data payload
- Validation errors: HTTP 422 with detail field
- Server errors: HTTP 500 with detail field
- Authentication failures: HTTP 401/403

## Developer Workflows

### Chat-bot Setup

```bash
cd chat-bot
docker compose up --build
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

Health check: `GET /health` → `{"status": "ok", "service": "bandurria-backend"}`

### Backend Setup

```bash
cd Prototipo\ Backend
make install     # Creates venv, installs dependencies
make run        # uvicorn on http://localhost:8080
make test       # pytest with verbose output
make alembic-rev m="description"  # Create migration
```

## Frontend Setup

```bash
cd Prototipo/proto-tipo
pnpm install    # (not npm; pnpm is preferred for workspace consistency)
pnpm dev        # Vite dev server on http://localhost:5173
```

**Development Flow**:
- Vite proxy routes `/chat` requests to `http://localhost:8000/chat` (see vite.config.ts)
- Hot reload enabled; changes reflect immediately
- Chat component auto-loads history on mount; auto-persists session in localStorage

## External Dependencies & Integration Points

### Vector Store & Embeddings

- **Model**: `nomic-embed-text-v1.5` (can be local `.gguf` in [models/](chat-bot/models))
- **Used in**: Intent detection, RAG context retrieval
- **Pattern**: Embed text → compute cosine similarity → rank by relevance

### LLM Integration

[llm.py](chat-bot/app/services/llm.py) - handles model inference. Prompt structure is critical; always examine `prompt_builder.py` to understand expected format.

### Meta OAuth

Backend integrates with Meta (Instagram) API via [meta_oauth.py](Prototipo%20Backend/app/api/routes/meta_oauth.py). Tokens stored in DB; handle token refresh before making API calls.

### Docker Compose Services

- **chat-bot**: FastAPI on port 8000, volumes for models
- **backend**: FastAPI on port 8080, connects to DB
- Check environment variables in docker-compose.yml for port/host overrides

## Common Pitfalls to Avoid

1. **Intent detection**: If a query doesn't match known intents, check entity extraction logic and similarity thresholds in [intent_detector.py](chat-bot/app/services/intent_detector.py)
2. **RAG retrieval**: If relevant posts aren't returned, verify `RAG_TOP_K` config and embedding model is loaded
3. **Database queries**: Always use connection's row_factory for dict access; don't assume column order
4. **Migrations**: Apply migrations in order; `alembic-downgrade -1` reverts one step
5. **CORS issues**: Frontend requests fail? Check CORS_ORIGINS in backend config matches your frontend URL
6. **Chat frontend loading**: Verify backend is running (`http://localhost:8000/health` should return `{"status": "ok"}`)
7. **Chat history not loading**: Ensure `/chat/history/{session_id}` endpoint returns proper format with `role` and `created_at` fields
8. **Session loss**: Check browser allows localStorage (not in private/incognito mode)

## File Structure Quick Reference

- **Business Logic**: `app/services/` (chat-bot) or `app/api/routes/` (backend)
- **Data Access**: `app/db/` + `app/crud/` (backend) or direct SQL (chat-bot)
- **Configuration**: `app/utils/config.py` or `app/core/config.py`
- **API Routes**: `app/api/` with request/response models defined inline or in schemas/
- **ML/Embeddings**: `app/services/embeddings.py`, `app/services/intent_detector.py`
- **Tests**: `tests/` directory; run with `make test` or `pytest`

---

**Last updated**: January 2026 | Focus on understanding the chat pipeline + backend CRUD patterns first
