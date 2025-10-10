#!/bin/bash
# Wrapper script para executar RPA com Xvfb (ambiente gráfico virtual)
cd /opt/imediatoseguros-rpa

# Criar log específico para esta sessão
LOG_FILE="logs/wrapper_$1.log"
echo "[DEBUG] Iniciando wrapper script com Xvfb" >> "$LOG_FILE"
echo "[DEBUG] Session: $1" >> "$LOG_FILE"
echo "[DEBUG] PWD: $(pwd)" >> "$LOG_FILE"
echo "[DEBUG] USER: $(whoami)" >> "$LOG_FILE"
echo "[DEBUG] LOG_FILE: $LOG_FILE" >> "$LOG_FILE"

# Configurar ambiente gráfico virtual
export DISPLAY=:99
echo "[DEBUG] DISPLAY: $DISPLAY" >> "$LOG_FILE"

# Executar RPA com Xvfb para ambiente gráfico virtual
echo "[DEBUG] Executando RPA com Xvfb..." >> "$LOG_FILE"
xvfb-run -a /opt/imediatoseguros-rpa/venv/bin/python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json >> "$LOG_FILE" 2>&1
RPA_EXIT_CODE=$?
echo "[DEBUG] RPA finalizado com código: $RPA_EXIT_CODE" >> "$LOG_FILE"

# Log de recursos do sistema
echo "[DEBUG] RAM: $(free -m | awk 'NR==2{printf "%.1f%%", $3*100/$2}')" >> "$LOG_FILE"
echo "[DEBUG] CPU: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)" >> "$LOG_FILE"

exit $RPA_EXIT_CODE






















