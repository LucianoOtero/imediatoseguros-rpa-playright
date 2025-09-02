#!/usr/bin/env python3
"""
TESTE TELAS 1 A 6 SEQUENCIAL - IMPLEMENTAÇÃO COMPLETA
Teste das Telas 1-6 usando Playwright com implementação da Tela 6

DESCRIÇÃO:
- Tela 1: Seleção do tipo de seguro (Carro)
- Tela 2: Inserção da placa
- Tela 3: Confirmação do veículo
- Tela 4: Veículo segurado
- Tela 5: Estimativa inicial (captura de dados)
- Tela 6: Itens do carro (nova implementação)

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 1.0.0
STATUS: Implementação completa das Telas 1-6
"""

import json
import time
import re
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

def exibir_mensagem(mensagem):
    """
    Exibe mensagem formatada com timestamp
    
    PARÂMETROS:
        mensagem (str): Mensagem a ser exibida
    
    COMPORTAMENTO:
        1. Formata mensagem com timestamp
        2. Exibe no terminal
        3. Formato: [HH:MM:SS] mensagem
    """
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {mensagem}")

def navegar_tela_1_playwright(page):
    """
    TELA 1: Seleção do tipo de seguro (Carro)
    
    DESCRIÇÃO:
        Navega para a Tela 1 e seleciona "Carro" como tipo de seguro
    
    ELEMENTOS IDENTIFICADOS:
        - Botão "Carro": button.group
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento inicial da página
        2. Localiza o botão "Carro"
        3. Verifica se está visível
        4. Clica no botão
        5. Aguarda transição para próxima tela
    
    PARÂMETROS:
        page: Objeto page do Playwright
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 1: Selecionando Carro..."
        - "✅ Botão 'Carro' clicado com sucesso"
        - "❌ Botão 'Carro' não está visível" (se falhar)
        - "❌ ERRO na Tela 1: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 1
        exibir_mensagem("📱 TELA 1: Selecionando Carro...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        time.sleep(3)
        
        # PASSO 3: Localizar o botão "Carro"
        botao_carro = page.locator("button.group").first
        
        # PASSO 4: Verificar se o botão está visível
        if botao_carro.is_visible():
            # PASSO 5: Clicar no botão "Carro"
            botao_carro.click()
            
            # PASSO 6: Confirmar sucesso da ação
            exibir_mensagem("✅ Botão 'Carro' clicado com sucesso")
            
            # PASSO 7: Aguardar transição para próxima tela
            time.sleep(3)
            
            # PASSO 8: Retornar sucesso
            return True
        else:
            # PASSO 9: Tratar caso onde botão não está visível
            exibir_mensagem("❌ Botão 'Carro' não está visível")
            return False
            
    except Exception as e:
        # PASSO 10: Tratar exceções durante a execução
        exibir_mensagem(f"❌ ERRO na Tela 1: {str(e)}")
        return False

def navegar_tela_2_playwright(page, placa):
    """
    TELA 2: Inserção da placa
    
    DESCRIÇÃO:
        Preenche o campo de placa e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS:
        - Campo placa: #placaTelaDadosPlaca
        - Botão continuar: #gtm-telaDadosAutoCotarComPlacaContinuar
    
    IMPLEMENTAÇÃO:
        1. Localiza o campo de placa
        2. Clica no campo para focar
        3. Preenche com a placa fornecida
        4. Localiza o botão "Continuar"
        5. Clica no botão para avançar
    
    PARÂMETROS:
        page: Objeto page do Playwright
        placa (str): Placa do veículo
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 2: Inserindo placa {placa}..."
        - "✅ Placa {placa} inserida com sucesso"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Campo de placa não encontrado" (se falhar)
        - "❌ ERRO na Tela 2: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 2
        exibir_mensagem(f"📱 TELA 2: Inserindo placa {placa}...")
        
        # PASSO 2: Localizar o campo de placa
        campo_placa = page.locator("#placaTelaDadosPlaca").first
        
        # PASSO 3: Clicar no campo para focar
        campo_placa.click()
        
        # PASSO 4: Preencher com a placa
        campo_placa.fill(placa)
        
        # PASSO 5: Confirmar preenchimento
        exibir_mensagem(f"✅ Placa {placa} inserida com sucesso")
        
        # PASSO 6: Localizar o botão "Continuar"
        botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
        
        # PASSO 7: Clicar no botão "Continuar"
        botao_continuar.click()
        
        # PASSO 8: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 9: Aguardar transição
        time.sleep(3)
        
        # PASSO 10: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 11: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 2: {str(e)}")
        return False

