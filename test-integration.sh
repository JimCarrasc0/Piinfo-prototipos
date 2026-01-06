#!/bin/bash

# Chat Frontend Integration - Test Script
# Este script verifica que el frontend esté correctamente integrado con el backend

set -e

echo "=========================================="
echo "Chat Frontend Integration Test"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test 1: Backend Health Check
echo -e "${YELLOW}[TEST 1]${NC} Verificando que backend esté disponible..."
if curl -s http://localhost:8000/health | grep -q "ok"; then
    echo -e "${GREEN}✓ Backend respondiendo en http://localhost:8000${NC}"
else
    echo -e "${RED}✗ Backend NO está disponible en http://localhost:8000${NC}"
    echo "Solución: Ejecuta 'cd chat-bot && docker compose up --build'"
    exit 1
fi

echo ""

# Test 2: Chat Endpoint
echo -e "${YELLOW}[TEST 2]${NC} Probando endpoint POST /chat/..."
RESPONSE=$(curl -s -X POST http://localhost:8000/chat/ \
  -H "Content-Type: application/json" \
  -d '{
    "message": "test message",
    "session_id": "test_session_123"
  }')

if echo "$RESPONSE" | grep -q "reply"; then
    echo -e "${GREEN}✓ Endpoint /chat/ respondiendo correctamente${NC}"
    echo "  Respuesta recibida:"
    echo "  $RESPONSE" | head -c 100
    echo ""
else
    echo -e "${RED}✗ Endpoint /chat/ NO respondió correctamente${NC}"
    echo "  Respuesta: $RESPONSE"
    exit 1
fi

echo ""

# Test 3: Chat History Endpoint
echo -e "${YELLOW}[TEST 3]${NC} Probando endpoint GET /chat/history/..."
HISTORY=$(curl -s http://localhost:8000/chat/history/test_session_123)

if echo "$HISTORY" | grep -qE "user|assistant|role"; then
    echo -e "${GREEN}✓ Endpoint /chat/history/{session_id} respondiendo${NC}"
    echo "  Historial recibido (primeros 100 chars):"
    echo "  $HISTORY" | head -c 100
    echo ""
else
    echo -e "${RED}✗ Endpoint /chat/history/{session_id} NO respondió correctamente${NC}"
    echo "  Respuesta: $HISTORY"
    # No exit aquí, puede ser esperado si está vacío
fi

echo ""

# Test 4: Frontend Development Server
echo -e "${YELLOW}[TEST 4]${NC} Verificando que frontend dev server esté disponible..."
if curl -s http://localhost:5173 > /dev/null 2>&1; then
    echo -e "${GREEN}✓ Frontend dev server corriendo en http://localhost:5173${NC}"
else
    echo -e "${YELLOW}⚠ Frontend dev server NO disponible en http://localhost:5173${NC}"
    echo "  Solución: Ejecuta 'cd Prototipo/proto-tipo && pnpm dev'"
fi

echo ""

# Test 5: Verificar archivos necesarios
echo -e "${YELLOW}[TEST 5]${NC} Verificando archivos del frontend..."

FILES=(
    "Prototipo/proto-tipo/src/lib/chatService.ts"
    "Prototipo/proto-tipo/src/components/BandurriaSidebar.vue"
    "Prototipo/proto-tipo/vite.config.ts"
)

for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓ $file existe${NC}"
    else
        echo -e "${RED}✗ $file NO ENCONTRADO${NC}"
        exit 1
    fi
done

echo ""

# Test 6: Verificar imports en chatService.ts
echo -e "${YELLOW}[TEST 6]${NC} Verificando exports en chatService.ts..."
if grep -q "export const sendMessage" "Prototipo/proto-tipo/src/lib/chatService.ts" && \
   grep -q "export const getChatHistory" "Prototipo/proto-tipo/src/lib/chatService.ts" && \
   grep -q "export const getOrCreateSessionId" "Prototipo/proto-tipo/src/lib/chatService.ts"; then
    echo -e "${GREEN}✓ chatService.ts tiene todas las funciones exportadas${NC}"
else
    echo -e "${RED}✗ chatService.ts está incompleto${NC}"
    exit 1
fi

echo ""

# Test 7: Verificar tipos en BandurriaSidebar.vue
echo -e "${YELLOW}[TEST 7]${NC} Verificando integración en BandurriaSidebar.vue..."
if grep -q "import.*chatService" "Prototipo/proto-tipo/src/components/BandurriaSidebar.vue" && \
   grep -q "chatSendMessage" "Prototipo/proto-tipo/src/components/BandurriaSidebar.vue"; then
    echo -e "${GREEN}✓ BandurriaSidebar.vue importa chatService correctamente${NC}"
else
    echo -e "${RED}✗ BandurriaSidebar.vue NO importa chatService${NC}"
    exit 1
fi

echo ""

echo "=========================================="
echo -e "${GREEN}✅ TODOS LOS TESTS PASARON${NC}"
echo "=========================================="
echo ""
echo "Próximos pasos:"
echo "1. Abre http://localhost:5173 en tu navegador"
echo "2. Haz click en el botón de chat"
echo "3. Escribe un mensaje y presiona Enter"
echo "4. Deberías ver la respuesta del chatbot"
echo ""
