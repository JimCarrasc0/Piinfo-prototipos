#!/bin/bash

# Start Piinfo-Prototipos with Docker
# NOTA: Seed removido - ejecutar manualmente si necesitas cargar datos de prueba
# Este script inicia todos los servicios usando docker-compose

set -e

echo "=========================================="
echo "Piinfo-Prototipos - Docker Startup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose no está instalado"
    exit 1
fi

echo -e "${BLUE}[INFO]${NC} Docker version: $(docker --version)"
echo -e "${BLUE}[INFO]${NC} docker-compose version: $(docker-compose --version)"
echo ""

# Build images
echo -e "${YELLOW}[STEP 1]${NC} Building images..."
docker-compose build

echo ""

# Start services
echo -e "${YELLOW}[STEP 2]${NC} Starting services..."
docker-compose up -d

echo ""

# Wait for services to be ready
echo -e "${YELLOW}[STEP 3]${NC} Waiting for services to be ready..."

# Backend health check
echo -n "  Backend..."
for i in {1..30}; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo -e " ${GREEN}✓${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

# Frontend health check
echo -n "  Frontend..."
for i in {1..10}; do
    if curl -s http://localhost:5173/healthz > /dev/null 2>&1; then
        echo -e " ${GREEN}✓${NC}"
        break
    fi
    echo -n "."
    sleep 1
done

echo ""
echo "=========================================="
echo -e "${GREEN}✅ SERVICIOS INICIADOS${NC}"
echo "=========================================="
echo ""
echo "URLs disponibles:"
echo -e "  🌐 Frontend:          ${BLUE}http://localhost:5173${NC}"
echo -e "  🤖 Backend API:       ${BLUE}http://localhost:8000${NC}"
echo -e "  📚 API Docs:          ${BLUE}http://localhost:8000/docs${NC}"
echo -e "  🏥 Health Check:      ${BLUE}http://localhost:8000/health${NC}"
echo ""
echo "Comandos útiles:"
echo "  Ver logs:         docker-compose logs -f"
echo "  Parar servicios:  docker-compose down"
echo "  Parar todo:       docker-compose down -v"
echo ""
