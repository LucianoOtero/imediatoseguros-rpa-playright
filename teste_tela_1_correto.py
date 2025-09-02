#!/usr/bin/env python3
"""
TESTE TELA 1 - SELEÇÃO CARRO (SELETOR CORRETO)
Script com o seletor correto baseado no HTML fornecido
"""

import json
import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🎯 TESTE TELA 1 - SELEÇÃO CARRO (SELETOR CORRETO)")
    print("=" * 50)
    
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
                
                # Aguardar um pouco para carregar completamente
                time.sleep(3)
                
                print("\n🎯 TELA 1: Procurando botão 'Carro' com seletor correto...")
                
                # Seletores baseados no HTML fornecido
                seletores_corretos = [
                    "button.group",                    # Classe CSS principal
                    "text=Carro",                      # Seletor por texto
                    "button:has-text('Carro')",        # Botão com texto
                    "button.group:has-text('Carro')",  # Combinação classe + texto
                    "css=button.group",                # CSS explícito
                    "xpath=//button[contains(@class,'group')]"  # XPath com classe
                ]
                
                botao_carro_encontrado = False
                
                for i, seletor in enumerate(seletores_corretos, 1):
                    try:
                        print(f"  {i}. Tentando seletor: {seletor}")
                        
                        elemento = page.locator(seletor).first
                        if elemento.is_visible():
                            print(f"✅ Elemento encontrado com seletor: {seletor}")
                            
                            # Verificar se é o botão correto
                            texto_elemento = elemento.text_content().strip()
                            print(f"   → Texto do elemento: '{texto_elemento}'")
                            
                            if "Carro" in texto_elemento:
                                print("✅ Confirmação: É o botão 'Carro' correto!")
                                
                                # Clicar no botão
                                elemento.click()
                                print("✅ Botão 'Carro' clicado com sucesso!")
                                
                                # Aguardar navegação
                                time.sleep(3)
                                page.wait_for_load_state('networkidle', timeout=10000)
                                
                                botao_carro_encontrado = True
                                break
                            else:
                                print("⚠️ Elemento encontrado mas não é o botão 'Carro'")
                                
                    except Exception as e:
                        print(f"   ❌ Falha com seletor {seletor}: {e}")
                        continue
                
                if botao_carro_encontrado:
                    print("\n🎉 TELA 1 CONCLUÍDA COM SUCESSO!")
                    print("✅ Botão 'Carro' clicado")
                    print("✅ Navegação para próxima tela realizada")
                    
                    # Aguardar um pouco para você ver o resultado
                    print("\n⏳ Aguardando 10 segundos para você visualizar...")
                    time.sleep(10)
                    
                else:
                    print("\n❌ TELA 1 FALHOU!")
                    print("❌ Nenhum seletor funcionou")
                    print("💡 Me ajude a identificar o seletor correto!")
                    
                    # Aguardar para você me orientar
                    print("\n⏳ Aguardando sua orientação...")
                    time.sleep(30)
                
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

