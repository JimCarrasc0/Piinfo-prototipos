# Frontend - Chat Integration Guide

## Descripción General

El frontend en `Prototipo/proto-tipo` ha sido refactorizado para integrarse con el chatbot BandurrIA backend en `http://localhost:8000`.

## Archivos Modificados

### 1. **chatService.ts** (NUEVO)
Ubicación: `src/lib/chatService.ts`

Servicio que encapsula toda la comunicación HTTP con el backend:

```typescript
// Enviar mensaje al chatbot
await sendMessage(message: string, sessionId: string): Promise<ChatResponse>

// Obtener historial de chat
await getChatHistory(sessionId: string): Promise<ChatMessage[]>

// Gestión de sesiones
getOrCreateSessionId(): string
generateSessionId(): string
```

**Configuración**: Endpoint base es `http://localhost:8000/chat`

### 2. **BandurriaSidebar.vue** (REFACTORIZADO)
Ubicación: `src/components/BandurriaSidebar.vue`

Cambios principales:
- ✅ Integración con `chatService.ts`
- ✅ Estados de carga (loading spinner)
- ✅ Manejo de errores con mensajes amigables
- ✅ Persistencia de sesión en localStorage
- ✅ Carga automática del historial de chat
- ✅ Soporte para desktop y mobile

### 3. **vite.config.ts** (ACTUALIZADO)
Se agregó configuración de proxy para desarrollo:

```typescript
server: {
  proxy: {
    '/chat': {
      target: 'http://localhost:8000',
      changeOrigin: true,
    },
  },
}
```

Esto permite evitar problemas de CORS en desarrollo.

## API Endpoints Esperados

### 1. Enviar Mensaje
```
POST http://localhost:8000/chat/

Request:
{
  "message": "Mi pregunta al chatbot",
  "session_id": "session_1234567890_abcdef"
}

Response:
{
  "session_id": "session_1234567890_abcdef",
  "reply": "Respuesta del chatbot..."
}
```

### 2. Obtener Historial
```
GET http://localhost:8000/chat/history/{session_id}

Response:
[
  {
    "role": "user",
    "content": "Mi pregunta",
    "created_at": "2026-01-06T10:30:00"
  },
  {
    "role": "assistant",
    "content": "Respuesta del chatbot",
    "created_at": "2026-01-06T10:30:05"
  }
]
```

## Flujo de Ejecución

1. **Inicialización** (onMounted):
   - Se genera/recupera `session_id` de localStorage
   - Se carga el historial de chat anterior
   - Se muestran "Quick Ideas" si es la primera vez

2. **Envío de Mensaje** (sendMessage):
   - Usuario escribe mensaje y presiona Enter o click en botón
   - Mensaje se agrega a la UI como "user"
   - Se muestra spinner de carga
   - Se envía al backend via `chatSendMessage()`
   - Se recibe respuesta y se muestra como "bot"

3. **Errores**:
   - Si la request falla, se muestra alert de error
   - Se permite reintentar

## Cómo Ejecutar

### Terminal 1 - Chat Backend
```bash
cd chat-bot
docker compose up --build
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Terminal 2 - Frontend
```bash
cd Prototipo/proto-tipo
pnpm install  # Primera vez
pnpm dev      # Vite dev server en http://localhost:5173
```

### Verificar Integración
1. Abre http://localhost:5173 en el navegador
2. Click en el botón de chat (esquina inferior derecha en mobile, sidebar derecha en desktop)
3. Escribe un mensaje y presiona Enter
4. Deberías ver:
   - El mensaje aparece en naranja (user message)
   - Spinner de carga
   - Respuesta del chatbot en gris (bot message)

## Solución de Problemas

### Error: "Error desconocido del servidor"
**Causa**: Backend no está corriendo o URL es incorrecta
**Solución**: 
- Verifica que `http://localhost:8000` esté disponible
- Revisa la consola del navegador (DevTools) para más detalles

### Error: CORS
**Causa**: Backend no tiene CORS configurado para localhost:5173
**Solución**: 
- El proxy en vite.config.ts debería manejarlo en desarrollo
- En producción, asegúrate que el backend tenga CORS configurado

### Sesión no se persiste
**Causa**: localStorage puede estar deshabilitado o limpiado
**Solución**:
- Abre DevTools → Application → LocalStorage
- Verifica que exista `chatSessionId`

## Variables de Entorno

No se requieren variables de entorno especiales en el frontend. El endpoint es hardcodeado a `http://localhost:8000/chat`.

Para cambiar en producción, edita `src/lib/chatService.ts`:

```typescript
const CHAT_API_URL = 'http://tu-dominio.com:puerto/chat'
```

## Próximas Mejoras

- [ ] Soporte para múltiples archivos (upload)
- [ ] Exportar conversación como PDF
- [ ] Búsqueda en historial
- [ ] Temas oscuro/claro con persistencia
- [ ] Reacción a mensajes (thumbs up/down)
- [ ] Typing indicator (cuando el bot está "escribiendo")

---

**Última actualización**: Enero 2026
