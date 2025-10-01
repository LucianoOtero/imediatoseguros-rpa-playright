#!/bin/bash
# Teste RPA Modular com monitoramento em tempo real

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Teste RPA Modular ==="

# Função de cleanup
cleanup() {
    if [ ! -z "$SESSION_ID" ]; then
        log_info "Limpando sessão $SESSION_ID..."
        # TODO: Implementar endpoint para cancelar sessão se necessário
    fi
}
trap cleanup EXIT

# Iniciar sessão
log_info "Iniciando sessão RPA Modular..."
RESPONSE=$(curl -s --connect-timeout $CONNECTION_TIMEOUT -X POST "$API_URL$START_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

if ! validate_json "$RESPONSE"; then
    log_error "Resposta inválida da API"
    echo "Resposta: $RESPONSE"
    exit 1
fi

SESSION_ID=$(echo "$RESPONSE" | jq -r '.session_id')
if [ "$SESSION_ID" = "null" ] || [ -z "$SESSION_ID" ]; then
    log_error "Falha ao criar sessão"
    echo "Resposta: $RESPONSE"
    exit 1
fi

log_success "Sessão criada: $SESSION_ID"

# Monitorar progresso com timeout
log_info "Monitorando progresso (timeout: ${TIMEOUT}s)..."
START_TIME=$(date +%s)
LAST_ETAPA=0
LAST_STATUS=""

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        log_error "Timeout atingido (${TIMEOUT}s)"
        exit 1
    fi
    
    PROGRESS=$(curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$PROGRESS_ENDPOINT/$SESSION_ID")
    if [ $? -ne 0 ]; then
        log_error "Falha ao consultar progresso"
        exit 1
    fi
    
    if ! validate_json "$PROGRESS"; then
        log_error "Resposta de progresso inválida"
        continue
    fi
    
    STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
    ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
    TOTAL=$(echo "$PROGRESS" | jq -r '.progress.total_etapas')
    PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
    MENSAGEM=$(echo "$PROGRESS" | jq -r '.progress.mensagem')
    
    # Só imprimir quando a etapa ou status mudar
    if [ "$ETAPA" != "$LAST_ETAPA" ] || [ "$STATUS" != "$LAST_STATUS" ]; then
        log_info "Etapa $ETAPA/$TOTAL ($PERCENTUAL%) - $STATUS: $MENSAGEM"
        LAST_ETAPA=$ETAPA
        LAST_STATUS=$STATUS
    fi
    
    # Verificar sucesso
    if [ "$STATUS" = "success" ] && [ "$ETAPA" = "5" ]; then
        ESTIMATIVAS=$(echo "$PROGRESS" | jq -r '.progress.estimativas.capturadas')
        if [ "$ESTIMATIVAS" = "true" ]; then
            log_success "Estimativas capturadas com sucesso!"
            echo "$PROGRESS" | jq '.progress.estimativas.dados'
            
            # Validar arquivo de progresso
            PROGRESS_FILE="$RPA_DATA_DIR/progress_${SESSION_ID}.json"
            if [ -f "$PROGRESS_FILE" ]; then
                log_success "Arquivo de progresso gerado: $PROGRESS_FILE"
            else
                log_warning "Arquivo de progresso não encontrado: $PROGRESS_FILE"
            fi
            break
        fi
    fi
    
    # Verificar erro
    if [ "$STATUS" = "failed" ] || [ "$STATUS" = "error" ]; then
        log_error "Erro na execução: $MENSAGEM"
        echo "Progresso completo: $PROGRESS"
        exit 1
    fi
    
    sleep $POLL_INTERVAL
done

log_success "Teste RPA Modular concluído com sucesso"
