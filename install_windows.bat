@echo off
REM ========================================
REM RPA Tô Segurado - Instalação Windows
REM ========================================
REM Script de instalação automatizada
REM Execute como Administrador se necessário

echo.
echo ========================================
echo    RPA Tô Segurado - Instalação
echo ========================================
echo.

REM Verificar se Python está instalado
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo Por favor, instale Python 3.8+ de: https://www.python.org/downloads/
    echo Marque "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)
echo ✅ Python encontrado
python --version

REM Verificar se pip está disponível
echo.
echo [2/6] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip não encontrado!
    echo Reinstale Python marcando "Add Python to PATH"
    pause
    exit /b 1
)
echo ✅ pip encontrado

REM Criar ambiente virtual
echo.
echo [3/6] Criando ambiente virtual...
if exist "venv" (
    echo ⚠️ Ambiente virtual já existe, removendo...
    rmdir /s /q "venv"
)
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Erro ao criar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual criado

REM Ativar ambiente virtual
echo.
echo [4/6] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ Erro ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual ativado

REM Instalar dependências
echo.
echo [5/6] Instalando dependências...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências
    echo Tente executar manualmente: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✅ Dependências instaladas

REM Verificar ChromeDriver
echo.
echo [6/6] Verificando ChromeDriver...
if not exist "chromedriver\chromedriver-win64\chromedriver.exe" (
    echo ⚠️ ChromeDriver não encontrado!
    echo.
    echo 📥 Baixe o ChromeDriver de: https://chromedriver.chromium.org/
    echo 📁 Extraia para: .\chromedriver\chromedriver-win64\
    echo.
    echo Estrutura esperada:
    echo chromedriver\
    echo └── chromedriver-win64\
    echo     └── chromedriver.exe
    echo.
) else (
    echo ✅ ChromeDriver encontrado
)

REM Finalização
echo.
echo ========================================
echo    ✅ INSTALAÇÃO CONCLUÍDA!
echo ========================================
echo.
echo 🚀 Para executar o RPA:
echo 1. Ative o ambiente virtual: venv\Scripts\activate
echo 2. Execute: python executar_todas_telas_corrigido.py
echo.
echo 📚 Consulte o README.md para mais informações
echo.
pause
