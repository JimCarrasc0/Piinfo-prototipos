# Docker Setup - Piinfo-Prototipos

## Descripción

Este documento explica cómo ejecutar toda la plataforma usando Docker y docker-compose.

## Estructura

```
piinfo-prototipos/
├── docker-compose.yml          ← Orquestación (Frontend + Backend)
├── docker-start.sh             ← Script inicio (Linux/macOS)
├── docker-start.bat            ← Script inicio (Windows)
├── run-seed.sh                 ← Cargar datos de prueba (Linux/macOS)
├── run-seed.bat                ← Cargar datos de prueba (Windows)
├── chat-bot/
│   ├── Dockerfile              ← Backend FastAPI
│   └── docker-compose.yml      ← (legado) docker-compose local
└── Prototipo/proto-tipo/
    ├── Dockerfile              ← Frontend Vue 3 + Nginx
    ├── nginx.conf              ← Configuración de Nginx
    └── .dockerignore
```

## Requisitos

- Docker Desktop (versión 20.10+)
- docker-compose (versión 1.29+)
- 4 GB RAM disponible (recomendado)

**Instalación**:
- [Docker Desktop para Windows](https://docs.docker.com/desktop/install/windows-install/)
- Incluye docker-compose automáticamente

## Quick Start

### Opción 1: Todo en Docker (Recomendado)

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

Espera hasta ver:
```
tradar-chatbot        | Uvicorn running on http://0.0.0.0:8000
proto-tipo-frontend   | nginx: master process started
```

**Tiempo de startup**: ~10-15 segundos

Luego accede:
- 🌐 **Frontend**: http://localhost:5173
- 🤖 **Backend Docs**: http://localhost:8000/docs
- 🏥 **Backend Health**: http://localhost:8000/health

### Opción 1b: Cargar Datos de Prueba (Opcional)

Si quieres datos de prueba en la base de datos:

```bash
# Windows
run-seed.bat

# Linux/macOS
bash run-seed.sh
```

> **Nota**: Esto tarda 1-2 minutos la primera vez (descarga modelo de embeddings)

### Opción 2: Solo Backend (desarrollo frontend local)

```bash
# Ejecutar solo el backend
docker-compose up tradar-chatbot

# En otra terminal, ejecutar frontend local
cd Prototipo/proto-tipo
pnpm dev
# → http://localhost:5173
```

## Servicios

### 1. tradar-seed (REMOVIDO - Ejecutar Manualmente)
- **Propósito**: Inicializar la base de datos con datos de prueba
- **Comando**: `bash run-seed.sh` (Linux/macOS) o `run-seed.bat` (Windows)
- **Tiempo**: ~1-2 minutos (incluye descarga de modelo)
- **Ejecución**: Solo cuando necesites datos de prueba

```bash
# Ejecutar manualmente
run-seed.bat      # Windows
bash run-seed.sh  # Linux/macOS
```

### 2. tradar-chatbot (Backend)
- **Imagen**: Dockerfile de chat-bot
- **Puerto**: 8000
- **Ruta**: http://localhost:8000
- **Health**: GET /health → {"status": "ok"}
- **Documentación**: http://localhost:8000/docs

**Variables de entorno**:
```
VISTO en: chat-bot/.env
DB_PATH=/app/data/chatbot.db
API_PORT=8000
EMBEDDING_MODEL_NAME=nomic-ai/nomic-embed-text-v1.5
RAG_TOP_K=5
```

### 3. proto-tipo-frontend (Frontend)
- **Imagen**: Dockerfile de proto-tipo
- **Puerto**: 5173 (mapeado internamente a 80)
- **Runtime**: Nginx (servidor de archivos estáticos)
- **Health**: GET /healthz → "healthy"

**Features**:
- Build optimizado con multi-stage (build → runtime)
- Compresión gzip
- Cache-busting para CSS/JS
- Proxy transparente a `/chat` → backend

## Volumenes

```yaml
chat-bot:
  - ./chat-bot/data:/app/data                     # Base de datos SQLite
  - ~/.cache/huggingface:/root/.cache/huggingface # Caché de modelos

frontend:
  - (ninguno en producción, basado en imagen)
```

## Redes

```
piinfo-network (bridge)
├── tradar-chatbot (8000/tcp)
└── proto-tipo-frontend (80/tcp → 5173 externamente)
```

## Comandos Útiles

### Iniciar servicios
```bash
# Iniciar todos (primera vez con build)
docker-compose up --build

# Iniciar en background
docker-compose up -d

# Iniciar sin rebuild
docker-compose up
```

### Ver logs
```bash
# Todos los servicios
docker-compose logs -f

# Solo un servicio
docker-compose logs -f tradar-chatbot
docker-compose logs -f proto-tipo-frontend

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Parar servicios
```bash
# Parar sin eliminar volúmenes
docker-compose down

# Parar y eliminar todo (incluyendo volúmenes)
docker-compose down -v

# Parar un servicio específico
docker-compose stop tradar-chatbot
```

### Rebuild
```bash
# Rebuildar todo
docker-compose build --no-cache

# Rebuildar un servicio específico
docker-compose build --no-cache tradar-chatbot
```

### Ejecutar comandos en un contenedor
```bash
# Bash en frontend
docker exec -it proto-tipo-frontend sh

# Bash en backend
docker exec -it tradar-chatbot bash

# Ejecutar comando único
docker exec tradar-chatbot python -c "import app; print('OK')"
```

## Desarrollo

### Cambios en Backend (Python)
1. Edita código en `chat-bot/app/...`
2. Rebuilda: `docker-compose build tradar-chatbot`
3. Reinicia: `docker-compose up tradar-chatbot`

### Cambios en Frontend (Vue/TypeScript)
**Si está containerizado**:
1. Edita código en `Prototipo/proto-tipo/src/...`
2. Rebuilda: `docker-compose build proto-tipo-frontend`
3. Reinicia: `docker-compose up proto-tipo-frontend`

**Mejor (desarrollo rápido)**:
```bash
# Usa Vite localmente (hot reload)
cd Prototipo/proto-tipo
pnpm dev

# Backend en Docker
docker-compose up tradar-chatbot
```

## Problemas Comunes

### Puerto ya en uso
```
Error: port is already in use

Solución:
docker-compose down  # Parar otros contenedores
docker ps            # Ver qué más está usando el puerto
lsof -i :5173        # Ver procesos en puerto 5173
```

### Backend no responde
```
Error: Cannot connect to http://localhost:8000

Solución:
docker-compose logs tradar-chatbot  # Ver logs
docker-compose ps                   # Verificar estado
# Asegúrate de que esté healthy
```

### Frontend muestra página en blanco
```
Solución:
1. Abre DevTools (F12)
2. Console → ¿Hay errores?
3. Network → ¿Errores 404 o 5xx?
4. Verifica: docker-compose logs proto-tipo-frontend
5. Limpia: docker-compose down -v && docker-compose up --build
```

### CORS error en /chat/
```
Error: Access to XMLHttpRequest blocked by CORS

Solución:
1. El proxy de Nginx debe estar configurado
2. Verifica nginx.conf → location /chat/
3. Reinicia: docker-compose restart proto-tipo-frontend
```

## Produção

### Actualizar imagen base
```bash
# En Dockerfile
FROM node:20-alpine  # Nueva versión
RUN npm install -g pnpm  # Actualizar pnpm
```

### Reducir tamaño de imagen

**Dockerfile (Frontend)**:
```dockerfile
# Multi-stage ya está optimizado
# Build: ~500 MB
# Runtime: ~50 MB (Nginx)
```

**Optimizaciones adicionales**:
```dockerfile
# .dockerignore: Excluye node_modules, .git, etc.
# pnpm install --frozen-lockfile: Reproducible builds
```

### Registry privado

```bash
# Taggear imagen
docker tag proto-tipo-frontend:latest registry.example.com/proto-tipo:v1.0

# Push
docker push registry.example.com/proto-tipo:v1.0

# Usar en docker-compose.yml
image: registry.example.com/proto-tipo:v1.0
```

## Health Checks

Ambos servicios incluyen health checks:

```bash
# Backend
curl http://localhost:8000/health
# {"status": "ok", "service": "bandurria-backend"}

# Frontend
curl http://localhost:5173/healthz
# healthy
```

## Performance

### Tamaños de imagen

```
chat-bot:
  - Base Python: ~400 MB
  - Con dependencias: ~800 MB

proto-tipo-frontend:
  - Build stage: ~600 MB
  - Runtime (Nginx): ~30 MB
  - Final: ~80 MB
```

### Tiempo de startup

```
tradar-seed:      30-60s (solo primera vez)
tradar-chatbot:   5-10s
proto-tipo-frontend: 2-3s
Total: ~10-15s (subsecuentes)
```

## Monitoreo

### Ver métricas
```bash
# Uso de CPU/Memoria
docker stats

# Detalles de un contenedor
docker inspect proto-tipo-frontend
```

### Logs persistentes
```bash
# Los logs se almacenan en:
# ~/.docker/desktop/vm/data/Docker.raw

# Ver con journalctl (Linux)
journalctl -u docker
```

---

**Última actualización**: Enero 2026  
**Status**: ✅ Listo para producción
