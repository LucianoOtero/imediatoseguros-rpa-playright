#!/usr/bin/env python3
"""
TESTE TELAS 1 A 5 SEQUENCIAL CORRIGIDO: Versão com aguardo para carregamento da Tela 5
"""
import json
import sys
import time
from playwright.sync_api import sync_playwright

def exibir_mensagem(mensagem):
    """Exibe mensagem formatada"""
    print(f"[{time.strftime('%H:%M:%S')}] {mensagem}")

def navegar_tela_1_playwright(page):
    """TELA 1: Seleção do tipo de seguro (Carro)"""
    try:
        exibir_mensagem("📱 TELA 1: Selecionando Carro...")
        time.sleep(3)
        botao_carro = page.locator("button.group").first
        if botao_carro.is_visible():
            botao_carro.click()
            exibir_mensagem("✅ Botão 'Carro' clicado com sucesso")
            time.sleep(3)
            return True
        else:
            exibir_mensagem("❌ Botão 'Carro' não está visível")
            return False
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 1: {str(e)}")
        return False

def navegar_tela_2_playwright(page, placa):
    """TELA 2: Inserção da placa"""
    try:
        exibir_mensagem(f"📱 TELA 2: Inserindo placa {placa}...")
        time.sleep(3)
        campo_placa = page.locator("#placaTelaDadosPlaca").first
        if campo_placa.is_visible():
            campo_placa.click()
            campo_placa.fill(placa)
            exibir_mensagem(f"✅ Placa {placa} inserida com sucesso")
            botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
            if botao_continuar.is_visible():
                botao_continuar.click()
                exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
                time.sleep(3)
                return True
            else:
                exibir_mensagem("❌ Botão 'Continuar' não está visível")
                return False
        else:
            exibir_mensagem("❌ Campo de placa não está visível")
            return False
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 2: {str(e)}")
        return False

def navegar_tela_3_playwright(page):
    """TELA 3: Confirmação do veículo"""
    try:
        exibir_mensagem("📱 TELA 3: Confirmando veículo...")
        time.sleep(3)
        botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            time.sleep(3)
            return True
        else:
            exibir_mensagem("❌ Botão 'Continuar' não está visível")
            return False
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 3: {str(e)}")
        return False

def navegar_tela_4_playwright(page, veiculo_segurado):
    """TELA 4: Veículo segurado"""
    try:
        exibir_mensagem(f"📱 TELA 4: Veículo já segurado ({veiculo_segurado})...")
        time.sleep(3)
        if veiculo_segurado == "Não":
            botao_nao = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
            if botao_nao.is_visible():
                botao_nao.click()
                exibir_mensagem("✅ 'Não' selecionado com sucesso")
                time.sleep(3)
                return True
            else:
                exibir_mensagem("❌ Botão 'Não' não está visível")
                return False
        else:
            exibir_mensagem("⚠️ Lógica para 'Sim' não implementada")
            return False
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 4: {str(e)}")
        return False

def navegar_tela_5_playwright(page):
    """TELA 5: Estimativa Inicial - Captura dados dos cards"""
    try:
        exibir_mensagem("📱 TELA 5: Estimativa Inicial - Aguardando carregamento...")
        
        # Aguardar carregamento inicial
        time.sleep(5)
        
        # Aguardar até que os elementos apareçam (máximo 30 segundos)
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            exibir_mensagem(f"🔄 Tentativa {tentativa + 1}/{max_tentativas} - Aguardando elementos...")
            
            # Verificar se os cards apareceram
            cards_cobertura = page.locator(".min-w-0")
            if cards_cobertura.count() > 0:
                exibir_mensagem(f"✅ Cards encontrados: {cards_cobertura.count()}")
                break
            
            # Verificar se o botão "Continuar" apareceu
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("✅ Botão 'Continuar' encontrado")
                break
            
            # Verificar se há elementos com preços
            elementos_preco = page.locator("text=R$")
            if elementos_preco.count() > 0:
                exibir_mensagem(f"✅ Elementos com preços encontrados: {elementos_preco.count()}")
                break
            
            # Aguardar mais um pouco
            time.sleep(1)
            tentativa += 1
        
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Timeout: Elementos da Tela 5 não apareceram")
            return False
        
        # Captura dados dos cards de cobertura
        dados_capturados = capturar_dados_carrossel_estimativas_playwright(page)
        
        if dados_capturados:
            exibir_mensagem(f"📊 Dados capturados: {len(dados_capturados.get('coberturas_detalhadas', []))} coberturas")
            exibir_mensagem(f"💰 Valores encontrados: {dados_capturados.get('valores_encontrados', 0)}")
        
        # Clica no botão "Continuar" para ir para a próxima tela
        try:
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("🔄 Clicando no botão 'Continuar' da Tela 5")
                botao_continuar.click()
                time.sleep(3)
                exibir_mensagem("✅ Navegação da Tela 5 concluída")
                return True
            else:
                exibir_mensagem("❌ Botão 'Continuar' não encontrado na Tela 5")
                return False
        except Exception as e:
            exibir_mensagem(f"❌ ERRO ao clicar no botão 'Continuar': {str(e)}")
            return False
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 5: {str(e)}")
        return False

