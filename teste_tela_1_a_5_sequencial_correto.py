#!/usr/bin/env python3
"""
TESTE SEQUENCIAL CORRETO: TELA 1 → TELA 2 → TELA 3 → TELA 4 → TELA 5
Executa Tela 1, Tela 2, Tela 3, Tela 4 e Tela 5 sequencialmente
"""

import json
import sys
import time
from playwright.sync_api import sync_playwright


def main():
    """Função principal"""
    print("🎯 TESTE SEQUENCIAL CORRETO: TELA 1 → TELA 2 → TELA 3 → TELA 4 → TELA 5")
    print("=" * 65)
    
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
        
        # TELA 5: Capturar dados da estimativa
        print("\n📱 TELA 5: Capturando dados da estimativa...")
        try:
            # Aguardar elementos da estimativa
            page.wait_for_selector("text=estimativa, text=inicial, text=carrossel, text=cobertura", timeout=20000)
            print("✅ Elementos da estimativa detectados")
            
            # Capturar dados estruturados
            dados_carrossel = capturar_dados_carrossel_estimativas_playwright(page)
            
            # Exibir resumo dos dados capturados
            if dados_carrossel:
                print(f"✅ Dados capturados: {len(dados_carrossel.get('coberturas_detalhadas', []))} coberturas")
                print(f"   → Seguradoras: {', '.join(dados_carrossel.get('seguradoras', []))}")
                print(f"   → Valores encontrados: {dados_carrossel.get('valores_encontrados', 0)}")
            
            # Clicar no botão "Continuar" da gravação
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
            if botao_continuar.is_visible():
                botao_continuar.click()
                print("✅ Botão 'Continuar' clicado com sucesso")
                print(f"   → Seletor usado: #gtm-telaEstimativaContinuarParaCotacaoFinal")
                
                time.sleep(3)
            else:
                print("❌ ERRO: Botão 'Continuar' não está visível")
                return False
        except Exception as e:
            print(f"❌ ERRO na Tela 5: {str(e)}")
            return False
        
        print("\n🎉 SUCESSO TOTAL! Todas as telas executadas com sucesso!")
        print("=" * 65)
        
        # Fechar browser
        browser.close()
        playwright.stop()
        
        return True
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        return False


def capturar_dados_carrossel_estimativas_playwright(page):
    """
    Captura dados estruturados do carrossel de estimativas (Tela 5)
    """
    try:
        from datetime import datetime
        
        # Estrutura de dados baseada no projeto Selenium
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "url": page.url,
            "titulo": page.title,
            "coberturas_detalhadas": [],
            "beneficios_gerais": [],
            "valores_encontrados": 0,
            "seguradoras": [],
            "elementos_detectados": []
        }
        
        # Estratégia de captura baseada no projeto Selenium
        # 1. Procurar por cards que contêm as coberturas
        cards_cobertura = page.locator("//*[contains(@class, 'card') or contains(@class, 'cobertura') or contains(@class, 'plano') or contains(@class, 'estimativa')]")
        
        if cards_cobertura.count() > 0:
            print(f"✅ Encontrados {cards_cobertura.count()} cards de cobertura")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    
                    # Capturar dados do card
                    dados_card = {
                        "indice": i + 1,
                        "seguradora": "",
                        "preco": "",
                        "coberturas": [],
                        "beneficios": [],
                        "texto_completo": card.text_content().strip() if card.text_content() else ""
                    }
                    
                    # Tentar extrair seguradora
                    seguradora_element = card.locator("//*[contains(text(), 'Seguradora') or contains(text(), 'Seguro') or contains(@class, 'seguradora')]").first
                    if seguradora_element.is_visible():
                        dados_card["seguradora"] = seguradora_element.text_content().strip()
                        if dados_card["seguradora"] not in dados_carrossel["seguradoras"]:
                            dados_carrossel["seguradoras"].append(dados_card["seguradora"])
                    
                    # Tentar extrair preço
                    preco_element = card.locator("//*[contains(text(), 'R$') or contains(text(), 'preço') or contains(text(), 'valor')]").first
                    if preco_element.is_visible():
                        dados_card["preco"] = preco_element.text_content().strip()
                        dados_carrossel["valores_encontrados"] += 1
                    
                    # Adicionar card aos dados
                    dados_carrossel["coberturas_detalhadas"].append(dados_card)
                    
                except Exception as e:
                    print(f"⚠️ Erro ao processar card {i+1}: {str(e)}")
                    continue
        
        # 2. Procurar por elementos de benefícios gerais
        beneficios_elementos = page.locator("//*[contains(text(), 'benefício') or contains(text(), 'vantagem') or contains(text(), 'incluso')]")
        
        for i in range(beneficios_elementos.count()):
            try:
                beneficio = beneficios_elementos.nth(i)
                if beneficio.is_visible():
                    dados_carrossel["beneficios_gerais"].append(beneficio.text_content().strip())
            except Exception:
                continue
        
        # 3. Registrar elementos detectados
        dados_carrossel["elementos_detectados"] = [
            f"Cards de cobertura: {cards_cobertura.count()}",
            f"Benefícios: {len(dados_carrossel['beneficios_gerais'])}",
            f"Seguradoras: {len(dados_carrossel['seguradoras'])}"
        ]
        
        print(f"✅ Captura concluída: {len(dados_carrossel['coberturas_detalhadas'])} coberturas")
        return dados_carrossel
        
    except Exception as e:
        print(f"❌ ERRO na captura de dados: {str(e)}")
        return None


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
