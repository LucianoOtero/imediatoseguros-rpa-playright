#!/usr/bin/env python3
"""
IDENTIFICAR TELA 5: Executa até Tela 5 e para para identificação dos elementos
"""

import json
import sys
import time
from playwright.sync_api import sync_playwright


def main():
    """Função principal"""
    print("🎯 IDENTIFICANDO ELEMENTOS DA TELA 5")
    print("=" * 45)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        print("✅ Parâmetros carregados")
        print(f"🚗 Placa: {parametros['placa']}")
        print(f"🚗 Veículo segurado: {parametros['veiculo_segurado']}")
        
        # Configurar browser
        print("\n🖥️ Configurando browser...")
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1139, 'height': 1375})
        page = context.new_page()
        
        # Navegar para o site
        print("\n🌐 Navegando para o site...")
        page.goto("https://www.app.tosegurado.com.br/imediatoseguros")
        time.sleep(3)
        
        # TELA 1: Clicar no botão "Carro"
        print("\n📱 TELA 1: Selecionando 'Carro'...")
        try:
            botao_carro = page.locator("button.group").first
            if botao_carro.is_visible():
                texto_elemento = botao_carro.text_content().strip()
                if "Carro" in texto_elemento:
                    botao_carro.click()
                    print("✅ Botão 'Carro' clicado com sucesso")
                    print(f"   → Seletor usado: button.group")
                    print(f"   → Texto confirmado: '{texto_elemento}'")
                    
                    # Aguardar navegação
                    time.sleep(5)
                else:
                    print("❌ ERRO: Elemento encontrado mas não é o botão 'Carro'")
                    return False
            else:
                print("❌ ERRO: Botão 'Carro' não está visível")
                return False
        except Exception as e:
            print(f"❌ ERRO na Tela 1: {str(e)}")
            return False
        
        # TELA 2: Preencher placa
        print("\n📱 TELA 2: Inserindo placa...")
        try:
            # Preencher placa
            campo_placa = page.locator("#placaTelaDadosPlaca").first
            if campo_placa.is_visible():
                campo_placa.click()
                print("✅ Campo de placa clicado")
                
                campo_placa.fill(parametros['placa'])
                print(f"✅ Placa {parametros['placa']} inserida com sucesso")
                print(f"   → Seletor usado: #placaTelaDadosPlaca")
                
                time.sleep(2)
                
                # Clicar no botão "Continuar"
                botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
                if botao_continuar.is_visible():
                    botao_continuar.click()
                    print("✅ Botão 'Continuar' clicado com sucesso")
                    print(f"   → Seletor usado: #gtm-telaDadosAutoCotarComPlacaContinuar")
                    
                    time.sleep(3)
                else:
                    print("❌ ERRO: Botão 'Continuar' não está visível")
                    return False
            else:
                print("❌ ERRO: Campo de placa não está visível")
                return False
        except Exception as e:
            print(f"❌ ERRO na Tela 2: {str(e)}")
            return False
        
        # TELA 3: Clicar em "Continuar"
        print("\n📱 TELA 3: Clicando em 'Continuar'...")
        try:
            botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
            if botao_continuar.is_visible():
                botao_continuar.click()
                print("✅ Botão 'Continuar' clicado com sucesso")
                print(f"   → Seletor usado: #gtm-telaInfosAutoContinuar")
                
                time.sleep(3)
            else:
                print("❌ ERRO: Botão 'Continuar' não está visível")
                return False
        except Exception as e:
            print(f"❌ ERRO na Tela 3: {str(e)}")
            return False
        
        # TELA 4: Selecionar radio "Não"
        print("\n📱 TELA 4: Selecionando 'Não' para veículo segurado...")
        try:
            # Selecionar radio "Não"
            radio_nao = page.locator("text=Não").first
            if radio_nao.is_visible():
                radio_nao.click()
                print("✅ Radio 'Não' selecionado com sucesso")
                print(f"   → Seletor usado: text=Não")
                
                time.sleep(2)
                
                # Clicar no botão "Continuar"
                botao_continuar = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
                if botao_continuar.is_visible():
                    botao_continuar.click()
                    print("✅ Botão 'Continuar' clicado com sucesso")
                    print(f"   → Seletor usado: #gtm-telaRenovacaoVeiculoContinuar")
                    
                    time.sleep(3)
                else:
                    print("❌ ERRO: Botão 'Continuar' não está visível")
                    return False
            else:
                print("❌ ERRO: Radio 'Não' não está visível")
                return False
        except Exception as e:
            print(f"❌ ERRO na Tela 4: {str(e)}")
            return False
        
        # TELA 5: PARAR PARA IDENTIFICAÇÃO
        print("\n📱 TELA 5: PARADO PARA IDENTIFICAÇÃO DOS ELEMENTOS")
        print("=" * 50)
        print("🔍 INFORMAÇÕES DA PÁGINA ATUAL:")
        print(f"   → URL: {page.url}")
        print(f"   → Título: {page.title}")
        
        # Tentar identificar elementos
        print("\n🔍 TENTANDO IDENTIFICAR ELEMENTOS:")
        
        # 1. Procurar por botões "Continuar"
        botoes_continuar = page.locator("button").filter(has_text="Continuar")
        print(f"   → Botões 'Continuar' encontrados: {botoes_continuar.count()}")
        
        # 2. Procurar por elementos com "estimativa"
        elementos_estimativa = page.locator("text=estimativa")
        print(f"   → Elementos com 'estimativa': {elementos_estimativa.count()}")
        
        # 3. Procurar por elementos com "carrossel"
        elementos_carrossel = page.locator("text=carrossel")
        print(f"   → Elementos com 'carrossel': {elementos_carrossel.count()}")
        
        # 4. Procurar por elementos com "cobertura"
        elementos_cobertura = page.locator("text=cobertura")
        print(f"   → Elementos com 'cobertura': {elementos_cobertura.count()}")
        
        # 5. Procurar por preços (R$)
        precos = page.locator("text=R$")
        print(f"   → Elementos com 'R$': {precos.count()}")
        
        # 6. Procurar por seguradoras
        seguradoras = page.locator("text=Seguradora")
        print(f"   → Elementos com 'Seguradora': {seguradoras.count()}")
        
        print("\n⏸️ BROWSER PAUSADO - AGUARDANDO SUAS INSTRUÇÕES")
        print("=" * 50)
        print("Por favor, me ajude a identificar:")
        print("1. Qual é o título/texto desta tela?")
        print("2. Existe algum botão 'Continuar'? Qual o ID/classe?")
        print("3. Existem cards de cobertura? Como identificá-los?")
        print("4. Existem preços/valores? Como identificá-los?")
        
        # Manter o browser aberto
        input("\nPressione ENTER para fechar o browser...")
        
        # Fechar browser
        browser.close()
        playwright.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
