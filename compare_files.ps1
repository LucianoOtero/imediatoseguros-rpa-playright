# Localizar arquivos automaticamente
$basePath = Get-ChildItem -Path "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros" -Recurse -Filter "add_travelangels_dev.php" -File | Where-Object { $_.FullName -like "*mdmidia\dev\webhooks*" } | Select-Object -First 1
$file1 = $basePath.FullName
$file2 = $file1 -replace 'add_travelangels_dev\.php$', 'add_travelangels_servidor_dev.php'

if (-not (Test-Path $file2)) {
    Write-Host "ERRO: Arquivo servidor não encontrado: $file2" -ForegroundColor Red
    exit 1
}

Write-Host "=== COMPARAÇÃO DE ARQUIVOS ===" -ForegroundColor Cyan
Write-Host "Local: $file1" -ForegroundColor Yellow
Write-Host "Servidor: $file2" -ForegroundColor Yellow
Write-Host ""

$content1 = Get-Content $file1
$content2 = Get-Content $file2

Write-Host "Local: $($content1.Count) linhas"
Write-Host "Servidor: $($content2.Count) linhas"
Write-Host ""

$maxLines = [Math]::Max($content1.Count, $content2.Count)
$diffCount = 0

for ($i = 0; $i -lt $maxLines; $i++) {
    $line1 = if ($i -lt $content1.Count) { $content1[$i] } else { '[ARQUIVO FINALIZOU AQUI]' }
    $line2 = if ($i -lt $content2.Count) { $content2[$i] } else { '[ARQUIVO FINALIZOU AQUI]' }
    
    if ($line1 -ne $line2) {
        $diffCount++
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
        Write-Host "Linha $($i+1):" -ForegroundColor Yellow
        
        if ($line1 -ne '[ARQUIVO FINALIZOU AQUI]') {
            Write-Host "  [LOCAL]    $line1" -ForegroundColor Red
        }
        
        if ($line2 -ne '[ARQUIVO FINALIZOU AQUI]') {
            Write-Host "  [SERVIDOR] $line2" -ForegroundColor Green
        }
        
        Write-Host ""
    }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Total de linhas diferentes: $diffCount" -ForegroundColor Cyan

