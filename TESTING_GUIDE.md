# Chat Integration - End-to-End Testing Guide

## Tabla de Contenidos
1. [Setup Inicial](#setup-inicial)
2. [Test Cases](#test-cases)
3. [Debugging](#debugging)
4. [Performance](#performance)

## Setup Inicial

### Requerimientos
- Backend corriendo: `http://localhost:8000`
- Frontend corriendo: `http://localhost:5173`
- Browser moderno (Chrome, Firefox, Safari, Edge)
- LocalStorage habilitado (no estar en incognito/private)

### Verificación Rápida
```bash
# En una terminal, desde la raíz del proyecto:
bash test-integration.sh
```

Si todos los tests pasan, está listo para QA manual.

---

## Test Cases

### TC-001: Primera Visita - Session Creation
**Objetivo**: Verificar que se cree una nueva sesión en la primera visita

**Pasos**:
1. Abre DevTools (F12) → Application → Clear All
2. Navega a http://localhost:5173
3. Abre DevTools → Application → LocalStorage → localhost:5173
4. Verifica que exista clave `chatSessionId`

**Resultado esperado**: ✅ Key existe con formato `session_<timestamp>_<random>`

**Evidencia**: Screenshot de localStorage

---

### TC-002: Enviar Mensaje - Happy Path
**Objetivo**: Enviar un mensaje y recibir respuesta del bot

**Pasos**:
1. Haz click en botón de chat
2. Escribe: "Hola, ¿cómo estás?"
3. Presiona Enter
4. Espera respuesta

**Resultado esperado**:
- ✅ Mensaje "Hola, ¿cómo estás?" aparece en naranja (derecha)
- ✅ Spinner de carga aparece
- ✅ Respuesta del bot aparece en gris (izquierda)
- ✅ Respuesta es coherente y del backend (no fake)

**Evidencia**: Screenshot de conversación

---

### TC-003: Enviar Mensaje - Teclado (Enter)
**Objetivo**: Verificar que Enter envía el mensaje

**Pasos**:
1. Escribe en textarea: "test"
2. Presiona Shift+Enter (NO debe enviar)
3. Verifica que se agregue nueva línea
4. Presiona Enter sin Shift
5. Verifica que se envíe

**Resultado esperado**: ✅ Solo Enter (sin Shift) envía el mensaje

---

### TC-004: Historial Persistente
**Objetivo**: Verificar que el historial se guarde y cargue

**Pasos**:
1. Envía 3 mensajes distintos
2. Recarga la página (Ctrl+F5)
3. Verifica el chat nuevamente

**Resultado esperado**:
- ✅ Los 3 mensajes siguen visibles
- ✅ Misma `session_id` en localStorage
- ✅ Quick Ideas no aparecen (ya hay historial)

**Evidencia**: Screenshot antes y después del reload

---

### TC-005: Error Handling - Backend Offline
**Objetivo**: Verificar manejo graceful cuando backend no responde

**Pasos**:
1. Detén el backend
2. Envía un mensaje
3. Espera 3-5 segundos

**Resultado esperado**:
- ✅ Spinner desaparece
- ✅ Mensaje de error aparece (rojo)
- ✅ Error contiene detalles ("Connection refused", etc)
- ✅ Usuario puede reintentar (input habilitado)

**Evidencia**: Screenshot del error

---

### TC-006: Error Handling - Bad Request
**Objetivo**: Verificar manejo de errores del servidor

**Pasos**:
1. (Opcional) Modifica `chatService.ts` para enviar payload inválido
2. Envía un mensaje
3. Verifica respuesta del servidor

**Resultado esperado**:
- ✅ Alert de error visible
- ✅ Mensaje describe el error
- ✅ No hay crash en consola

---

### TC-007: Loading State
**Objetivo**: Verificar que el UI responda correctamente durante carga

**Pasos**:
1. Abre DevTools → Network
2. Throttle a "Slow 3G"
3. Envía un mensaje
4. Observa UI mientras carga

**Resultado esperado**:
- ✅ Textarea deshabilitado (disabled)
- ✅ Botón de envío muestra spinner
- ✅ Textarea tiene opacidad reducida
- ✅ User input no se procesa durante carga

---

### TC-008: Mobile Responsive
**Objetivo**: Verificar funcionamiento en pantalla móvil

**Pasos**:
1. Abre DevTools → Toggle device toolbar (Ctrl+Shift+M)
2. Elige iPhone 12
3. Click en botón de chat (esquina inferior derecha)
4. Envía un mensaje
5. Verifica que se vea bien en pantalla pequeña

**Resultado esperado**:
- ✅ Botón flotante visible
- ✅ Modal de chat cubre 80% de pantalla
- ✅ Scroll funciona dentro del chat
- ✅ Teclado no rompe layout (si es mobile real)

**Evidencia**: Screenshot en device móvil

---

### TC-009: Desktop Sidebar
**Objetivo**: Verificar funcionamiento en desktop (sidebar)

**Pasos**:
1. Redimensiona navegador a 1400px+
2. Verifica que sidebar derecho aparezca (no necesita click)
3. Envía un mensaje
4. Verifica UX

**Resultado esperado**:
- ✅ Sidebar visible permanentemente
- ✅ Responsive design correcto
- ✅ No hay scroll horizontal
- ✅ Mensajes visibles completos

---

### TC-010: Quick Ideas Interaction
**Objetivo**: Verificar que quick ideas funcionan

**Pasos**:
1. Abre chat en nueva sesión (limpia localStorage)
2. Verifica que 3 quick ideas aparezcan
3. Click en "Analizar Tendencias"
4. Espera respuesta

**Resultado esperado**:
- ✅ Quick ideas desaparecen
- ✅ Mensaje de la idea aparece como user message
- ✅ Bot responde
- ✅ No aparecen quick ideas de nuevo

---

### TC-011: Session Isolation
**Objetivo**: Verificar que diferentes sessiones no compartan historial

**Pasos**:
1. Limpia localStorage
2. Envía mensaje 1: "Session A"
3. Envía mensaje 2: "Session B"  
4. Copia `session_id` de localStorage
5. Abre nueva pestaña (private/incognito)
6. Navega a http://localhost:5173
7. Modifica localStorage para usar session_id anterior (CTRL+SHIFT+K)
8. Recarga

**Resultado esperado**:
- ✅ Historial se carga correctamente
- ✅ Session A y B separadas
- ✅ No hay mezcla de mensajes

---

### TC-012: Long Messages
**Objetivo**: Verificar que mensajes largos se manejen

**Pasos**:
1. Genera mensaje de 500+ caracteres
2. Cópialo al chat
3. Envía
4. Espera respuesta

**Resultado esperado**:
- ✅ Mensaje aparece sin truncarse visualmente
- ✅ Texto envuelto correctamente
- ✅ Backend lo procesa sin error

---

## Debugging

### Problema: Spinner infinito
```
Síntoma: Mensaje stuck en "Procesando tu solicitud..."
Solución:
1. Abre DevTools → Network
2. Verifica si request a /chat/ llegó al servidor
3. Verifica status code (200 = OK, 5xx = error backend)
4. Si timeout, aumenta timeout en chatService.ts:
   const timeout = 30000; // ms
```

### Problema: Mensaje no aparece
```
Síntoma: Escribe mensaje, no aparece
Solución:
1. Abre Console (DevTools)
2. Verifica si hay errores rojos
3. Verifica que inputValue.trim() no esté vacío
4. Verifica que isLoadingMessage = false
```

### Problema: Historia no carga
```
Síntoma: Recargo página, no hay mensajes previos
Solución:
1. Abre localStorage:
   localStorage.getItem('chatSessionId')
2. Verifica que devuelva algo (no null)
3. Prueba manualmente:
   curl http://localhost:8000/chat/history/{session_id}
4. Verifica formato de respuesta
```

### Problema: CORS Error
```
Síntoma: Error en Console: "Access to XMLHttpRequest blocked by CORS"
Solución:
1. Verifica backend CORS config (Prototipo Backend/app/core/config.py)
2. Asegúrate que localhost:5173 esté en CORS_ORIGINS
3. Si dev, reinicia vite dev server
```

---

## Performance

### Métricas Objetivo
| Métrica | Target | Cómo Medir |
|---------|--------|-----------|
| Time to First Chat | < 2s | DevTools → Performance |
| Send Message → Response | < 5s | Browser DevTools → Network |
| History Load | < 1s | Network → /history |
| Scroll Responsiveness | 60 FPS | DevTools → Performance → Record |

### Cómo medir
```javascript
// En Console:
console.time('send-message');
// ... envía mensaje ...
console.timeEnd('send-message');
```

### Optimizaciones Posibles
- [ ] Virtualizar lista de mensajes si > 100 msgs
- [ ] Lazy load historial (pagination)
- [ ] Debounce input para prevenir multiple sends
- [ ] Caché de sesiones recientes

---

## Sign-Off Checklist

Antes de dar por aprobado el integration test:

- [ ] TC-001 pasó (session creation)
- [ ] TC-002 pasó (happy path)
- [ ] TC-005 pasó (error handling)
- [ ] TC-007 pasó (loading states)
- [ ] TC-008 pasó (mobile responsive)
- [ ] TC-009 pasó (desktop sidebar)
- [ ] No hay errores en console
- [ ] LocalStorage funciona
- [ ] Performance dentro de target
- [ ] UX es smooth (no lag)

**Firma**:
```
Tester: ________________
Fecha: ________________
Resultado: ✅ APROBADO / ❌ FALLIDO
```

---

**Documento**: Chat Integration QA
**Versión**: 1.0
**Fecha**: Enero 2026
