#!/usr/bin/env python3
"""
TESTE DO LOGIN PLAYWRIGHT
Script para testar apenas o login do RPA Playwright
"""

import json
import sys
from playwright.sync_api import sync_playwright
from executar_rpa_playwright import setup_playwright_browser, realizar_login_automatico_playwright

def main():
    """Função principal"""
    print("🔐 TESTE DO LOGIN PLAYWRIGHT")
    print("=" * 40)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        print(f"📧 Email: {parametros['autenticacao']['email_login']}")
        print(f"🔒 Senha: {'*' * len(parametros['autenticacao']['senha_login'])}")
        
        # Configurar browser
        print("\n🖥️ Configurando browser Playwright...")
        playwright, browser, context, page = setup_playwright_browser(headless=False)
        
        if not page:
            print("❌ Falha ao configurar browser")
            return 1
        
        try:
            # Navegar para o site
            url_base = parametros.get("url_base", "https://www.app.tosegurado.com.br/imediatoseguros")
            print(f"🌐 Navegando para: {url_base}")
            
            page.goto(url_base)
            page.wait_for_load_state('networkidle')
            print("✅ Página carregada")
            
            # Testar login
            print("\n🔐 Testando login automático...")
            resultado_login = realizar_login_automatico_playwright(page, parametros)
            
            if resultado_login:
                print("✅ LOGIN REALIZADO COM SUCESSO!")
                print("🎉 RPA Playwright está funcionando!")
                
                # Aguardar um pouco para visualizar
                import time
                time.sleep(5)
                
            else:
                print("❌ LOGIN FALHOU!")
                print("🔧 Verificar configurações de login")
            
            return 0
            
        finally:
            # Fechar browser
            if browser:
                browser.close()
            if playwright:
                playwright.stop()
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

