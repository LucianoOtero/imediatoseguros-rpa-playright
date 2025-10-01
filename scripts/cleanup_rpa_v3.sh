#!/bin/bash
# /opt/imediatoseguros-rpa/scripts/cleanup_rpa_v3.sh
# Script para limpeza de sessões RPA

set -e

SESSION_ID=$1
FORCE=$2

# Verificar parâmetros
if [ -z "$SESSION_ID" ]; then
    echo "ERRO: Uso: $0 <session_id> [force]"
    exit 1
fi

SESSION_DIR="/opt/imediatoseguros-rpa/sessions/${SESSION_ID}"

# Verificar se diretório da sessão existe
if [ ! -d "$SESSION_DIR" ]; then
    echo "AVISO: Sessão não encontrada: $SESSION_ID"
    exit 0
fi

# Parar serviço se estiver rodando
if systemctl is-active --quiet "rpa-session-${SESSION_ID}"; then
    echo "Parando serviço rpa-session-${SESSION_ID}..."
    systemctl stop "rpa-session-${SESSION_ID}"
fi

# Remover service unit
if [ -f "/etc/systemd/system/rpa-session-${SESSION_ID}.service" ]; then
    echo "Removendo service unit..."
    rm -f "/etc/systemd/system/rpa-session-${SESSION_ID}.service"
    systemctl daemon-reload
fi

# Remover diretório da sessão
if [ "$FORCE" = "force" ]; then
    echo "Removendo diretório da sessão (forçado)..."
    rm -rf "$SESSION_DIR"
else
    # Verificar se sessão está inativa há mais de 1 hora
    if [ -f "${SESSION_DIR}/status.json" ]; then
        STATUS_TIME=$(grep -o '"timestamp":"[^"]*"' "${SESSION_DIR}/status.json" | cut -d'"' -f4)
        if [ ! -z "$STATUS_TIME" ]; then
            STATUS_EPOCH=$(date -d "$STATUS_TIME" +%s 2>/dev/null || echo "0")
            CURRENT_EPOCH=$(date +%s)
            DIFF=$((CURRENT_EPOCH - STATUS_EPOCH))
            
            if [ $DIFF -gt 3600 ]; then  # 1 hora
                echo "Removendo sessão inativa há mais de 1 hora..."
                rm -rf "$SESSION_DIR"
            else
                echo "Sessão ainda ativa, não removendo (inativa há $((DIFF/60)) minutos)"
            fi
        else
            echo "Não foi possível determinar timestamp da sessão"
        fi
    else
        echo "Arquivo de status não encontrado, removendo sessão..."
        rm -rf "$SESSION_DIR"
    fi
fi

echo "Limpeza concluída para sessão: $SESSION_ID"

