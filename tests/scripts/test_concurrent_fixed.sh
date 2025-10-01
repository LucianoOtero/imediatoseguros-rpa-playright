#!/bin/bash
# Script para testes concorrentes com progress tracker corrigido

echo "=== Testes Concorrentes (Progress Tracker Corrigido) ==="

# Função para iniciar sessão
start_session() {
    local session_num=$1
    curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id'
}

# Iniciar múltiplas sessões
echo "1. Iniciando 3 sessões simultâneas..."
for i in {1..3}; do
    SESSION_ID=$(start_session $i)
    echo "Sessão $i: $SESSION_ID"
    echo "$SESSION_ID" >> /tmp/sessions_concurrent.txt
done

# Monitorar todas as sessões
echo "2. Monitorando todas as sessões..."
START_TIME=$(date +%s)
TIMEOUT=1800  # 30 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    echo "=== Status das Sessões ($(date)) ==="
    ALL_COMPLETED=true
    
    while read -r SESSION_ID; do
        PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
        STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
        ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
        PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
        
        echo "Sessão $SESSION_ID: $STATUS (Etapa $ETAPA, $PERCENTUAL%)"
        
        if [ "$STATUS" != "success" ] && [ "$STATUS" != "failed" ]; then
            ALL_COMPLETED=false
        fi
    done < /tmp/sessions_concurrent.txt
    
    if [ "$ALL_COMPLETED" = true ]; then
        echo "Todas as sessões concluídas!"
        break
    fi
    
    sleep 10
done

# Limpar arquivo temporário
rm -f /tmp/sessions_concurrent.txt

echo "=== Testes Concorrentes concluídos ==="
