# Refactorización Frontend - Chat Integration

## Resumen de Cambios

Se ha refactorizado completamente el frontend `Prototipo/proto-tipo` para integrar el chatbot BandurrIA con el backend en `http://localhost:8000`.

## Archivos Modificados

### 1. ✨ **chatService.ts** (NUEVO)
**Ubicación**: `src/lib/chatService.ts`

Servicio TypeScript que encapsula toda la comunicación HTTP con el backend:

```typescript
// Core Functions
- sendMessage(message: string, sessionId: string): Promise<ChatResponse>
- getChatHistory(sessionId: string): Promise<ChatMessage[]>
- getOrCreateSessionId(): string
- generateSessionId(): string

// Types
- ChatRequest { message, session_id }
- ChatResponse { session_id, reply }
- ChatMessage { role, content, created_at }
```

**API Base**: `http://localhost:8000/chat`

### 2. 🔄 **BandurriaSidebar.vue** (REFACTORIZADO)
**Ubicación**: `src/components/BandurriaSidebar.vue`

**Cambios principales**:
- ✅ Eliminadas respuestas simuladas (mock data)
- ✅ Integración real con backend via `chatService.ts`
- ✅ Loading spinner durante espera de respuesta
- ✅ Manejo robusto de errores con mensajes descriptivos
- ✅ Persistencia de sesión en localStorage
- ✅ Auto-carga del historial al inicializar
- ✅ Nuevos iconos: `Loader2` y `AlertCircle` de lucide-vue-next
- ✅ Estados visuales mejorados (disabled, loading, error)

**Flujo de datos**:
```
User Input → sendMessage() 
  → sessionId + message 
  → chatSendMessage() 
  → API POST /chat/ 
  → response.reply 
  → UI render
```

### 3. 🔧 **vite.config.ts** (ACTUALIZADO)
**Ubicación**: `vite.config.ts`

Agregada configuración de proxy para desarrollo:

```typescript
server: {
  proxy: {
    '/chat': {
      target: 'http://localhost:8000',
      changeOrigin: true,
      rewrite: (path) => path,
    },
  },
}
```

**Propósito**: Evitar problemas de CORS durante desarrollo. En producción, el frontend se servirá desde la misma URL que el backend.

## Endpoints API Esperados

El backend DEBE exponer estos endpoints:

### POST /chat/
```
Request:
{
  "message": "usuario pregunta algo",
  "session_id": "session_1234567890_abc123"
}

Response (200 OK):
{
  "session_id": "session_1234567890_abc123",
  "reply": "respuesta del chatbot"
}
```

### GET /chat/history/{session_id}
```
Response (200 OK):
[
  {
    "role": "user",
    "content": "primer mensaje",
    "created_at": "2026-01-06T10:30:00"
  },
  {
    "role": "assistant",
    "content": "respuesta",
    "created_at": "2026-01-06T10:30:05"
  }
]
```

## Estados de UI

El componente ahora maneja 4 estados visuales:

### 1. Empty State (Inicial)
- Quick Ideas visibles
- Input habilitado
- Sin mensajes

### 2. Loading State
- Spinner en el botón de envío
- Textarea deshabilitado
- Mensaje "Procesando tu solicitud..."

### 3. Chat Active
- Mensajes visibles (usuario en naranja, bot en gris)
- Quick Ideas ocultas
- Scroll automático al último mensaje

### 4. Error State
- Alert rojo con mensaje de error
- Usuario puede reintentar
- Último mensaje de error mostrado

## Gestión de Sesiones

- **Primera visita**: Se genera nueva `session_id` con `generateSessionId()`
- **Subsecuentes**: Se recupera de localStorage via `getOrCreateSessionId()`
- **Persistencia**: localStorage key = `chatSessionId`
- **Historial**: Se carga automáticamente al montar el componente

## Cómo Probar

### Prerequisitos
- Backend corriendo: `http://localhost:8000`
- Frontend dev server: `http://localhost:5173`

### Pasos
1. Abre http://localhost:5173
2. Click en botón chat (mobile) o sidebar derecha (desktop)
3. Escribe: "hola"
4. Presiona Enter o click en botón envío
5. Espera respuesta del bot

### Esperado
- ✅ Mensaje aparece en naranja
- ✅ Spinner de carga visible
- ✅ Respuesta aparece en gris
- ✅ Mensajes persisten al recargar página (si sesión persiste)

## Cambios de Estructura (Breaking)

⚠️ **IMPORTANTE**: El componente anterior usaba datos simulados. Si el frontend ya estaba en uso:

- ❌ Las respuestas de mock ya no funcionan
- ✅ Ahora conecta al backend REAL
- ✅ El historial se guarda en la API

**Esto es intencional y esperado** - el chat era un prototipo, ahora es funcional.

## Configuración de Environment

No se requieren variables de environment. El endpoint está hardcodeado a:
```
http://localhost:8000/chat
```

Para cambiar en producción, edita `src/lib/chatService.ts` línea 7:
```typescript
const CHAT_API_URL = 'https://api.produccion.com/chat'
```

## Troubleshooting

| Problema | Causa | Solución |
|----------|-------|----------|
| "Error desconocido del servidor" | Backend no responde | Verifica `http://localhost:8000/docs` |
| CORS error en consola | Proxy no configurado | Reinicia `pnpm dev` |
| Sesión no persiste | localStorage deshabilitado | Abre DevTools → App → LocalStorage |
| Mensaje cuelga en "Procesando..." | Backend timeout | Aumenta timeout en chatService.ts |

## Pruebas Recomendadas

```bash
# 1. Verificar backend health
curl http://localhost:8000/health

# 2. Probar endpoint chat
curl -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "hola",
    "session_id": "test_123"
  }'

# 3. Cargar historial
curl http://localhost:8000/chat/history/test_123
```

## Próximas Mejoras Sugeridas

- [ ] Agregar soporte para archivos (upload)
- [ ] Indicador de "escribiendo..." del bot
- [ ] Búsqueda en historial de conversaciones
- [ ] Reacciones a mensajes (👍 👎)
- [ ] Exportar conversación como PDF
- [ ] Modo oscuro persistente
- [ ] Indicador de nueva sesión
- [ ] Límite de mensajes por sesión (si aplicable)

---

**Fecha**: Enero 6, 2026
**Actualizado por**: AI Agent
**Status**: ✅ Listo para testing
