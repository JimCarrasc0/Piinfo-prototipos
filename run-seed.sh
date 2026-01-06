#!/bin/bash

# Ejecutar seed_dummy_data manualmente
# Esto carga datos de prueba en la base de datos

echo "=========================================="
echo "Chat-Bot - Seed Dummy Data"
echo "=========================================="
echo ""

if ! command -v docker &> /dev/null; then
    echo "❌ Docker no está instalado"
    exit 1
fi

echo "[STEP 1] Building chat-bot image..."
docker build -t tradar-chatbot:seed ./chat-bot

echo ""
echo "[STEP 2] Running seed script..."
echo "  Esto puede tomar 1-2 minutos (descargando modelo por primera vez)..."
docker run --rm \
  -v ./chat-bot/data:/app/data \
  -v ~/.cache/huggingface:/root/.cache/huggingface \
  --env-file ./chat-bot/.env \
  tradar-chatbot:seed \
  python -m scripts.seed_dummy_data

echo ""
echo "=========================================="
echo "✅ Seed completado exitosamente"
echo "=========================================="
echo ""
echo "Datos cargados en: ./chat-bot/data/chatbot.db"
echo ""