def navegar_tela_3_playwright(page):
    """
    TELA 3: Confirmação do veículo
    
    DESCRIÇÃO:
        Confirma as informações do veículo clicando em "Continuar"
    
    ELEMENTOS IDENTIFICADOS:
        - Botão continuar: #gtm-telaInfosAutoContinuar
    
    IMPLEMENTAÇÃO:
        1. Localiza o botão "Continuar"
        2. Verifica se está visível
        3. Clica no botão
        4. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 3: Confirmando informações do veículo..."
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Botão 'Continuar' não encontrado" (se falhar)
        - "❌ ERRO na Tela 3: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 3
        exibir_mensagem("📱 TELA 3: Confirmando informações do veículo...")
        
        # PASSO 2: Localizar o botão "Continuar"
        botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
        
        # PASSO 3: Verificar se está visível
        if botao_continuar.is_visible():
            # PASSO 4: Clicar no botão "Continuar"
            botao_continuar.click()
            
            # PASSO 5: Confirmar clique
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            
            # PASSO 6: Aguardar transição
            time.sleep(3)
            
            # PASSO 7: Retornar sucesso
            return True
        else:
            # PASSO 8: Tratar caso onde botão não está visível
            exibir_mensagem("❌ Botão 'Continuar' não encontrado")
            return False
            
    except Exception as e:
        # PASSO 9: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 3: {str(e)}")
        return False

def navegar_tela_4_playwright(page, veiculo_segurado):
    """
    TELA 4: Veículo segurado
    
    DESCRIÇÃO:
        Responde se o veículo já está segurado baseado no parâmetro
    
    ELEMENTOS IDENTIFICADOS:
        - Botão "Não": #gtm-telaRenovacaoVeiculoContinuar
    
    IMPLEMENTAÇÃO:
        1. Verifica o parâmetro veiculo_segurado
        2. Localiza o botão correspondente
        3. Clica no botão
        4. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
        veiculo_segurado (str): "Sim" ou "Não"
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 4: Respondendo se veículo está segurado..."
        - "✅ Resposta '{veiculo_segurado}' selecionada com sucesso"
        - "❌ Opção '{veiculo_segurado}' não encontrada" (se falhar)
        - "❌ ERRO na Tela 4: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 4
        exibir_mensagem("📱 TELA 4: Respondendo se veículo está segurado...")
        
        # PASSO 2: Verificar parâmetro e localizar botão
        if veiculo_segurado == "Não":
            botao_nao = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
            botao_nao.click()
            exibir_mensagem("✅ Resposta 'Não' selecionada com sucesso")
        else:
            # Implementar lógica para "Sim" se necessário
            exibir_mensagem(f"⚠️ Opção '{veiculo_segurado}' não implementada ainda")
            return False
        
        # PASSO 3: Aguardar transição
        time.sleep(3)
        
        # PASSO 4: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 5: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 4: {str(e)}")
        return False

