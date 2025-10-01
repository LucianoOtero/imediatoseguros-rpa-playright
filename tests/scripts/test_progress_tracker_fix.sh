#!/bin/bash
# Script para corrigir e testar progress tracker

echo "=== Correção do Progress Tracker ==="

# 1. Verificar problema atual
echo "1. Verificando problema atual..."
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão criada: $SESSION_ID"

# 2. Verificar se arquivo JSON foi criado
echo "2. Verificando arquivo JSON..."
sleep 5
if [ -f "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo JSON criado"
    cat "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" | jq .
else
    echo "❌ Arquivo JSON não criado"
fi

# 3. Verificar progresso via API
echo "3. Verificando progresso via API..."
PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
echo "$PROGRESS" | jq .

# 4. Monitorar em tempo real
echo "4. Monitorando em tempo real..."
START_TIME=$(date +%s)
TIMEOUT=300  # 5 minutos

while true; do
    CURRENT_TIME=$(date +%s)
    ELAPSED=$((CURRENT_TIME - START_TIME))
    
    if [ $ELAPSED -gt $TIMEOUT ]; then
        echo "Timeout atingido (${TIMEOUT}s)"
        break
    fi
    
    PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
    STATUS=$(echo "$PROGRESS" | jq -r '.progress.status')
    ETAPA=$(echo "$PROGRESS" | jq -r '.progress.etapa_atual')
    PERCENTUAL=$(echo "$PROGRESS" | jq -r '.progress.percentual')
    MENSAGEM=$(echo "$PROGRESS" | jq -r '.progress.mensagem')
    
    echo "$(date): Status: $STATUS, Etapa: $ETAPA, Percentual: $PERCENTUAL, Mensagem: $MENSAGEM"
    
    if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
        echo "Execução concluída com status: $STATUS"
        break
    fi
    
    sleep 2
done

echo "=== Correção do Progress Tracker concluída ==="
