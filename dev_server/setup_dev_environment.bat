@echo off
echo 🚀 CONFIGURANDO AMBIENTE DE DESENVOLVIMENTO - RPA IMEDIATO SEGUROS
echo.

REM Criar estrutura de diretórios
echo 📁 Criando estrutura de diretórios...
if not exist "dev_server" mkdir dev_server
if not exist "dev_server\frontend" mkdir dev_server\frontend
if not exist "dev_server\backend" mkdir dev_server\backend
if not exist "dev_server\backend\api" mkdir dev_server\backend\api
if not exist "dev_server\backend\rpa" mkdir dev_server\backend\rpa
if not exist "dev_server\backend\logs" mkdir dev_server\backend\logs
if not exist "dev_server\scripts" mkdir dev_server\scripts

echo ✅ Estrutura de diretórios criada!
echo.

REM Verificar Python
echo 🐍 Verificando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado! Instale Python 3.8+ primeiro.
    pause
    exit /b 1
)

REM Verificar se Playwright está instalado
echo 🎭 Verificando Playwright...
python -c "import playwright; print('Playwright OK')" 2>nul
if %errorlevel% neq 0 (
    echo 📦 Instalando Playwright...
    pip install playwright
    python -m playwright install chromium
)

REM Instalar dependências Python
echo 📦 Instalando dependências Python...
pip install flask flask-cors redis requests psutil python-dotenv

echo.
echo ✅ Ambiente de desenvolvimento configurado!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo 1. Execute: dev_server\scripts\start_redis.bat
echo 2. Execute: dev_server\scripts\start_backend.bat
echo 3. Execute: dev_server\scripts\start_frontend.bat
echo.
pause























