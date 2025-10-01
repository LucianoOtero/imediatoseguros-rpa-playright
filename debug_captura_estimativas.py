#!/usr/bin/env python3
"""
Script de debug para investigar a captura de estimativas via PHP
"""

import os
import sys
import json
import time
from datetime import datetime

def log_debug(message, force_print=True):
    """Log de debug que sempre imprime"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_msg = f"[{timestamp}] DEBUG: {message}"
    print(log_msg)
    
    # Salvar em arquivo também
    with open("logs/debug_captura.log", "a", encoding="utf-8") as f:
        f.write(log_msg + "\n")

def main():
    log_debug("=== INICIANDO DEBUG CAPTURA ESTIMATIVAS ===")
    
    # Verificar ambiente
    log_debug(f"DISPLAY: {os.environ.get('DISPLAY', 'NÃO DEFINIDO')}")
    log_debug(f"USER: {os.environ.get('USER', 'NÃO DEFINIDO')}")
    log_debug(f"PWD: {os.getcwd()}")
    
    # Simular a função de captura
    log_debug("Simulando captura de estimativas...")
    
    try:
        # Importar módulos necessários
        from playwright.sync_api import sync_playwright
        log_debug("Playwright importado com sucesso")
        
        # Simular captura
        dados_simulados = {
            "coberturas_detalhadas": [
                {
                    "nome_cobertura": "Teste",
                    "valores": {"de": "R$ 100,00", "ate": "R$ 200,00"}
                }
            ]
        }
        
        log_debug(f"Dados simulados: {json.dumps(dados_simulados, indent=2)}")
        
        # Simular ProgressTracker
        try:
            from utils.progress_database_json import DatabaseProgressTracker
            tracker = DatabaseProgressTracker(total_etapas=5, session_id="debug_test")
            tracker.add_estimativas(dados_simulados)
            log_debug("ProgressTracker atualizado com sucesso")
            
            # Verificar se foi salvo
            progress_data = tracker.get_progress()
            if progress_data.get('dados_extra', {}).get('estimativas_tela_5'):
                log_debug("Estimativas salvas no ProgressTracker")
            else:
                log_debug("ERRO: Estimativas NÃO salvas no ProgressTracker")
                
        except Exception as e:
            log_debug(f"ERRO ProgressTracker: {e}")
            
    except Exception as e:
        log_debug(f"ERRO geral: {e}")
    
    log_debug("=== FIM DO DEBUG ===")

if __name__ == "__main__":
    main()


