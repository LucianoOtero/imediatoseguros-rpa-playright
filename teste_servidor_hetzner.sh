#!/bin/bash

# =============================================================================
# SCRIPT DE TESTE COMPLETO - SERVIDOR HETZNER RPA
# =============================================================================
# Data: 26/01/2025
# Servidor: rpaimediatoseguros.com.br (37.27.92.160)
# =============================================================================

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Função para imprimir status
print_status() {
    local status=$1
    local message=$2
    if [ "$status" = "OK" ]; then
        echo -e "${GREEN}✅ $message${NC}"
    elif [ "$status" = "ERROR" ]; then
        echo -e "${RED}❌ $message${NC}"
    elif [ "$status" = "WARNING" ]; then
        echo -e "${YELLOW}⚠️  $message${NC}"
    else
        echo -e "${BLUE}ℹ️  $message${NC}"
    fi
}

# Função para testar conectividade
test_connectivity() {
    local url=$1
    local description=$2
    if curl -s -I "$url" > /dev/null 2>&1; then
        print_status "OK" "$description: $url"
        return 0
    else
        print_status "ERROR" "$description: $url"
        return 1
    fi
}

# Função para testar serviço
test_service() {
    local service=$1
    local description=$2
    if systemctl is-active --quiet "$service"; then
        print_status "OK" "$description: $service ativo"
        return 0
    else
        print_status "ERROR" "$description: $service inativo"
        return 1
    fi
}

# Função para testar porta
test_port() {
    local port=$1
    local description=$2
    if netstat -tlnp | grep -q ":$port "; then
        print_status "OK" "$description: Porta $port ouvindo"
        return 0
    else
        print_status "ERROR" "$description: Porta $port não está ouvindo"
        return 1
    fi
}

# Função para testar comando
test_command() {
    local command=$1
    local description=$2
    if command -v "$command" > /dev/null 2>&1; then
        print_status "OK" "$description: $command instalado"
        return 0
    else
        print_status "ERROR" "$description: $command não encontrado"
        return 1
    fi
}

echo -e "${BLUE}=============================================================================${NC}"
echo -e "${BLUE}🧪 TESTE COMPLETO DO SERVIDOR HETZNER RPA${NC}"
echo -e "${BLUE}=============================================================================${NC}"
echo -e "${BLUE}Servidor: rpaimediatoseguros.com.br (37.27.92.160)${NC}"
echo -e "${BLUE}Data: $(date)${NC}"
echo -e "${BLUE}=============================================================================${NC}"
echo

# Contadores
total_tests=0
passed_tests=0
failed_tests=0

# =============================================================================
# 1. TESTES DE SISTEMA
# =============================================================================
echo -e "${YELLOW}📋 1. TESTES DE SISTEMA${NC}"
echo "----------------------------------------"

# Teste 1.1: Sistema operacional
total_tests=$((total_tests + 1))
if [ -f /etc/os-release ]; then
    os_info=$(grep PRETTY_NAME /etc/os-release | cut -d'"' -f2)
    print_status "OK" "Sistema: $os_info"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Sistema: Não foi possível identificar o OS"
    failed_tests=$((failed_tests + 1))
fi

# Teste 1.2: Uptime
total_tests=$((total_tests + 1))
uptime_info=$(uptime -p)
print_status "OK" "Uptime: $uptime_info"
passed_tests=$((passed_tests + 1))

# Teste 1.3: Memória
total_tests=$((total_tests + 1))
memory_info=$(free -h | grep Mem | awk '{print $3 "/" $2}')
print_status "OK" "Memória: $memory_info"
passed_tests=$((passed_tests + 1))

# Teste 1.4: Disco
total_tests=$((total_tests + 1))
disk_info=$(df -h / | tail -1 | awk '{print $3 "/" $2 " (" $5 " usado)"}')
print_status "OK" "Disco: $disk_info"
passed_tests=$((passed_tests + 1))

echo

# =============================================================================
# 2. TESTES DE SERVIÇOS
# =============================================================================
echo -e "${YELLOW}🔧 2. TESTES DE SERVIÇOS${NC}"
echo "----------------------------------------"

