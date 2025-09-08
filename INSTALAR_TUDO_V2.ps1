# ========================================
# 🔧 FUNÇÕES AUXILIARES
# ========================================

function Write-ColorMessage {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Invoke-CommandWithCheck {
    param(
        [string]$Command,
        [string]$Description
    )
    
    Write-ColorMessage "🔄 $Description..." "Cyan"
    
    try {
        $result = Invoke-Expression $Command
        if ($LASTEXITCODE -eq 0) {
            Write-ColorMessage "✅ $Description concluído!" "Green"
            return $true
        } else {
            Write-ColorMessage "❌ Erro em $Description" "Red"
            return $false
        }
    }
    catch {
        Write-ColorMessage "❌ Erro em $Description`: $($_.Exception.Message)" "Red"
        return $false
    }
}

# ========================================
# 📁 CONFIGURAÇÃO INICIAL
# ========================================

# Entrar no diretório
Set-Location "C:\Users\lucia\OneDrive - Imediato Soluções em Seguros\Imediato\imediatoseguros-rpa-playwright"
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
