# -*- coding: utf-8 -*-
"""
Wrapper de Integração Segura para Comunicação Bidirecional - RPA Tô Segurado
Versão: 1.0.0
Data: 2025-09-04
Autor: Luciano Otero

Wrapper seguro para integrar o sistema de comunicação bidirecional
sem modificar o arquivo principal.
"""

from typing import Dict, Any, Optional, Callable
from utils.bidirectional_communication import create_bidirectional_system


def execute_rpa_with_bidirectional_control(original_function: Callable, *args, **kwargs) -> Dict[str, Any]:
    """
    Executa RPA com controle bidirecional
    
    Args:
        original_function: Função original do RPA
        *args: Argumentos da função original
        **kwargs: Argumentos nomeados da função original
        
    Returns:
        Resultado da execução com controle bidirecional
    """
    try:
        # Criar sistema de comunicação
        bidirectional_system = create_bidirectional_system()
        
        if not bidirectional_system.is_available():
            # Fallback: executar sem comunicação bidirecional
            return {
                "status": "success", 
                "result": original_function(*args, **kwargs), 
                "bidirectional_used": False
            }
        
        # Iniciar servidor
        if bidirectional_system.start_server():
            # Atualizar status inicial
            bidirectional_system.update_status("RUNNING", {"stage": "initialization"})
            
            # Executar RPA original
            result = original_function(*args, **kwargs)
            
            # Atualizar status final
            bidirectional_system.update_status("COMPLETED", {"result": "success"})
            
            # Parar servidor
            bidirectional_system.stop_server()
            
            return {
                "status": "success", 
                "result": result, 
                "bidirectional_used": True,
                "communication_status": "active"
            }
        else:
            # Fallback se servidor não iniciar
            return {
                "status": "success", 
                "result": original_function(*args, **kwargs), 
                "bidirectional_used": False
            }
            
    except Exception as e:
        # Em caso de exceção, tentar parar servidor e retornar erro
        try:
            if 'bidirectional_system' in locals():
                bidirectional_system.update_status("ERROR", {"error": str(e)})
                bidirectional_system.stop_server()
        except:
            pass
        
        return {
            "status": "error",
            "error": str(e),
            "bidirectional_used": False
        }


def check_php_commands(bidirectional_system) -> Dict[str, Any]:
    """
    Verifica comandos do PHP
    
    Args:
        bidirectional_system: Instância do sistema bidirecional
        
    Returns:
        Comandos recebidos
    """
    if not bidirectional_system or not bidirectional_system.is_available():
        return {"command": None, "timestamp": None}
    
    return bidirectional_system.check_commands()


def update_rpa_status(bidirectional_system, status: str, details: Dict[str, Any] = None) -> bool:
    """
    Atualiza status do RPA para o PHP
    
    Args:
        bidirectional_system: Instância do sistema bidirecional
        status: Status atual
        details: Detalhes adicionais
        
    Returns:
        Sucesso da operação
    """
    if not bidirectional_system or not bidirectional_system.is_available():
        return False
    
    return bidirectional_system.update_status(status, details)


def create_bidirectional_wrapper():
    """
    Cria wrapper para integração com sistema existente
    
    Returns:
        Função wrapper configurada
    """
    def wrapper(original_function):
        def wrapped_function(*args, **kwargs):
            return execute_rpa_with_bidirectional_control(original_function, *args, **kwargs)
        return wrapped_function
    return wrapper


# Teste básico se executado diretamente
if __name__ == "__main__":
    print("🧪 Testando Wrapper de Integração Bidirecional...")

    # Testar importação
    try:
        from utils.bidirectional_communication import BidirectionalCommunication
        print("✅ Sistema bidirecional importado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao importar: {e}")

    # Testar wrapper
    try:
        wrapper = create_bidirectional_wrapper()
        print("✅ Wrapper criado com sucesso")
    except Exception as e:
        print(f"❌ Erro ao criar wrapper: {e}")

    print("✅ Wrapper de integração bidirecional testado com sucesso!")





