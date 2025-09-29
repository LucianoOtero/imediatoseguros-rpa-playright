#!/bin/bash
# /opt/imediatoseguros-rpa/scripts/start_rpa_v3.sh
# Script para iniciar execução RPA via systemd

set -e

SESSION_ID=$1
CONFIG_FILE=$2
SESSION_DIR="/opt/imediatoseguros-rpa/sessions/${SESSION_ID}"
BASE_DIR="/opt/imediatoseguros-rpa"

# Verificar parâmetros
if [ -z "$SESSION_ID" ] || [ -z "$CONFIG_FILE" ]; then
    echo "ERRO: Uso: $0 <session_id> <config_file>"
    exit 1
fi

# Verificar se arquivo de configuração existe
if [ ! -f "$CONFIG_FILE" ]; then
    echo "ERRO: Arquivo de configuração não encontrado: $CONFIG_FILE"
    exit 1
fi

# Criar diretório da sessão se não existir
mkdir -p "${SESSION_DIR}/logs"

# Função para atualizar progresso
update_progress() {
    local etapa=$1
    local status=$2
    local mensagem=$3
    
    cat > "${SESSION_DIR}/progress.json" << PROGEOF
{
    "session_id": "${SESSION_ID}",
    "etapa_atual": $etapa,
    "total_etapas": 5,
    "status": "$status",
    "mensagem": "$mensagem",
    "timestamp": "$(date -Iseconds)",
    "percentual": $((etapa * 20))
}
PROGEOF
    
    echo "[$(date -Iseconds)] [ETAPA $etapa] $mensagem" >> "${SESSION_DIR}/logs/progress.log"
}

# Função para atualizar status
update_status() {
    local status=$1
    local mensagem=$2
    
    cat > "${SESSION_DIR}/status.json" << STATEOF
{
    "session_id": "${SESSION_ID}",
    "status": "$status",
    "mensagem": "$mensagem",
    "timestamp": "$(date -Iseconds)",
    "pid": $$
}
STATEOF
}

# Função para log de erro
log_error() {
    local mensagem=$1
    echo "[$(date -Iseconds)] [ERRO] $mensagem" >> "${SESSION_DIR}/logs/rpa.log"
}

# Iniciar execução
update_status "starting" "Iniciando RPA"
update_progress 0 "iniciando" "Iniciando RPA"

# Criar script de execução
cat > "${SESSION_DIR}/run_rpa.sh" << 'RUNEOF'
#!/bin/bash
set -e

# Variáveis de ambiente
export PATH="/opt/imediatoseguros-rpa/venv/bin:/usr/local/bin:/usr/bin:/bin"
export PYTHONPATH="/opt/imediatoseguros-rpa"
export DISPLAY=":99"
export HOME="/opt/imediatoseguros-rpa"
export USER="root"
export PWD="/opt/imediatoseguros-rpa"
export LANG="C"
export LC_ALL="C"
export PLAYWRIGHT_BROWSERS_PATH="/opt/imediatoseguros-rpa/.playwright"

# Função para atualizar progresso
update_progress() {
    local etapa=$1
    local status=$2
    local mensagem=$3
    
    cat > "${SESSION_DIR}/progress.json" << PROGEOF
{
    "session_id": "${SESSION_ID}",
    "etapa_atual": $etapa,
    "total_etapas": 5,
    "status": "$status",
    "mensagem": "$mensagem",
    "timestamp": "$(date -Iseconds)",
    "percentual": $((etapa * 20))
}
PROGEOF
    
    echo "[$(date -Iseconds)] [ETAPA $etapa] $mensagem" >> "${SESSION_DIR}/logs/progress.log"
}

# Função para atualizar status
update_status() {
    local status=$1
    local mensagem=$2
    
    cat > "${SESSION_DIR}/status.json" << STATEOF
{
    "session_id": "${SESSION_ID}",
    "status": "$status",
    "mensagem": "$mensagem",
    "timestamp": "$(date -Iseconds)",
    "pid": $$
}
STATEOF
}

