@echo off
REM Start Piinfo-Prototipos with Docker (Windows)
REM NOTA: Seed removido - ejecutar manualmente si necesitas cargar datos de prueba

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo Piinfo-Prototipos - Docker Startup
echo ==========================================
echo.

REM Check Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo. ERROR: Docker no esta instalado o no esta en PATH
    pause
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo. ERROR: docker-compose no esta instalado
    pause
    exit /b 1
)

echo [INFO] Docker version:
docker --version
echo [INFO] docker-compose version:
docker-compose --version
echo.

REM Build images
echo [STEP 1] Building images...
docker-compose build
if errorlevel 1 (
    echo. ERROR: Build fallido
    pause
    exit /b 1
)

echo.

REM Start services
echo [STEP 2] Starting services...
docker-compose up -d
if errorlevel 1 (
    echo. ERROR: No se pudieron iniciar los servicios
    pause
    exit /b 1
)

echo.

REM Wait for services
echo [STEP 3] Waiting for services...

set RETRIES=30
set "COUNTER=0"
echo.  Backend...
:wait_backend
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 0 (
    echo  ^OK
    goto wait_frontend
)
set /a COUNTER+=1
if %COUNTER% lss %RETRIES% (
    timeout /t 1 /nobreak >nul
    goto wait_backend
)

:wait_frontend
set COUNTER=0
echo.  Frontend...
:wait_frontend_loop
curl -s http://localhost:5173/healthz >nul 2>&1
if errorlevel 0 (
    echo  ^OK
    goto done
)
set /a COUNTER+=1
if %COUNTER% lss 10 (
    timeout /t 1 /nobreak >nul
    goto wait_frontend_loop
)

:done
echo.
echo ==========================================
echo Servicios iniciados exitosamente
echo ==========================================
echo.
echo URLs disponibles:
echo.   Frontend:          http://localhost:5173
echo.   Backend API:       http://localhost:8000
echo.   API Docs:          http://localhost:8000/docs
echo.   Health Check:      http://localhost:8000/health
echo.
echo Comandos utiles:
echo.   Ver logs:         docker-compose logs -f
echo.   Parar servicios:  docker-compose down
echo.   Parar todo:       docker-compose down -v
echo.
pause
