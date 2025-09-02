#!/usr/bin/env python3
"""
TESTE TELA 1 INTERATIVO
Script que abre o site e aguarda orientação para clicar no botão correto
"""

import json
import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🎯 TESTE TELA 1 INTERATIVO")
    print("=" * 40)
    print("O site será aberto e você pode me orientar sobre onde clicar!")
    print("=" * 40)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        
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
            
            # Acessar o site
            url_base = "https://www.app.tosegurado.com.br/imediatoseguros"
            print(f"\n🌐 Acessando: {url_base}")
            
            try:
                page.goto(url_base, timeout=30000)
                page.wait_for_load_state('networkidle', timeout=30000)
                title = page.title()
                print(f"✅ Site carregado: {title}")
                
                print("\n🎯 SITE ABERTO!")
                print("=" * 30)
                print("Agora você pode me orientar sobre:")
                print("1. Onde está o botão 'Carro'")
                print("2. Qual seletor usar")
                print("3. Como clicar corretamente")
                print("=" * 30)
                
                # Aguardar orientação
                print("\n⏳ Aguardando sua orientação...")
                print("💡 Me diga onde está o botão 'Carro'!")
                
                # Manter o browser aberto por 60 segundos
                time.sleep(60)
                
                print("\n✅ Teste concluído!")
                print("📝 Com sua orientação, vou ajustar o seletor correto!")
                
            except Exception as e:
                print(f"❌ Erro ao acessar site: {e}")
            
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

