#!/usr/bin/env python3
"""
TESTE BROWSER SIMPLES
Script que abre o browser e aguarda orientação
"""

import json
import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🎯 TESTE BROWSER SIMPLES")
    print("=" * 30)
    
    try:
        # Configurar browser
        print("\n🖥️ Abrindo browser Playwright...")
        playwright = sync_playwright().start()
        
        try:
            # Configurar browser
            browser = playwright.chromium.launch(
                headless=False,  # Modo visual para você acompanhar
                args=[
                    '--no-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-web-security'
                ]
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            
            page = context.new_page()
            page.set_default_timeout(60000)  # 60 segundos timeout
            
            print("✅ Browser configurado")
            
            # Tentar acessar o site
            url_base = "https://www.app.tosegurado.com.br/imediatoseguros"
            print(f"\n🌐 Tentando acessar: {url_base}")
            
            try:
                # Tentar navegar sem aguardar networkidle
                page.goto(url_base, timeout=30000)
                print("✅ Navegação inicial realizada")
                
                # Aguardar um pouco
                time.sleep(5)
                
                print("\n🎯 BROWSER ABERTO!")
                print("=" * 25)
                print("O site carregou?")
                print("Você consegue ver a página?")
                print("=" * 25)
                
                # Aguardar orientação
                print("\n⏳ Aguardando sua confirmação...")
                print("💡 Me diga se o site carregou!")
                
                # Manter o browser aberto por 60 segundos
                time.sleep(60)
                
                print("\n✅ Teste concluído!")
                
            except Exception as e:
                print(f"❌ Erro na navegação: {e}")
                print("💡 Tentando abrir apenas o browser...")
                
                # Tentar abrir uma página simples
                try:
                    page.goto("https://www.google.com", timeout=30000)
                    print("✅ Google carregado como teste")
                    time.sleep(30)
                except Exception as e2:
                    print(f"❌ Erro ao carregar Google: {e2}")
            
            return 0
            
        finally:
            # Fechar browser
            if 'browser' in locals():
                browser.close()
            playwright.stop()
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

