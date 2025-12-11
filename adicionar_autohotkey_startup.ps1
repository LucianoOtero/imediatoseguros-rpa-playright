# ============================================
# SCRIPT: ADICIONAR AUTOHOTKEY AO STARTUP
# ============================================
# 
# Este script adiciona o programa AutoHotkey (KEYS.ahk)
# ao startup do Windows, criando um atalho na pasta de startup.
#
# Data: 14/11/2025
# ============================================

# Caminho do arquivo AutoHotkey
$ahkScriptPath = "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Documentos\AutoHotkey\KEYS.ahk"

# Verificar se o arquivo existe
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "🔍 VERIFICANDO ARQUIVO AUTOHOTKEY" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

if (-not (Test-Path $ahkScriptPath)) {
    Write-Host "❌ ERRO: Arquivo não encontrado!" -ForegroundColor Red
    Write-Host "   Caminho: $ahkScriptPath" -ForegroundColor Yellow
    Write-Host "`nPor favor, verifique se o arquivo existe e tente novamente.`n" -ForegroundColor Yellow
    Read-Host "Pressione Enter para sair"
    exit 1
}

Write-Host "✅ Arquivo encontrado: $ahkScriptPath" -ForegroundColor Green

# Localizar executável do AutoHotkey
Write-Host "`n🔍 Localizando executável do AutoHotkey..." -ForegroundColor Yellow

$ahkExecutable = $null
$possiblePaths = @(
    "C:\Program Files\AutoHotkey\AutoHotkey.exe",
    "C:\Program Files (x86)\AutoHotkey\AutoHotkey.exe",
    "$env:LOCALAPPDATA\Programs\AutoHotkey\AutoHotkey.exe",
    "$env:ProgramFiles\AutoHotkey\AutoHotkey.exe",
    "$env:ProgramFiles(x86)\AutoHotkey\AutoHotkey.exe",
    "C:\AutoHotkey\AutoHotkey.exe"
)

foreach ($path in $possiblePaths) {
    if (Test-Path $path) {
        $ahkExecutable = $path
        Write-Host "✅ Executável encontrado: $path" -ForegroundColor Green
        break
    }
}

# Se não encontrou nos caminhos comuns, tentar encontrar via PATH
if (-not $ahkExecutable) {
    try {
        $ahkInPath = Get-Command "AutoHotkey.exe" -ErrorAction SilentlyContinue
        if ($ahkInPath) {
            $ahkExecutable = $ahkInPath.Source
            Write-Host "✅ Executável encontrado no PATH: $ahkExecutable" -ForegroundColor Green
        }
    } catch {
        # Continuar
    }
}

# Se ainda não encontrou, tentar encontrar arquivos .exe relacionados ao AutoHotkey
if (-not $ahkExecutable) {
    Write-Host "⚠️  Executável não encontrado nos locais padrão. Buscando..." -ForegroundColor Yellow
    
    $searchPaths = @(
        "C:\Program Files",
        "C:\Program Files (x86)",
        "$env:LOCALAPPDATA\Programs",
        "$env:ProgramFiles",
        "$env:ProgramFiles(x86)"
    )
    
    foreach ($searchPath in $searchPaths) {
        if (Test-Path $searchPath) {
            $found = Get-ChildItem -Path $searchPath -Filter "AutoHotkey*.exe" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
            if ($found) {
                $ahkExecutable = $found.FullName
                Write-Host "✅ Executável encontrado: $ahkExecutable" -ForegroundColor Green
                break
            }
        }
    }
}

if (-not $ahkExecutable) {
    Write-Host "`n❌ ERRO: Executável do AutoHotkey não encontrado!" -ForegroundColor Red
    Write-Host "`nPor favor, instale o AutoHotkey ou informe o caminho do executável." -ForegroundColor Yellow
    Write-Host "`nLocais verificados:" -ForegroundColor Yellow
    foreach ($path in $possiblePaths) {
        Write-Host "   - $path" -ForegroundColor Gray
    }
    Write-Host "`nVocê pode baixar o AutoHotkey em: https://www.autohotkey.com/" -ForegroundColor Cyan
    Read-Host "`nPressione Enter para sair"
    exit 1
}

