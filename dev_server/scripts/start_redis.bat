@echo off
echo 🔴 INICIANDO REDIS PARA DESENVOLVIMENTO
echo.

REM Verificar se Redis está instalado
redis-server --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Redis não encontrado!
    echo 📥 Baixe e instale Redis para Windows:
    echo https://github.com/microsoftarchive/redis/releases
    echo.
    echo Ou use Docker:
    echo docker run -d -p 6379:6379 redis:alpine
    pause
    exit /b 1
)

echo 🚀 Iniciando Redis na porta 6379...
redis-server --port 6379 --maxmemory 100mb --maxmemory-policy allkeys-lru

pause























