# Script PowerShell para testar se o cache do Cloudflare está desabilitado
# Execute: .\testar_cache_cloudflare.ps1

Write-Host "🔍 Testando Cache do Cloudflare para arquivos JS em /webhooks/" -ForegroundColor Cyan
Write-Host ""

$url = "https://dev.bpsegurosimediato.com.br/webhooks/MODAL_WHATSAPP_DEFINITIVO.js"

try {
    Write-Host "📡 Fazendo requisição HEAD para: $url" -ForegroundColor Yellow
    Write-Host ""
    
    $response = Invoke-WebRequest -Uri $url -Method Head -UseBasicParsing
    
    Write-Host "✅ Status Code: $($response.StatusCode)" -ForegroundColor Green
    Write-Host ""
    
    # Verificar headers relevantes
    $cfCacheStatus = $response.Headers['cf-cache-status']
    $cfRay = $response.Headers['cf-ray']
    $cacheControl = $response.Headers['Cache-Control']
    
    Write-Host "📊 Headers de Cache:" -ForegroundColor Cyan
    Write-Host "  cf-cache-status: $cfCacheStatus" -ForegroundColor $(if ($cfCacheStatus -in @('DYNAMIC', 'BYPASS')) { 'Green' } else { 'Red' })
    Write-Host "  Cache-Control: $cacheControl" -ForegroundColor Yellow
    Write-Host "  CF-Ray: $cfRay" -ForegroundColor Gray
    Write-Host ""
    
    # Interpretação
    if ($cfCacheStatus -eq 'DYNAMIC' -or $cfCacheStatus -eq 'BYPASS') {
        Write-Host "✅ SUCESSO: O cache está DESABILITADO!" -ForegroundColor Green
        Write-Host "   O arquivo NÃO será cacheado pelo Cloudflare." -ForegroundColor Green
    } elseif ($cfCacheStatus -eq 'HIT') {
        Write-Host "⚠️  ATENÇÃO: O cache ainda está ATIVO (HIT)" -ForegroundColor Yellow
        Write-Host "   Faça purge manual no Cloudflare ou aguarde alguns minutos." -ForegroundColor Yellow
    } elseif ($cfCacheStatus -eq 'MISS') {
        Write-Host "ℹ️  Informação: Cache MISS (primeira requisição)" -ForegroundColor Blue
        Write-Host "   A regra está funcionando, mas pode levar alguns minutos para propagar." -ForegroundColor Blue
    } else {
        Write-Host "❓ Status desconhecido: $cfCacheStatus" -ForegroundColor Yellow
    }
    
    Write-Host ""
    Write-Host "🔗 URL testada: $url" -ForegroundColor Gray
    
} catch {
    Write-Host "❌ Erro ao fazer requisição:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    
    if ($_.Exception.Response) {
        Write-Host "Status Code: $($_.Exception.Response.StatusCode.value__)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📝 Dica: Execute este script novamente após fazer purge no Cloudflare" -ForegroundColor Cyan
Write-Host "   para confirmar que o cache foi limpo." -ForegroundColor Cyan











