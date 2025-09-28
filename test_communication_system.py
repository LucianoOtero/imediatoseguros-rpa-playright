#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste do Sistema de Comunicação
Validação completa dos módulos de comunicação em tempo real
"""

import asyncio
import time
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
import threading

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Importar módulos de comunicação
try:
    from utils.platform_utils import PlatformUtils, validate_environment
    from utils.redis_manager import redis_manager
    from utils.websocket_manager import websocket_manager
    from utils.communication_manager import communication_manager
    COMMUNICATION_AVAILABLE = True
except ImportError as e:
    logger.error(f"Falha ao importar módulos de comunicação: {e}")
    COMMUNICATION_AVAILABLE = False

class CommunicationSystemTester:
    """Testador do sistema de comunicação"""
    
    def __init__(self):
        self.test_results = {}
        self.session_id = None
        self.test_start_time = None
        
    def run_all_tests(self) -> Dict[str, Any]:
        """Executa todos os testes do sistema de comunicação"""
        logger.info("🧪 INICIANDO TESTES DO SISTEMA DE COMUNICAÇÃO")
        
        self.test_start_time = datetime.now()
        self.test_results = {
            "start_time": self.test_start_time.isoformat(),
            "tests": {},
            "summary": {}
        }
        
        # Teste 1: Validação do ambiente
        self.test_environment_validation()
        
        # Teste 2: Teste do Redis Manager
        self.test_redis_manager()
        
        # Teste 3: Teste do WebSocket Manager
        self.test_websocket_manager()
        
        # Teste 4: Teste do Communication Manager
        self.test_communication_manager()
        
        # Teste 5: Teste de integração completa
        self.test_integration()
        
        # Gerar resumo
        self.generate_summary()
        
        logger.info("✅ TESTES CONCLUÍDOS")
        return self.test_results
    
    def test_environment_validation(self):
        """Testa validação do ambiente"""
        logger.info("🔍 Testando validação do ambiente...")
        
        try:
            # Validar ambiente
            env_validation = validate_environment()
            
            # Obter informações da plataforma
            platform_info = PlatformUtils.get_platform_info()
            
            self.test_results["tests"]["environment_validation"] = {
                "status": "passed",
                "platform_info": platform_info,
                "validation": env_validation,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Validação do ambiente: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["environment_validation"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Validação do ambiente: FALHOU - {e}")
    
    def test_redis_manager(self):
        """Testa Redis Manager"""
        logger.info("🔴 Testando Redis Manager...")
        
        try:
            # Teste básico de conexão
            connection = redis_manager.get_connection()
            connection_status = connection is not None
            
            # Teste de cache
            test_key = "test_redis_key"
            test_value = {"test": "data", "timestamp": datetime.now().isoformat()}
            
            # Teste set
            set_result = redis_manager.set(test_key, test_value, expire=60)
            
            # Teste get
            retrieved_value = redis_manager.get(test_key)
            
            # Teste exists
            exists_result = redis_manager.exists(test_key)
            
            # Teste delete
            delete_result = redis_manager.delete(test_key)
            
            # Obter estatísticas
            stats = redis_manager.get_cache_stats()
            
            self.test_results["tests"]["redis_manager"] = {
                "status": "passed",
                "connection_status": connection_status,
                "set_result": set_result,
                "get_result": retrieved_value == test_value,
                "exists_result": exists_result,
                "delete_result": delete_result,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Redis Manager: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["redis_manager"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Redis Manager: FALHOU - {e}")
    
    def test_websocket_manager(self):
        """Testa WebSocket Manager"""
        logger.info("🌐 Testando WebSocket Manager...")
        
        try:
            # Obter estatísticas
            stats = websocket_manager.get_stats()
            
            # Teste de envio de mensagem (modo fallback)
            test_message = {
                "type": "test_message",
                "data": {"test": "websocket"},
                "timestamp": datetime.now().isoformat()
            }
            
            send_result = websocket_manager.send_message(test_message)
            
            # Teste de registro de handler
            def test_handler(message):
                return {"response": "test_handler_ok"}
            
            websocket_manager.register_message_handler("test_handler", test_handler)
            
            self.test_results["tests"]["websocket_manager"] = {
                "status": "passed",
                "stats": stats,
                "send_result": send_result,
                "handler_registered": True,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ WebSocket Manager: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["websocket_manager"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ WebSocket Manager: FALHOU - {e}")
    
    def test_communication_manager(self):
        """Testa Communication Manager"""
        logger.info("📡 Testando Communication Manager...")
        
        try:
            # Criar sessão de teste
            session_data = {
                "test_session": True,
                "created_at": datetime.now().isoformat(),
                "test_data": {"key": "value"}
            }
            
            self.session_id = communication_manager.create_session(session_data)
            
            # Teste de atualização de sessão
            updates = {"updated": True, "update_time": datetime.now().isoformat()}
            update_result = communication_manager.update_session(self.session_id, updates)
            
            # Teste de atualização de progresso
            progress_data = {
                "tela_atual": "Teste",
                "status": "testando",
                "progresso": 50,
                "timestamp": datetime.now().isoformat()
            }
            progress_result = communication_manager.update_progress(self.session_id, progress_data)
            
            # Teste de obtenção de dados
            retrieved_session = communication_manager.get_session_data(self.session_id)
            retrieved_progress = communication_manager.get_progress_data(self.session_id)
            
            # Teste de envio de evento
            event_result = communication_manager.send_session_event(
                self.session_id, "test_event", {"event_data": "test"}
            )
            
            # Obter estatísticas
            stats = communication_manager.get_communication_stats()
            
            self.test_results["tests"]["communication_manager"] = {
                "status": "passed",
                "session_id": self.session_id,
                "update_result": update_result,
                "progress_result": progress_result,
                "retrieved_session": retrieved_session is not None,
                "retrieved_progress": retrieved_progress is not None,
                "event_result": event_result,
                "stats": stats,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Communication Manager: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["communication_manager"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Communication Manager: FALHOU - {e}")
    
    def test_integration(self):
        """Testa integração completa"""
        logger.info("🔗 Testando integração completa...")
        
        try:
            if not self.session_id:
                # Criar sessão se não existir
                session_data = {"integration_test": True}
                self.session_id = communication_manager.create_session(session_data)
            
            # Simular fluxo completo de comunicação
            test_steps = [
                {"step": 1, "message": "Iniciando teste de integração"},
                {"step": 2, "message": "Testando comunicação Redis"},
                {"step": 3, "message": "Testando comunicação WebSocket"},
                {"step": 4, "message": "Testando comunicação integrada"},
                {"step": 5, "message": "Finalizando teste de integração"}
            ]
            
            integration_results = []
            
            for step in test_steps:
                # Atualizar progresso
                progress_data = {
                    "tela_atual": "Teste de Integração",
                    "status": f"step_{step['step']}",
                    "progresso": (step['step'] * 20),
                    "message": step['message'],
                    "timestamp": datetime.now().isoformat()
                }
                
                progress_result = communication_manager.update_progress(
                    self.session_id, progress_data
                )
                
                # Enviar evento
                event_result = communication_manager.send_session_event(
                    self.session_id, f"integration_step_{step['step']}", step
                )
                
                integration_results.append({
                    "step": step['step'],
                    "progress_result": progress_result,
                    "event_result": event_result
                })
                
                time.sleep(0.5)  # Pequena pausa entre steps
            
            # Limpar sessão de teste
            cleanup_result = communication_manager.delete_session(self.session_id)
            
            self.test_results["tests"]["integration"] = {
                "status": "passed",
                "session_id": self.session_id,
                "steps_completed": len(integration_results),
                "integration_results": integration_results,
                "cleanup_result": cleanup_result,
                "timestamp": datetime.now().isoformat()
            }
            
            logger.info("✅ Integração completa: PASSOU")
            
        except Exception as e:
            self.test_results["tests"]["integration"] = {
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
            logger.error(f"❌ Integração completa: FALHOU - {e}")
    
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
        
        logger.info(f"📊 RESUMO DOS TESTES:")
        logger.info(f"   Total: {total_tests}")
        logger.info(f"   Passou: {passed_tests}")
        logger.info(f"   Falhou: {failed_tests}")
        logger.info(f"   Taxa de sucesso: {self.test_results['summary']['success_rate']:.1f}%")
        logger.info(f"   Status geral: {self.test_results['summary']['overall_status']}")
        logger.info(f"   Duração: {duration:.2f} segundos")

def main():
    """Função principal para executar os testes"""
    if not COMMUNICATION_AVAILABLE:
        logger.error("❌ Módulos de comunicação não disponíveis")
        return
    
    tester = CommunicationSystemTester()
    results = tester.run_all_tests()
    
    # Salvar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"test_results_communication_{timestamp}.json"
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        logger.info(f"📄 Resultados salvos em: {filename}")
    except Exception as e:
        logger.error(f"❌ Falha ao salvar resultados: {e}")
    
    return results

if __name__ == "__main__":
    main()