def capturar_dados_carrossel_estimativas_playwright(page):
    """Captura dados estruturados do carrossel de estimativas (Tela 5)"""
    try:
        from datetime import datetime
        
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
        
        # Tentar diferentes seletores para os cards
        seletores_cards = [
            ".min-w-0",
            "[class*='card']",
            "[class*='cobertura']",
            "[class*='plano']",
            "[class*='estimativa']"
        ]
        
        cards_cobertura = None
        for seletor in seletores_cards:
            cards_cobertura = page.locator(seletor)
            if cards_cobertura.count() > 0:
                exibir_mensagem(f"🔍 Usando seletor '{seletor}': {cards_cobertura.count()} cards")
                break
        
        if cards_cobertura and cards_cobertura.count() > 0:
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    
                    # Captura o nome da cobertura
                    nome_cobertura = ""
                    try:
                        nome_elemento = card.locator(".flex .text-white")
                        if nome_elemento.count() > 0:
                            nome_cobertura = nome_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura o preço
                    preco = ""
                    try:
                        preco_elemento = card.locator(".font-semibold:nth-child(2)")
                        if preco_elemento.count() > 0:
                            preco = preco_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura faixa de preço (se existir)
                    faixa_preco = ""
                    try:
                        faixa_elemento = card.locator(".text-primary .text-primary")
                        if faixa_elemento.count() > 0:
                            faixa_preco = faixa_elemento.first.text_content().strip()
                    except:
                        pass
                    
                    # Captura benefícios
                    beneficios = []
                    try:
                        beneficios_elementos = card.locator(".py-4 .text-sm")
                        for j in range(beneficios_elementos.count()):
                            beneficio = beneficios_elementos.nth(j).text_content().strip()
                            if beneficio:
                                beneficios.append(beneficio)
                    except:
                        pass
                    
                    # Monta o objeto da cobertura
                    if nome_cobertura or preco:
                        cobertura = {
                            "indice": i + 1,
                            "nome": nome_cobertura,
                            "preco": preco,
                            "faixa_preco": faixa_preco,
                            "beneficios": beneficios,
                            "card_selector": f"{seletor}:nth-child({i + 1})"
                        }
                        
                        dados_carrossel["coberturas_detalhadas"].append(cobertura)
                        
                        # Conta valores encontrados
                        if preco and "R$" in preco:
                            dados_carrossel["valores_encontrados"] += 1
                        
                        exibir_mensagem(f"📋 Card {i + 1}: {nome_cobertura} - {preco}")
                        
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao processar card {i + 1}: {str(e)}")
                    continue
        
        # Captura benefícios gerais da página
        try:
            beneficios_gerais = page.locator("text=benefício, text=vantagem, text=incluso")
            for i in range(beneficios_gerais.count()):
                beneficio = beneficios_gerais.nth(i).text_content().strip()
                if beneficio and beneficio not in dados_carrossel["beneficios_gerais"]:
                    dados_carrossel["beneficios_gerais"].append(beneficio)
        except:
            pass
        
        # Resumo dos elementos detectados
        dados_carrossel["elementos_detectados"] = [
            f"Cards de cobertura: {len(dados_carrossel['coberturas_detalhadas'])}",
            f"Benefícios gerais: {len(dados_carrossel['beneficios_gerais'])}",
            f"Valores encontrados: {dados_carrossel['valores_encontrados']}"
        ]
        
        exibir_mensagem(f"✅ Captura concluída: {len(dados_carrossel['coberturas_detalhadas'])} coberturas processadas")
        
        return dados_carrossel
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na captura de dados: {str(e)}")
        return None

def main():
    """Função principal"""
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 5 SEQUENCIAL CORRIGIDO")
        exibir_mensagem("=" * 60)
        
        with sync_playwright() as playwright:
            # Configurar browser
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1139, 'height': 1378},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # Navegar para a página inicial
            exibir_mensagem("🌐 Navegando para a página inicial...")
            page.goto("https://www.app.tosegurado.com.br/imediatoseguros")
            time.sleep(3)
            
            # TELA 1: Seleção Carro
            if not navegar_tela_1_playwright(page):
                exibir_mensagem("❌ FALHA NA TELA 1")
                return False
            
            # TELA 2: Inserção Placa
            if not navegar_tela_2_playwright(page, parametros['placa']):
                exibir_mensagem("❌ FALHA NA TELA 2")
                return False
            
            # TELA 3: Confirmação Veículo
            if not navegar_tela_3_playwright(page):
                exibir_mensagem("❌ FALHA NA TELA 3")
                return False
            
            # TELA 4: Veículo Segurado
            if not navegar_tela_4_playwright(page, parametros['veiculo_segurado']):
                exibir_mensagem("❌ FALHA NA TELA 4")
                return False
            
            # TELA 5: Estimativa Inicial
            if not navegar_tela_5_playwright(page):
                exibir_mensagem("❌ FALHA NA TELA 5")
                return False
            
            exibir_mensagem("\n" + "=" * 60)
            exibir_mensagem("🏁 TESTE TELAS 1 A 5 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem("=" * 60)
            
            # Aguardar um pouco para visualizar o resultado
            time.sleep(5)
            
            browser.close()
            return True
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO GERAL: {str(e)}")
        return False

if __name__ == "__main__":
    sucesso = main()
    if sucesso:
        exibir_mensagem("✅ TESTE CONCLUÍDO COM SUCESSO!")
        sys.exit(0)
    else:
        exibir_mensagem("❌ TESTE FALHOU!")
        sys.exit(1)
