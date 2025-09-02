#!/usr/bin/env python3
"""
TELA 1 SIMPLES - APENAS CLICAR NO BOTÃO CARRO
Script focado apenas na primeira tela
"""

import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🎯 TELA 1 SIMPLES - BOTÃO CARRO")
    print("=" * 40)
    
    try:
        # Configurar browser
        print("\n🖥️ Abrindo browser...")
        playwright = sync_playwright().start()
        
        try:
            # Configurar browser
            browser = playwright.chromium.launch(
                headless=False,  # Modo visual
                args=['--no-sandbox']
            )
            
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080}
            )
            
            page = context.new_page()
            page.set_default_timeout(30000)
            
            print("✅ Browser configurado")
            
            # Acessar o site
            url = "https://www.app.tosegurado.com.br/imediatoseguros"
            print(f"\n🌐 Acessando: {url}")
            
            page.goto(url)
            print("✅ Site acessado")
            
            # Aguardar carregamento
            time.sleep(3)
            
            print("\n🎯 PROCURANDO BOTÃO 'CARRO'...")
            
            # Seletores baseados no HTML que você forneceu
            seletores = [
                "button.group",                    # Classe CSS
                "text=Carro",                      # Texto
                "button:has-text('Carro')",        # Botão com texto
                "css=button.group",                # CSS explícito
            ]
            
            for i, seletor in enumerate(seletores, 1):
                try:
                    print(f"  {i}. Tentando: {seletor}")
                    
                    elemento = page.locator(seletor).first
                    if elemento.is_visible():
                        print(f"✅ Elemento encontrado!")
                        
                        # Verificar texto
                        texto = elemento.text_content().strip()
                        print(f"   → Texto: '{texto}'")
                        
                        if "Carro" in texto:
                            print("✅ É o botão Carro!")
                            
                            # CLICAR
                            elemento.click()
                            print("🎉 BOTÃO CARRO CLICADO!")
                            
                            # Aguardar navegação
                            time.sleep(5)
                            print("✅ Navegação realizada")
                            
                            # Aguardar para você ver
                            print("\n⏳ Aguardando 15 segundos...")
                            time.sleep(15)
                            
                            return 0
                        else:
                            print("⚠️ Não é o botão Carro")
                            
                except Exception as e:
                    print(f"   ❌ Falha: {e}")
                    continue
            
            print("\n❌ NENHUM SELETOR FUNCIONOU!")
            print("💡 Me ajude a identificar o seletor correto!")
            
            # Aguardar orientação
            print("\n⏳ Aguardando 30 segundos...")
            time.sleep(30)
            
            return 1
            
        finally:
            if 'browser' in locals():
                browser.close()
            playwright.stop()
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())

