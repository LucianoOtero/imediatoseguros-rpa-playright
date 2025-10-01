#!/bin/bash
# Script de teste de carga e performance

echo "=== Teste de Carga e Performance ==="

# Configurações
CONCURRENT_SESSIONS=5
TEST_DURATION=600  # 10 minutos
LOG_FILE="/tmp/load_test_$(date +%Y%m%d_%H%M%S).log"

# Função para iniciar sessão
start_session() {
    local session_num=$1
    local start_time=$(date +%s)
    
    SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')
    
    local end_time=$(date +%s)
    local response_time=$((end_time - start_time))
    
    echo "$(date): Sessão $session_num criada: $SESSION_ID (${response_time}s)" >> "$LOG_FILE"
    echo "$SESSION_ID" >> /tmp/sessions_load.txt
}

# Função para monitorar sessão
monitor_session() {
    local session_id=$1
    local start_time=$(date +%s)
    
    while true; do
        local current_time=$(date +%s)
        local elapsed=$((current_time - start_time))
        
        if [ $elapsed -gt $TEST_DURATION ]; then
            echo "$(date): Timeout para sessão $session_id" >> "$LOG_FILE"
            break
        fi
        
        PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$session_id)
        STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
        
        if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
            local end_time=$(date +%s)
            local total_time=$((end_time - start_time))
            echo "$(date): Sessão $session_id concluída: $STATUS (${total_time}s)" >> "$LOG_FILE"
            break
        fi
        
        sleep 5
    done
}

# Executar teste de carga
echo "Iniciando teste de carga com $CONCURRENT_SESSIONS sessões..."
echo "Duração: $TEST_DURATION segundos"
echo "Log: $LOG_FILE"

# Iniciar sessões
for i in $(seq 1 $CONCURRENT_SESSIONS); do
    start_session $i &
done

# Aguardar todas as sessões iniciarem
sleep 10

# Monitorar todas as sessões
while read -r SESSION_ID; do
    monitor_session "$SESSION_ID" &
done < /tmp/sessions_load.txt

# Aguardar conclusão
wait

# Limpar arquivo temporário
rm -f /tmp/sessions_load.txt

echo "=== Teste de carga concluído ==="
echo "Log salvo em: $LOG_FILE"
