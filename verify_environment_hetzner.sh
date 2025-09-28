#!/bin/bash
# 🔍 VERIFICAÇÃO DE AMBIENTE - HETZNER/UBUNTU
# Script para verificar se o ambiente está pronto para o RPA v3.6.0

set -e  # Parar em caso de erro

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Função para log colorido
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
}

info() {
    echo -e "${BLUE}[$(date +'%Y-%d %H:%M:%S')] INFO: $1${NC}"
}

success() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] ✅ $1${NC}"
}

fail() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ❌ $1${NC}"
}

# Variáveis de verificação
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# Função para verificar comando
check_command() {
    local cmd=$1
    local name=$2
    local required=${3:-true}
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if command -v "$cmd" &> /dev/null; then
        local version=$(eval "$cmd --version 2>/dev/null | head -1" || echo "versão não detectada")
        success "$name: $version"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        if [ "$required" = "true" ]; then
            fail "$name: não encontrado"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        else
            warn "$name: não encontrado (opcional)"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    fi
}

# Função para verificar serviço
check_service() {
    local service=$1
    local name=$2
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if systemctl is-active --quiet "$service"; then
        success "$name: ativo"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    elif systemctl is-enabled --quiet "$service"; then
        warn "$name: habilitado mas inativo"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    else
        fail "$name: não encontrado ou inativo"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Função para verificar porta
check_port() {
    local port=$1
    local name=$2
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if netstat -tuln | grep -q ":$port "; then
        success "$name: porta $port aberta"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "$name: porta $port não está aberta"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar arquivo
check_file() {
    local file=$1
    local name=$2
    local required=${3:-true}
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [ -f "$file" ]; then
        local size=$(du -h "$file" | cut -f1)
        success "$name: encontrado ($size)"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        if [ "$required" = "true" ]; then
            fail "$name: não encontrado"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        else
            warn "$name: não encontrado (opcional)"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    fi
}

# Função para verificar diretório
check_directory() {
    local dir=$1
    local name=$2
    local required=${3:-true}
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [ -d "$dir" ]; then
        local files=$(find "$dir" -type f | wc -l)
        success "$name: encontrado ($files arquivos)"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        if [ "$required" = "true" ]; then
            fail "$name: não encontrado"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        else
            warn "$name: não encontrado (opcional)"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    fi
}

# Função para verificar conexão Redis
check_redis_connection() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if command -v redis-cli &> /dev/null; then
        if redis-cli ping | grep -q "PONG"; then
            success "Redis: conectado e respondendo"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            fail "Redis: não está respondendo"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    else
        fail "Redis: redis-cli não encontrado"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Função para verificar módulos Python
check_python_module() {
    local module=$1
    local name=$2
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if python3 -c "import $module" 2>/dev/null; then
        local version=$(python3 -c "import $module; print(getattr($module, '__version__', 'versão não detectada'))" 2>/dev/null || echo "versão não detectada")
        success "$name: $version"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        fail "$name: não encontrado"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Função para verificar permissões
check_permissions() {
    local path=$1
    local name=$2
    local required_perm=$3
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if [ -e "$path" ]; then
        local perms=$(stat -c "%a" "$path" 2>/dev/null || echo "000")
        if [ "$perms" = "$required_perm" ] || [ "$perms" = "755" ] || [ "$perms" = "777" ]; then
            success "$name: permissões OK ($perms)"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            warn "$name: permissões podem estar incorretas ($perms)"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    else
        fail "$name: caminho não existe"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Função para verificar espaço em disco
check_disk_space() {
    local path=${1:-.}
    local min_gb=${2:-5}
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local available=$(df "$path" | tail -1 | awk '{print $4}')
    local available_gb=$((available / 1024 / 1024))
    
    if [ "$available_gb" -ge "$min_gb" ]; then
        success "Espaço em disco: ${available_gb}GB disponível"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Espaço em disco: apenas ${available_gb}GB disponível (mínimo: ${min_gb}GB)"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar memória
check_memory() {
    local min_gb=${1:-2}
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local total_mem=$(free -g | awk 'NR==2{print $2}')
    
    if [ "$total_mem" -ge "$min_gb" ]; then
        success "Memória RAM: ${total_mem}GB total"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Memória RAM: apenas ${total_mem}GB total (mínimo: ${min_gb}GB)"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar conectividade de rede
check_network() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if ping -c 1 8.8.8.8 &> /dev/null; then
        success "Conectividade de rede: OK"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        fail "Conectividade de rede: falha"
        FAILED_CHECKS=$((FAILED_CHECKS + 1))
        return 1
    fi
}

# Função para verificar configuração Nginx
check_nginx_config() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if command -v nginx &> /dev/null; then
        if nginx -t &> /dev/null; then
            success "Nginx: configuração válida"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            fail "Nginx: configuração inválida"
            FAILED_CHECKS=$((FAILED_CHECKS + 1))
            return 1
        fi
    else
        warn "Nginx: não encontrado"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar certificados SSL
check_ssl_certificates() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local cert_paths=(
        "/etc/ssl/certs/ssl-cert-snakeoil.pem"
        "/etc/letsencrypt/live/*/fullchain.pem"
        "/etc/ssl/certs/ca-certificates.crt"
    )
    
    local found_cert=false
    for path in "${cert_paths[@]}"; do
        if ls $path &> /dev/null; then
            found_cert=true
            break
        fi
    done
    
    if [ "$found_cert" = true ]; then
        success "Certificados SSL: encontrados"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Certificados SSL: não encontrados"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar logs
check_logs() {
    local log_dir="/var/log"
    local required_logs=("syslog" "auth.log")
    
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local found_logs=0
    for log in "${required_logs[@]}"; do
        if [ -f "$log_dir/$log" ]; then
            found_logs=$((found_logs + 1))
        fi
    done
    
    if [ "$found_logs" -gt 0 ]; then
        success "Logs do sistema: $found_logs/${#required_logs[@]} encontrados"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Logs do sistema: não encontrados"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar firewall
check_firewall() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    if command -v ufw &> /dev/null; then
        local status=$(ufw status | head -1)
        if echo "$status" | grep -q "active"; then
            success "Firewall UFW: ativo"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            warn "Firewall UFW: inativo"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    elif command -v iptables &> /dev/null; then
        local rules=$(iptables -L | wc -l)
        if [ "$rules" -gt 3 ]; then
            success "Firewall iptables: $rules regras ativas"
            PASSED_CHECKS=$((PASSED_CHECKS + 1))
            return 0
        else
            warn "Firewall iptables: poucas regras"
            WARNING_CHECKS=$((WARNING_CHECKS + 1))
            return 0
        fi
    else
        warn "Firewall: não encontrado"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar backups
check_backups() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local backup_dirs=(
        "/var/backups"
        "/home/backup"
        "/opt/backup"
        "./backup_*"
    )
    
    local found_backups=0
    for dir in "${backup_dirs[@]}"; do
        if ls $dir &> /dev/null; then
            found_backups=$((found_backups + 1))
        fi
    done
    
    if [ "$found_backups" -gt 0 ]; then
        success "Backups: $found_backups diretórios encontrados"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Backups: nenhum diretório encontrado"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para verificar processos RPA
check_rpa_processes() {
    TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
    
    local rpa_processes=$(ps aux | grep -E "(python.*rpa|node.*websocket|redis)" | grep -v grep | wc -l)
    
    if [ "$rpa_processes" -gt 0 ]; then
        success "Processos RPA: $rpa_processes em execução"
        PASSED_CHECKS=$((PASSED_CHECKS + 1))
        return 0
    else
        warn "Processos RPA: nenhum em execução"
        WARNING_CHECKS=$((WARNING_CHECKS + 1))
        return 0
    fi
}

# Função para gerar relatório
generate_report() {
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local report_file="environment_report_${timestamp}.txt"
    
    {
        echo "=========================================="
        echo "RELATÓRIO DE VERIFICAÇÃO DE AMBIENTE"
        echo "=========================================="
        echo "Data: $(date)"
        echo "Sistema: $(uname -a)"
        echo "Usuário: $(whoami)"
        echo "Diretório: $(pwd)"
        echo ""
        echo "RESUMO:"
        echo "  Total de verificações: $TOTAL_CHECKS"
        echo "  Passou: $PASSED_CHECKS"
        echo "  Falhou: $FAILED_CHECKS"
        echo "  Avisos: $WARNING_CHECKS"
        echo ""
        
        if [ "$FAILED_CHECKS" -eq 0 ]; then
            echo "STATUS GERAL: ✅ AMBIENTE PRONTO"
        elif [ "$FAILED_CHECKS" -le 2 ]; then
            echo "STATUS GERAL: ⚠️ AMBIENTE PARCIALMENTE PRONTO"
        else
            echo "STATUS GERAL: ❌ AMBIENTE NÃO PRONTO"
        fi
        
        echo ""
        echo "RECOMENDAÇÕES:"
        
        if [ "$FAILED_CHECKS" -gt 0 ]; then
            echo "  - Corrigir os itens que falharam"
        fi
        
        if [ "$WARNING_CHECKS" -gt 0 ]; then
            echo "  - Revisar os itens com avisos"
        fi
        
        echo "  - Executar testes: python3 run_all_tests.py"
        echo "  - Monitorar serviços: ./monitor_services.sh"
        echo ""
        echo "=========================================="
    } > "$report_file"
    
    echo "📄 Relatório salvo em: $report_file"
}

# MAIN SCRIPT
echo -e "${CYAN}"
echo "=========================================="
echo "🔍 VERIFICAÇÃO DE AMBIENTE - HETZNER/UBUNTU"
echo "=========================================="
echo -e "${NC}"

log "Iniciando verificação de ambiente..."
log "Sistema: $(uname -a)"
log "Usuário: $(whoami)"
log "Diretório: $(pwd)"
echo ""

# 1. VERIFICAÇÕES BÁSICAS DO SISTEMA
echo -e "${BLUE}📋 VERIFICAÇÕES BÁSICAS DO SISTEMA${NC}"
echo "----------------------------------------"

check_command "python3" "Python 3" true
check_command "pip3" "Pip 3" true
check_command "node" "Node.js" true
check_command "npm" "NPM" true
check_command "git" "Git" true
check_command "curl" "Curl" true
check_command "wget" "Wget" false
check_command "unzip" "Unzip" false
check_command "htop" "Htop" false
check_command "vim" "Vim" false
check_command "nano" "Nano" false

echo ""

# 2. VERIFICAÇÕES DE SERVIÇOS
echo -e "${BLUE}🔧 VERIFICAÇÕES DE SERVIÇOS${NC}"
echo "----------------------------------------"

check_service "redis-server" "Redis Server"
check_service "nginx" "Nginx" false
check_service "apache2" "Apache" false
check_service "mysql" "MySQL" false
check_service "postgresql" "PostgreSQL" false

echo ""

# 3. VERIFICAÇÕES DE CONECTIVIDADE
echo -e "${BLUE}🌐 VERIFICAÇÕES DE CONECTIVIDADE${NC}"
echo "----------------------------------------"

check_redis_connection
check_port "6379" "Redis"
check_port "8765" "WebSocket"
check_port "80" "HTTP"
check_port "443" "HTTPS"
check_network

echo ""

# 4. VERIFICAÇÕES DE MÓDULOS PYTHON
echo -e "${BLUE}🐍 VERIFICAÇÕES DE MÓDULOS PYTHON${NC}"
echo "----------------------------------------"

check_python_module "redis" "Redis Python"
check_python_module "websockets" "WebSockets Python"
check_python_module "asyncio" "Asyncio"
check_python_module "psutil" "PSUtil"
check_python_module "playwright" "Playwright"
check_python_module "requests" "Requests"
check_python_module "json" "JSON"
check_python_module "logging" "Logging"

echo ""

# 5. VERIFICAÇÕES DE ARQUIVOS E DIRETÓRIOS
echo -e "${BLUE}📁 VERIFICAÇÕES DE ARQUIVOS E DIRETÓRIOS${NC}"
echo "----------------------------------------"

check_directory "utils" "Diretório Utils" true
check_file "utils/platform_utils.py" "Platform Utils" true
check_file "utils/redis_manager.py" "Redis Manager" true
check_file "utils/websocket_manager.py" "WebSocket Manager" true
check_file "utils/communication_manager.py" "Communication Manager" true
check_file "tela_2_placa.py" "Tela 2" true
check_file "tela_3_confirmacao_veiculo.py" "Tela 3" true
check_file "tela_4_confirmacao_segurado.py" "Tela 4" true
check_file "tela_5_estimativas.py" "Tela 5" true
check_file "websocket_server.js" "WebSocket Server" true
check_file "package.json" "Package.json" true
check_file "test_communication_system.py" "Teste Comunicação" true
check_file "test_rpa_modules.py" "Teste RPA" true
check_file "run_all_tests.py" "Teste Geral" true

echo ""

# 6. VERIFICAÇÕES DE PERMISSÕES
echo -e "${BLUE}🔐 VERIFICAÇÕES DE PERMISSÕES${NC}"
echo "----------------------------------------"

check_permissions "." "Diretório atual" "755"
check_permissions "utils" "Diretório Utils" "755"
check_permissions "websocket_server.js" "WebSocket Server" "755"
check_permissions "package.json" "Package.json" "644"

echo ""

# 7. VERIFICAÇÕES DE RECURSOS
echo -e "${BLUE}💻 VERIFICAÇÕES DE RECURSOS${NC}"
echo "----------------------------------------"

check_disk_space "." "10"
check_memory "4"
check_rpa_processes

echo ""

# 8. VERIFICAÇÕES DE SEGURANÇA
echo -e "${BLUE}🛡️ VERIFICAÇÕES DE SEGURANÇA${NC}"
echo "----------------------------------------"

check_firewall
check_ssl_certificates
check_logs
check_backups

echo ""

# 9. VERIFICAÇÕES DE CONFIGURAÇÃO
echo -e "${BLUE}⚙️ VERIFICAÇÕES DE CONFIGURAÇÃO${NC}"
echo "----------------------------------------"

check_nginx_config
check_file "nginx_rpaimediatoseguros.conf" "Config Nginx" false
check_file "bidirectional_config.json" "Config Bidirecional" false
check_file "rpa-websocket.service" "Service WebSocket" false

echo ""

# 10. RESUMO FINAL
echo -e "${CYAN}📊 RESUMO FINAL${NC}"
echo "=========================================="

log "Total de verificações: $TOTAL_CHECKS"
success "Passou: $PASSED_CHECKS"
if [ "$FAILED_CHECKS" -gt 0 ]; then
    fail "Falhou: $FAILED_CHECKS"
else
    success "Falhou: $FAILED_CHECKS"
fi
if [ "$WARNING_CHECKS" -gt 0 ]; then
    warn "Avisos: $WARNING_CHECKS"
else
    success "Avisos: $WARNING_CHECKS"
fi

echo ""

# Status geral
if [ "$FAILED_CHECKS" -eq 0 ]; then
    success "🎉 AMBIENTE PRONTO PARA RPA v3.6.0!"
    echo ""
    log "Próximos passos:"
    log "  1. Execute: ./start_services.sh"
    log "  2. Execute: python3 run_all_tests.py"
    log "  3. Execute: ./monitor_services.sh"
elif [ "$FAILED_CHECKS" -le 2 ]; then
    warn "⚠️ AMBIENTE PARCIALMENTE PRONTO"
    echo ""
    log "Recomendações:"
    log "  - Corrigir os itens que falharam"
    log "  - Revisar os itens com avisos"
    log "  - Executar testes após correções"
else
    fail "❌ AMBIENTE NÃO PRONTO"
    echo ""
    log "Ações necessárias:"
    log "  - Corrigir os itens que falharam"
    log "  - Instalar dependências faltantes"
    log "  - Configurar serviços necessários"
fi

echo ""

# Gerar relatório
generate_report

echo ""
log "Verificação concluída!"
