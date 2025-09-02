#!/usr/bin/env python3
"""
DEBUG TELA 5: Pausa na Tela 5 para verificar elementos
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

def debug_tela_5(page):
    """DEBUG TELA 5: Analisa elementos presentes"""
    try:
        exibir_mensagem("🔍 DEBUG TELA 5: Analisando elementos da página")
        exibir_mensagem("=" * 50)
        
        # Informações básicas da página
        exibir_mensagem(f"📄 URL: {page.url}")
        exibir_mensagem(f"📄 Título: {page.title}")
        
        # Verificar título esperado
        titulo_esperado = "Confira abaixo a estimativa inicial para o seu seguro carro!"
        titulo_elemento = page.locator("text=" + titulo_esperado)
        exibir_mensagem(f"🔍 Título esperado encontrado: {titulo_elemento.count()}")
        
        # Verificar diferentes variações do título
        variacoes_titulo = [
            "estimativa inicial",
            "estimativa",
            "seguro carro",
            "Confira abaixo"
        ]
        
        for variacao in variacoes_titulo:
            elementos = page.locator(f"text={variacao}")
            exibir_mensagem(f"🔍 '{variacao}': {elementos.count()} elementos")
        
        # Verificar cards de cobertura
        cards_cobertura = page.locator(".min-w-0")
        exibir_mensagem(f"🔍 Cards '.min-w-0': {cards_cobertura.count()}")
        
        # Verificar outros seletores de cards
        seletores_cards = [
            ".card",
            ".cobertura", 
            ".plano",
            ".estimativa",
            "[class*='card']",
            "[class*='cobertura']"
        ]
        
        for seletor in seletores_cards:
            elementos = page.locator(seletor)
            exibir_mensagem(f"🔍 '{seletor}': {elementos.count()} elementos")
        
        # Verificar botões "Continuar"
        botoes_continuar = page.locator("button").filter(has_text="Continuar")
        exibir_mensagem(f"🔍 Botões 'Continuar': {botoes_continuar.count()}")
        
        # Verificar botão específico da Tela 5
        botao_especifico = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
        exibir_mensagem(f"🔍 Botão específico Tela 5: {botao_especifico.count()}")
        
        # Verificar elementos com preços
        elementos_preco = page.locator("text=R$")
        exibir_mensagem(f"🔍 Elementos com 'R$': {elementos_preco.count()}")
        
        # Verificar elementos com "estimativa"
        elementos_estimativa = page.locator("text=estimativa")
        exibir_mensagem(f"🔍 Elementos 'estimativa': {elementos_estimativa.count()}")
        
        # Capturar screenshot
        screenshot_path = f"debug_tela_5_{int(time.time())}.png"
        page.screenshot(path=screenshot_path)
        exibir_mensagem(f"📸 Screenshot salvo: {screenshot_path}")
        
        # Aguardar input do usuário
        exibir_mensagem("\n⏸️ PAUSADO PARA ANÁLISE")
        exibir_mensagem("Verifique o screenshot e pressione ENTER para continuar...")
        input()
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO no debug: {str(e)}")
        return False

def main():
    """Função principal"""
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("🚀 INICIANDO DEBUG TELA 5")
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
            
            # DEBUG TELA 5: Analisar elementos
            debug_tela_5(page)
            
            browser.close()
            return True
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO GERAL: {str(e)}")
        return False

if __name__ == "__main__":
    sucesso = main()
    if sucesso:
        exibir_mensagem("✅ DEBUG CONCLUÍDO!")
        sys.exit(0)
    else:
        exibir_mensagem("❌ DEBUG FALHOU!")
        sys.exit(1)
