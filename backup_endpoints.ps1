$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$basePath = 'C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros\Imediato\mdmidia\dev\webhooks\'

$file1 = Join-Path $basePath 'add_travelangels_dev.php'
$file2 = Join-Path $basePath 'add_webflow_octa_dev.php'

$backup1 = Join-Path $basePath "add_travelangels_dev.php.backup_$timestamp"
$backup2 = Join-Path $basePath "add_webflow_octa_dev.php.backup_$timestamp"

if (Test-Path $file1) {
    Copy-Item $file1 -Destination $backup1 -Force
    Write-Host "✅ Backup criado: add_travelangels_dev.php.backup_$timestamp" -ForegroundColor Green
} else {
    Write-Host "❌ Arquivo não encontrado: $file1" -ForegroundColor Red
}

if (Test-Path $file2) {
    Copy-Item $file2 -Destination $backup2 -Force
    Write-Host "✅ Backup criado: add_webflow_octa_dev.php.backup_$timestamp" -ForegroundColor Green
} else {
    Write-Host "❌ Arquivo não encontrado: $file2" -ForegroundColor Red
}

Write-Host ""
Write-Host "Timestamp: $timestamp" -ForegroundColor Cyan











