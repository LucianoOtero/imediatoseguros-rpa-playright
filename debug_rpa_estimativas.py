#!/usr/bin/env python3
"""
Script de debug para investigar por que as estimativas não são capturadas via PHP
"""

import os
import sys
import json
from datetime import datetime

def log_debug(message):
    """Log de debug com timestamp"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] DEBUG: {message}")

def main():
    log_debug("=== INICIANDO DEBUG RPA ESTIMATIVAS ===")
    
    # Verificar variáveis de ambiente
    log_debug(f"DISPLAY: {os.environ.get('DISPLAY', 'NÃO DEFINIDO')}")
    log_debug(f"USER: {os.environ.get('USER', 'NÃO DEFINIDO')}")
    log_debug(f"PWD: {os.getcwd()}")
    
    # Verificar se estamos no venv
    python_path = sys.executable
    log_debug(f"Python path: {python_path}")
    log_debug(f"Venv ativo: {'venv' in python_path}")
    
    # Verificar módulos
    try:
        import playwright
        log_debug("Playwright disponível")
    except ImportError as e:
        log_debug(f"Playwright NÃO disponível: {e}")
    
    try:
        import utils.progress_database_json
        log_debug("ProgressTracker JSON disponível")
    except ImportError as e:
        log_debug(f"ProgressTracker JSON NÃO disponível: {e}")
    
    # Simular execução do RPA
    log_debug("Simulando execução do RPA...")
    
    # Verificar se o arquivo existe
    rpa_file = "executar_rpa_modular_telas_1_a_5.py"
    if os.path.exists(rpa_file):
        log_debug(f"Arquivo RPA encontrado: {rpa_file}")
        
        # Ler o arquivo e verificar DISPLAY_ENABLED
        with open(rpa_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'DISPLAY_ENABLED = True' in content:
            log_debug("DISPLAY_ENABLED está definido como True no código")
        elif 'DISPLAY_ENABLED = False' in content:
            log_debug("DISPLAY_ENABLED está definido como False no código")
        else:
            log_debug("DISPLAY_ENABLED não encontrado no código")
            
        if 'modo_silencioso' in content:
            log_debug("modo_silencioso encontrado no código")
        else:
            log_debug("modo_silencioso NÃO encontrado no código")
            
    else:
        log_debug(f"Arquivo RPA NÃO encontrado: {rpa_file}")
    
    log_debug("=== FIM DO DEBUG ===")

if __name__ == "__main__":
    main()