# Função para log de erro
log_error() {
    local mensagem=$1
    echo "[$(date -Iseconds)] [ERRO] $mensagem" >> "${SESSION_DIR}/logs/rpa.log"
}

# Iniciar execução
update_status "running" "Executando RPA"
update_progress 1 "executando" "Iniciando Tela 1"

# Executar RPA
cd /opt/imediatoseguros-rpa

# Verificar se Python existe
if [ ! -f "/opt/imediatoseguros-rpa/venv/bin/python" ]; then
    log_error "Python não encontrado em /opt/imediatoseguros-rpa/venv/bin/python"
    update_status "failed" "Python não encontrado"
    exit 1
fi

# Verificar se script modular existe
if [ ! -f "/opt/imediatoseguros-rpa/executar_rpa_modular_telas_1_a_5.py" ]; then
    log_error "Script modular não encontrado"
    update_status "failed" "Script modular não encontrado"
    exit 1
fi

# Executar RPA com xvfb-run
echo "[$(date -Iseconds)] [INFO] Iniciando execução RPA" >> "${SESSION_DIR}/logs/rpa.log"
echo "[$(date -Iseconds)] [INFO] Comando: xvfb-run -a /opt/imediatoseguros-rpa/venv/bin/python executar_rpa_modular_telas_1_a_5.py --config ${CONFIG_FILE} --session ${SESSION_ID} --progress-tracker json --modo-silencioso" >> "${SESSION_DIR}/logs/rpa.log"

xvfb-run -a /opt/imediatoseguros-rpa/venv/bin/python \
    executar_rpa_modular_telas_1_a_5.py \
    --config "${CONFIG_FILE}" \
    --session "${SESSION_ID}" \
    --progress-tracker json \
    --modo-silencioso

# Verificar resultado
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    update_status "completed" "RPA concluído com sucesso"
    update_progress 5 "concluido" "RPA concluído com sucesso"
    echo "[$(date -Iseconds)] [INFO] RPA concluído com sucesso" >> "${SESSION_DIR}/logs/rpa.log"
else
    update_status "failed" "RPA falhou com código $EXIT_CODE"
    update_progress 5 "erro" "RPA falhou com código $EXIT_CODE"
    echo "[$(date -Iseconds)] [ERRO] RPA falhou com código $EXIT_CODE" >> "${SESSION_DIR}/logs/rpa.log"
fi

exit $EXIT_CODE
RUNEOF

# Tornar script executável
chmod +x "${SESSION_DIR}/run_rpa.sh"

# Criar service unit
cat > "/opt/imediatoseguros-rpa/systemd/rpa-session-${SESSION_ID}.service" << EOF
[Unit]
Description=RPA Session ${SESSION_ID}
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/imediatoseguros-rpa
ExecStart=${SESSION_DIR}/run_rpa.sh
Restart=no
StandardOutput=append:${SESSION_DIR}/logs/rpa.log
StandardError=append:${SESSION_DIR}/logs/rpa.log
Environment=SESSION_ID=${SESSION_ID}
Environment=SESSION_DIR=${SESSION_DIR}
Environment=CONFIG_FILE=${CONFIG_FILE}

[Install]
WantedBy=multi-user.target
EOF

# Copiar para systemd
cp "/opt/imediatoseguros-rpa/systemd/rpa-session-${SESSION_ID}.service" "/etc/systemd/system/"

# Recarregar systemd
systemctl daemon-reload

# Iniciar serviço
systemctl start "rpa-session-${SESSION_ID}"

# Verificar se iniciou
sleep 2
if systemctl is-active --quiet "rpa-session-${SESSION_ID}"; then
    echo "Service started: rpa-session-${SESSION_ID}"
    update_status "started" "Serviço iniciado com sucesso"
    update_progress 0 "iniciado" "Serviço iniciado, aguardando execução"
else
    echo "ERRO: Falha ao iniciar serviço rpa-session-${SESSION_ID}"
    update_status "failed" "Falha ao iniciar serviço"
    exit 1
fi
