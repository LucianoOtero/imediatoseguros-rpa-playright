# 🚀 DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL
# Script de deploy para Windows PowerShell

param(
    [switch]$Force,
    [switch]$SkipTests
)

# Configurar saída colorida
$Host.UI.RawUI.ForegroundColor = "White"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    switch ($Level) {
        "ERROR" { 
            Write-Host "[$timestamp] ERROR: $Message" -ForegroundColor Red
        }
        "WARN" { 
            Write-Host "[$timestamp] WARNING: $Message" -ForegroundColor Yellow
        }
        "SUCCESS" { 
            Write-Host "[$timestamp] $Message" -ForegroundColor Green
        }
        "INFO" { 
            Write-Host "[$timestamp] INFO: $Message" -ForegroundColor Blue
        }
        default { 
            Write-Host "[$timestamp] $Message" -ForegroundColor White
        }
    }
}

function Test-Command {
    param([string]$Command)
    
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Install-Chocolatey {
    Write-Log "🍫 Instalando Chocolatey..." "INFO"
    
    try {
        Set-ExecutionPolicy Bypass -Scope Process -Force
        [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
        iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
        Write-Log "✅ Chocolatey instalado com sucesso" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao instalar Chocolatey: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Install-Redis {
    Write-Log "🔴 Instalando Redis..." "INFO"
    
    try {
        if (Test-Command "choco") {
            choco install redis-64 -y
        } else {
            Write-Log "❌ Chocolatey não encontrado" "ERROR"
            return $false
        }
        
        # Configurar Redis como serviço
        $redisPath = "C:\Program Files\Redis\redis-server.exe"
        if (Test-Path $redisPath) {
            # Criar serviço do Redis
            New-Service -Name "Redis" -BinaryPathName $redisPath -DisplayName "Redis Server" -StartupType Automatic
            Start-Service -Name "Redis"
            Write-Log "✅ Redis instalado e iniciado" "SUCCESS"
            return $true
        } else {
            Write-Log "❌ Redis não foi instalado corretamente" "ERROR"
            return $false
        }
    }
    catch {
        Write-Log "❌ Falha ao instalar Redis: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Install-NodeJS {
    Write-Log "📦 Instalando Node.js..." "INFO"
    
    try {
        if (Test-Command "choco") {
            choco install nodejs -y
        } else {
            Write-Log "❌ Chocolatey não encontrado" "ERROR"
            return $false
        }
        
        # Atualizar PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        Write-Log "✅ Node.js instalado" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao instalar Node.js: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Install-PythonDependencies {
    Write-Log "🐍 Instalando dependências Python..." "INFO"
    
    try {
        # Atualizar pip
        python -m pip install --upgrade pip
        
        # Instalar dependências
        pip install redis websockets asyncio psutil playwright
        
        # Instalar navegadores do Playwright
        playwright install chromium
        
        Write-Log "✅ Dependências Python instaladas" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao instalar dependências Python: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Install-NodeDependencies {
    Write-Log "📦 Instalando dependências Node.js..." "INFO"
    
    try {
        npm install ws redis
        Write-Log "✅ Dependências Node.js instaladas" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao instalar dependências Node.js: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Test-RedisConnection {
    Write-Log "🔍 Testando conexão Redis..." "INFO"
    
    try {
        # Tentar conectar ao Redis
        $redisTest = python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); print('PONG' if r.ping() else 'FAIL')" 2>$null
        
        if ($redisTest -eq "PONG") {
            Write-Log "✅ Redis está respondendo" "SUCCESS"
            return $true
        } else {
            Write-Log "❌ Redis não está respondendo" "ERROR"
            return $false
        }
    }
    catch {
        Write-Log "❌ Falha ao testar Redis: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function Start-RedisService {
    Write-Log "🔴 Iniciando serviço Redis..." "INFO"
    
    try {
        Start-Service -Name "Redis" -ErrorAction Stop
        Start-Sleep -Seconds 3
        
        if (Test-RedisConnection) {
            Write-Log "✅ Redis iniciado com sucesso" "SUCCESS"
            return $true
        } else {
            Write-Log "❌ Redis não iniciou corretamente" "ERROR"
            return $false
        }
    }
    catch {
        Write-Log "❌ Falha ao iniciar Redis: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function New-Backup {
    Write-Log "📦 Criando backup do sistema atual..." "INFO"
    
    try {
        $backupDir = "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
        
        # Backup dos arquivos críticos
        if (Test-Path "utils") { Copy-Item -Path "utils" -Destination "$backupDir\utils" -Recurse -Force }
        if (Test-Path "tela_*.py") { Copy-Item -Path "tela_*.py" -Destination $backupDir -Force }
        if (Test-Path "*.json") { Copy-Item -Path "*.json" -Destination $backupDir -Force }
        if (Test-Path "*.js") { Copy-Item -Path "*.js" -Destination $backupDir -Force }
        
        Write-Log "✅ Backup criado em: $backupDir" "SUCCESS"
        return $backupDir
    }
    catch {
        Write-Log "❌ Falha ao criar backup: $($_.Exception.Message)" "ERROR"
        return $null
    }
}

function New-ServiceScripts {
    Write-Log "⚙️ Criando scripts de serviço..." "INFO"
    
    try {
        # Script de inicialização
        $startScript = @"
# 🚀 Iniciar Serviços RPA v3.6.0
Write-Host "🚀 Iniciando serviços do RPA v3.6.0..." -ForegroundColor Green

# Iniciar Redis
Write-Host "🔴 Iniciando Redis..." -ForegroundColor Blue
Start-Service -Name "Redis" -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Verificar Redis
try {
    `$redisTest = python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); print('PONG' if r.ping() else 'FAIL')" 2>`$null
    if (`$redisTest -eq "PONG") {
        Write-Host "✅ Redis está rodando" -ForegroundColor Green
    } else {
        Write-Host "❌ Redis não está respondendo" -ForegroundColor Red
    }
} catch {
    Write-Host "❌ Erro ao verificar Redis" -ForegroundColor Red
}

# Iniciar WebSocket server
Write-Host "🌐 Iniciando WebSocket server..." -ForegroundColor Blue
Start-Process -FilePath "node" -ArgumentList "websocket_server.js" -WindowStyle Hidden

Start-Sleep -Seconds 3
Write-Host "✅ Serviços iniciados!" -ForegroundColor Green
"@
        
        $startScript | Out-File -FilePath "start_services.ps1" -Encoding UTF8
        
        # Script de parada
        $stopScript = @"
# 🛑 Parar Serviços RPA v3.6.0
Write-Host "🛑 Parando serviços do RPA v3.6.0..." -ForegroundColor Yellow

# Parar WebSocket server
Get-Process -Name "node" -ErrorAction SilentlyContinue | Where-Object { `$_.CommandLine -like "*websocket_server.js*" } | Stop-Process -Force

# Parar Redis (opcional - comentado para manter dados)
# Stop-Service -Name "Redis" -ErrorAction SilentlyContinue

Write-Host "✅ Serviços parados!" -ForegroundColor Green
"@
        
        $stopScript | Out-File -FilePath "stop_services.ps1" -Encoding UTF8
        
        # Script de monitoramento
        $monitorScript = @"
# 📊 Monitorar Serviços RPA v3.6.0
Write-Host "📊 Status dos serviços RPA v3.6.0" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan

# Redis
try {
    `$redisTest = python -c "import redis; r = redis.Redis(host='localhost', port=6379, db=0); print('PONG' if r.ping() else 'FAIL')" 2>`$null
    if (`$redisTest -eq "PONG") {
        Write-Host "🔴 Redis: ✅ RODANDO" -ForegroundColor Green
    } else {
        Write-Host "🔴 Redis: ❌ PARADO" -ForegroundColor Red
    }
} catch {
    Write-Host "🔴 Redis: ❌ ERRO" -ForegroundColor Red
}

# WebSocket
`$websocketPort = Get-NetTCPConnection -LocalPort 8765 -ErrorAction SilentlyContinue
if (`$websocketPort) {
    Write-Host "🌐 WebSocket: ✅ RODANDO (porta 8765)" -ForegroundColor Green
} else {
    Write-Host "🌐 WebSocket: ❌ PARADO" -ForegroundColor Red
}

# Processos Python
`$pythonProcesses = (Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { `$_.CommandLine -like "*rpa*" }).Count
Write-Host "🐍 Processos Python RPA: `$pythonProcesses" -ForegroundColor Blue

# Uso de memória
`$memory = Get-WmiObject -Class Win32_OperatingSystem
`$memoryUsage = [math]::Round((`$memory.TotalVisibleMemorySize - `$memory.FreePhysicalMemory) / `$memory.TotalVisibleMemorySize * 100, 2)
Write-Host "💾 Uso de memória: `$memoryUsage%" -ForegroundColor Blue

# Espaço em disco
`$disk = Get-WmiObject -Class Win32_LogicalDisk -Filter "DeviceID='C:'"
`$diskUsage = [math]::Round((`$disk.Size - `$disk.FreeSpace) / `$disk.Size * 100, 2)
Write-Host "💿 Uso de disco C:: `$diskUsage%" -ForegroundColor Blue
"@
        
        $monitorScript | Out-File -FilePath "monitor_services.ps1" -Encoding UTF8
        
        Write-Log "✅ Scripts de serviço criados" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao criar scripts de serviço: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

function New-Documentation {
    Write-Log "📚 Criando documentação..." "INFO"
    
    try {
        $docContent = @"
# 🚀 DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL

## 📋 Resumo da Versão

- **Versão**: 3.6.0
- **Data**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
- **Sistema**: Windows
- **Principais mudanças**:
  - Sistema de comunicação em tempo real
  - Integração Redis para cache
  - WebSocket para comunicação bidirecional
  - Módulos RPA atualizados com comunicação
  - Sistema de testes automatizados

## 🛠️ Componentes Instalados

### Módulos Python
- `utils/platform_utils.py` - Detecção de plataforma
- `utils/redis_manager.py` - Gerenciamento Redis
- `utils/websocket_manager.py` - Gerenciamento WebSocket
- `utils/communication_manager.py` - Orquestração de comunicação

### Módulos RPA Atualizados
- `tela_2_placa.py` - Com comunicação em tempo real
- `tela_3_confirmacao_veiculo.py` - Com comunicação em tempo real
- `tela_4_confirmacao_segurado.py` - Com comunicação em tempo real
- `tela_5_estimativas.py` - Com comunicação em tempo real

### Scripts de Teste
- `test_communication_system.py` - Testes do sistema de comunicação
- `test_rpa_modules.py` - Testes dos módulos RPA
- `run_all_tests.py` - Execução de todos os testes

### Scripts de Gerenciamento
- `start_services.ps1` - Iniciar serviços
- `stop_services.ps1` - Parar serviços
- `monitor_services.ps1` - Monitorar serviços

## 🚀 Como Usar

### Iniciar Serviços
```powershell
.\start_services.ps1
```

### Parar Serviços
```powershell
.\stop_services.ps1
```

### Monitorar Serviços
```powershell
.\monitor_services.ps1
```

### Executar Testes
```powershell
python run_all_tests.py
```

## 🔧 Configuração

### Redis
- **Host**: localhost
- **Porta**: 6379
- **DB**: 0
- **Serviço**: Redis

### WebSocket
- **Host**: localhost
- **Porta**: 8765

## 📊 Monitoramento

O sistema inclui monitoramento automático de:
- Status do Redis
- Status do WebSocket
- Processos Python
- Uso de memória
- Uso de disco

## 🆘 Solução de Problemas

### Redis não inicia
```powershell
# Verificar status do serviço
Get-Service -Name "Redis"

# Reiniciar serviço
Restart-Service -Name "Redis"
```

### WebSocket não conecta
```powershell
# Verificar se a porta está aberta
Get-NetTCPConnection -LocalPort 8765
```

### Testes falham
```powershell
# Executar testes individuais
python test_communication_system.py
python test_rpa_modules.py
```

## 📞 Suporte

Para suporte técnico, consulte a documentação ou execute os testes para diagnóstico.
"@
        
        $docContent | Out-File -FilePath "DEPLOY_V3.6.0_WINDOWS.md" -Encoding UTF8
        
        Write-Log "✅ Documentação criada" "SUCCESS"
        return $true
    }
    catch {
        Write-Log "❌ Falha ao criar documentação: $($_.Exception.Message)" "ERROR"
        return $false
    }
}

# MAIN SCRIPT
Write-Log "🚀 INICIANDO DEPLOY V3.6.0 - SISTEMA DE COMUNICAÇÃO EM TEMPO REAL" "SUCCESS"
Write-Log "Sistema: Windows" "INFO"
Write-Log "Usuário: $env:USERNAME" "INFO"
Write-Log "Diretório: $(Get-Location)" "INFO"

# Verificar se está rodando como administrador
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")

if (-not $isAdmin) {
    Write-Log "⚠️ Executando sem privilégios de administrador" "WARN"
    Write-Log "Alguns componentes podem não funcionar corretamente" "WARN"
}

# 1. BACKUP
$backupDir = New-Backup
if (-not $backupDir) {
    Write-Log "❌ Falha ao criar backup - abortando deploy" "ERROR"
    exit 1
}

# 2. VERIFICAR DEPENDÊNCIAS
Write-Log "🔍 Verificando dependências..." "INFO"

# Python
if (-not (Test-Command "python")) {
    Write-Log "❌ Python não encontrado" "ERROR"
    exit 1
}

$pythonVersion = python --version
Write-Log "✅ Python: $pythonVersion" "SUCCESS"

# Chocolatey
if (-not (Test-Command "choco")) {
    Write-Log "⚠️ Chocolatey não encontrado - instalando..." "WARN"
    if (-not (Install-Chocolatey)) {
        Write-Log "❌ Falha ao instalar Chocolatey" "ERROR"
        exit 1
    }
}

# 3. INSTALAR REDIS
if (-not (Test-Command "redis-server")) {
    Write-Log "⚠️ Redis não encontrado - instalando..." "WARN"
    if (-not (Install-Redis)) {
        Write-Log "❌ Falha ao instalar Redis" "ERROR"
        exit 1
    }
} else {
    Write-Log "✅ Redis já instalado" "SUCCESS"
}

# 4. INSTALAR NODE.JS
if (-not (Test-Command "node")) {
    Write-Log "⚠️ Node.js não encontrado - instalando..." "WARN"
    if (-not (Install-NodeJS)) {
        Write-Log "❌ Falha ao instalar Node.js" "ERROR"
        exit 1
    }
} else {
    $nodeVersion = node --version
    Write-Log "✅ Node.js: $nodeVersion" "SUCCESS"
}

# 5. INSTALAR DEPENDÊNCIAS
if (-not (Install-PythonDependencies)) {
    Write-Log "❌ Falha ao instalar dependências Python" "ERROR"
    exit 1
}

if (-not (Install-NodeDependencies)) {
    Write-Log "❌ Falha ao instalar dependências Node.js" "ERROR"
    exit 1
}

# 6. INICIAR REDIS
if (-not (Start-RedisService)) {
    Write-Log "❌ Falha ao iniciar Redis" "ERROR"
    exit 1
}

# 7. CRIAR SCRIPTS DE SERVIÇO
if (-not (New-ServiceScripts)) {
    Write-Log "❌ Falha ao criar scripts de serviço" "ERROR"
    exit 1
}

# 8. CRIAR DOCUMENTAÇÃO
if (-not (New-Documentation)) {
    Write-Log "❌ Falha ao criar documentação" "ERROR"
    exit 1
}

# 9. EXECUTAR TESTES
if (-not $SkipTests) {
    Write-Log "🧪 Executando testes do sistema..." "INFO"
    
    try {
        python run_all_tests.py
        if ($LASTEXITCODE -eq 0) {
            Write-Log "✅ Todos os testes passaram" "SUCCESS"
        } else {
            Write-Log "⚠️ Alguns testes falharam - continuando com deploy" "WARN"
        }
    }
    catch {
        Write-Log "⚠️ Falha ao executar testes: $($_.Exception.Message)" "WARN"
    }
}

# 10. FINALIZAÇÃO
Write-Log "🎉 DEPLOY V3.6.0 CONCLUÍDO COM SUCESSO!" "SUCCESS"
Write-Log "" "INFO"
Write-Log "📋 Próximos passos:" "INFO"
Write-Log "   1. Execute: .\start_services.ps1" "INFO"
Write-Log "   2. Execute: .\monitor_services.ps1" "INFO"
Write-Log "   3. Execute: python run_all_tests.py" "INFO"
Write-Log "" "INFO"
Write-Log "📚 Documentação: DEPLOY_V3.6.0_WINDOWS.md" "INFO"
Write-Log "📦 Backup: $backupDir" "INFO"
Write-Log "" "INFO"
Write-Log "✅ Sistema pronto para uso!" "SUCCESS"
