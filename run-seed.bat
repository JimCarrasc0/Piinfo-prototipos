@echo off
REM Ejecutar seed_dummy_data manualmente
REM Esto carga datos de prueba en la base de datos

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Chat-Bot - Seed Dummy Data
echo ==========================================
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo. ERROR: Docker no esta instalado o no esta en PATH
    pause
    exit /b 1
)

echo [STEP 1] Building chat-bot image...
docker build -t tradar-chatbot:seed ./chat-bot
if errorlevel 1 (
    echo. ERROR: Build fallido
    pause
    exit /b 1
)

echo.
echo [STEP 2] Running seed script...
echo.   Esto puede tomar 1-2 minutos (descargando modelo por primera vez)...
docker run --rm ^
  -v ./chat-bot/data:/app/data ^
  -v %USERPROFILE%\.cache\huggingface:/root/.cache/huggingface ^
  --env-file ./chat-bot/.env ^
  tradar-chatbot:seed ^
  python -m scripts.seed_dummy_data

if errorlevel 1 (
    echo. ERROR: Seed fallido
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Seed completado exitosamente
echo ==========================================
echo.
echo Datos cargados en: ./chat-bot/data/chatbot.db
echo.
pause
