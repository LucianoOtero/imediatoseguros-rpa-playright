#!/bin/bash
# Script de preparação do ambiente de teste

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Preparação do Ambiente de Teste ==="

# Verificar se estamos no servidor correto
if [ "$(hostname)" != "ubuntu-2gb-hel1-1" ]; then
    log_error "Execute este script no servidor Hetzner"
    exit 1
fi
log_success "Servidor correto: $(hostname)"

# Verificar serviços críticos
log_info "Verificando serviços..."
services=("nginx" "php8.3-fpm" "redis-server")
for service in "${services[@]}"; do
    if systemctl is-active --quiet "$service"; then
        log_success "$service está ativo"
    else
        log_error "Serviço $service não está ativo"
        exit 1
    fi
done

# Verificar se a API V4 está respondendo
log_info "Verificando API V4..."
if curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$HEALTH_ENDPOINT" | jq -e '.success' >/dev/null 2>&1; then
    log_success "API V4 está respondendo"
else
    log_error "API V4 não está respondendo"
    exit 1
fi

# Limpar dados de teste anteriores
log_info "Limpando dados de teste anteriores..."
rm -f "$RPA_DATA_DIR"/progress_test_*
rm -f "$RPA_DATA_DIR"/history_test_*
rm -f "$RPA_DATA_DIR"/dados_planos_seguro_test_*
rm -f "$SESSIONS_DIR"/test_*
log_success "Dados de teste anteriores limpos"

# Verificar permissões
log_info "Verificando permissões..."
directories=("$RPA_DATA_DIR" "$SESSIONS_DIR" "$SCRIPTS_DIR")
for dir in "${directories[@]}"; do
    if [ -w "$dir" ]; then
        log_success "$dir é gravável"
    else
        log_error "Diretório $dir não é gravável"
        exit 1
    fi
done

# Verificar implementação --data (opcional)
log_info "Verificando implementação --data..."
if grep -q "add_argument.*--data" /opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py; then
    log_success "RPA Modular tem --data implementado"
else
    log_warning "RPA Modular pode não ter --data implementado"
fi

if grep -q "add_argument.*--data" /opt/imediatoseguros-rpa/executar_rpa_imediato_playwright.py; then
    log_success "RPA Principal tem --data implementado"
else
    log_warning "RPA Principal pode não ter --data implementado"
fi

log_success "Preparação concluída com sucesso"
