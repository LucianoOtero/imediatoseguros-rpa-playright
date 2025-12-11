# Script para medir performance do Cursor com e sem VPN
# Uso: .\test_cursor_vpn_performance.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "TESTE DE PERFORMANCE CURSOR COM/SEM VPN" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Função para testar latência usando HTTP (mais confiável que ICMP)
function Test-Latency {
    param([string]$Target, [int]$Count = 5)
    
    Write-Host "  Testando $Target..." -ForegroundColor Gray -NoNewline
    
    # Tentar primeiro com Test-Connection (ICMP)
    try {
        $results = Test-Connection -TargetName $Target -Count $Count -ErrorAction Stop
        if ($results -and $results.Count -gt 0) {
            $responseTimes = $results | Where-Object { $_.ResponseTime -gt 0 } | Select-Object -ExpandProperty ResponseTime
            if ($responseTimes.Count -gt 0) {
                $avg = ($responseTimes | Measure-Object -Average).Average
                $min = ($responseTimes | Measure-Object -Minimum).Minimum
                $max = ($responseTimes | Measure-Object -Maximum).Maximum
                Write-Host " OK" -ForegroundColor Green
                return @{
                    Average = [math]::Round($avg, 2)
                    Minimum = $min
                    Maximum = $max
                }
            }
        }
    } catch {
        # ICMP bloqueado, tentar HTTP
    }
    
    # Se ICMP falhou, tentar HTTP
    try {
        $times = @()
        $protocol = if ($Target -match '^\d+\.\d+\.\d+\.\d+$') { "http://$Target" } else { "https://$Target" }
        
        for ($i = 1; $i -le $Count; $i++) {
            $start = Get-Date
            try {
                $response = Invoke-WebRequest -Uri $protocol -Method Head -TimeoutSec 5 -UseBasicParsing -ErrorAction Stop
                $end = Get-Date
                $latency = ($end - $start).TotalMilliseconds
                if ($latency -gt 0) {
                    $times += $latency
                }
            } catch {
                # Ignorar erros individuais
            }
        }
        
        if ($times.Count -gt 0) {
            $avg = ($times | Measure-Object -Average).Average
            $min = ($times | Measure-Object -Minimum).Minimum
            $max = ($times | Measure-Object -Maximum).Maximum
            Write-Host " OK (HTTP)" -ForegroundColor Green
            return @{
                Average = [math]::Round($avg, 2)
                Minimum = [math]::Round($min, 2)
                Maximum = [math]::Round($max, 2)
            }
        } else {
            Write-Host " SEM RESPOSTA" -ForegroundColor Yellow
            return $null
        }
    } catch {
        Write-Host " FALHOU" -ForegroundColor Red
        return $null
    }
}

# Função para testar velocidade de download
function Test-DownloadSpeed {
    param([string]$Url, [string]$OutputFile)
    
    $startTime = Get-Date
    try {
        $progressPreference = 'SilentlyContinue'
        Invoke-WebRequest -Uri $Url -OutFile $OutputFile -ErrorAction Stop | Out-Null
        $endTime = Get-Date
        $duration = ($endTime - $startTime).TotalSeconds
        $fileSize = (Get-Item $OutputFile).Length / 1MB
        $speed = $fileSize / $duration
        Remove-Item $OutputFile -ErrorAction SilentlyContinue
        return @{
            Duration = [math]::Round($duration, 2)
            Speed = [math]::Round($speed, 2)
        }
    } catch {
        Remove-Item $OutputFile -ErrorAction SilentlyContinue
        return $null
    }
}

# Alvos para teste
$targets = @("8.8.8.8", "1.1.1.1", "google.com")
$downloadUrls = @(
    "https://speedtest.tele2.net/1MB.zip",
    "https://www.google.com/favicon.ico"
)

# ==========================================
# TESTE SEM VPN
# ==========================================
Write-Host "--- TESTE SEM VPN ---" -ForegroundColor Yellow
Write-Host "Desconecte o VPN e pressione Enter para continuar..." -ForegroundColor Gray
Read-Host

