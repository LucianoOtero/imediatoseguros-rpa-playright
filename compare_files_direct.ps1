# Usar caminhos diretos conhecidos
$file1Path = Get-ChildItem -Path "C:\Users\Luciano\OneDrive - Imediato Soluções em Seguros" -Recurse -Filter "add_travelangels_dev.php" | Where-Object { $_.DirectoryName -like "*dev\webhooks*" } | Select-Object -First 1

if ($null -eq $file1Path) {
    Write-Host "ERRO: Arquivo local não encontrado" -ForegroundColor Red
    exit 1
}

$file1 = $file1Path.FullName
$dir = $file1Path.DirectoryName
$file2 = Join-Path $dir "add_travelangels_servidor_dev.php"

if (-not (Test-Path $file2)) {
    Write-Host "ERRO: Arquivo servidor não encontrado: $file2" -ForegroundColor Red
    exit 1
}

Write-Host "=== COMPARAÇÃO DE ARQUIVOS ===" -ForegroundColor Cyan
Write-Host "Arquivo LOCAL:    $file1" -ForegroundColor Yellow
Write-Host "Arquivo SERVIDOR: $file2" -ForegroundColor Yellow
Write-Host ""

$content1 = Get-Content $file1 -Encoding UTF8
$content2 = Get-Content $file2 -Encoding UTF8

Write-Host "Local:    $($content1.Count) linhas" -ForegroundColor White
Write-Host "Servidor: $($content2.Count) linhas" -ForegroundColor White
Write-Host ""

$maxLines = [Math]::Max($content1.Count, $content2.Count)
$diffCount = 0
$differences = @()

for ($i = 0; $i -lt $maxLines; $i++) {
    $line1 = if ($i -lt $content1.Count) { $content1[$i] } else { '[FIM DO ARQUIVO]' }
    $line2 = if ($i -lt $content2.Count) { $content2[$i] } else { '[FIM DO ARQUIVO]' }
    
    if ($line1 -ne $line2) {
        $diffCount++
        $differences += [PSCustomObject]@{
            Linha = $i + 1
            Local = $line1
            Servidor = $line2
        }
    }
}

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
Write-Host "Total de linhas diferentes: $diffCount" -ForegroundColor Cyan
Write-Host ""

if ($diffCount -gt 0) {
    Write-Host "DIFERENÇAS ENCONTRADAS:" -ForegroundColor Yellow
    Write-Host ""
    
    $differences | ForEach-Object {
        Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Gray
        Write-Host "Linha $($_.Linha):" -ForegroundColor Yellow
        
        if ($_.Local -ne '[FIM DO ARQUIVO]') {
            Write-Host "  [LOCAL]    " -NoNewline -ForegroundColor Red
            Write-Host $_.Local -ForegroundColor Red
        }
        
        if ($_.Servidor -ne '[FIM DO ARQUIVO]') {
            Write-Host "  [SERVIDOR] " -NoNewline -ForegroundColor Green
            Write-Host $_.Servidor -ForegroundColor Green
        }
        
        Write-Host ""
    }
} else {
    Write-Host "✅ ARQUIVOS SÃO IDÊNTICOS!" -ForegroundColor Green
}











