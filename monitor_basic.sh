#!/bin/bash
# Script de monitoramento básico para RPA

LOG_FILE="logs/rpa_basic.log"
ALERT_EMAIL="admin@imediatoseguros.com.br"

# Verificar se o log existe
if [ ! -f "$LOG_FILE" ]; then
    echo "Log file not found: $LOG_FILE"
    exit 1
fi

# Contar sessões nas últimas 24 horas
SESSIONS_24H=$(grep -c "$(date '+%Y-%m-%d')" "$LOG_FILE")

# Verificar se há muitas sessões (alerta se > 200)
if [ "$SESSIONS_24H" -gt 200 ]; then
    echo "Alerta: $SESSIONS_24H sessões nas últimas 24 horas" | \
    mail -s "RPA High Usage Alert" "$ALERT_EMAIL"
fi

# Verificar se há erros nas últimas 2 horas
ERRORS_2H=$(grep -c "ERRO" "$LOG_FILE" | tail -n 100)

if [ "$ERRORS_2H" -gt 10 ]; then
    echo "Alerta: $ERRORS_2H erros nas últimas 2 horas" | \
    mail -s "RPA Error Alert" "$ALERT_EMAIL"
fi

# Verificar espaço em disco
DISK_USAGE=$(df -h . | awk 'NR==2 {print $5}' | sed 's/%//')

if [ "$DISK_USAGE" -gt 80 ]; then
    echo "Alerta: $DISK_USAGE% de uso do disco" | \
    mail -s "RPA Disk Space Alert" "$ALERT_EMAIL"
fi

echo "Monitoramento básico concluído:"
echo "- Sessões nas últimas 24h: $SESSIONS_24H"
echo "- Erros nas últimas 2h: $ERRORS_2H"
echo "- Uso do disco: $DISK_USAGE%"






















