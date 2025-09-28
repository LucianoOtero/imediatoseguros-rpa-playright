#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Executar Todos os Testes
Script principal para executar todos os testes do sistema
"""

import sys
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_communication_tests():
    """Executa testes do sistema de comunicação"""
    logger.info("🧪 EXECUTANDO TESTES DO SISTEMA DE COMUNICAÇÃO")
    
    try:
        from test_communication_system import CommunicationSystemTester
        
        tester = CommunicationSystemTester()
        results = tester.run_all_tests()
        
        return results
    except Exception as e:
        logger.error(f"❌ Falha ao executar testes de comunicação: {e}")
        return None

def run_rpa_tests():
    """Executa testes dos módulos RPA"""
    logger.info("🧪 EXECUTANDO TESTES DOS MÓDULOS RPA")
    
    try:
        from test_rpa_modules import RPAModulesTester
        
        tester = RPAModulesTester()
        results = tester.run_all_tests()
        
        return results
    except Exception as e:
        logger.error(f"❌ Falha ao executar testes RPA: {e}")
        return None

def main():
    """Função principal"""
    logger.info("🚀 INICIANDO EXECUÇÃO DE TODOS OS TESTES")
    
    start_time = datetime.now()
    all_results = {
        "start_time": start_time.isoformat(),
        "tests": {},
        "summary": {}
    }
    
    # Executar testes de comunicação
    communication_results = run_communication_tests()
    if communication_results:
        all_results["tests"]["communication_system"] = communication_results
    
    # Executar testes RPA
    rpa_results = run_rpa_tests()
    if rpa_results:
        all_results["tests"]["rpa_modules"] = rpa_results
    
    # Gerar resumo geral
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    total_test_suites = len(all_results["tests"])
    successful_suites = sum(1 for suite in all_results["tests"].values() 
                           if suite.get("summary", {}).get("overall_status") == "PASSED")
    
    all_results["summary"] = {
        "end_time": end_time.isoformat(),
        "duration_seconds": duration,
        "total_test_suites": total_test_suites,
        "successful_suites": successful_suites,
        "failed_suites": total_test_suites - successful_suites,
        "overall_status": "PASSED" if successful_suites == total_test_suites else "FAILED"
    }
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_all_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Resultados salvos em: {filename}")
    except Exception as e:
        logger.error(f"❌ Falha ao salvar resultados: {e}")
    
    # Exibir resumo
    logger.info("📊 RESUMO GERAL DOS TESTES:")
    logger.info(f"   Suites de teste: {total_test_suites}")
    logger.info(f"   Suites bem-sucedidas: {successful_suites}")
    logger.info(f"   Suites com falha: {total_test_suites - successful_suites}")
    logger.info(f"   Status geral: {all_results['summary']['overall_status']}")
    logger.info(f"   Duração total: {duration:.2f} segundos")
    
    return all_results

if __name__ == "__main__":
    main()
