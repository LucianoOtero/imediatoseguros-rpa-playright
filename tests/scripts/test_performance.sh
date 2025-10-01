#!/bin/bash
# test_performance.sh

echo "=== Teste de Performance ==="

# 1. Medir tempo de criação de script
echo "1. Medindo tempo de criação de script..."
START_TIME=$(date +%s)

SESSION_RESPONSE=$(curl -s -X POST http://37.27.92.160/api/rpa/start \
  -H "Content-Type: application/json" \
  -d '{"cpf":"12345678901","nome":"PERFORMANCE TEST","placa":"PERF123","cep":"01234567","email":"perf@test.com","celular":"11999999999","ano":"2020"}')

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Tempo de criação: ${DURATION}s"

if [ $DURATION -lt 5 ]; then
    echo "✅ Performance adequada (< 5s)"
else
    echo "⚠️ Performance degradada (>= 5s)"
fi

# 2. Testar concorrência real
echo "2. Testando concorrência com 5 sessões simultâneas..."
for i in {1..5}; do
    (curl -s -X POST http://37.27.92.160/api/rpa/start \
      -H "Content-Type: application/json" \
      -d "{\"cpf\":\"1234567890${i}\",\"nome\":\"CONCURRENT TEST ${i}\",\"placa\":\"CONC${i}\",\"cep\":\"0123456${i}\",\"email\":\"conc${i}@test.com\",\"celular\":\"1199999999${i}\",\"ano\":\"2020\"}") &
done
wait

echo "✅ Teste de concorrência concluído"

echo "=== Teste de performance concluído ==="
