#!/bin/bash
# /opt/imediatoseguros-rpa/scripts/monitor_rpa_v3.sh
# Script para monitorar execução RPA

set -e

SESSION_ID=$1

# Verificar parâmetros
if [ -z "$SESSION_ID" ]; then
    echo "ERRO: Uso: $0 <session_id>"
    exit 1
fi

SESSION_DIR="/opt/imediatoseguros-rpa/sessions/${SESSION_ID}"

# Verificar se diretório da sessão existe
if [ ! -d "$SESSION_DIR" ]; then
    echo "{\"error\": \"Sessão não encontrada: $SESSION_ID\"}"
    exit 1
fi

# Verificar status do serviço
SERVICE_STATUS=$(systemctl is-active "rpa-session-${SESSION_ID}" 2>/dev/null || echo "inactive")

# Ler progresso
if [ -f "${SESSION_DIR}/progress.json" ]; then
    PROGRESS=$(cat "${SESSION_DIR}/progress.json")
else
    PROGRESS='{"error": "Arquivo de progresso não encontrado"}'
fi

# Ler status
if [ -f "${SESSION_DIR}/status.json" ]; then
    STATUS=$(cat "${SESSION_DIR}/status.json")
else
    STATUS='{"error": "Arquivo de status não encontrado"}'
fi

# Ler logs recentes
if [ -f "${SESSION_DIR}/logs/progress.log" ]; then
    LOGS=$(tail -20 "${SESSION_DIR}/logs/progress.log" | sed 's/"/\\"/g' | tr '\n' '|')
else
    LOGS="Nenhum log encontrado"
fi

# Ler logs de execução
if [ -f "${SESSION_DIR}/logs/rpa.log" ]; then
    RPA_LOGS=$(tail -10 "${SESSION_DIR}/logs/rpa.log" | sed 's/"/\\"/g' | tr '\n' '|')
else
    RPA_LOGS="Nenhum log de execução encontrado"
fi

# Verificar se há arquivos de resultado
RESULT_FILES=""
if [ -d "${SESSION_DIR}" ]; then
    RESULT_FILES=$(find "${SESSION_DIR}" -name "*.json" -not -name "progress.json" -not -name "status.json" -not -name "config.json" 2>/dev/null | head -5 | tr '\n' ',' | sed 's/,$//')
fi

# Verificar PID do processo
PID=""
if [ -f "${SESSION_DIR}/status.json" ]; then
    PID=$(grep -o '"pid":[0-9]*' "${SESSION_DIR}/status.json" | cut -d':' -f2)
fi

# Verificar se processo está rodando
PROCESS_RUNNING="false"
if [ ! -z "$PID" ] && kill -0 "$PID" 2>/dev/null; then
    PROCESS_RUNNING="true"
fi

# Retornar JSON
cat << EOF
{
    "session_id": "${SESSION_ID}",
    "service_status": "${SERVICE_STATUS}",
    "process_running": ${PROCESS_RUNNING},
    "pid": "${PID}",
    "progress": ${PROGRESS},
    "status": ${STATUS},
    "logs": "${LOGS}",
    "rpa_logs": "${RPA_LOGS}",
    "result_files": "${RESULT_FILES}",
    "timestamp": "$(date -Iseconds)"
}
EOF















