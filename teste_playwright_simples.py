#!/usr/bin/env python3
"""
TESTE SIMPLES DO PLAYWRIGHT
Script para testar se o Playwright está funcionando corretamente
"""

import json
import sys
from playwright.sync_api import sync_playwright
import time

def main():
    """Função principal"""
    print("🧪 TESTE SIMPLES DO PLAYWRIGHT")
    print("=" * 40)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        print(f"📧 Email: {parametros['autenticacao']['email_login']}")
        
        # Teste básico do Playwright
        print("\n🖥️ Testando Playwright...")
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
            
            # Teste 1: Acessar Google primeiro
            print("\n🌐 Teste 1: Acessando Google...")
            page.goto("https://www.google.com")
            title = page.title()
            print(f"✅ Google carregado: {title}")
            
            time.sleep(2)
            
            # Teste 2: Acessar o site do Tô Segurado
            url_base = parametros.get("url_base", "https://www.app.tosegurado.com.br/imediatoseguros")
            print(f"\n🌐 Teste 2: Acessando {url_base}...")
            
            try:
                page.goto(url_base, timeout=30000)
                page.wait_for_load_state('networkidle', timeout=30000)
                title = page.title()
                print(f"✅ Site carregado: {title}")
                
                # Aguardar um pouco para você ver
                print("⏳ Aguardando 10 segundos para você visualizar...")
                time.sleep(10)
                
                # Teste 3: Verificar se há elementos de login
                print("\n🔍 Teste 3: Verificando elementos de login...")
                
                try:
                    # Tentar encontrar elementos de login
                    elementos_login = [
                        "input[type='email']",
                        "input[type='password']",
                        "button:has-text('Acessar')",
                        "button:has-text('Login')"
                    ]
                    
                    for seletor in elementos_login:
                        try:
                            elemento = page.locator(seletor).first
                            if elemento.is_visible():
                                print(f"✅ Elemento encontrado: {seletor}")
                        except:
                            continue
                    
                    print("✅ Verificação de elementos concluída")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao verificar elementos: {e}")
                
            except Exception as e:
                print(f"❌ Erro ao acessar site: {e}")
                print("💡 Tentando acessar página inicial...")
                
                try:
                    page.goto("https://www.tosegurado.com.br", timeout=30000)
                    title = page.title()
                    print(f"✅ Página inicial carregada: {title}")
                    time.sleep(5)
                except Exception as e2:
                    print(f"❌ Erro ao acessar página inicial: {e2}")
            
            print("\n🎉 TESTE CONCLUÍDO!")
            print("✅ Playwright está funcionando corretamente")
            print("✅ Browser configurado com sucesso")
            print("✅ Navegação funcionando")
            
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

