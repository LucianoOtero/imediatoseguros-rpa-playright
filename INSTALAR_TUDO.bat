@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ========================================
REM 🖥️ SCRIPT DE INSTALAÇÃO COMPLETA - IMEDIATO SEGUROS RPA
REM ========================================
REM Data de Criação: 04/09/2025
REM Autor: Luciano Otero
REM Versão: 1.0.0
REM ========================================

echo.
echo 🖥️ SCRIPT DE INSTALAÇÃO COMPLETA - IMEDIATO SEGUROS RPA
echo ========================================================
echo Data: %date% %time%
echo Sistema: %OS%
echo ========================================================
echo.

REM ========================================
REM 📋 VERIFICAÇÃO DE PRÉ-REQUISITOS
REM ========================================

echo 📋 VERIFICANDO PRÉ-REQUISITOS...
echo.

REM Verificar se Python está instalado
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado!
    echo.
    echo 📥 FAÇA O DOWNLOAD DO PYTHON:
    echo    https://www.python.org/downloads/
    echo.
    echo ⚠️ IMPORTANTE: Marque "Add Python to PATH" durante a instalação
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
    echo ✅ Python encontrado: !PYTHON_VERSION!
)

REM Verificar se Git está instalado
echo 🔍 Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado!
    echo.
    echo 📥 FAÇA O DOWNLOAD DO GIT:
    echo    https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
) else (
    for /f "tokens=*" %%i in ('git --version 2^>^&1') do set GIT_VERSION=%%i
    echo ✅ Git encontrado: !GIT_VERSION!
)

echo.
echo ✅ PRÉ-REQUISITOS ATENDIDOS!
echo.

REM ========================================
REM 🚀 CLONAGEM DO REPOSITÓRIO
REM ========================================

echo 🚀 CLONANDO REPOSITÓRIO...
echo.

REM Verificar se o diretório já existe
if exist "imediatoseguros-rpa-playwright" (
    echo ⚠️ Diretório já existe. Removendo...
    rmdir /s /q "imediatoseguros-rpa-playwright"
)

REM Clonar repositório
echo 📥 Clonando repositório do GitHub...
git clone https://github.com/LucianoOtero/imediatoseguros-rpa-playright.git
if %errorlevel% neq 0 (
    echo ❌ Erro ao clonar repositório!
    echo Verifique sua conexão com a internet.
    pause
    exit /b 1
)

REM Entrar no diretório
cd imediatoseguros-rpa-playright
if %errorlevel% neq 0 (
    echo ❌ Erro ao entrar no diretório!
    pause
    exit /b 1
)

echo ✅ Repositório clonado com sucesso!
echo.

REM ========================================
REM 📦 INSTALAÇÃO DE DEPENDÊNCIAS
REM ========================================

echo 📦 INSTALANDO DEPENDÊNCIAS...
echo.

REM Atualizar pip
echo 🔧 Atualizando pip...
python -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo ❌ Erro ao atualizar pip!
    pause
    exit /b 1
)

REM Instalar Playwright
echo 🌐 Instalando Playwright...
python -m pip install playwright==1.55.0
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar Playwright!
    pause
    exit /b 1
)

REM Instalar navegadores Playwright
echo 🌐 Instalando navegadores Playwright...
python -m playwright install
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar navegadores!
    pause
    exit /b 1
)

REM Instalar outras dependências essenciais
echo 📦 Instalando dependências essenciais...
python -m pip install selenium==4.35.0 requests==2.32.4 pandas==2.3.2 numpy==2.2.6 beautifulsoup4==4.13.5 pydantic==2.11.7 psutil==7.0.0 python-dotenv==1.1.1 tqdm==4.67.1 colorama==0.4.6 lxml==6.0.1
if %errorlevel% neq 0 (
    echo ❌ Erro ao instalar dependências!
    pause
    exit /b 1
)

echo ✅ Dependências instaladas com sucesso!
echo.

