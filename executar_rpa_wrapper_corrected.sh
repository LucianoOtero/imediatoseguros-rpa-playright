#!/bin/bash
# Wrapper script para executar RPA com debug
cd /opt/imediatoseguros-rpa
echo "[DEBUG] Iniciando wrapper script" >> logs/wrapper_debug.log
echo "[DEBUG] Session: $1" >> logs/wrapper_debug.log
echo "[DEBUG] PWD: $(pwd)" >> logs/wrapper_debug.log
echo "[DEBUG] USER: $(whoami)" >> logs/wrapper_debug.log

# CORREÇÃO: Usar Python do venv diretamente (sem source)
echo "[DEBUG] Executando RPA com Python do venv..." >> logs/wrapper_debug.log
PLAYWRIGHT_BROWSERS_PATH=/opt/imediatoseguros-rpa/.playwright /opt/imediatoseguros-rpa/venv/bin/python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json
echo "[DEBUG] RPA finalizado com código: $?" >> logs/wrapper_debug.log


