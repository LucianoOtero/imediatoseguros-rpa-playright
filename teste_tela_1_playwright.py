#!/usr/bin/env python3
"""
TESTE TELA 1 - SELEÇÃO DO TIPO DE SEGURO (CARRO)
Script para testar apenas a primeira tela do RPA Playwright
"""

import json
import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🎯 TESTE TELA 1 - SELEÇÃO CARRO")
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
            
            # Tentar acessar a página inicial primeiro
            print("\n🌐 Tentando página inicial: https://www.tosegurado.com.br")
            
            try:
                page.goto("https://www.tosegurado.com.br", timeout=30000)
                page.wait_for_load_state('networkidle', timeout=30000)
                title = page.title()
                print(f"✅ Página inicial carregada: {title}")
                
                # Aguardar um pouco
                time.sleep(3)
                
                # Agora tentar navegar para a seção específica
                print("\n🌐 Navegando para: /imediatoseguros")
                
                try:
                    page.goto("https://www.tosegurado.com.br/imediatoseguros", timeout=30000)
                    page.wait_for_load_state('networkidle', timeout=30000)
                    print("✅ Seção imediatoseguros carregada")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao acessar seção específica: {e}")
                    print("💡 Tentando continuar na página atual...")
                
                # Aguardar um pouco para carregar completamente
                time.sleep(3)
                
                print("\n🎯 TELA 1: Procurando botão 'Carro'...")
                
                # Tentar diferentes seletores baseados na gravação
                seletores_teste = [
                    "css=.group:nth-child(1)",  # Seletor da gravação
                    "text=Carro",                # Seletor por texto
                    "button:has-text('Carro')", # Seletor por botão com texto
                    "xpath=//button[contains(.,'Carro')]",  # XPath da gravação
                    "[data-testid*='carro']",    # Possível data-testid
                    ".btn-carro",                # Possível classe CSS
                    "a[href*='carro']"           # Possível link
                ]
                
                botao_carro_encontrado = False
                
                for i, seletor in enumerate(seletores_teste, 1):
                    try:
                        print(f"  {i}. Tentando seletor: {seletor}")
                        
                        elemento = page.locator(seletor).first
                        if elemento.is_visible():
                            print(f"✅ Elemento encontrado com seletor: {seletor}")
                            
                            # Clicar no botão
                            elemento.click()
                            print("✅ Botão 'Carro' clicado com sucesso!")
                            
                            # Aguardar navegação
                            time.sleep(3)
                            page.wait_for_load_state('networkidle', timeout=10000)
                            
                            botao_carro_encontrado = True
                            break
                            
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
                print(f"❌ Erro ao acessar página inicial: {e}")
            
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
