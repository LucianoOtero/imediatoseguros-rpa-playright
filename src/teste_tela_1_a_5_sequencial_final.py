#!/usr/bin/env python3
"""
TESTE TELAS 1 A 5 SEQUENCIAL FINAL: Executa Telas 1-5 com Tela 5 corrigida
"""
import json
import sys
import time
import re
import os
from datetime import datetime
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
        exibir_mensagem("📱 TELA 5: Estimativa Inicial - Aguardando cálculo da estimativa...")
        
        # Aguardar carregamento inicial
        time.sleep(5)
        
        # Aguardar até que o elemento específico apareça (máximo 30 segundos)
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            exibir_mensagem(f"🔄 Tentativa {tentativa + 1}/{max_tentativas} - Aguardando cards de cobertura...")
            
            # Verificar se o elemento específico apareceu (div com bg-primary)
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                exibir_mensagem(f"✅ Elemento de estimativa encontrado: {elemento_estimativa.count()} cards")
                break
            
            # Verificar se há elementos com preços
            elementos_preco = page.locator("text=R$")
            if elementos_preco.count() > 0:
                exibir_mensagem(f"✅ Elementos com preços encontrados: {elementos_preco.count()}")
                break
            
            # Verificar se o botão "Continuar" apareceu
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("✅ Botão 'Continuar' encontrado")
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
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "url": str(page.url),
            "titulo": str(page.title),
            "coberturas_detalhadas": [],
            "beneficios_gerais": [],
            "valores_encontrados": 0,
            "seguradoras": [],
            "elementos_detectados": []
        }
        
        # Captura os cards de cobertura usando o seletor específico identificado
        cards_cobertura = page.locator("div.bg-primary")
        
        if cards_cobertura.count() > 0:
            exibir_mensagem(f"🔍 Encontrados {cards_cobertura.count()} cards de cobertura (bg-primary)")
            
            for i in range(cards_cobertura.count()):
                try:
                    card = cards_cobertura.nth(i)
                    
                    # Captura o texto completo do card
                    card_text = card.text_content().strip() if card.text_content() else ""
                    
                    if not card_text or len(card_text) < 10:
                        continue
                    
                    cobertura_info = {
                        "indice": i + 1,
                        "nome_cobertura": "",
                        "valores": {
                            "de": "",
                            "ate": ""
                        },
                        "beneficios": [],
                        "texto_completo": card_text
                    }
                    
                    # Extrair nome da cobertura (texto dentro do button)
                    nome_cobertura = ""
                    try:
                        nome_elemento = card.locator("button p.text-white")
                        if nome_elemento.count() > 0:
                            nome_cobertura = nome_elemento.first.text_content().strip()
                            cobertura_info["nome_cobertura"] = nome_cobertura
                    except:
                        pass
                    
                    # Se não encontrou pelo seletor específico, tentar por regex
                    if not nome_cobertura:
                        cobertura_patterns = [
                            r"Cobertura\s+([A-Za-zÀ-ÿ\s]+?)(?:\s|$)",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Cobertura",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Compreensiva",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+Roubo",
                            r"([A-Za-zÀ-ÿ\s]+?)\s+RCF"
                        ]
                        
                        for pattern in cobertura_patterns:
                            match = re.search(pattern, card_text, re.IGNORECASE)
                            if match:
                                cobertura_info["nome_cobertura"] = match.group(1).strip()
                                break
                    
                    # Buscar valores usando o seletor específico identificado
                    try:
                        # Procurar por elementos com valores usando o seletor correto
                        elementos_preco = page.locator("p.text-primary.underline")
                        if elementos_preco.count() > i:
                            preco_text = elementos_preco.nth(i).text_content().strip()
                            
                            # Extrair valores "de" e "até" usando regex
                            valor_patterns = [
                                r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                                r"([0-9.,]+)\s*até\s*([0-9.,]+)"
                            ]
                            
                            for pattern in valor_patterns:
                                match = re.search(pattern, preco_text, re.IGNORECASE)
                                if match:
                                    cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                                    cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                                    break
                    except:
                        pass
                    
                    # Se não encontrou valores específicos, tentar no texto do card
                    if not cobertura_info["valores"]["de"]:
                        valor_patterns = [
                            r"De\s*R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                            r"R\$\s*([0-9.,]+)\s*até\s*R\$\s*([0-9.,]+)",
                            r"([0-9.,]+)\s*até\s*([0-9.,]+)"
                        ]
                        
                        for pattern in valor_patterns:
                            match = re.search(pattern, card_text, re.IGNORECASE)
                            if match:
                                cobertura_info["valores"]["de"] = f"R$ {match.group(1)}"
                                cobertura_info["valores"]["ate"] = f"R$ {match.group(2)}"
                                break
                    
                    # Extrair benefícios usando o seletor específico identificado
                    try:
                        # Procurar por elementos de benefícios próximos ao card
                        elementos_beneficios = page.locator("div.gap-3.flex.flex-col.pl-4.mt-3")
                        if elementos_beneficios.count() > i:
                            container_beneficios = elementos_beneficios.nth(i)
                            beneficios_texto = container_beneficios.locator("p.text-sm.text-gray-100.font-normal")
                            
                            for j in range(beneficios_texto.count()):
                                beneficio_texto = beneficios_texto.nth(j).text_content().strip()
                                if beneficio_texto:
                                    cobertura_info["beneficios"].append({
                                        "nome": beneficio_texto,
                                        "status": "incluido"
                                    })
                    except:
                        pass
                    
                    # Fallback: procurar por benefícios conhecidos no texto do card
                    if not cobertura_info["beneficios"]:
                        beneficios_conhecidos = [
                            "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
                            "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
                            "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
                            "Danos corporais a terceiro", "Assistência", "Carro reserva",
                            "Vidros", "Acidentes", "Colisão", "Terceiros", "Materiais", "Corporais"
                        ]
                        
                        for beneficio in beneficios_conhecidos:
                            if beneficio.lower() in card_text.lower():
                                cobertura_info["beneficios"].append({
                                    "nome": beneficio,
                                    "status": "incluido"
                                })
                    
                    # Se encontrou dados válidos, adicionar à lista
                    if cobertura_info["nome_cobertura"] or cobertura_info["valores"]["de"]:
                        dados_carrossel["coberturas_detalhadas"].append(cobertura_info)
                        
                        # Conta valores encontrados
                        if cobertura_info["valores"]["de"]:
                            dados_carrossel["valores_encontrados"] += 1
                        
                        exibir_mensagem(f"📋 Card {i + 1}: {cobertura_info['nome_cobertura']} - De {cobertura_info['valores']['de']} até {cobertura_info['valores']['ate']}")
                        
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao processar card {i + 1}: {str(e)}")
                    continue
        
        # Procurar por valores monetários gerais (fallback)
        valores_monetarios = page.locator("text=R$")
        dados_carrossel["valores_encontrados"] = max(dados_carrossel["valores_encontrados"], valores_monetarios.count())
        
        # Procurar por benefícios gerais na página
        beneficios_gerais = [
            "Colisão e Acidentes", "Roubo e Furto", "Incêndio", "Danos a terceiros",
            "Assistência 24h", "Carro Reserva", "Vidros", "Roubo", "Furto",
            "Danos parciais em tentativas de roubo", "Danos materiais a terceiros",
            "Danos corporais a terceiro"
        ]
        
        for beneficio in beneficios_gerais:
            elementos = page.locator(f"text={beneficio}")
            if elementos.count() > 0:
                dados_carrossel["beneficios_gerais"].append({
                    "nome": beneficio,
                    "encontrado": True,
                    "quantidade_elementos": elementos.count()
                })
        
        # Procurar por seguradoras
        seguradoras_texto = [
            "Seguradora", "seguradora", "Seguro", "seguro",
            "Allianz", "allianz", "Porto", "porto", "SulAmérica", "sulamerica",
            "Bradesco", "bradesco", "Itaú", "itau", "Santander", "santander"
        ]
        
        for seguradora in seguradoras_texto:
            elementos = page.locator(f"text={seguradora}")
            if elementos.count() > 0:
                for j in range(min(elementos.count(), 3)):  # Limitar a 3 elementos
                    texto = elementos.nth(j).text_content().strip()
                    if texto and len(texto) > 2:
                        dados_carrossel["seguradoras"].append({
                            "nome": texto,
                            "seletor": "texto_contido"
                        })
        
        # Procurar por elementos específicos do carrossel
        elementos_carrossel = page.locator("[class*='carousel'], [class*='slider'], [class*='swiper']")
        if elementos_carrossel.count() > 0:
            dados_carrossel["elementos_detectados"].append("carrossel_detectado")
        
        # Capturar texto completo da página para análise
        page_content = page.content()
        page_text = page_content.lower() if page_content else ""
        
        # Verificar presença de palavras-chave
        palavras_chave = ["estimativa", "carrossel", "cobertura", "preço", "valor", "plano"]
        for palavra in palavras_chave:
            if palavra in page_text:
                dados_carrossel["elementos_detectados"].append(f"palavra_chave: {palavra}")
        
        # Salvar dados em arquivo temporário
        temp_dir = "temp/captura_carrossel"
        os.makedirs(temp_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        json_path = f"{temp_dir}/carrossel_estimativas_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_carrossel, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"💾 DADOS SALVOS: {json_path}")
        exibir_mensagem(f"📊 RESUMO: {len(dados_carrossel['coberturas_detalhadas'])} coberturas detalhadas, {len(dados_carrossel['beneficios_gerais'])} benefícios gerais")
        
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
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 5 SEQUENCIAL FINAL")
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