Write-Host ""
Write-Host "Testando latência (sem VPN)..." -ForegroundColor Cyan
$resultsWithoutVPN = @{}
foreach ($target in $targets) {
    $result = Test-Latency -Target $target -Count 5
    if ($result) {
        $resultsWithoutVPN[$target] = $result
        Write-Host "    Média: $($result.Average)ms (Min: $($result.Minimum)ms, Max: $($result.Maximum)ms)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Testando velocidade de download (sem VPN)..." -ForegroundColor Cyan
$downloadWithoutVPN = $null
foreach ($url in $downloadUrls) {
    Write-Host "  Tentando: $url..." -ForegroundColor Gray -NoNewline
    $downloadWithoutVPN = Test-DownloadSpeed -Url $url -OutputFile "$env:TEMP\test_vpn_$(Get-Random).zip"
    if ($downloadWithoutVPN) {
        Write-Host " OK" -ForegroundColor Green
        Write-Host "    Velocidade: $($downloadWithoutVPN.Speed) MB/s (Tempo: $($downloadWithoutVPN.Duration)s)" -ForegroundColor Gray
        break
    } else {
        Write-Host " FALHOU" -ForegroundColor Yellow
    }
}
if (-not $downloadWithoutVPN) {
    Write-Host "  Todos os servidores de teste falharam" -ForegroundColor Red
}

# ==========================================
# TESTE COM VPN
# ==========================================
Write-Host ""
Write-Host "--- TESTE COM VPN ---" -ForegroundColor Yellow
Write-Host "Conecte ao Proton VPN (servidor São Paulo) e pressione Enter para continuar..." -ForegroundColor Gray
Read-Host

# Aguardar estabilização
Write-Host "Aguardando estabilização da conexão VPN (5 segundos)..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Testando latência (com VPN)..." -ForegroundColor Cyan
$resultsWithVPN = @{}
foreach ($target in $targets) {
    $result = Test-Latency -Target $target -Count 5
    if ($result) {
        $resultsWithVPN[$target] = $result
        Write-Host "    Média: $($result.Average)ms (Min: $($result.Minimum)ms, Max: $($result.Maximum)ms)" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "Testando velocidade de download (com VPN)..." -ForegroundColor Cyan
$downloadWithVPN = $null
foreach ($url in $downloadUrls) {
    Write-Host "  Tentando: $url..." -ForegroundColor Gray -NoNewline
    $downloadWithVPN = Test-DownloadSpeed -Url $url -OutputFile "$env:TEMP\test_vpn_$(Get-Random).zip"
    if ($downloadWithVPN) {
        Write-Host " OK" -ForegroundColor Green
        Write-Host "    Velocidade: $($downloadWithVPN.Speed) MB/s (Tempo: $($downloadWithVPN.Duration)s)" -ForegroundColor Gray
        break
    } else {
        Write-Host " FALHOU" -ForegroundColor Yellow
    }
}
if (-not $downloadWithVPN) {
    Write-Host "  Todos os servidores de teste falharam" -ForegroundColor Red
}

# ==========================================
# RESULTADOS COMPARATIVOS
# ==========================================
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "RESULTADOS COMPARATIVOS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($target in $targets) {
    if ($resultsWithoutVPN[$target] -and $resultsWithVPN[$target]) {
        $diff = $resultsWithVPN[$target].Average - $resultsWithoutVPN[$target].Average
        if ($resultsWithoutVPN[$target].Average -gt 0) {
            $percent = ($diff / $resultsWithoutVPN[$target].Average) * 100
        } else {
            $percent = 0
        }
        Write-Host "${target}:" -ForegroundColor Yellow
        Write-Host "  Sem VPN: $($resultsWithoutVPN[$target].Average)ms" -ForegroundColor Gray
        Write-Host "  Com VPN: $($resultsWithVPN[$target].Average)ms" -ForegroundColor Gray
        if ($diff -gt 0) {
            Write-Host "  Diferença: +$([math]::Round($diff, 2))ms (+$([math]::Round($percent, 1))%)" -ForegroundColor Red
        } elseif ($diff -lt 0) {
            Write-Host "  Diferença: $([math]::Round($diff, 2))ms ($([math]::Round($percent, 1))%)" -ForegroundColor Green
        } else {
            Write-Host "  Diferença: 0ms (0%)" -ForegroundColor Gray
        }
        Write-Host ""
    }
}

if ($downloadWithoutVPN -and $downloadWithVPN) {
    $speedDiff = $downloadWithVPN.Speed - $downloadWithoutVPN.Speed
    if ($downloadWithoutVPN.Speed -gt 0) {
        $speedPercent = ($speedDiff / $downloadWithoutVPN.Speed) * 100
    } else {
        $speedPercent = 0
    }
    Write-Host "Velocidade de Download:" -ForegroundColor Yellow
    Write-Host "  Sem VPN: $($downloadWithoutVPN.Speed) MB/s" -ForegroundColor Gray
    Write-Host "  Com VPN: $($downloadWithVPN.Speed) MB/s" -ForegroundColor Gray
    if ($speedDiff -lt 0) {
        Write-Host "  Diferença: $([math]::Round($speedDiff, 2)) MB/s ($([math]::Round($speedPercent, 1))%)" -ForegroundColor Red
    } elseif ($speedDiff -gt 0) {
        Write-Host "  Diferença: +$([math]::Round($speedDiff, 2)) MB/s (+$([math]::Round($speedPercent, 1))%)" -ForegroundColor Green
    } else {
        Write-Host "  Diferença: 0 MB/s (0%)" -ForegroundColor Gray
    }
} elseif ($downloadWithoutVPN -or $downloadWithVPN) {
    Write-Host "Velocidade de Download:" -ForegroundColor Yellow
    Write-Host "  Dados incompletos - não foi possível comparar" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "TESTE CONCLUÍDO" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ANÁLISE DOS RESULTADOS" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

if ($downloadWithoutVPN -and $downloadWithVPN) {
    $speedReduction = $downloadWithVPN.Speed / $downloadWithoutVPN.Speed * 100
    Write-Host "Impacto do VPN na Velocidade:" -ForegroundColor Yellow
    if ($speedReduction -lt 50) {
        Write-Host "  ⚠️  ALTO IMPACTO: VPN reduz velocidade em mais de 50%" -ForegroundColor Red
        Write-Host "  Recomendação: Considerar desativar VPN durante uso intenso do Cursor" -ForegroundColor Yellow
    } elseif ($speedReduction -lt 75) {
        Write-Host "  🟡 IMPACTO MODERADO: VPN reduz velocidade em 25-50%" -ForegroundColor Yellow
        Write-Host "  Recomendação: Impacto perceptível, mas pode ser aceitável" -ForegroundColor Gray
    } else {
        Write-Host "  ✅ IMPACTO BAIXO: VPN reduz velocidade em menos de 25%" -ForegroundColor Green
        Write-Host "  Recomendação: Impacto mínimo, VPN pode ser usado normalmente" -ForegroundColor Gray
    }
    Write-Host ""
}

Write-Host "Dica: Teste também o Cursor AI manualmente:" -ForegroundColor Yellow
Write-Host "  1. Faça a mesma pergunta com e sem VPN" -ForegroundColor Gray
Write-Host "  2. Meça o tempo de resposta" -ForegroundColor Gray
Write-Host "  3. Compare os resultados" -ForegroundColor Gray
Write-Host ""

