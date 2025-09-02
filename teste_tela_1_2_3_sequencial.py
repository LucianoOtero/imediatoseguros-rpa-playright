#!/usr/bin/env python3
"""
TESTE SEQUENCIAL: TELA 1 → TELA 2 → TELA 3
Executa Tela 1, Tela 2 e Tela 3 sequencialmente
"""

import json
import sys
import time
from playwright.sync_api import sync_playwright

def main():
    """Função principal"""
    print("🎯 TESTE SEQUENCIAL: TELA 1 → TELA 2 → TELA 3")
    print("=" * 50)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        print(f"🚗 Placa: {parametros['placa']}")
        
        # Configurar browser
        print("\n🖥️ Configurando browser...")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        try:
            # Navegar para o site
            url_base = "https://www.app.tosegurado.com.br/imediatoseguros"
            print(f"\n🌐 Acessando: {url_base}")
            
            page.goto(url_base)
            print("✅ Site acessado")
            
            # ========================================
            # TELA 1: CLICAR NO BOTÃO "CARRO"
            # ========================================
            print("\n🎯 TELA 1: PROCURANDO BOTÃO 'CARRO'...")
            
            # Aguardar carregamento
            time.sleep(3)
            
            # Tentar o seletor que já funciona
            try:
                botao_carro = page.locator("button.group").first
                if botao_carro.is_visible():
                    texto_elemento = botao_carro.text_content().strip()
                    if "Carro" in texto_elemento:
                        botao_carro.click()
                        print("✅ Botão 'Carro' clicado com sucesso")
                        print(f"   → Seletor usado: button.group")
                        print(f"   → Texto confirmado: '{texto_elemento}'")
                    else:
                        print("❌ Elemento encontrado mas não é o botão 'Carro'")
                        return 1
                else:
                    print("❌ Botão 'Carro' não está visível")
                    return 1
                    
            except Exception as e:
                print(f"❌ ERRO na Tela 1: {str(e)}")
                return 1
            
            # Aguardar navegação
            time.sleep(3)
            print("✅ TELA 1 CONCLUÍDA - Navegação para Tela 2 realizada")
            
            # ========================================
            # TELA 2: PREENCHER PLACA
            # ========================================
            print("\n🎯 TELA 2: PREENCHENDO PLACA...")
            
            # Aguardar carregamento da Tela 2
            time.sleep(3)
            
            try:
                # Verificar se estamos na Tela 2
                elemento_tela2 = page.locator("text=Placa do veículo").first
                if elemento_tela2.is_visible():
                    print("✅ Confirmação: Estamos na Tela 2")
                else:
                    print("⚠️ Elemento da Tela 2 não detectado, continuando...")
                
                # Preencher placa usando o seletor correto da gravação
                campo_placa = page.locator("#placaTelaDadosPlaca").first
                if campo_placa.is_visible():
                    # Clicar no campo primeiro
                    campo_placa.click()
                    print("✅ Campo de placa clicado")
                    
                    # Preencher a placa
                    campo_placa.fill(parametros['placa'])
                    print(f"✅ Placa {parametros['placa']} inserida com sucesso")
                    print(f"   → Seletor usado: #placaTelaDadosPlaca")
                    
                    # Aguardar carregamento
                    time.sleep(2)
                    
                    # Clicar no botão "Continuar" usando o seletor correto da gravação
                    botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
                    if botao_continuar.is_visible():
                        botao_continuar.click()
                        print("✅ Botão 'Continuar' clicado com sucesso")
                        print(f"   → Seletor usado: #gtm-telaDadosAutoCotarComPlacaContinuar")
                        
                        # Aguardar navegação
                        time.sleep(3)
                        print("✅ TELA 2 CONCLUÍDA - Navegação para Tela 3 realizada")
                        
                    else:
                        print("❌ ERRO: Botão 'Continuar' não está visível")
                        return 1
                else:
                    print("❌ ERRO: Campo de placa não está visível")
                    return 1
                
            except Exception as e:
                print(f"❌ ERRO na Tela 2: {str(e)}")
                return 1
            
            # ========================================
            # TELA 3: CLICAR NO BOTÃO "CONTINUAR"
            # ========================================
            print("\n🎯 TELA 3: CLICANDO NO BOTÃO 'CONTINUAR'...")
            
            # Aguardar carregamento da Tela 3
            time.sleep(3)
            
            try:
                # Clicar no botão "Continuar" da Tela 3 usando o seletor da gravação
                botao_continuar_tela3 = page.locator("#gtm-telaInfosAutoContinuar").first
                if botao_continuar_tela3.is_visible():
                    botao_continuar_tela3.click()
                    print("✅ Botão 'Continuar' da Tela 3 clicado com sucesso")
                    print(f"   → Seletor usado: #gtm-telaInfosAutoContinuar")
                    
                    # Aguardar navegação
                    time.sleep(3)
                    print("✅ TELA 3 CONCLUÍDA - Navegação para Tela 4 realizada")
                    
                    print("\n🎉 SUCESSO! TELA 1 → TELA 2 → TELA 3 → TELA 4")
                    print("✅ Tela 1: Botão 'Carro' clicado")
                    print("✅ Tela 2: Placa preenchida e 'Continuar' clicado")
                    print("✅ Tela 3: Botão 'Continuar' clicado")
                    print("✅ Pronto para implementar Tela 4")
                    
                    return 0
                else:
                    print("❌ ERRO: Botão 'Continuar' da Tela 3 não está visível")
                    return 1
                
            except Exception as e:
                print(f"❌ ERRO na Tela 3: {str(e)}")
                return 1
            
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