def navegar_tela_5_playwright(page):
    """
    TELA 5: Estimativa inicial - CAPTURA DE DADOS
    
    DESCRIÇÃO:
        Aguarda carregamento da estimativa e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS:
        - Cards de cobertura: div.bg-primary
        - Botão continuar: #gtm-telaEstimativaContinuarParaCotacaoFinal
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento dos elementos de estimativa
        2. Verifica se os cards estão presentes
        3. Clica no botão "Continuar"
        4. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 5: Aguardando carregamento da estimativa..."
        - "✅ Estimativa carregada com sucesso"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Elementos da estimativa não carregaram" (se falhar)
        - "❌ ERRO na Tela 5: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 5
        exibir_mensagem("📱 TELA 5: Aguardando carregamento da estimativa...")
        
        # PASSO 2: Aguardar até que o elemento específico apareça (máximo 30 segundos)
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                break
            time.sleep(1)
            tentativa += 1
        
        # PASSO 3: Verificar se encontrou elementos
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Elementos da estimativa não carregaram")
            return False
        
        # PASSO 4: Confirmar carregamento
        exibir_mensagem("✅ Estimativa carregada com sucesso")
        
        # PASSO 5: Localizar e clicar no botão "Continuar"
        botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
        botao_continuar.click()
        
        # PASSO 6: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 7: Aguardar transição
        time.sleep(3)
        
        # PASSO 8: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 9: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 5: {str(e)}")
        return False

def navegar_tela_6_playwright(page):
    """
    TELA 6: Itens do carro
    
    DESCRIÇÃO:
        Navega pela Tela 6 (Itens do carro) e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Botão continuar: #gtm-telaItensAutoContinuar
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 6
        2. Localiza o botão "Continuar"
        3. Clica no botão
        4. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 6: Navegando pelos itens do carro..."
        - "✅ Tela 6 carregada com sucesso"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Tela 6 não carregou" (se falhar)
        - "❌ ERRO na Tela 6: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 6
        exibir_mensagem("📱 TELA 6: Navegando pelos itens do carro...")
        
        # PASSO 2: Aguardar carregamento da Tela 6 (máximo 20 segundos)
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            botao_continuar = page.locator("#gtm-telaItensAutoContinuar")
            if botao_continuar.count() > 0 and botao_continuar.first.is_visible():
                break
            time.sleep(1)
            tentativa += 1
        
        # PASSO 3: Verificar se encontrou o botão
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Tela 6 não carregou")
            return False
        
        # PASSO 4: Confirmar carregamento
        exibir_mensagem("✅ Tela 6 carregada com sucesso")
        
        # PASSO 5: Clicar no botão "Continuar"
        botao_continuar.first.click()
        
        # PASSO 6: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 7: Aguardar transição
        time.sleep(3)
        
        # PASSO 8: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 9: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 6: {str(e)}")
        return False

def main():
    """
    Função principal que executa o teste das Telas 1-6 sequencialmente
    
    FLUXO:
        1. Carrega parâmetros do JSON
        2. Configura browser Playwright
        3. Executa Tela 1 → Tela 2 → Tela 3 → Tela 4 → Tela 5 → Tela 6
        4. Exibe resultados de cada tela
        5. Fecha browser
    
    RETORNO:
        int: 0 se sucesso, 1 se falha
    """
    try:
        # Carregar parâmetros
        with open('config/parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 6 SEQUENCIAL")
        exibir_mensagem("=" * 60)
        exibir_mensagem(f"🚗 Placa: {parametros['placa']}")
        exibir_mensagem(f"📋 Veículo segurado: {parametros['veiculo_segurado']}")
        
        # Configurar browser
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            context = browser.new_context(
                viewport={'width': 1139, 'height': 1378},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            # Navegar para o site
            url_base = "https://www.app.tosegurado.com.br/imediatoseguros"
            exibir_mensagem(f"🌐 Navegando para: {url_base}")
            
            page.goto(url_base)
            time.sleep(3)  # Aguardar carregamento inicial
            exibir_mensagem("✅ Página carregada")
            
            # Executar Telas 1-6 sequencialmente
            telas_executadas = 0
            
            # TELA 1
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_1_playwright(page):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 1 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 1 FALHOU!")
                return 1
            
            # TELA 2
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_2_playwright(page, parametros['placa']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 2 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 2 FALHOU!")
                return 1
            
            # TELA 3
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_3_playwright(page):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 3 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 3 FALHOU!")
                return 1
            
            # TELA 4
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_4_playwright(page, parametros['veiculo_segurado']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 4 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 4 FALHOU!")
                return 1
            
            # TELA 5
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_5_playwright(page):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 5 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 5 FALHOU!")
                return 1
            
            # TELA 6
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_6_playwright(page):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 6 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 6 FALHOU!")
                return 1
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 TESTE TELAS 1 A 6 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/6")
            exibir_mensagem("✅ Todas as telas funcionaram corretamente")
            exibir_mensagem("✅ Navegação sequencial realizada com sucesso")
            
            # Aguardar para visualizar resultado final
            exibir_mensagem("\n⏳ Aguardando 10 segundos para visualizar resultado...")
            time.sleep(10)
            
            return 0
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO GERAL: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())
