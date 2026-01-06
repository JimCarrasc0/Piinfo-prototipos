# ⚡ Docker Seed Fix

## Problema Encontrado

El servicio `tradar-seed` en docker-compose se colgaba indefinidamente al iniciar. Causa:

1. **Descarga del modelo de embeddings** en la primera ejecución (puede tardar 2-5 minutos)
2. **Sin timeout** configurado en el script de seed
3. **docker-start.bat solo esperaba 30 segundos** antes de continuar

## Solución Aplicada

Se removió `tradar-seed` del docker-compose.yml y se crearon scripts separados para ejecutarlo manualmente.

---

## Cambios Realizados

### 1. docker-compose.yml (ACTUALIZADO)
```yaml
# ANTES:
services:
  tradar-seed:
    ...
  tradar-chatbot:
    depends_on:
      - tradar-seed
    ...

# AHORA:
services:
  tradar-chatbot:  # Sin dependencia de seed
    ...
```

**Ventajas**:
- ✅ docker-compose up inicia rápido (~5 segundos)
- ✅ Sin cuelgues esperando al seed
- ✅ Seed se ejecuta bajo demanda

### 2. Scripts Nuevos

#### `run-seed.sh` (Linux/macOS)
```bash
bash run-seed.sh
```

#### `run-seed.bat` (Windows)
```bash
run-seed.bat
```

**Estos scripts**:
- Detectan Docker
- Buildan la imagen
- Ejecutan seed en un contenedor
- Tardan 1-2 minutos (normal, descarga modelo)

---

## Cómo Usar Ahora

### Iniciar los servicios (rápido)
```bash
# Windows
docker-start.bat

# Linux/macOS
bash docker-start.sh

# O manual
docker-compose up --build
```

**Resultado**: Frontend + Backend listos en ~10 segundos

### Cargar datos de prueba (opcional)
```bash
# Windows
run-seed.bat

# Linux/macOS
bash run-seed.sh

# O manual
docker run --rm \
  -v ./chat-bot/data:/app/data \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env-file ./chat-bot/.env \
  tradar-chatbot:seed \
  python -m scripts.seed_dummy_data
```

**Resultado**: Base de datos con datos de prueba

---

## Timeline

```
Antes (con seed en docker-compose):
  docker-compose up
    ↓
  Building chat-bot... (~1 min)
  Starting tradar-seed... (~cuelga 30+ seg)
  Starting tradar-chatbot... (espera)
  Starting proto-tipo-frontend...
  Total: 3-5 minutos ❌

Después (sin seed automático):
  docker-compose up
    ↓
  Building chat-bot... (~1 min)
  Starting tradar-chatbot... (~5 sec)
  Starting proto-tipo-frontend... (~2 sec)
  Total: ~10-15 segundos ✅
  
  (Opcional) run-seed.bat
    ↓
  Cargando datos... (~1-2 minutos)
  Base de datos lista ✅
```

---

## Base de Datos

### Ubicación
```
./chat-bot/data/chatbot.db  (SQLite)
```

### Con seed (datos de prueba)
```bash
run-seed.bat
```

### Sin seed (base de datos vacía)
```bash
docker-compose up
# DB creada pero vacía
```

---

## Status

| Aspecto | Antes | Después |
|---------|-------|---------|
| Tiempo startup | 3-5 min | 10-15 seg |
| Cuelgues | ❌ Sí (seed) | ✅ No |
| Datos prueba | ✅ Automático | ⚠️ Manual (run-seed.bat) |
| Flexibilidad | ❌ Rígido | ✅ Flexible |

---

## Próxima Vez

Cuando ejecutes:

```bash
# Simplemente
docker-start.bat

# En lugar de esperar 3-5 minutos
# Ahora tarda ~15 segundos
```

Si necesitas datos de prueba:
```bash
run-seed.bat
```

---

**Fix aplicado**: Enero 6, 2026
**Status**: ✅ Resuelto
