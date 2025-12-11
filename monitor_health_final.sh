#!/bin/bash
# monitor_health.sh
# Script de monitoramento automático dos health checks

# Configurações
HEALTH_ENDPOINT="https://bpsegurosimediato.com.br/health.php"
DEV_HEALTH_ENDPOINT="https://bpsegurosimediato.com.br/dev/health.php"
WEBHOOK_HEALTH_ENDPOINT="https://bpsegurosimediato.com.br/webhook_health.php"
LOG_FILE="/var/www/html/logs/health_monitor.log"
ALERT_EMAIL="admin@bpsegurosimediato.com.br"
CHECK_INTERVAL=300  # 5 minutos
MAX_FAILURES=3
FAILURE_COUNT=0

# Função para log
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Função para enviar alerta
send_alert() {
    local message="$1"
    local subject="ALERTA: Health Check Falhou - bpsegurosimediato.com.br"
    
    log_message "ALERTA: $message"
    
    # Enviar email (se configurado)
    if command -v mail >/dev/null 2>&1; then
        echo "$message" | mail -s "$subject" "$ALERT_EMAIL"
    fi
    
    # Log adicional para debugging
    log_message "Alerta enviado para: $ALERT_EMAIL"
}

# Função para verificar health check
check_health() {
    local endpoint="$1"
    local environment="$2"
    
    # Fazer requisição com timeout
    response=$(curl -s -w "%{http_code}" -o /tmp/health_response.json --max-time 30 "$endpoint")
    http_code="${response: -3}"
    
    if [ "$http_code" = "200" ]; then
        # Verificar se resposta contém status ok ou warning (ambos são aceitáveis)
        # Usar tr para remover quebras de linha e espaços
        status=$(cat /tmp/health_response.json | tr -d '\n' | tr -d ' ' | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
        
        if [ "$status" = "ok" ]; then
            log_message "Health check $environment: OK"
            return 0
        elif [ "$status" = "warning" ]; then
            log_message "Health check $environment: WARNING (aceitável)"
            return 0  # Warning é aceitável
        else
            log_message "Health check $environment: ERROR (status: $status)"
            return 2
        fi
    else
        log_message "Health check $environment: HTTP $http_code"
        return 2
    fi
}

# Função para verificar logs recentes
check_recent_logs() {
    local log_file="$1"
    local max_age_minutes=10
    
    if [ -f "$log_file" ]; then
        # Verificar se arquivo foi modificado nos últimos X minutos
        if [ $(find "$log_file" -mmin -$max_age_minutes | wc -l) -gt 0 ]; then
            log_message "Log $log_file: Ativo (modificado nos últimos $max_age_minutes minutos)"
            return 0
        else
            log_message "Log $log_file: Inativo (não modificado nos últimos $max_age_minutes minutos)"
            return 1
        fi
    else
        log_message "Log $log_file: Não encontrado"
        return 2
    fi
}

# Função principal de monitoramento
main_monitor() {
    log_message "Iniciando monitoramento de health checks..."
    
    # Verificar health check de produção
    if check_health "$HEALTH_ENDPOINT" "PRODUÇÃO"; then
        FAILURE_COUNT=0
    else
        FAILURE_COUNT=$((FAILURE_COUNT + 1))
        log_message "Falha #$FAILURE_COUNT no health check de produção"
        
        if [ $FAILURE_COUNT -ge $MAX_FAILURES ]; then
            send_alert "Health check de produção falhou $FAILURE_COUNT vezes consecutivas. Verificar imediatamente!"
            FAILURE_COUNT=0  # Reset para evitar spam
        fi
    fi
    
    # Verificar health check de webhooks
    if check_health "$WEBHOOK_HEALTH_ENDPOINT" "WEBHOOKS"; then
        log_message "Health check de webhooks: OK"
    else
        log_message "Health check de webhooks: FALHOU"
    fi
    
    # Verificar health check de desenvolvimento (se disponível)
    if check_health "$DEV_HEALTH_ENDPOINT" "DESENVOLVIMENTO"; then
        log_message "Health check de desenvolvimento: OK"
    else
        log_message "Health check de desenvolvimento: FALHOU"
    fi
    
    # Verificar logs recentes
    check_recent_logs "/var/www/html/logs_travelangels.txt"
    check_recent_logs "/var/www/html/octa_webflow_webhook.log"
    check_recent_logs "/var/www/html/dev/logs/general_dev.txt"
    
    # Verificar espaço em disco
    disk_usage=$(df /var/www/html | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$disk_usage" -gt 90 ]; then
        send_alert "Espaço em disco crítico: ${disk_usage}% usado em /var/www/html"
    elif [ "$disk_usage" -gt 80 ]; then
        log_message "AVISO: Espaço em disco alto: ${disk_usage}% usado"
    fi
    
    # Verificar memória
    memory_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100.0}')
    if [ "$memory_usage" -gt 90 ]; then
        send_alert "Uso de memória crítico: ${memory_usage}%"
    elif [ "$memory_usage" -gt 80 ]; then
        log_message "AVISO: Uso de memória alto: ${memory_usage}%"
    fi
    
    log_message "Monitoramento concluído. Próxima verificação em $CHECK_INTERVAL segundos"
}

# Função para executar uma única verificação
single_check() {
    log_message "Executando verificação única..."
    main_monitor
    exit 0
}

# Função para executar monitoramento contínuo
continuous_monitor() {
    log_message "Iniciando monitoramento contínuo (intervalo: $CHECK_INTERVAL segundos)"
    
    while true; do
        main_monitor
        sleep $CHECK_INTERVAL
    done
}

# Verificar argumentos
case "${1:-continuous}" in
    "single")
        single_check
        ;;
    "continuous")
        continuous_monitor
        ;;
    "test")
        log_message "Modo de teste - executando verificações..."
        check_health "$HEALTH_ENDPOINT" "TESTE"
        check_health "$WEBHOOK_HEALTH_ENDPOINT" "TESTE-WEBHOOKS"
        check_health "$DEV_HEALTH_ENDPOINT" "TESTE-DEV"
        ;;
    *)
        echo "Uso: $0 [single|continuous|test]"
        echo "  single     - Executar uma única verificação"
        echo "  continuous - Monitoramento contínuo (padrão)"
        echo "  test       - Modo de teste"
        exit 1
        ;;
esac

































