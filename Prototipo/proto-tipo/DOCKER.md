# Proto-Tipo Frontend - Docker Setup

## Descripción

Frontend Vue 3 + Vite containerizado con:
- ✅ Build optimizado (multi-stage)
- ✅ Servidor Nginx para archivos estáticos
- ✅ Compresión gzip
- ✅ Cache busting
- ✅ Proxy transparente al backend

## Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `Dockerfile` | Build multi-stage: Builder → Nginx runtime |
| `nginx.conf` | Configuración de Nginx (SPA, proxy) |
| `.dockerignore` | Archivos a excluir del build |
| `.env.example` | Variables de entorno de ejemplo |

## Build

### Local (sin Docker)
```bash
pnpm install
pnpm build
# Output: dist/
```

### Con Docker
```bash
docker build -t proto-tipo:latest .

# O con docker-compose
docker-compose build proto-tipo-frontend
```

## Ejecutar

### Docker standalone
```bash
docker run -p 5173:80 proto-tipo:latest
# Accede: http://localhost:5173
```

### Docker-compose (desde raíz del proyecto)
```bash
docker-compose up proto-tipo-frontend
```

### Con backend
```bash
docker-compose up
# Ambos servicios: frontend + backend
```

## Desarrollo

### Opción 1: Local (recomendado para desarrollo)
```bash
# Hot reload, cambios instantáneos
pnpm dev
# http://localhost:5173
```

### Opción 2: Docker con volumen (live reload)
```bash
docker run -v $(pwd):/app -p 5173:80 proto-tipo:latest
```

## Variables de Entorno

`.env.example`:
```
VITE_API_URL=/chat
VITE_APP_TITLE=T-Radar BandurrIA
```

**Usar en Docker**:
```bash
docker run -e VITE_API_URL=/chat -p 5173:80 proto-tipo:latest
```

## URLs Internas

En Docker:
- Proxy `/chat/*` → Backend (a través de Nginx)
- Healthz `/healthz` → 200 OK

En desarrollo local:
- `/chat/*` → `http://localhost:8000/chat/*`
- Proxy configurado en `vite.config.ts`

## Tamaño de Imagen

```
Builder stage (build):     ~600 MB
Runtime stage (Nginx):      ~80 MB (final)
```

Optimizaciones:
- Alpine Linux (no full OS)
- Nginx lightweight
- Solo archivos compilados en runtime

## Logs

```bash
# Ver logs en tiempo real
docker-compose logs -f proto-tipo-frontend

# Ver últimas 100 líneas
docker-compose logs --tail=100 proto-tipo-frontend
```

## Debugging

### Entrar al contenedor
```bash
docker exec -it proto-tipo-frontend sh
# Luego: ls -la /usr/share/nginx/html/
```

### Ver archivos compilados
```bash
docker exec proto-tipo-frontend ls -la /usr/share/nginx/html/
```

### Verificar config de Nginx
```bash
docker exec proto-tipo-frontend nginx -T
```

## Performance

- **Build time**: ~2-3 minutos (primera vez)
- **Startup**: ~2-3 segundos
- **Gzip compression**: Reducción ~70% en CSS/JS
- **Cache**: 1 año para assets (`*.js`, `*.css`)

## Producción

### Cambios recomendados en `nginx.conf`:

```nginx
# 1. Agregar HTTPS
listen 443 ssl;
ssl_certificate /etc/nginx/certs/cert.pem;
ssl_certificate_key /etc/nginx/certs/key.pem;

# 2. Security headers
add_header Strict-Transport-Security "max-age=31536000" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "SAMEORIGIN" always;

# 3. Rate limiting
limit_req_zone $binary_remote_addr zone=general:10m rate=10r/s;
limit_req zone=general burst=20;
```

### Multi-stage registry push

```bash
# Build
docker build -t registry.example.com/proto-tipo:v1.0 .

# Push
docker push registry.example.com/proto-tipo:v1.0

# Usar
docker pull registry.example.com/proto-tipo:v1.0
```

## Troubleshooting

### Puerto en uso
```bash
sudo lsof -i :5173
kill -9 <PID>
```

### Página en blanco
1. `docker-compose logs proto-tipo-frontend`
2. Verifica `/usr/share/nginx/html/index.html` existe
3. Reconstruye: `docker-compose build --no-cache`

### CORS error
1. Verifica nginx.conf → `/chat/` location
2. Asegúrate que Backend esté corriendo
3. Test: `curl http://localhost:8000/health`

### Build muy lento
```bash
# Usa caché de builder
docker-compose build --build-arg BUILDKIT_INLINE_CACHE=1

# O usa BuildKit
DOCKER_BUILDKIT=1 docker build .
```

## Próximas Mejoras

- [ ] Agregar HTTPS/SSL
- [ ] Health check mejorado
- [ ] Métricas de Prometheus
- [ ] Log aggregation
- [ ] CDN integration
- [ ] Service worker (PWA)

---

**Última actualización**: Enero 2026
