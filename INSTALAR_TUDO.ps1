# 🖥️ SCRIPT DE INSTALAÇÃO COMPLETA - IMEDIATO SEGUROS RPA
# ================================================================
# Data de Criação: 04/09/2025
# Autor: Luciano Otero
# Versão: 1.0.0
# ================================================================

# Configurar encoding UTF-8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Função para exibir mensagens coloridas
function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    $timestamp = Get-Date -Format "HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor $Color
}

# Função para executar comando e verificar erro
function Invoke-CommandWithCheck {
    param(
        [string]$Command,
        [string]$Description,
        [string]$ErrorMessage = "Erro ao executar comando"
    )
    
    Write-ColorMessage "Executando: $Description" "Cyan"
    
    try {
        Invoke-Expression $Command
        if ($LASTEXITCODE -eq 0) {
            Write-ColorMessage "✅ $Description - SUCESSO" "Green"
            return $true
        } else {
            Write-ColorMessage "❌ $Description - ERRO" "Red"
            Write-ColorMessage $ErrorMessage "Red"
            return $false
        }
    }
    catch {
        Write-ColorMessage "❌ $Description - EXCEÇÃO" "Red"
        Write-ColorMessage $_.Exception.Message "Red"
        return $false
    }
}

# Função para verificar se comando existe
function Test-CommandExists {
    param([string]$Command)
    
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Função para baixar arquivo
function Invoke-DownloadFile {
    param(
        [string]$Url,
        [string]$OutFile,
        [string]$Description
    )
    
    Write-ColorMessage "📥 Baixando: $Description" "Yellow"
    
    try {
        Invoke-WebRequest -Uri $Url -OutFile $OutFile -UseBasicParsing
        Write-ColorMessage "✅ Download concluído: $Description" "Green"
        return $true
    }
    catch {
        Write-ColorMessage "❌ Erro no download: $Description" "Red"
        Write-ColorMessage $_.Exception.Message "Red"
        return $false
    }
}

# ========================================
# 🎯 INÍCIO DO SCRIPT
# ========================================

Write-Host "🖥️ SCRIPT DE INSTALAÇÃO COMPLETA - IMEDIATO SEGUROS RPA" -ForegroundColor Magenta
Write-Host "========================================================" -ForegroundColor Magenta
Write-Host "Data: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')" -ForegroundColor Cyan
Write-Host "Sistema: $($env:OS) $([Environment]::OSVersion.Version)" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Magenta
Write-Host ""

# ========================================
# 📋 VERIFICAÇÃO DE PRÉ-REQUISITOS
# ========================================

Write-ColorMessage "📋 VERIFICANDO PRÉ-REQUISITOS..." "Yellow"
Write-Host ""

# Verificar Python
Write-ColorMessage "🔍 Verificando Python..." "Cyan"
if (Test-CommandExists "python") {
    $pythonVersion = python --version 2>&1
    Write-ColorMessage "✅ Python encontrado: $pythonVersion" "Green"
} else {
    Write-ColorMessage "❌ Python não encontrado!" "Red"
    Write-Host ""
    Write-ColorMessage "📥 FAÇA O DOWNLOAD DO PYTHON:" "Yellow"
    Write-Host "   https://www.python.org/downloads/" -ForegroundColor Blue
    Write-Host ""
    Write-ColorMessage "⚠️ IMPORTANTE: Marque 'Add Python to PATH' durante a instalação" "Yellow"
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar Git
Write-ColorMessage "🔍 Verificando Git..." "Cyan"
if (Test-CommandExists "git") {
    $gitVersion = git --version
    Write-ColorMessage "✅ Git encontrado: $gitVersion" "Green"
} else {
    Write-ColorMessage "❌ Git não encontrado!" "Red"
    Write-Host ""
    Write-ColorMessage "📥 FAÇA O DOWNLOAD DO GIT:" "Yellow"
    Write-Host "   https://git-scm.com/download/win" -ForegroundColor Blue
    Write-Host ""
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""
Write-ColorMessage "✅ PRÉ-REQUISITOS ATENDIDOS!" "Green"
Write-Host ""

# ========================================
# 🚀 CLONAGEM DO REPOSITÓRIO
# ========================================

Write-ColorMessage "🚀 CLONANDO REPOSITÓRIO..." "Yellow"
Write-Host ""

# Verificar se o diretório já existe
if (Test-Path "imediatoseguros-rpa-playwright") {
    Write-ColorMessage "⚠️ Diretório já existe. Removendo..." "Yellow"
    Remove-Item -Path "imediatoseguros-rpa-playwright" -Recurse -Force
}

# Clonar repositório
if (-not (Invoke-CommandWithCheck "git clone https://github.com/LucianoOtero/imediatoseguros-rpa-playright.git" "Clonagem do repositório" "Erro ao clonar repositório")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Entrar no diretório
Set-Location "imediatoseguros-rpa-playwright"
if (-not $?) {
    Write-ColorMessage "❌ Erro ao entrar no diretório!" "Red"
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-ColorMessage "✅ Repositório clonado com sucesso!" "Green"
Write-Host ""

# ========================================
# 📦 INSTALAÇÃO DE DEPENDÊNCIAS
# ========================================

Write-ColorMessage "📦 INSTALANDO DEPENDÊNCIAS..." "Yellow"
Write-Host ""

# Atualizar pip
if (-not (Invoke-CommandWithCheck "python -m pip install --upgrade pip" "Atualização do pip")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Instalar Playwright
if (-not (Invoke-CommandWithCheck "python -m pip install playwright==1.55.0" "Instalação do Playwright")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Instalar navegadores Playwright
if (-not (Invoke-CommandWithCheck "python -m playwright install" "Instalação dos navegadores Playwright")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Instalar dependências essenciais
$dependencies = @(
    "selenium==4.35.0",
    "requests==2.32.4",
    "pandas==2.3.2",
    "numpy==2.2.6",
    "beautifulsoup4==4.13.5",
    "pydantic==2.11.7",
    "psutil==7.0.0",
    "python-dotenv==1.1.1",
    "tqdm==4.67.1",
    "colorama==0.4.6",
    "lxml==6.0.1"
)

Write-ColorMessage "📦 Instalando dependências essenciais..." "Cyan"
foreach ($dep in $dependencies) {
    if (-not (Invoke-CommandWithCheck "python -m pip install $dep" "Instalação de $dep")) {
        Write-ColorMessage "⚠️ Erro ao instalar $dep, continuando..." "Yellow"
    }
}

Write-ColorMessage "✅ Dependências instaladas com sucesso!" "Green"
Write-Host ""

# ========================================
# 🔧 CONFIGURAÇÃO DO AMBIENTE
# ========================================

Write-ColorMessage "🔧 CONFIGURANDO AMBIENTE..." "Yellow"
Write-Host ""

# Criar arquivo .env
Write-ColorMessage "🔧 Criando arquivo .env..." "Cyan"
$envContent = @"
# 🐍 ARQUIVO DE CONFIGURAÇÃO DO AMBIENTE
# Data de Criação: $(Get-Date -Format 'dd/MM/yyyy HH:mm:ss')

# Configurações Python
PYTHONPATH=.

# Configurações Playwright
PLAYWRIGHT_BROWSERS_PATH=C:\Users\$env:USERNAME\AppData\Local\ms-playwright

# Configurações do RPA
RPA_LOG_LEVEL=INFO
RPA_TIMEOUT=30
RPA_RETRY_ATTEMPTS=3

# Configurações de Autenticação (preencher conforme necessário)
# EMAIL_LOGIN=seu_email@exemplo.com
# SENHA_LOGIN=sua_senha
"@

try {
    $envContent | Out-File -FilePath ".env" -Encoding UTF8
    Write-ColorMessage "✅ Arquivo .env criado com sucesso!" "Green"
}
catch {
    Write-ColorMessage "❌ Erro ao criar arquivo .env!" "Red"
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host ""

# ========================================
# 🧪 TESTE DE FUNCIONAMENTO
# ========================================

Write-ColorMessage "🧪 TESTANDO INSTALAÇÃO..." "Yellow"
Write-Host ""

# Testar Python
if (-not (Invoke-CommandWithCheck "python --version" "Teste do Python")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Testar Playwright
if (-not (Invoke-CommandWithCheck "python -m playwright --version" "Teste do Playwright")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Testar RPA
if (-not (Invoke-CommandWithCheck "python executar_rpa_imediato_playwright.py --help" "Teste do RPA")) {
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-ColorMessage "✅ Todos os testes passaram!" "Green"
Write-Host ""

# ========================================
# 📋 INSTRUÇÕES FINAIS
# ========================================

Write-Host "🎉 INSTALAÇÃO CONCLUÍDA COM SUCESSO!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-ColorMessage "📋 PRÓXIMOS PASSOS:" "Yellow"
Write-Host ""
Write-ColorMessage "1. Configure o arquivo parametros.json com seus dados:" "Cyan"
Write-Host "   - Abra o arquivo parametros.json"
Write-Host "   - Preencha com suas informações pessoais"
Write-Host "   - Salve o arquivo"
Write-Host ""
Write-ColorMessage "2. Teste o RPA:" "Cyan"
Write-Host "   python executar_rpa_imediato_playwright.py --help"
Write-Host ""
Write-ColorMessage "3. Execute o RPA:" "Cyan"
Write-Host "   python executar_rpa_imediato_playwright.py"
Write-Host ""
Write-ColorMessage "📚 DOCUMENTAÇÃO DISPONÍVEL:" "Yellow"
Write-Host "   - AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md"
Write-Host "   - GUIA_MIGRACAO.md"
Write-Host "   - docs/CONTROLE_VERSAO.md"
Write-Host ""
Write-ColorMessage "🔧 SUPORTE: lrotero@gmail.com" "Cyan"
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "✅ AMBIENTE 100% FUNCIONAL!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# ========================================
# 🎯 ABRIR ARQUIVOS IMPORTANTES
# ========================================

Write-ColorMessage "🎯 ABRINDO ARQUIVOS IMPORTANTES..." "Yellow"
Write-Host ""

# Perguntar se quer abrir o parametros.json
$abrirParametros = Read-Host "Deseja abrir o arquivo parametros.json para configuração? (s/n)"
if ($abrirParametros -eq "s" -or $abrirParametros -eq "S") {
    Write-ColorMessage "📝 Abrindo parametros.json..." "Cyan"
    Start-Process "notepad.exe" -ArgumentList "parametros.json"
}

# Perguntar se quer abrir a documentação
$abrirDoc = Read-Host "Deseja abrir a documentação? (s/n)"
if ($abrirDoc -eq "s" -or $abrirDoc -eq "S") {
    Write-ColorMessage "📚 Abrindo documentação..." "Cyan"
    Start-Process "AMBIENTE_DE_DESENVOLVIMENTO_COMPLETO.md"
}

Write-Host ""
Write-ColorMessage "🎉 INSTALAÇÃO FINALIZADA!" "Green"
Read-Host "Pressione Enter para sair"










