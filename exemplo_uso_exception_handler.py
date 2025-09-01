#!/usr/bin/env python3
"""
EXEMPLO DE USO - EXCEPTION HANDLER
==================================

Este arquivo demonstra como usar o sistema de exception handler
para substituir as mensagens de erro técnicas por mensagens limpas.
"""

from exception_handler import (
    handle_selenium_exception,
    handle_retry_attempt,
    format_success_message,
    set_session_info
)

def exemplo_implementar_tela_estado_civil(driver, estado_civil_condutor):
    """
    EXEMPLO: Como implementar a Tela de Estado Civil usando o Exception Handler
    
    ANTES (técnico e poluído):
    ===========================
    exibir_mensagem(f"⚠️ Tentativa 1 falhou: {e1}")
    
    DEPOIS (limpo e profissional):
    ==============================
    message = handle_selenium_exception(e1, "Campo Estado Civil")
    exibir_mensagem(message)
    """
    
    opcao_selecionada = False
    
    # Configurar informações da sessão para logging
    set_session_info({
        "tela": "Estado Civil Condutor",
        "elemento": "estadoCivilTelaCondutorPrincipal",
        "valor": estado_civil_condutor
    })
    
    # Tentativa 1: CSS Selector direto
    try:
        opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
        opcao.click()
        message = format_success_message("Campo Estado Civil selecionado", "CSS Selector")
        exibir_mensagem(message)
        opcao_selecionada = True
        
    except Exception as e1:
        # ANTES: exibir_mensagem(f"⚠️ Tentativa 1 falhou: {e1}")
        # DEPOIS: Mensagem limpa para terminal + log completo
        message = handle_retry_attempt(1, 3, e1, "Campo Estado Civil")
        exibir_mensagem(message)
        
        # Tentativa 2: JavaScript click
        try:
            opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
            driver.execute_script("arguments[0].click();", opcao)
            message = format_success_message("Campo Estado Civil selecionado", "JavaScript")
            exibir_mensagem(message)
            opcao_selecionada = True
            
        except Exception as e2:
            message = handle_retry_attempt(2, 3, e2, "Campo Estado Civil")
            exibir_mensagem(message)
            
            # Tentativa 3: ActionChains
            try:
                opcao = driver.find_element(By.CSS_SELECTOR, ".MuiButtonBase-root:nth-child(1)")
                ActionChains(driver).move_to_element(opcao).click().perform()
                message = format_success_message("Campo Estado Civil selecionado", "ActionChains")
                exibir_mensagem(message)
                opcao_selecionada = True
                
            except Exception as e3:
                message = handle_retry_attempt(3, 3, e3, "Campo Estado Civil")
                exibir_mensagem(message)
    
    if not opcao_selecionada:
        exibir_mensagem("❌ Todas as tentativas de seleção falharam")
    
    return opcao_selecionada

def exemplo_selecionar_corretor(driver, usar_corretor_atual):
    """
    EXEMPLO: Como implementar seleção de corretor usando o Exception Handler
    """
    
    if usar_corretor_atual:
        # Selecionar "Sim, continuar com meu corretor"
        try:
            opcao_sim = driver.find_element(By.CSS_SELECTOR, ".cursor-pointer:nth-child(1) > .border .font-workSans")
            opcao_sim.click()
            message = format_success_message("'Sim, continuar com meu corretor' selecionado")
            print(message)
            
        except Exception as e:
            # ANTES: print(f"⚠️ Tentativa 1 falhou: {e}")
            # DEPOIS: Mensagem limpa + log completo
            message = handle_retry_attempt(1, 3, e, "Seleção 'Sim, continuar com meu corretor'")
            print(message)
            
            # Tentativa 2: Via JavaScript
            try:
                opcao_sim = driver.find_element(By.CSS_SELECTOR, ".cursor-pointer:nth-child(1) > .border .font-workSans")
                driver.execute_script("arguments[0].click();", opcao_sim)
                message = format_success_message("'Sim, continuar com meu corretor' selecionado", "JavaScript")
                print(message)
                
            except Exception as e2:
                message = handle_retry_attempt(2, 3, e2, "Seleção 'Sim, continuar com meu corretor'")
                print(message)
                
                # Tentativa 3: Via texto
                if not clicar_radio_via_javascript(driver, "Sim, continuar com meu corretor", "Sim continuar corretor"):
                    print("❌ Erro: Falha ao selecionar 'Sim, continuar com meu corretor'")
                    return False
                message = format_success_message("'Sim, continuar com meu corretor' selecionado", "Texto")
                print(message)

def exemplo_uso_avancado():
    """
    EXEMPLO: Uso avançado com informações detalhadas do elemento
    """
    
    # Informações detalhadas do elemento para logging
    element_info = {
        "selector": "button#continuar",
        "tag_name": "button",
        "text": "Continuar",
        "url": "https://exemplo.com/tela1",
        "page_title": "Tela de Dados"
    }
    
    try:
        # Simular operação que pode falhar
        raise ElementNotInteractableException("element not interactable")
        
    except Exception as e:
        # Capturar exceção com informações detalhadas
        message = handle_selenium_exception(
            exception=e,
            context="Botão Continuar",
            element_info=element_info,
            show_retry_info=True
        )
        print(message)

if __name__ == "__main__":
    print("📚 EXEMPLOS DE USO - EXCEPTION HANDLER")
    print("=" * 50)
    print()
    print("✅ Sistema de exceções configurado")
    print("📋 Logs detalhados em 'rpa_exceptions.log'")
    print("💻 Terminal limpo e profissional")
    print("🔍 Debugging completo nos logs")
    print()
    print("📖 Consulte este arquivo para implementar no seu RPA")
