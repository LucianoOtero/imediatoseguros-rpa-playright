#!/bin/bash
# Script para testar progress tracker corrigido

echo "=== Teste Progress Tracker Corrigido ==="

# 1. Criar nova sessão
echo "1. Criando nova sessão..."
SESSION_ID=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"97137189768","nome":"ALEX KAMINSKI","placa":"EYQ4J41","cep":"03317000","email":"alex.kaminski@imediatoseguros.com.br","celular":"11953288466","ano":"2009"}' | jq -r '.session_id')

echo "Sessão criada: $SESSION_ID"

# 2. Aguardar alguns segundos para o RPA iniciar
echo "2. Aguardando RPA iniciar..."
sleep 10

# 3. Verificar se arquivo JSON foi criado
echo "3. Verificando arquivo JSON..."
if [ -f "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo JSON criado"
    cat "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" | jq .
else
    echo "❌ Arquivo JSON não criado"
fi

# 4. Verificar progresso via API
echo "4. Verificando progresso via API..."
PROGRESS=$(curl -s http://37.27.92.160/api/rpa/progress/$SESSION_ID)
echo "$PROGRESS" | jq .

# 5. Monitorar em tempo real por 2 minutos
echo "5. Monitorando em tempo real (2 minutos)..."
START_TIME=$(date +%s)
TIMEOUT=120  # 2 minutos

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
    SOURCE=$(echo "$PROGRESS" | jq -r '.progress.source')
    
    echo "$(date): Status: $STATUS, Etapa: $ETAPA, Percentual: $PERCENTUAL, Mensagem: $MENSAGEM, Source: $SOURCE"
    
    if [ "$STATUS" = "success" ] || [ "$STATUS" = "failed" ]; then
        echo "Execução concluída com status: $STATUS"
        break
    fi
    
    sleep 5
done

# 6. Verificar arquivo final
echo "6. Verificando arquivo final..."
if [ -f "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" ]; then
    echo "✅ Arquivo JSON final:"
    cat "/opt/imediatoseguros-rpa/rpa_data/progress_${SESSION_ID}.json" | jq .
else
    echo "❌ Arquivo JSON final não encontrado"
fi

echo "=== Teste Progress Tracker Corrigido concluído ==="
