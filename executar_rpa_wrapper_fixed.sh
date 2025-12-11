#!/bin/bash
# Wrapper script para executar RPA com debug
cd /opt/imediatoseguros-rpa
echo "[DEBUG] Iniciando wrapper script" >> logs/wrapper_debug.log
echo "[DEBUG] Session: $1" >> logs/wrapper_debug.log
echo "[DEBUG] PWD: $(pwd)" >> logs/wrapper_debug.log
echo "[DEBUG] USER: $(whoami)" >> logs/wrapper_debug.log

source venv/bin/activate
echo "[DEBUG] Venv ativado" >> logs/wrapper_debug.log

# CORREÇÃO: Remover --modo-silencioso para restaurar logs de debug
echo "[DEBUG] Executando RPA..." >> logs/wrapper_debug.log
PLAYWRIGHT_BROWSERS_PATH=/opt/imediatoseguros-rpa/.playwright python3 executar_rpa_modular_telas_1_a_5.py --session "$1" --progress-tracker json
echo "[DEBUG] RPA finalizado com código: $?" >> logs/wrapper_debug.log



