# Teste 2.1: Nginx
total_tests=$((total_tests + 1))
if test_service "nginx" "Nginx"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 2.2: Redis
total_tests=$((total_tests + 1))
if test_service "redis-server" "Redis"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 2.3: PHP-FPM
total_tests=$((total_tests + 1))
if test_service "php8.3-fpm" "PHP-FPM"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 2.4: WebSocket
total_tests=$((total_tests + 1))
if test_service "rpa-websocket" "WebSocket"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 3. TESTES DE PORTAS
# =============================================================================
echo -e "${YELLOW}🌐 3. TESTES DE PORTAS${NC}"
echo "----------------------------------------"

# Teste 3.1: Porta 80 (HTTP)
total_tests=$((total_tests + 1))
if test_port "80" "HTTP"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 3.2: Porta 443 (HTTPS)
total_tests=$((total_tests + 1))
if test_port "443" "HTTPS"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 3.3: Porta 8080 (WebSocket)
total_tests=$((total_tests + 1))
if test_port "8080" "WebSocket"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 3.4: Porta 6379 (Redis)
total_tests=$((total_tests + 1))
if test_port "6379" "Redis"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 4. TESTES DE CONECTIVIDADE
# =============================================================================
echo -e "${YELLOW}🔗 4. TESTES DE CONECTIVIDADE${NC}"
echo "----------------------------------------"

# Teste 4.1: HTTP local
total_tests=$((total_tests + 1))
if test_connectivity "http://localhost" "HTTP Local"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 4.2: HTTPS local
total_tests=$((total_tests + 1))
if test_connectivity "https://localhost" "HTTPS Local"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 4.3: HTTP externo
total_tests=$((total_tests + 1))
if test_connectivity "http://rpaimediatoseguros.com.br" "HTTP Externo"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 4.4: HTTPS externo
total_tests=$((total_tests + 1))
if test_connectivity "https://rpaimediatoseguros.com.br" "HTTPS Externo"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 4.5: Redirecionamento HTTP → HTTPS
total_tests=$((total_tests + 1))
redirect_status=$(curl -s -I "http://rpaimediatoseguros.com.br" | grep -i "location" | grep -i "https")
if [ -n "$redirect_status" ]; then
    print_status "OK" "Redirecionamento HTTP → HTTPS funcionando"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Redirecionamento HTTP → HTTPS não funcionando"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 5. TESTES DE DNS
# =============================================================================
echo -e "${YELLOW}🌍 5. TESTES DE DNS${NC}"
echo "----------------------------------------"

# Teste 5.1: Resolução DNS principal
total_tests=$((total_tests + 1))
dns_result=$(nslookup rpaimediatoseguros.com.br | grep "Address:" | tail -1 | awk '{print $2}')
if [ "$dns_result" = "37.27.92.160" ]; then
    print_status "OK" "DNS principal: rpaimediatoseguros.com.br → $dns_result"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "DNS principal: rpaimediatoseguros.com.br → $dns_result (esperado: 37.27.92.160)"
    failed_tests=$((failed_tests + 1))
fi

# Teste 5.2: Resolução DNS www
total_tests=$((total_tests + 1))
dns_www_result=$(nslookup www.rpaimediatoseguros.com.br | grep "Address:" | tail -1 | awk '{print $2}')
if [ "$dns_www_result" = "37.27.92.160" ]; then
    print_status "OK" "DNS www: www.rpaimediatoseguros.com.br → $dns_www_result"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "DNS www: www.rpaimediatoseguros.com.br → $dns_www_result (esperado: 37.27.92.160)"
    failed_tests=$((failed_tests + 1))
fi

# Teste 5.3: Resolução DNS API
total_tests=$((total_tests + 1))
dns_api_result=$(nslookup api.rpaimediatoseguros.com.br | grep "Address:" | tail -1 | awk '{print $2}')
if [ "$dns_api_result" = "37.27.92.160" ]; then
    print_status "OK" "DNS API: api.rpaimediatoseguros.com.br → $dns_api_result"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "DNS API: api.rpaimediatoseguros.com.br → $dns_api_result (esperado: 37.27.92.160)"
    failed_tests=$((failed_tests + 1))
fi

# Teste 5.4: Resolução DNS WebSocket
total_tests=$((total_tests + 1))
dns_ws_result=$(nslookup websocket.rpaimediatoseguros.com.br | grep "Address:" | tail -1 | awk '{print $2}')
if [ "$dns_ws_result" = "37.27.92.160" ]; then
    print_status "OK" "DNS WebSocket: websocket.rpaimediatoseguros.com.br → $dns_ws_result"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "DNS WebSocket: websocket.rpaimediatoseguros.com.br → $dns_ws_result (esperado: 37.27.92.160)"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 6. TESTES DE SSL
