# Script para descobrir MAC Address e IP do PC
# Uso: .\descobrir_mac_ip_pc.ps1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "INFORMAÇÕES DE REDE DO PC" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Descobrir adaptadores de rede ativos
$adapters = Get-NetAdapter | Where-Object {$_.Status -eq "Up"}

if ($adapters.Count -eq 0) {
    Write-Host "Nenhum adaptador de rede ativo encontrado." -ForegroundColor Red
    exit
}

Write-Host "--- Adaptadores de Rede Ativos ---" -ForegroundColor Yellow
Write-Host ""

foreach ($adapter in $adapters) {
    Write-Host "Adaptador: $($adapter.Name)" -ForegroundColor Cyan
    Write-Host "  MAC Address: $($adapter.MacAddress)" -ForegroundColor Green
    Write-Host "  Descrição: $($adapter.InterfaceDescription)" -ForegroundColor Gray
    
    # Descobrir IP associado
    $ipConfig = Get-NetIPAddress -InterfaceIndex $adapter.InterfaceIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue
    if ($ipConfig) {
        foreach ($ip in $ipConfig) {
            if ($ip.IPAddress -like "192.168.*" -or $ip.IPAddress -like "10.*" -or $ip.IPAddress -like "172.*") {
                Write-Host "  IP Address: $($ip.IPAddress)" -ForegroundColor Green
                Write-Host "  Subnet Mask: $($ip.PrefixLength)" -ForegroundColor Gray
            }
        }
    }
    
    # Descobrir Gateway
    $gateway = Get-NetRoute -InterfaceIndex $adapter.InterfaceIndex -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($gateway) {
        Write-Host "  Gateway: $($gateway.NextHop)" -ForegroundColor Yellow
    }
    
    Write-Host ""
}

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "INFORMAÇÕES PARA IP-MAC BINDING" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Encontrar adaptador principal (geralmente Ethernet ou Wi-Fi)
$mainAdapter = $adapters | Where-Object {$_.Name -like "*Ethernet*" -or $_.Name -like "*Wi-Fi*" -or $_.Name -like "*LAN*"} | Select-Object -First 1
if (-not $mainAdapter) {
    $mainAdapter = $adapters | Select-Object -First 1
}

if ($mainAdapter) {
    $macAddress = $mainAdapter.MacAddress
    $ipAddress = (Get-NetIPAddress -InterfaceIndex $mainAdapter.InterfaceIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
    
    Write-Host "Adaptador Principal: $($mainAdapter.Name)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Para adicionar no roteador:" -ForegroundColor Cyan
    Write-Host "  IP Address:   $ipAddress" -ForegroundColor Green
    Write-Host "  MAC Address:   $macAddress" -ForegroundColor Green
    Write-Host "  Interface:     LAN (ou interface principal)" -ForegroundColor Gray
    Write-Host "  Description:   PC Desenvolvimento (ou nome de sua escolha)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Formato MAC para roteador:" -ForegroundColor Cyan
    Write-Host "  $($macAddress -replace '-',':')" -ForegroundColor Green
    Write-Host ""
}

Write-Host "==========================================" -ForegroundColor Green
Write-Host "PRONTO PARA CONFIGURAR NO ROTEADOR" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""


