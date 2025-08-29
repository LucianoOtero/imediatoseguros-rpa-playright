# ========================================
# RPA Tô Segurado - Instalação Windows
# ========================================
# Script PowerShell de instalação automatizada
# Execute como Administrador se necessário

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    RPA Tô Segurado - Instalação" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se Python está instalado
Write-Host "[1/6] Verificando Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Python encontrado" -ForegroundColor Green
        Write-Host $pythonVersion -ForegroundColor Gray
    } else {
        throw "Python não encontrado"
    }
} catch {
    Write-Host "❌ Python não encontrado!" -ForegroundColor Red
    Write-Host "Por favor, instale Python 3.8+ de: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Marque 'Add Python to PATH' durante a instalação" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar se pip está disponível
Write-Host ""
Write-Host "[2/6] Verificando pip..." -ForegroundColor Yellow
try {
    $pipVersion = pip --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ pip encontrado" -ForegroundColor Green
        Write-Host $pipVersion -ForegroundColor Gray
    } else {
        throw "pip não encontrado"
    }
} catch {
    Write-Host "❌ pip não encontrado!" -ForegroundColor Red
    Write-Host "Reinstale Python marcando 'Add Python to PATH'" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Criar ambiente virtual
Write-Host ""
Write-Host "[3/6] Criando ambiente virtual..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "⚠️ Ambiente virtual já existe, removendo..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force "venv"
}

try {
    python -m venv venv
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ambiente virtual criado" -ForegroundColor Green
    } else {
        throw "Erro ao criar ambiente virtual"
    }
} catch {
    Write-Host "❌ Erro ao criar ambiente virtual" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Ativar ambiente virtual
Write-Host ""
Write-Host "[4/6] Ativando ambiente virtual..." -ForegroundColor Yellow
try {
    & "venv\Scripts\Activate.ps1"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Ambiente virtual ativado" -ForegroundColor Green
    } else {
        throw "Erro ao ativar ambiente virtual"
    }
} catch {
    Write-Host "❌ Erro ao ativar ambiente virtual" -ForegroundColor Red
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Instalar dependências
Write-Host ""
Write-Host "[5/6] Instalando dependências..." -ForegroundColor Yellow
try {
    pip install --upgrade pip
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependências instaladas" -ForegroundColor Green
    } else {
        throw "Erro ao instalar dependências"
    }
} catch {
    Write-Host "❌ Erro ao instalar dependências" -ForegroundColor Red
    Write-Host "Tente executar manualmente: pip install -r requirements.txt" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

# Verificar ChromeDriver
Write-Host ""
Write-Host "[6/6] Verificando ChromeDriver..." -ForegroundColor Yellow
if (Test-Path "chromedriver\chromedriver-win64\chromedriver.exe") {
    Write-Host "✅ ChromeDriver encontrado" -ForegroundColor Green
} else {
    Write-Host "⚠️ ChromeDriver não encontrado!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📥 Baixe o ChromeDriver de: https://chromedriver.chromium.org/" -ForegroundColor Cyan
    Write-Host "📁 Extraia para: .\chromedriver\chromedriver-win64\" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Estrutura esperada:" -ForegroundColor White
    Write-Host "chromedriver\" -ForegroundColor Gray
    Write-Host "└── chromedriver-win64\" -ForegroundColor Gray
    Write-Host "    └── chromedriver.exe" -ForegroundColor Gray
    Write-Host ""
}

# Finalização
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    ✅ INSTALAÇÃO CONCLUÍDA!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "🚀 Para executar o RPA:" -ForegroundColor White
Write-Host "1. Ative o ambiente virtual: venv\Scripts\Activate.ps1" -ForegroundColor Gray
Write-Host "2. Execute: python executar_todas_telas_corrigido.py" -ForegroundColor Gray
Write-Host ""
Write-Host "📚 Consulte o README.md para mais informações" -ForegroundColor Cyan
Write-Host ""
Read-Host "Pressione Enter para sair"
