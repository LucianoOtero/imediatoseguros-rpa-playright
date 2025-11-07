# Script para testar acesso ao arquivo unificado
$url = "https://dev.bpsegurosimediato.com.br/webhooks/FooterCodeSiteDefinitivoCompleto.js"

Write-Host "🔍 Testando acesso ao arquivo unificado..." -ForegroundColor Cyan
Write-Host "URL: $url"
Write-Host ""

try {
    # Tentar fazer requisição HEAD primeiro
    Write-Host "1. Testando requisição HEAD..." -ForegroundColor Yellow
    try {
        $headResponse = Invoke-WebRequest -Uri $url -Method Head -ErrorAction Stop
        Write-Host "   ✅ Status: $($headResponse.StatusCode)" -ForegroundColor Green
        Write-Host "   Content-Type: $($headResponse.Headers.'Content-Type')" -ForegroundColor Green
        Write-Host "   Content-Length: $($headResponse.Headers.'Content-Length') bytes" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  HEAD não suportado, tentando GET..." -ForegroundColor Yellow
    }
    
    # Fazer requisição GET completa
    Write-Host ""
    Write-Host "2. Testando requisição GET..." -ForegroundColor Yellow
    $response = Invoke-WebRequest -Uri $url -ErrorAction Stop
    
    Write-Host "   ✅ Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "   Content-Type: $($response.Headers.'Content-Type')" -ForegroundColor Green
    Write-Host "   Tamanho do conteúdo: $($response.Content.Length) caracteres" -ForegroundColor Green
    Write-Host ""
    
    # Verificar se é JavaScript válido
    Write-Host "3. Verificando conteúdo..." -ForegroundColor Yellow
    if ($response.Content -match '^\s*/\*\*' -or $response.Content -match '^\s*\(function\(') {
        Write-Host "   ✅ Parece ser um arquivo JavaScript válido" -ForegroundColor Green
    } else {
        Write-Host "   ⚠️  Conteúdo não parece ser JavaScript" -ForegroundColor Yellow
    }
    
    # Mostrar primeiras linhas
    Write-Host ""
    Write-Host "4. Primeiras 5 linhas do arquivo:" -ForegroundColor Yellow
    $firstLines = ($response.Content -split "`n")[0..4]
    foreach ($line in $firstLines) {
        Write-Host "   $line" -ForegroundColor Gray
    }
    
    Write-Host ""
    Write-Host "✅ Arquivo acessível e válido!" -ForegroundColor Green
    
} catch {
    Write-Host ""
    Write-Host "❌ ERRO ao acessar arquivo:" -ForegroundColor Red
    Write-Host "   $($_.Exception.Message)" -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "   Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
        Write-Host "   Isso significa que o arquivo ainda não foi copiado para o servidor." -ForegroundColor Yellow
        Write-Host ""
        Write-Host "📋 Próximo passo: Executar comando SCP para copiar arquivo:" -ForegroundColor Cyan
        Write-Host "   scp `"02-DEVELOPMENT\custom-codes\FooterCodeSiteDefinitivoCompleto.js`" root@46.62.174.150:/var/www/html/dev/webhooks/FooterCodeSiteDefinitivoCompleto.js" -ForegroundColor White
    }
}

