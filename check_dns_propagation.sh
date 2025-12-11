#!/bin/bash
# check_dns_propagation.sh
# Script para verificar propagação do DNS

DOMAIN="test.bpsegurosimediato.com.br"
LOG_FILE="/var/log/dns_check.log"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificando propagação do DNS para $DOMAIN" | tee -a "$LOG_FILE"

# Verificar com nslookup
echo "=== NSLOOKUP ===" | tee -a "$LOG_FILE"
nslookup "$DOMAIN" | tee -a "$LOG_FILE"

# Verificar com dig
echo "=== DIG ===" | tee -a "$LOG_FILE"
dig "$DOMAIN" | tee -a "$LOG_FILE"

# Verificar conectividade
echo "=== PING ===" | tee -a "$LOG_FILE"
ping -c 3 "$DOMAIN" | tee -a "$LOG_FILE"

# Verificar HTTP
echo "=== HTTP TEST ===" | tee -a "$LOG_FILE"
curl -I "http://$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Verificação concluída" | tee -a "$LOG_FILE"

































