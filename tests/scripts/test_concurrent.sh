#!/bin/bash
# Teste de execuções concorrentes

# Carregar configurações
source "$(dirname "$0")/../config/test_config.sh"

set -e

log_info "=== Teste de Execuções Concorrentes ==="

# Função de cleanup
cleanup() {
    if [ ! -z "$SESSION1" ]; then
        log_info "Limpando sessão 1: $SESSION1"
    fi
    if [ ! -z "$SESSION2" ]; then
        log_info "Limpando sessão 2: $SESSION2"
    fi
}
trap cleanup EXIT

# Iniciar 2 sessões simultâneas
log_info "Iniciando 2 sessões simultâneas..."

RESPONSE1=$(curl -s --connect-timeout $CONNECTION_TIMEOUT -X POST "$API_URL$START_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

RESPONSE2=$(curl -s --connect-timeout $CONNECTION_TIMEOUT -X POST "$API_URL$START_ENDPOINT" \
  -H "Content-Type: application/json" \
  -d "$TEST_DATA")

SESSION1=$(echo "$RESPONSE1" | jq -r '.session_id')
SESSION2=$(echo "$RESPONSE2" | jq -r '.session_id')

if [ "$SESSION1" = "null" ] || [ -z "$SESSION1" ] || [ "$SESSION2" = "null" ] || [ -z "$SESSION2" ]; then
    log_error "Falha ao criar uma ou ambas as sessões"
    echo "Resposta 1: $RESPONSE1"
    echo "Resposta 2: $RESPONSE2"
    exit 1
fi

log_success "Sessões criadas: $SESSION1 e $SESSION2"

# Monitorar ambas as sessões
log_info "Monitorando ambas as sessões..."
START_TIME=$(date +%s)
SESSION1_COMPLETED=false
SESSION2_COMPLETED=false

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        log_error "Timeout atingido (${TIMEOUT}s)"
        exit 1
    fi
    
    # Consultar progresso das duas sessões
    PROGRESS1=$(curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$PROGRESS_ENDPOINT/$SESSION1")
    PROGRESS2=$(curl -s --connect-timeout $CONNECTION_TIMEOUT "$API_URL$PROGRESS_ENDPOINT/$SESSION2")
    
    STATUS1=$(echo "$PROGRESS1" | jq -r '.progress.status')
    STATUS2=$(echo "$PROGRESS2" | jq -r '.progress.status')
    
    ETAPA1=$(echo "$PROGRESS1" | jq -r '.progress.etapa_atual')
    ETAPA2=$(echo "$PROGRESS2" | jq -r '.progress.etapa_atual')
    
    PERCENTUAL1=$(echo "$PROGRESS1" | jq -r '.progress.percentual')
    PERCENTUAL2=$(echo "$PROGRESS2" | jq -r '.progress.percentual')
    
    # Log a cada 10 segundos ou quando houver mudança significativa
    if [ $((ELAPSED % 10)) -eq 0 ] || [ "$STATUS1" != "$LAST_STATUS1" ] || [ "$STATUS2" != "$LAST_STATUS2" ]; then
        log_info "Sessão 1: Etapa $ETAPA1 ($PERCENTUAL1%) - $STATUS1 | Sessão 2: Etapa $ETAPA2 ($PERCENTUAL2%) - $STATUS2"
        LAST_STATUS1=$STATUS1
        LAST_STATUS2=$STATUS2
    fi
    
    # Verificar se ambas concluíram
    if [ "$STATUS1" = "success" ] && [ "$STATUS2" = "success" ]; then
        log_success "Ambas as sessões concluídas com sucesso!"
        break
    fi
    
    # Verificar se alguma falhou
    if [ "$STATUS1" = "failed" ] || [ "$STATUS1" = "error" ] || [ "$STATUS2" = "failed" ] || [ "$STATUS2" = "error" ]; then
        log_error "Uma das sessões falhou!"
        echo "Progresso Sessão 1: $PROGRESS1"
        echo "Progresso Sessão 2: $PROGRESS2"
        exit 1
    fi
    
    sleep $POLL_INTERVAL
done

log_success "Teste de execuções concorrentes concluído com sucesso"
