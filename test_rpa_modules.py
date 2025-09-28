#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste dos Módulos RPA
Validação dos módulos das telas 2-5 com comunicação em tempo real
"""

import time
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from unittest.mock import Mock, MagicMock

# Configurar logging com codificação UTF-8
import sys
import io

# Configurar stdout para UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Importar módulos RPA
try:
    from tela_2_placa import navegar_tela_2_playwright, exibir_mensagem as exibir_mensagem_tela2
    from tela_3_confirmacao_veiculo import navegar_tela_3_playwright, exibir_mensagem as exibir_mensagem_tela3
    from tela_4_confirmacao_segurado import navegar_tela_4_playwright, exibir_mensagem as exibir_mensagem_tela4
    from tela_5_estimativas import navegar_tela_5_playwright, exibir_mensagem as exibir_mensagem_tela5
    RPA_MODULES_AVAILABLE = True
except ImportError as e:
    logger.error(f"Falha ao importar módulos RPA: {e}")
    RPA_MODULES_AVAILABLE = False

# Importar módulos de comunicação
try:
    from utils.communication_manager import communication_manager
    COMMUNICATION_AVAILABLE = True
except ImportError:
    COMMUNICATION_AVAILABLE = False

class RPAModulesTester:
    """Testador dos módulos RPA"""
    
    def __init__(self):
        self.test_results = {}
        self.session_id = None
        self.test_start_time = None
        self.mock_page = None
        
    def create_mock_page(self):
        """Cria mock do Playwright Page"""
        mock_page = Mock()
        
        # Mock para get_by_role
        mock_element = Mock()
        mock_element.fill = Mock()
        mock_element.click = Mock()
        mock_element.select_option = Mock()
        
        mock_page.get_by_role = Mock(return_value=mock_element)
        mock_page.wait_for_selector = Mock()
        mock_page.wait_for_function = Mock()
        mock_page.query_selector_all = Mock(return_value=[])
        mock_page.wait_for_load_state = Mock()
        
        return mock_page
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Executa todos os testes dos módulos RPA"""
        logger.info("🧪 INICIANDO TESTES DOS MÓDULOS RPA")
        
        self.test_start_time = datetime.now()
        self.test_results = {
            "start_time": self.test_start_time.isoformat(),
            "tests": {},
            "summary": {}
        }
        
        # Criar mock do Page
        self.mock_page = self.create_mock_page()
        
        # Criar sessão de teste
        if COMMUNICATION_AVAILABLE:
            session_data = {
                "test_session": True,
                "created_at": datetime.now().isoformat(),
                "test_type": "rpa_modules"
            }
            self.session_id = communication_manager.create_session(session_data)
        
        # Teste 1: Tela 2 - Placa
        self.test_tela_2_placa()
        
        # Teste 2: Tela 3 - Confirmação do Veículo
        self.test_tela_3_confirmacao_veiculo()
        
        # Teste 3: Tela 4 - Confirmação de Veículo Segurado
        self.test_tela_4_confirmacao_segurado()
        
        # Teste 4: Tela 5 - Estimativas
        self.test_tela_5_estimativas()
        
        # Teste 5: Teste de integração entre telas
        self.test_integration_between_screens()
        
        # Limpar sessão de teste
        if COMMUNICATION_AVAILABLE and self.session_id:
            communication_manager.delete_session(self.session_id)
        
        # Gerar resumo
        self.generate_summary()
        
        logger.info("✅ TESTES DOS MÓDULOS RPA CONCLUÍDOS")
        return self.test_results
    
    def test_tela_2_placa(self):
        """Testa Tela 2 - Placa"""
        logger.info("🔍 Testando Tela 2 - Placa...")
        
        try:
            # Dados de teste
            veiculo_segurado = {
                "placa": "ABC1234",
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2020,
                "cor": "Branco"
            }
            
            # Executar navegação
            result = navegar_tela_2_playwright(
                self.mock_page, 
                veiculo_segurado, 
                self.session_id
            )
            
            # Verificar se função exibir_mensagem funciona
            exibir_mensagem_tela2("Teste de mensagem Tela 2", self.session_id)
            
            self.test_results["tests"]["tela_2_placa"] = {
                "status": "passed",
                "result": result,
                "veiculo_segurado": veiculo_segurado,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Tela 2 - Placa: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["tela_2_placa"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Tela 2 - Placa: FALHOU - {e}")
    
    def test_tela_3_confirmacao_veiculo(self):
        """Testa Tela 3 - Confirmação do Veículo"""
        logger.info("🔍 Testando Tela 3 - Confirmação do Veículo...")
        
        try:
            # Dados de teste
            veiculo_segurado = {
                "placa": "ABC1234",
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2020,
                "cor": "Branco"
            }
            
            # Executar navegação
            result = navegar_tela_3_playwright(
                self.mock_page, 
                veiculo_segurado, 
                self.session_id
            )
            
            # Verificar se função exibir_mensagem funciona
            exibir_mensagem_tela3("Teste de mensagem Tela 3", self.session_id)
            
            self.test_results["tests"]["tela_3_confirmacao_veiculo"] = {
                "status": "passed",
                "result": result,
                "veiculo_segurado": veiculo_segurado,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Tela 3 - Confirmação do Veículo: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["tela_3_confirmacao_veiculo"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Tela 3 - Confirmação do Veículo: FALHOU - {e}")
    
    def test_tela_4_confirmacao_segurado(self):
        """Testa Tela 4 - Confirmação de Veículo Segurado"""
        logger.info("🔍 Testando Tela 4 - Confirmação de Veículo Segurado...")
        
        try:
            # Dados de teste
            veiculo_segurado = {
                "placa": "ABC1234",
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2020,
                "cor": "Branco"
            }
            
            # Executar navegação
            result = navegar_tela_4_playwright(
                self.mock_page, 
                veiculo_segurado, 
                self.session_id
            )
            
            # Verificar se função exibir_mensagem funciona
            exibir_mensagem_tela4("Teste de mensagem Tela 4", self.session_id)
            
            self.test_results["tests"]["tela_4_confirmacao_segurado"] = {
                "status": "passed",
                "result": result,
                "veiculo_segurado": veiculo_segurado,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Tela 4 - Confirmação de Veículo Segurado: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["tela_4_confirmacao_segurado"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Tela 4 - Confirmação de Veículo Segurado: FALHOU - {e}")
    
    def test_tela_5_estimativas(self):
        """Testa Tela 5 - Estimativas"""
        logger.info("🔍 Testando Tela 5 - Estimativas...")
        
        try:
            # Executar navegação
            result = navegar_tela_5_playwright(
                self.mock_page, 
                self.session_id
            )
            
            # Verificar se função exibir_mensagem funciona
            exibir_mensagem_tela5("Teste de mensagem Tela 5", self.session_id)
            
            self.test_results["tests"]["tela_5_estimativas"] = {
                "status": "passed",
                "result": result,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Tela 5 - Estimativas: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["tela_5_estimativas"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Tela 5 - Estimativas: FALHOU - {e}")
    
    def test_integration_between_screens(self):
        """Testa integração entre telas"""
        logger.info("🔗 Testando integração entre telas...")
        
        try:
            # Dados de teste
            veiculo_segurado = {
                "placa": "ABC1234",
                "marca": "Toyota",
                "modelo": "Corolla",
                "ano": 2020,
                "cor": "Branco"
            }
            
            # Simular fluxo completo
            integration_results = []
            
            # Tela 2
            result_tela2 = navegar_tela_2_playwright(
                self.mock_page, veiculo_segurado, self.session_id
            )
            integration_results.append({"tela": "2", "result": result_tela2})
            
            # Tela 3
            result_tela3 = navegar_tela_3_playwright(
                self.mock_page, veiculo_segurado, self.session_id
            )
            integration_results.append({"tela": "3", "result": result_tela3})
            
            # Tela 4
            result_tela4 = navegar_tela_4_playwright(
                self.mock_page, veiculo_segurado, self.session_id
            )
            integration_results.append({"tela": "4", "result": result_tela4})
            
            # Tela 5
            result_tela5 = navegar_tela_5_playwright(
                self.mock_page, self.session_id
            )
            integration_results.append({"tela": "5", "result": result_tela5})
            
            # Verificar se todas as telas passaram
            all_passed = all(result["result"] for result in integration_results)
            
            self.test_results["tests"]["integration_between_screens"] = {
                "status": "passed" if all_passed else "failed",
                "integration_results": integration_results,
                "all_passed": all_passed,
                "session_id": self.session_id,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Integração entre telas: PASSOU" if all_passed else "❌ Integração entre telas: FALHOU")
            
        except Exception as e:
            self.test_results["tests"]["integration_between_screens"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Integração entre telas: FALHOU - {e}")
    
    def generate_summary(self):
        """Gera resumo dos testes"""
        end_time = datetime.now()
        duration = (end_time - self.test_start_time).total_seconds()
        
        total_tests = len(self.test_results["tests"])
        passed_tests = sum(1 for test in self.test_results["tests"].values() 
                          if test["status"] == "passed")
        failed_tests = total_tests - passed_tests
        
        self.test_results["summary"] = {
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "overall_status": "PASSED" if failed_tests == 0 else "FAILED"
        }
        
        logger.info(f"📊 RESUMO DOS TESTES RPA:")
        logger.info(f"   Total: {total_tests}")
        logger.info(f"   Passou: {passed_tests}")
        logger.info(f"   Falhou: {failed_tests}")
        logger.info(f"   Taxa de sucesso: {self.test_results['summary']['success_rate']:.1f}%")
        logger.info(f"   Status geral: {self.test_results['summary']['overall_status']}")
        logger.info(f"   Duração: {duration:.2f} segundos")

def main():
    """Função principal para executar os testes"""
    if not RPA_MODULES_AVAILABLE:
        logger.error("❌ Módulos RPA não disponíveis")
        return
    
    tester = RPAModulesTester()
    results = tester.run_all_tests()
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_rpa_modules_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Resultados salvos em: {filename}")
    except Exception as e:
        logger.error(f"❌ Falha ao salvar resultados: {e}")
    
    return results

if __name__ == "__main__":
    main()
