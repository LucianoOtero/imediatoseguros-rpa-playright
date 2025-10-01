#!/bin/bash
# validation_enhanced.sh

echo "=== Validação Aprimorada ==="

# 1. Health check
echo "1. Verificando health check..."
HEALTH_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/health)
STATUS=$(echo "$HEALTH_RESPONSE" | jq -r '.health.status')
if [ "$STATUS" = "healthy" ]; then
    echo "✅ Health check passou"
else
    echo "❌ Health check falhou"
    exit 1
fi

# 2. Métricas
echo "2. Verificando métricas..."
METRICS_RESPONSE=$(curl -s http://37.27.92.160/api/rpa/metrics)
echo "Métricas: $METRICS_RESPONSE"

# 3. Teste de stress aprimorado
echo "3. Teste de stress aprimorado..."
SESSION_IDS=()

for i in {1..10}; do
    SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d "{\"cpf\":\"1234567890${i}\",\"nome\":\"STRESS TEST ${i}\",\"placa\":\"STR${i}\",\"cep\":\"0123456${i}\",\"email\":\"stress${i}@test.com\",\"celular\":\"1199999999${i}\",\"ano\":\"2020\"}")
    
    SESSION_ID=$(echo "$SESSION_RESPONSE" | jq -r '.session_id')
    SESSION_IDS+=("$SESSION_ID")
    echo "Sessão $i: $SESSION_ID"
    
    sleep 0.5  # Pausa menor para teste mais realista
done

# 4. Verificar criação de scripts
echo "4. Verificando criação de scripts..."
ALL_SCRIPTS_CREATED=true

for SESSION_ID in "${SESSION_IDS[@]}"; do
    if [ -f "/opt/imediatoseguros-rpa/scripts/start_rpa_v4_${SESSION_ID}.sh" ]; then
        echo "✅ Script criado para sessão: $SESSION_ID"
    else
        echo "❌ Script não criado para sessão: $SESSION_ID"
        ALL_SCRIPTS_CREATED=false
    fi
done

if [ "$ALL_SCRIPTS_CREATED" = true ]; then
    echo "✅ Teste de stress aprimorado PASSOU"
else
    echo "❌ Teste de stress aprimorado FALHOU"
    exit 1
fi

echo "=== Validação aprimorada concluída ==="
