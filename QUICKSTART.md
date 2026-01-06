# ⚡ Quick Start - Chat Frontend Integration

## 30 Segundos: Verificar que Funciona

```bash
# En terminal, desde raíz del proyecto
bash test-integration.sh
```

**Resultado esperado**: ✅ Todos los tests pasan

---

## 2 Minutos: Setup Completo

### Terminal 1 - Backend (Puerto 8000)
```bash
cd chat-bot
docker compose up --build
```

Espera hasta ver:
```
✓ Documentación en http://localhost:8000/docs
✓ Health check en http://localhost:8000/health
```

### Terminal 2 - Frontend (Puerto 5173)
```bash
cd Prototipo/proto-tipo
pnpm install
pnpm dev
```

Espera hasta ver:
```
VITE v7.3.0  ready in XXX ms

➜  Local:   http://localhost:5173/
```

### Terminal 3 - Navega a la App
```
Abre: http://localhost:5173
```

---

## Testing Manual - 1 Minuto

1. **Abre DevTools** (F12)
2. **LocalStorage Check**:
   - Applications → LocalStorage → localhost:5173
   - Busca: `chatSessionId` (debe existir)
   
3. **Chat Test**:
   - Click botón chat (mobile: esquina inferior derecha | desktop: sidebar derecha)
   - Escribe: "Hola"
   - Presiona: Enter
   
4. **Resultado Esperado**:
   - ✅ Mensaje aparece en naranja
   - ✅ Spinner de carga visible
   - ✅ Respuesta del bot en gris
   - ✅ Sin errores en Console

---

## Archivos Clave

| Archivo | Qué es | Dónde |
|---------|--------|-------|
| **chatService.ts** | Cliente HTTP → Backend | `src/lib/chatService.ts` |
| **BandurriaSidebar.vue** | Componente UI del chat | `src/components/BandurriaSidebar.vue` |
| **vite.config.ts** | Config dev (proxy) | `vite.config.ts` |

---

## API Endpoints (Backend debe tener estos)

### POST /chat/
```bash
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "hola",
    "session_id": "test_123"
  }'
```

### GET /chat/history/{session_id}
```bash
curl http://localhost:8000/chat/history/test_123
```

---

## Problema? Aquí están las Soluciones

| Síntoma | Solución |
|---------|----------|
| "Error desconocido del servidor" | Verifica: `curl http://localhost:8000/health` |
| CORS error en console | Reinicia: `pnpm dev` |
| Session no persiste | DevTools → Application → Storage: ¿Limpio localStorage? |
| Spinner infinito | Network tab → ¿Request llegó a /chat/? |
| Nada funciona | Ejecuta: `bash test-integration.sh` |

---

## Documentación Completa

- 📖 **Integración**: [CHAT_INTEGRATION.md](Prototipo/proto-tipo/CHAT_INTEGRATION.md)
- 🔬 **Testing**: [TESTING_GUIDE.md](TESTING_GUIDE.md)
- 🔧 **Detalles Técnicos**: [FRONTEND_REFACTOR.md](FRONTEND_REFACTOR.md)
- 📋 **Resumen**: [REFACTOR_SUMMARY.md](REFACTOR_SUMMARY.md)

---

**Status**: ✅ Listo para Testing  
**Última actualización**: Enero 2026  
**Tiempo estimado para full test**: 10 minutos