REM ========================================
REM 🔧 CONFIGURAÇÃO DO AMBIENTE
REM ========================================

echo 🔧 CONFIGURANDO AMBIENTE...
echo.

REM Criar arquivo .env
echo 🔧 Criando arquivo .env...
(
echo # 🐍 ARQUIVO DE CONFIGURAÇÃO DO AMBIENTE
echo # Data de Criação: %date% %time%
echo.
echo # Configurações Python
echo PYTHONPATH=.
echo.
echo # Configurações Playwright
echo PLAYWRIGHT_BROWSERS_PATH=C:\Users\%USERNAME%\AppData\Local\ms-playwright
echo.
echo # Configurações do RPA
echo RPA_LOG_LEVEL=INFO
echo RPA_TIMEOUT=30
echo RPA_RETRY_ATTEMPTS=3
echo.
echo # Configurações de Autenticação ^(preencher conforme necessário^)
echo # EMAIL_LOGIN=seu_email@exemplo.com
echo # SENHA_LOGIN=sua_senha
) > .env

if %errorlevel% neq 0 (
    echo ❌ Erro ao criar arquivo .env!
    pause
    exit /b 1
)

echo ✅ Arquivo .env criado com sucesso!
echo.

REM ========================================
REM 🧪 TESTE DE FUNCIONAMENTO
REM ========================================

echo 🧪 TESTANDO INSTALAÇÃO...
echo.

REM Testar Python
echo 🔍 Testando Python...
python --version
if %errorlevel% neq 0 (
    echo ❌ Teste do Python falhou!
    pause
    exit /b 1
)

REM Testar Playwright
echo 🔍 Testando Playwright...
python -m playwright --version
if %errorlevel% neq 0 (
    echo ❌ Teste do Playwright falhou!
    pause
    exit /b 1
)

REM Testar RPA
echo 🔍 Testando RPA...
python executar_rpa_imediato_playwright.py --help >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Teste do RPA falhou!
    pause
    exit /b 1
)

echo ✅ Todos os testes passaram!
echo.

REM ========================================
REM 📋 INSTRUÇÕES FINAIS
REM ========================================

echo 🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!
echo ========================================
echo.
echo 📋 PRÓXIMOS PASSOS:
echo.
echo 1. Configure o arquivo parametros.json com seus dados:
echo    - Abra o arquivo parametros.json
echo    - Preencha com suas informações pessoais
echo    - Salve o arquivo
echo.
echo 2. Teste o RPA:
echo    python executar_rpa_imediato_playwright.py --help
echo.
echo 3. Execute o RPA:
echo    python executar_rpa_imediato_playwright.py
echo.
echo 📚 DOCUMENTAÇÃO DISPONÍVEL:
echo    - AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md
echo    - GUIA_MIGRACAO.md
echo    - docs/CONTROLE_VERSAO.md
echo.
echo 🔧 SUPORTE: lrotero@gmail.com
echo.
echo ========================================
echo ✅ AMBIENTE 100%% FUNCIONAL!
echo ========================================
echo.

REM ========================================
REM 🎯 ABRIR ARQUIVOS IMPORTANTES
REM ========================================

echo 🎯 ABRINDO ARQUIVOS IMPORTANTES...
echo.

REM Perguntar se quer abrir o parametros.json
set /p ABRIR_PARAMETROS="Deseja abrir o arquivo parametros.json para configuração? (s/n): "
if /i "!ABRIR_PARAMETROS!"=="s" (
    echo 📝 Abrindo parametros.json...
    notepad parametros.json
)

REM Perguntar se quer abrir a documentação
set /p ABRIR_DOC="Deseja abrir a documentação? (s/n): "
if /i "!ABRIR_DOC!"=="s" (
    echo 📚 Abrindo documentação...
    start AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md
)

echo.
echo 🎉 INSTALAÇÃO FINALIZADA!
echo Pressione qualquer tecla para sair...
pause >nul

endlocal










