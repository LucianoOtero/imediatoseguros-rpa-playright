# Script PowerShell para copiar FooterCodeSiteDefinitivoCompleto.js para servidor
# Uso: Execute no PowerShell a partir do diretório raiz do projeto

$SERVER = "root@46.62.174.150"
$REMOTE_PATH = "/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js"
$LOCAL_FILE = "02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js"

Write-Host "📤 Copiando arquivo unificado para servidor..." -ForegroundColor Cyan
Write-Host "Origem: $LOCAL_FILE"
Write-Host "Destino: $SERVER`:$REMOTE_PATH"
Write-Host ""

# Verificar se arquivo local existe
if (-not (Test-Path $LOCAL_FILE)) {
    Write-Host "❌ ERRO: Arquivo local não encontrado: $LOCAL_FILE" -ForegroundColor Red
    exit 1
}

# Criar backup no servidor (se arquivo já existir)
Write-Host "📋 Criando backup no servidor (se existir)..." -ForegroundColor Yellow
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupCmd = "if [ -f $REMOTE_PATH ]; then cp $REMOTE_PATH ${REMOTE_PATH}.backup_$timestamp; echo '✅ Backup criado'; fi"
ssh $SERVER $backupCmd

# Copiar arquivo
Write-Host "📤 Copiando arquivo..." -ForegroundColor Yellow
$localFullPath = (Resolve-Path $LOCAL_FILE).Path
scp "$localFullPath" "${SERVER}:${REMOTE_PATH}"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Arquivo copiado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "🔍 Verificações:" -ForegroundColor Cyan
    Write-Host "1. Verificando arquivo no servidor..."
    ssh $SERVER "ls -lh $REMOTE_PATH"
    Write-Host ""
    Write-Host "2. Verificando tamanho..."
    ssh $SERVER "wc -c $REMOTE_PATH"
    Write-Host ""
    Write-Host "3. Testar URL:" -ForegroundColor Yellow
    Write-Host "   https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js"
    Write-Host ""
    Write-Host "✅ Pronto para Fase 3 (Backup Webflow)!" -ForegroundColor Green
} else {
    Write-Host "❌ ERRO ao copiar arquivo" -ForegroundColor Red
    exit 1
}






