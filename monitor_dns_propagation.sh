#!/bin/bash
# monitor_dns_propagation.sh
# Script para monitorar propagação do DNS

DOMAIN="test.bpsegurosimediato.com.br"
LOG_FILE="/var/log/dns_monitor.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Iniciando monitoramento do DNS para $DOMAIN" | tee -a "$LOG_FILE"

while true; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificando DNS..." | tee -a "$LOG_FILE"
    
    # Verificar com nslookup
    result=$(nslookup "$DOMAIN" 2>&1)
    
    if echo "$result" | grep -q "46.62.174.150"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ DNS PROPAGADO! $DOMAIN resolve para 46.62.174.150" | tee -a "$LOG_FILE"
        echo "=== RESULTADO ===" | tee -a "$LOG_FILE"
        echo "$result" | tee -a "$LOG_FILE"
        break
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ⏳ DNS ainda não propagado. Aguardando..." | tee -a "$LOG_FILE"
        echo "$result" | tee -a "$LOG_FILE"
    fi
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] Aguardando 5 minutos para próxima verificação..." | tee -a "$LOG_FILE"
    sleep 300
done

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Monitoramento concluído!" | tee -a "$LOG_FILE"

































