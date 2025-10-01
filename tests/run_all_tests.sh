#!/bin/bash
# Script para executar todos os testes em sequência

# Carregar configurações
source "$(dirname "$0")/config/test_config.sh"

set -e

log_info "=== Execução Completa dos Testes API V4 ==="

# Função para executar teste com timeout
run_test_with_timeout() {
    local test_name="$1"
    local test_script="$2"
    local timeout_seconds="$3"
    
    log_info "Iniciando $test_name..."
    
    if timeout "$timeout_seconds" "$test_script"; then
        log_success "$test_name concluído com sucesso"
        return 0
    else
        local exit_code=$?
        if [ $exit_code -eq 124 ]; then
            log_error "$test_name atingiu timeout de ${timeout_seconds}s"
        else
            log_error "$test_name falhou com código $exit_code"
        fi
        return $exit_code
    fi
}

# Verificar se estamos no servidor correto
if [ "$(hostname)" != "ubuntu-2gb-hel1-1" ]; then
    log_error "Execute este script no servidor Hetzner"
    exit 1
fi

# Verificar se os scripts existem
SCRIPT_DIR="$(dirname "$0")/scripts"
if [ ! -d "$SCRIPT_DIR" ]; then
    log_error "Diretório de scripts não encontrado: $SCRIPT_DIR"
    exit 1
fi

# Executar testes em sequência
log_info "Iniciando sequência de testes..."

# 1. Preparação (5 minutos)
if ! run_test_with_timeout "Preparação do Ambiente" "$SCRIPT_DIR/test_prepare.sh" 300; then
    log_error "Falha na preparação. Abortando testes."
    exit 1
fi

# 2. Teste RPA Modular (15 minutos)
if ! run_test_with_timeout "Teste RPA Modular" "$SCRIPT_DIR/test_modular.sh" 900; then
    log_error "Falha no teste modular. Continuando com validação..."
fi

# 3. Teste RPA Principal (15 minutos)
if ! run_test_with_timeout "Teste RPA Principal" "$SCRIPT_DIR/test_principal.sh" 900; then
    log_error "Falha no teste principal. Continuando com validação..."
fi

# 4. Teste Concorrente (20 minutos)
if ! run_test_with_timeout "Teste Concorrente" "$SCRIPT_DIR/test_concurrent.sh" 1200; then
    log_error "Falha no teste concorrente. Continuando com validação..."
fi

# 5. Validação (5 minutos)
if ! run_test_with_timeout "Validação de Arquivos" "$SCRIPT_DIR/test_validation.sh" 300; then
    log_error "Falha na validação."
    exit 1
fi

# Resumo final
log_success "=== Todos os Testes Concluídos ==="
log_info "Verifique os logs acima para detalhes de cada teste"
log_info "Arquivos de progresso em: $RPA_DATA_DIR"
log_info "Arquivos de resultados em: /opt/imediatoseguros-rpa/"

# Listar arquivos gerados
log_info "Arquivos de progresso gerados:"
find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 2>/dev/null | head -5 || log_warning "Nenhum arquivo de progresso encontrado"

log_info "Arquivos de resultados gerados:"
find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 2>/dev/null | head -5 || log_warning "Nenhum arquivo de resultados encontrado"
