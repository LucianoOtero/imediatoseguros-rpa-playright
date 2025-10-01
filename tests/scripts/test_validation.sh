#!/bin/bash
# Validação de arquivos gerados

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Validação de Arquivos ==="

# Função para validar JSON
validate_json_file() {
    local file="$1"
    if [ ! -f "$file" ]; then
        log_error "Arquivo não encontrado: $file"
        return 1
    fi
    
    if command_exists jq; then
        if jq . "$file" >/dev/null 2>&1; then
            log_success "JSON válido: $(basename "$file")"
            return 0
        else
            log_error "JSON inválido: $(basename "$file")"
            return 1
        fi
    else
        if python3 -m json.tool "$file" >/dev/null 2>&1; then
            log_success "JSON válido: $(basename "$file")"
            return 0
        else
            log_error "JSON inválido: $(basename "$file")"
            return 1
        fi
    fi
}

# Validar arquivos de progresso
log_info "Validando arquivos de progresso..."
PROGRESS_FILES=$(find "$RPA_DATA_DIR" -name "progress_*.json" -mtime -1 | head -10)

if [ -z "$PROGRESS_FILES" ]; then
    log_warning "Nenhum arquivo de progresso recente encontrado"
else
    for file in $PROGRESS_FILES; do
        log_info "Validando: $(basename "$file")"
        
        if ! validate_json_file "$file"; then
            continue
        fi
        
        # Verificar campos obrigatórios
        ETAPA=$(jq -r '.etapa_atual' "$file")
        STATUS=$(jq -r '.status' "$file")
        SESSION_ID=$(jq -r '.session_id' "$file")
        TIMESTAMP=$(jq -r '.timestamp_atualizacao' "$file")
        
        log_info "  - Etapa: $ETAPA"
        log_info "  - Status: $STATUS"
        log_info "  - Session ID: $SESSION_ID"
        log_info "  - Timestamp: $TIMESTAMP"
        
        # Validar estimativas
        if [ "$ETAPA" = "5" ] || [ "$ETAPA" = "15" ]; then
            ESTIMATIVAS=$(jq -r '.dados_extra.estimativas_tela_5' "$file")
            if [ "$ESTIMATIVAS" != "null" ] && [ "$ESTIMATIVAS" != "false" ]; then
                COBERTURAS=$(jq -r '.dados_extra.estimativas_tela_5.coberturas_detalhadas | length' "$file")
                log_success "  - Estimativas capturadas ($COBERTURAS coberturas)"
            else
                log_warning "  - Estimativas não capturadas"
            fi
        fi
        
        # Validar resultados finais
        if [ "$ETAPA" = "15" ]; then
            PLANO_REC=$(jq -r '.dados_extra.plano_recomendado' "$file")
            if [ "$PLANO_REC" != "null" ]; then
                VALOR_REC=$(jq -r '.dados_extra.plano_recomendado.valor' "$file")
                log_success "  - Resultados finais capturados (Recomendado: $VALOR_REC)"
            else
                log_warning "  - Resultados finais não capturados"
            fi
        fi
        
        echo ""
    done
fi

# Validar arquivos de resultados
log_info "Validando arquivos de resultados..."
RESULT_FILES=$(find /opt/imediatoseguros-rpa/ -name "dados_planos_seguro_*.json" -mtime -1 | head -5)

if [ -z "$RESULT_FILES" ]; then
    log_warning "Nenhum arquivo de resultados recente encontrado"
else
    for file in $RESULT_FILES; do
        log_info "Validando: $(basename "$file")"
        
        if ! validate_json_file "$file"; then
            continue
        fi
        
        PLANO_REC=$(jq -r '.plano_recomendado.valor' "$file")
        PLANO_ALT=$(jq -r '.plano_alternativo.valor' "$file")
        
        log_info "  - Plano Recomendado: $PLANO_REC"
        log_info "  - Plano Alternativo: $PLANO_ALT"
        
        # Validar se os valores são válidos
        if [[ "$PLANO_REC" =~ ^R\$[0-9.,]+$ ]] && [[ "$PLANO_ALT" =~ ^R\$[0-9.,]+$ ]]; then
            log_success "  - Valores válidos"
        else
            log_warning "  - Valores podem estar inválidos"
        fi
        
        echo ""
    done
fi

log_success "Validação concluída"