# =============================================================================
echo -e "${YELLOW}🔒 6. TESTES DE SSL${NC}"
echo "----------------------------------------"

# Teste 6.1: Certificado SSL
total_tests=$((total_tests + 1))
if [ -f "/etc/letsencrypt/live/rpaimediatoseguros.com.br/fullchain.pem" ]; then
    cert_expiry=$(openssl x509 -in /etc/letsencrypt/live/rpaimediatoseguros.com.br/fullchain.pem -noout -dates | grep notAfter | cut -d= -f2)
    print_status "OK" "Certificado SSL: Válido até $cert_expiry"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Certificado SSL: Arquivo não encontrado"
    failed_tests=$((failed_tests + 1))
fi

# Teste 6.2: Renovação automática
total_tests=$((total_tests + 1))
if systemctl list-timers | grep -q "certbot.timer"; then
    print_status "OK" "Renovação automática: Timer configurado"
    passed_tests=$((passed_tests + 1))
else
    print_status "WARNING" "Renovação automática: Timer não encontrado"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 7. TESTES DE PYTHON E PLAYWRIGHT
# =============================================================================
echo -e "${YELLOW}🐍 7. TESTES DE PYTHON E PLAYWRIGHT${NC}"
echo "----------------------------------------"

# Teste 7.1: Python
total_tests=$((total_tests + 1))
if test_command "python3" "Python 3"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 7.2: Pip
total_tests=$((total_tests + 1))
if test_command "pip3" "Pip 3"; then
    passed_tests=$((passed_tests + 1))
else
    failed_tests=$((failed_tests + 1))
fi

# Teste 7.3: Playwright
total_tests=$((total_tests + 1))
if [ -d "/var/www/rpaimediatoseguros.com.br/venv" ]; then
    source /var/www/rpaimediatoseguros.com.br/venv/bin/activate
    if python -c "import playwright; print('Playwright instalado')" 2>/dev/null; then
        print_status "OK" "Playwright: Instalado no venv"
        passed_tests=$((passed_tests + 1))
    else
        print_status "ERROR" "Playwright: Não instalado no venv"
        failed_tests=$((failed_tests + 1))
    fi
    deactivate
else
    print_status "ERROR" "Playwright: Virtual environment não encontrado"
    failed_tests=$((failed_tests + 1))
fi

# Teste 7.4: Browsers do Playwright
total_tests=$((total_tests + 1))
if [ -d "/var/www/rpaimediatoseguros.com.br/venv" ]; then
    source /var/www/rpaimediatoseguros.com.br/venv/bin/activate
    if python -c "from playwright.sync_api import sync_playwright; p = sync_playwright().start(); p.chromium.launch(); p.stop()" 2>/dev/null; then
        print_status "OK" "Browsers Playwright: Chromium funcionando"
        passed_tests=$((passed_tests + 1))
    else
        print_status "ERROR" "Browsers Playwright: Chromium não funcionando"
        failed_tests=$((failed_tests + 1))
    fi
    deactivate
else
    print_status "ERROR" "Browsers Playwright: Virtual environment não encontrado"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 8. TESTES DE REDIS
# =============================================================================
echo -e "${YELLOW}🔴 8. TESTES DE REDIS${NC}"
echo "----------------------------------------"

# Teste 8.1: Conectividade Redis
total_tests=$((total_tests + 1))
if redis-cli ping > /dev/null 2>&1; then
    print_status "OK" "Redis: Conectividade OK"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Redis: Conectividade falhou"
    failed_tests=$((failed_tests + 1))
fi

# Teste 8.2: Teste de escrita/leitura
total_tests=$((total_tests + 1))
if redis-cli set "test_key" "test_value" > /dev/null 2>&1 && redis-cli get "test_key" | grep -q "test_value"; then
    redis-cli del "test_key" > /dev/null 2>&1
    print_status "OK" "Redis: Escrita/leitura funcionando"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Redis: Escrita/leitura falhou"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 9. TESTES DE WEBSOCKET
# =============================================================================
echo -e "${YELLOW}🔌 9. TESTES DE WEBSOCKET${NC}"
echo "----------------------------------------"

