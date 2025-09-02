#!/usr/bin/env python3
"""
TESTE TELA 1 RPA COMPLETO
Teste da Tela 1 usando o RPA Playwright principal
"""

import json
import sys
from executar_rpa_playwright import setup_playwright_browser, navegar_tela_1_playwright

def main():
    """Função principal"""
    print("🎯 TESTE TELA 1 RPA COMPLETO")
    print("=" * 40)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        
        # Configurar browser
        print("\n🖥️ Configurando browser...")
        playwright, browser, context, page = setup_playwright_browser(headless=False)
        
        if not page:
            print("❌ Falha ao configurar browser")
            return 1
        
        try:
            # Navegar para o site
            url_base = "https://www.app.tosegurado.com.br/imediatoseguros"
            print(f"\n🌐 Navegando para: {url_base}")
            
            page.goto(url_base)
            page.wait_for_load_state('networkidle')
            print("✅ Página carregada")
            
            # Testar Tela 1
            print("\n🎯 TESTANDO TELA 1...")
            resultado = navegar_tela_1_playwright(page, parametros)
            
            if resultado:
                print("\n🎉 TELA 1 FUNCIONOU PERFEITAMENTE!")
                print("✅ Botão 'Carro' clicado com sucesso")
                print("✅ Navegação para próxima tela realizada")
                
                # Aguardar para visualizar
                print("\n⏳ Aguardando 10 segundos...")
                import time
                time.sleep(10)
                
            else:
                print("\n❌ TELA 1 FALHOU!")
                print("💡 Verificar logs acima")
            
            return 0 if resultado else 1
            
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