# Pasta de startup do usuário
$startupFolder = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup"
$shortcutName = "AutoHotkey - KEYS.lnk"
$shortcutPath = Join-Path $startupFolder $shortcutName

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "📝 CRIANDO ATALHO NO STARTUP" -ForegroundColor Cyan
Write-Host "============================================`n" -ForegroundColor Cyan

# Verificar se a pasta de startup existe, criar se não existir
if (-not (Test-Path $startupFolder)) {
    Write-Host "📁 Criando pasta de startup..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path $startupFolder -Force | Out-Null
    Write-Host "✅ Pasta criada: $startupFolder" -ForegroundColor Green
}

# Verificar se já existe um atalho
if (Test-Path $shortcutPath) {
    Write-Host "⚠️  Atalho já existe: $shortcutPath" -ForegroundColor Yellow
    $response = Read-Host "Deseja substituir? (S/N)"
    if ($response -ne "S" -and $response -ne "s") {
        Write-Host "`n❌ Operação cancelada pelo usuário.`n" -ForegroundColor Yellow
        exit 0
    }
    Remove-Item $shortcutPath -Force
    Write-Host "✅ Atalho antigo removido" -ForegroundColor Green
}

# Criar atalho usando WScript.Shell COM
try {
    Write-Host "🔗 Criando atalho..." -ForegroundColor Yellow
    
    $WScriptShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
    $Shortcut.TargetPath = $ahkExecutable
    $Shortcut.Arguments = "`"$ahkScriptPath`""
    $Shortcut.WorkingDirectory = Split-Path $ahkScriptPath -Parent
    $Shortcut.Description = "AutoHotkey - KEYS.ahk"
    $Shortcut.IconLocation = $ahkExecutable
    $Shortcut.Save()
    
    Write-Host "✅ Atalho criado com sucesso!" -ForegroundColor Green
    Write-Host "   Localização: $shortcutPath" -ForegroundColor Cyan
    
    # Verificar se o atalho foi criado corretamente
    if (Test-Path $shortcutPath) {
        Write-Host "`n============================================" -ForegroundColor Cyan
        Write-Host "✅ CONCLUÍDO COM SUCESSO!" -ForegroundColor Green
        Write-Host "============================================`n" -ForegroundColor Cyan
        
        Write-Host "📋 Resumo:" -ForegroundColor Yellow
        Write-Host "   - Arquivo: $ahkScriptPath" -ForegroundColor White
        Write-Host "   - Executável: $ahkExecutable" -ForegroundColor White
        Write-Host "   - Atalho: $shortcutPath" -ForegroundColor White
        Write-Host "`n✅ O programa será executado automaticamente no próximo login do Windows.`n" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  AVISO: O atalho pode não ter sido criado corretamente." -ForegroundColor Yellow
        Write-Host "   Por favor, verifique manualmente.`n" -ForegroundColor Yellow
    }
} catch {
    Write-Host "`n❌ ERRO ao criar atalho: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "`nPor favor, tente criar o atalho manualmente:`n" -ForegroundColor Yellow
    Write-Host "1. Abra a pasta: $startupFolder" -ForegroundColor Cyan
    Write-Host "2. Clique com o botão direito > Novo > Atalho" -ForegroundColor Cyan
    Write-Host "3. Digite: `"$ahkExecutable`" `"$ahkScriptPath`"" -ForegroundColor Cyan
    Write-Host "4. Nomeie o atalho: AutoHotkey - KEYS`n" -ForegroundColor Cyan
    Read-Host "Pressione Enter para sair"
    exit 1
}

Read-Host "`nPressione Enter para sair"