# Teste 9.1: Conectividade WebSocket
total_tests=$((total_tests + 1))
if curl -s -I "http://localhost:8080" > /dev/null 2>&1; then
    print_status "OK" "WebSocket: Servidor respondendo na porta 8080"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "WebSocket: Servidor não responde na porta 8080"
    failed_tests=$((failed_tests + 1))
fi

# Teste 9.2: Logs do WebSocket
total_tests=$((total_tests + 1))
if journalctl -u rpa-websocket --no-pager -n 5 | grep -q "WebSocket server"; then
    print_status "OK" "WebSocket: Logs indicam servidor ativo"
    passed_tests=$((passed_tests + 1))
else
    print_status "WARNING" "WebSocket: Logs não encontrados ou servidor inativo"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# 10. TESTES DE ARQUIVOS E DIRETÓRIOS
# =============================================================================
echo -e "${YELLOW}📁 10. TESTES DE ARQUIVOS E DIRETÓRIOS${NC}"
echo "----------------------------------------"

# Teste 10.1: Diretório web
total_tests=$((total_tests + 1))
if [ -d "/var/www/rpaimediatoseguros.com.br" ]; then
    print_status "OK" "Diretório web: /var/www/rpaimediatoseguros.com.br existe"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Diretório web: /var/www/rpaimediatoseguros.com.br não existe"
    failed_tests=$((failed_tests + 1))
fi

# Teste 10.2: Arquivo index.html
total_tests=$((total_tests + 1))
if [ -f "/var/www/rpaimediatoseguros.com.br/index.html" ]; then
    print_status "OK" "Arquivo index.html: Existe"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Arquivo index.html: Não existe"
    failed_tests=$((failed_tests + 1))
fi

# Teste 10.3: Diretório WebSocket
total_tests=$((total_tests + 1))
if [ -d "/var/www/rpaimediatoseguros.com.br/websocket" ]; then
    print_status "OK" "Diretório WebSocket: Existe"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Diretório WebSocket: Não existe"
    failed_tests=$((failed_tests + 1))
fi

# Teste 10.4: Arquivo WebSocket
total_tests=$((total_tests + 1))
if [ -f "/var/www/rpaimediatoseguros.com.br/websocket/websocket_server.js" ]; then
    print_status "OK" "Arquivo WebSocket: websocket_server.js existe"
    passed_tests=$((passed_tests + 1))
else
    print_status "ERROR" "Arquivo WebSocket: websocket_server.js não existe"
    failed_tests=$((failed_tests + 1))
fi

# Teste 10.5: Diretório RPA (pendente)
total_tests=$((total_tests + 1))
if [ -d "/var/www/rpaimediatoseguros.com.br/rpa" ]; then
    print_status "OK" "Diretório RPA: Existe"
    passed_tests=$((passed_tests + 1))
else
    print_status "WARNING" "Diretório RPA: Não existe (pendente upload)"
    failed_tests=$((failed_tests + 1))
fi

echo

# =============================================================================
# RESUMO FINAL
# =============================================================================
echo -e "${BLUE}=============================================================================${NC}"
echo -e "${BLUE}📊 RESUMO FINAL${NC}"
echo -e "${BLUE}=============================================================================${NC}"

echo -e "Total de testes: $total_tests"
echo -e "${GREEN}Testes aprovados: $passed_tests${NC}"
echo -e "${RED}Testes falharam: $failed_tests${NC}"

# Calcular porcentagem
if [ $total_tests -gt 0 ]; then
    percentage=$((passed_tests * 100 / total_tests))
    echo -e "Taxa de sucesso: $percentage%"
    
    if [ $percentage -ge 90 ]; then
        echo -e "${GREEN}🎉 EXCELENTE! Servidor funcionando perfeitamente!${NC}"
    elif [ $percentage -ge 80 ]; then
        echo -e "${YELLOW}⚠️  BOM! Alguns ajustes podem ser necessários.${NC}"
    elif [ $percentage -ge 70 ]; then
        echo -e "${YELLOW}⚠️  REGULAR! Vários problemas encontrados.${NC}"
    else
        echo -e "${RED}❌ CRÍTICO! Muitos problemas encontrados.${NC}"
    fi
fi

echo -e "${BLUE}=============================================================================${NC}"
echo -e "${BLUE}Teste concluído em: $(date)${NC}"
echo -e "${BLUE}=============================================================================${NC}"

# Exit code baseado no resultado
if [ $failed_tests -eq 0 ]; then
    exit 0
else
    exit 1
fi







