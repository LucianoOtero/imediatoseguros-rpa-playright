#!/usr/bin/env python3
"""
EXCEPTION HANDLER - SISTEMA DE CAPTURA E FORMATAÇÃO DE EXCEÇÕES SELENIUM
=======================================================================

Este módulo captura exceções Selenium e as formata de forma limpa para o terminal,
suprimindo stacktraces técnicos e mantendo apenas informações úteis para o usuário.
Todos os detalhes técnicos são registrados nos logs para debugging.

FUNCIONALIDADES:
- Captura exceções Selenium (element not interactable, etc.)
- Formata mensagens limpas para o terminal
- Suprime stacktraces técnicos
- Registra detalhes completos nos logs
- Mantém funcionalidade de retry intacta
"""

import logging
import traceback
import sys
from datetime import datetime
from typing import Optional, Dict, Any
from selenium.common.exceptions import (
    ElementNotInteractableException,
    ElementClickInterceptedException,
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
    WebDriverException
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('rpa_exceptions.log', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class SeleniumExceptionHandler:
    """Handler para capturar e formatar exceções Selenium"""
    
    def __init__(self):
        self.exception_count = 0
        self.session_info = {}
    
    def format_exception_for_terminal(self, exception: Exception, context: str = "") -> str:
        """Formata exceção para exibição limpa no terminal"""
        
        # Mapear tipos de exceção para mensagens amigáveis
        exception_messages = {
            ElementNotInteractableException: "Elemento não interativo",
            ElementClickInterceptedException: "Elemento interceptado por outro",
            StaleElementReferenceException: "Elemento desatualizado",
            TimeoutException: "Tempo limite excedido",
            NoSuchElementException: "Elemento não encontrado",
            WebDriverException: "Erro do navegador"
        }
        
        # Obter mensagem amigável
        exception_type = type(exception)
        if exception_type in exception_messages:
            friendly_message = exception_messages[exception_type]
        else:
            friendly_message = "Erro de automação"
        
        # Formatar mensagem para terminal
        if context:
            return f"⚠️  [WARNING] {friendly_message} - {context}"
        else:
            return f"⚠️  [WARNING] {friendly_message}"
    
    def log_exception_details(self, exception: Exception, context: str = "", 
                            element_info: Optional[Dict[str, Any]] = None):
        """Registra detalhes completos da exceção nos logs"""
        
        self.exception_count += 1
        
        # Informações básicas
        log_data = {
            "timestamp": datetime.now().isoformat(),
            "exception_count": self.exception_count,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
            "context": context,
            "traceback": traceback.format_exc()
        }
        
        # Adicionar informações do elemento se disponível
        if element_info:
            log_data.update(element_info)
        
        # Adicionar informações da sessão se disponível
        if self.session_info:
            log_data.update(self.session_info)
        
        # Logar detalhes completos
        logger.warning(f"EXCEÇÃO SELENIUM DETALHADA: {log_data}")
        
        # Logar stacktrace completo
        logger.debug(f"STACKTRACE COMPLETO:\n{traceback.format_exc()}")
    
    def handle_selenium_exception(self, exception: Exception, context: str = "", 
                                element_info: Optional[Dict[str, Any]] = None,
                                show_retry_info: bool = True) -> str:
        """Maneja exceção Selenium e retorna mensagem formatada para terminal"""
        
        # Formatar mensagem para terminal (limpa)
        terminal_message = self.format_exception_for_terminal(exception, context)
        
        # Adicionar informação de retry se solicitado
        if show_retry_info:
            terminal_message += "\n    🔄 Tentando novamente automaticamente..."
            terminal_message += "\n    📍 Aguardando elemento ficar disponível..."
        
        # Logar detalhes completos (para debugging)
        self.log_exception_details(exception, context, element_info)
        
        return terminal_message
    
    def set_session_info(self, session_info: Dict[str, Any]):
        """Define informações da sessão para logging"""
        self.session_info = session_info
    
    def handle_retry_attempt(self, attempt_number: int, max_attempts: int, 
                           exception: Exception, context: str = "") -> str:
        """Formata mensagem de tentativa de retry"""
        
        # Mensagem para terminal
        terminal_message = f"⚠️  [WARNING] Tentativa {attempt_number} falhou"
        
        # Adicionar contexto se disponível
        if context:
            terminal_message += f" - {context}"
        
        # Adicionar informações de retry
        if attempt_number < max_attempts:
            terminal_message += f"\n    🔄 Tentativa {attempt_number + 1} de {max_attempts}..."
            terminal_message += "\n    📍 Aguardando elemento ficar disponível..."
        else:
            terminal_message += f"\n    ❌ Todas as {max_attempts} tentativas falharam"
            terminal_message += "\n    📋 Verificando logs para detalhes..."
        
        # Logar detalhes completos
        self.log_exception_details(exception, f"Retry {attempt_number}/{max_attempts} - {context}")
        
        return terminal_message
    
    def format_success_message(self, context: str, method: str = "") -> str:
        """Formata mensagem de sucesso"""
        if method:
            return f"✅ {context} - {method}"
        else:
            return f"✅ {context}"

# Instância global do handler
exception_handler = SeleniumExceptionHandler()

def handle_selenium_exception(exception: Exception, context: str = "", 
                            element_info: Optional[Dict[str, Any]] = None,
                            show_retry_info: bool = True) -> str:
    """Função de conveniência para usar o handler global"""
    return exception_handler.handle_selenium_exception(exception, context, element_info, show_retry_info)

def handle_retry_attempt(attempt_number: int, max_attempts: int, 
                        exception: Exception, context: str = "") -> str:
    """Função de conveniência para formatar tentativas de retry"""
    return exception_handler.handle_retry_attempt(attempt_number, max_attempts, exception, context)

def format_success_message(context: str, method: str = "") -> str:
    """Função de conveniência para formatar mensagens de sucesso"""
    return exception_handler.format_success_message(context, method)

def set_session_info(session_info: Dict[str, Any]):
    """Função de conveniência para definir informações da sessão"""
    exception_handler.set_session_info(session_info)

# Exemplo de uso:
if __name__ == "__main__":
    print("🔧 SISTEMA DE EXCEÇÕES SELENIUM ATIVADO")
    print("=" * 50)
    
    # Simular exceção
    try:
        raise ElementNotInteractableException("element not interactable")
    except Exception as e:
        message = handle_selenium_exception(e, "Botão Continuar")
        print(message)
    
    print("\n📋 Verifique o arquivo 'rpa_exceptions.log' para detalhes completos")
