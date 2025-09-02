#!/usr/bin/env python3
"""
================================================================================
RPA TÔ SEGURADO - MIGRAÇÃO SELENIUM → PLAYWRIGHT
================================================================================

DESCRIÇÃO:
    Script principal para execução sequencial das Telas 1-5 do RPA Tô Segurado,
    implementado em Playwright para resolver problemas de detecção de elementos
    dinâmicos e StaleElementReferenceException do Selenium original.

FUNCIONALIDADES:
    - Navegação sequencial das Telas 1-5
    - Captura estruturada de dados da Tela 5 (Estimativa Inicial)
    - Parse de valores monetários "De R$ X até R$ Y"
    - Estruturação JSON alinhada com padrão esperado
    - Logs detalhados de execução

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 2.11.0
STATUS: Telas 1-5 funcionando perfeitamente
================================================================================
"""
import json
import sys
import time
import re
import os
from datetime import datetime
from playwright.sync_api import sync_playwright


def exibir_mensagem(mensagem):
    """
    ================================================================================
    FUNÇÃO: exibir_mensagem()
    ================================================================================
    
    DESCRIÇÃO:
        Exibe mensagens formatadas com timestamp para facilitar o debugging
        e acompanhamento da execução do RPA.
    
    PARÂMETROS:
        mensagem (str): Texto da mensagem a ser exibida
    
    RETORNO:
        None (apenas exibe no console)
    
    EXEMPLO:
        exibir_mensagem("📱 TELA 1: Selecionando Carro...")
        # Saída: [14:30:25] 📱 TELA 1: Selecionando Carro...
    ================================================================================
    """
    print(f"[{time.strftime('%H:%M:%S')}] {mensagem}")


def navegar_tela_1_playwright(page):
    """
    ================================================================================
    FUNÇÃO: navegar_tela_1_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Implementa a navegação da Tela 1 - Seleção do tipo de seguro.
        Esta é a primeira tela do fluxo, onde o usuário escolhe o tipo
        de seguro (Carro, Moto, etc.). No nosso caso, sempre selecionamos "Carro".
    
    ELEMENTOS IDENTIFICADOS:
        - Seletor: "button.group"
        - HTML: <button class="group">Carro</button>
        - Ação: Click no botão "Carro"
    
    ESTRATÉGIA DE IMPLEMENTAÇÃO:
        1. Aguardar 3 segundos para carregamento da página
        2. Localizar o botão usando seletor CSS "button.group"
        3. Verificar se o elemento está visível
        4. Clicar no botão se visível
        5. Aguardar 3 segundos para transição
        6. Retornar True/False baseado no sucesso
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        bool: True se navegação bem-sucedida, False caso contrário
    
    LOGS:
        - "📱 TELA 1: Selecionando Carro..."
        - "✅ Botão 'Carro' clicado com sucesso"
        - "❌ Botão 'Carro' não está visível"
        - "❌ ERRO na Tela 1: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 1
        exibir_mensagem("📱 TELA 1: Selecionando Carro...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        # Este delay é necessário para garantir que a página carregou completamente
        # e os elementos estão disponíveis para interação
        time.sleep(3)
        
        # PASSO 3: Localizar o botão "Carro" usando seletor CSS
        # O seletor "button.group" foi identificado através de inspeção visual
        # e gravações Selenium como referência
        botao_carro = page.locator("button.group").first
        
        # PASSO 4: Verificar se o botão está visível antes de clicar
        # Esta verificação previne erros de elemento não encontrado
        if botao_carro.is_visible():
            # PASSO 5: Clicar no botão "Carro"
            # Esta ação navega para a próxima tela (Tela 2)
            botao_carro.click()
            
            # PASSO 6: Confirmar sucesso da ação
            exibir_mensagem("✅ Botão 'Carro' clicado com sucesso")
            
            # PASSO 7: Aguardar transição para próxima tela
            # Este delay permite que a página carregue completamente
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
    ================================================================================
    FUNÇÃO: navegar_tela_2_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Implementa a navegação da Tela 2 - Inserção da placa do veículo.
        Esta tela permite ao usuário inserir a placa do veículo para
        que o sistema busque as informações do carro no banco de dados.
    
    ELEMENTOS IDENTIFICADOS:
        - Campo placa: "#placaTelaDadosPlaca"
        - Botão continuar: "#gtm-telaDadosAutoCotarComPlacaContinuar"
        - HTML: <input id="placaTelaDadosPlaca" />
        - HTML: <button id="gtm-telaDadosAutoCotarComPlacaContinuar">Continuar</button>
    
    ESTRATÉGIA DE IMPLEMENTAÇÃO:
        1. Aguardar 3 segundos para carregamento
        2. Localizar campo de placa
        3. Clicar no campo para focar
        4. Preencher com a placa fornecida
        5. Localizar botão "Continuar"
        6. Clicar no botão para prosseguir
        7. Aguardar transição
        8. Retornar status
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
        placa (str): Placa do veículo (ex: "EED-3D56")
    
    RETORNO:
        bool: True se navegação bem-sucedida, False caso contrário
    
    LOGS:
        - "📱 TELA 2: Inserindo placa {placa}..."
        - "✅ Placa {placa} inserida com sucesso"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Campo de placa não está visível"
        - "❌ Botão 'Continuar' não está visível"
        - "❌ ERRO na Tela 2: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 2
        exibir_mensagem(f"📱 TELA 2: Inserindo placa {placa}...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        # Este delay garante que a página carregou após a Tela 1
        time.sleep(3)
        
        # PASSO 3: Localizar o campo de inserção da placa
        # O seletor "#placaTelaDadosPlaca" foi identificado através de
        # inspeção visual e gravações Selenium
        campo_placa = page.locator("#placaTelaDadosPlaca").first
        
        # PASSO 4: Verificar se o campo está visível
        if campo_placa.is_visible():
            # PASSO 5: Clicar no campo para focar
            # Isso garante que o campo está ativo para receber input
            campo_placa.click()
            
            # PASSO 6: Preencher o campo com a placa fornecida
            # O método fill() do Playwright é mais robusto que send_keys()
            campo_placa.fill(placa)
            
            # PASSO 7: Confirmar preenchimento da placa
            exibir_mensagem(f"✅ Placa {placa} inserida com sucesso")
            
            # PASSO 8: Localizar o botão "Continuar"
            # Este botão confirma a inserção da placa e navega para Tela 3
            botao_continuar = page.locator("#gtm-telaDadosAutoCotarComPlacaContinuar").first
            
            # PASSO 9: Verificar se o botão está visível
            if botao_continuar.is_visible():
                # PASSO 10: Clicar no botão "Continuar"
                botao_continuar.click()
                
                # PASSO 11: Confirmar sucesso da navegação
                exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
                
                # PASSO 12: Aguardar transição para próxima tela
                time.sleep(3)
                
                # PASSO 13: Retornar sucesso
                return True
            else:
                # PASSO 14: Tratar caso onde botão não está visível
                exibir_mensagem("❌ Botão 'Continuar' não está visível")
                return False
        else:
            # PASSO 15: Tratar caso onde campo não está visível
            exibir_mensagem("❌ Campo de placa não está visível")
            return False
            
    except Exception as e:
        # PASSO 16: Tratar exceções durante a execução
        exibir_mensagem(f"❌ ERRO na Tela 2: {str(e)}")
        return False


def navegar_tela_3_playwright(page):
    """
    ================================================================================
    FUNÇÃO: navegar_tela_3_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Implementa a navegação da Tela 3 - Confirmação das informações do veículo.
        Esta tela exibe os dados do veículo encontrados pela placa inserida
        e solicita confirmação do usuário para prosseguir.
    
    ELEMENTOS IDENTIFICADOS:
        - Botão continuar: "#gtm-telaInfosAutoContinuar"
        - HTML: <button id="gtm-telaInfosAutoContinuar">Continuar</button>
    
    ESTRATÉGIA DE IMPLEMENTAÇÃO:
        1. Aguardar 3 segundos para carregamento
        2. Localizar botão "Continuar"
        3. Verificar se está visível
        4. Clicar no botão
        5. Aguardar transição
        6. Retornar status
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        bool: True se navegação bem-sucedida, False caso contrário
    
    LOGS:
        - "📱 TELA 3: Confirmando veículo..."
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Botão 'Continuar' não está visível"
        - "❌ ERRO na Tela 3: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 3
        exibir_mensagem("📱 TELA 3: Confirmando veículo...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        # Este delay garante que a página carregou após a Tela 2
        time.sleep(3)
        
        # PASSO 3: Localizar o botão "Continuar"
        # Este botão confirma as informações do veículo e navega para Tela 4
        botao_continuar = page.locator("#gtm-telaInfosAutoContinuar").first
        
        # PASSO 4: Verificar se o botão está visível
        if botao_continuar.is_visible():
            # PASSO 5: Clicar no botão "Continuar"
            # Esta ação confirma as informações do veículo
            botao_continuar.click()
            
            # PASSO 6: Confirmar sucesso da ação
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            
            # PASSO 7: Aguardar transição para próxima tela
            time.sleep(3)
            
            # PASSO 8: Retornar sucesso
            return True
        else:
            # PASSO 9: Tratar caso onde botão não está visível
            exibir_mensagem("❌ Botão 'Continuar' não está visível")
            return False
            
    except Exception as e:
        # PASSO 10: Tratar exceções durante a execução
        exibir_mensagem(f"❌ ERRO na Tela 3: {str(e)}")
        return False


def navegar_tela_4_playwright(page, veiculo_segurado):
    """
    ================================================================================
    FUNÇÃO: navegar_tela_4_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Implementa a navegação da Tela 4 - Verificação se o veículo já está segurado.
        Esta tela pergunta se o veículo já possui seguro ativo, para determinar
        se é uma renovação ou nova contratação.
    
    ELEMENTOS IDENTIFICADOS:
        - Botão "Não": "#gtm-telaRenovacaoVeiculoContinuar"
        - HTML: <button id="gtm-telaRenovacaoVeiculoContinuar">Não</button>
    
    ESTRATÉGIA DE IMPLEMENTAÇÃO:
        1. Aguardar 3 segundos para carregamento
        2. Verificar parâmetro veiculo_segurado
        3. Se "Não": localizar e clicar no botão "Não"
        4. Se "Sim": implementar lógica específica (não implementada)
        5. Aguardar transição
        6. Retornar status
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
        veiculo_segurado (str): "Sim" ou "Não"
    
    RETORNO:
        bool: True se navegação bem-sucedida, False caso contrário
    
    LOGS:
        - "📱 TELA 4: Veículo já segurado ({veiculo_segurado})..."
        - "✅ 'Não' selecionado com sucesso"
        - "❌ Botão 'Não' não está visível"
        - "⚠️ Lógica para 'Sim' não implementada"
        - "❌ ERRO na Tela 4: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 4
        exibir_mensagem(f"📱 TELA 4: Veículo já segurado ({veiculo_segurado})...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        # Este delay garante que a página carregou após a Tela 3
        time.sleep(3)
        
        # PASSO 3: Verificar o parâmetro veiculo_segurado
        # Este parâmetro determina qual opção selecionar
        if veiculo_segurado == "Não":
            # PASSO 4: Localizar o botão "Não"
            # Este botão indica que o veículo não está segurado
            botao_nao = page.locator("#gtm-telaRenovacaoVeiculoContinuar").first
            
            # PASSO 5: Verificar se o botão está visível
            if botao_nao.is_visible():
                # PASSO 6: Clicar no botão "Não"
                # Esta ação indica que é uma nova contratação
                botao_nao.click()
                
                # PASSO 7: Confirmar sucesso da ação
                exibir_mensagem("✅ 'Não' selecionado com sucesso")
                
                # PASSO 8: Aguardar transição para próxima tela
                time.sleep(3)
                
                # PASSO 9: Retornar sucesso
                return True
            else:
                # PASSO 10: Tratar caso onde botão não está visível
                exibir_mensagem("❌ Botão 'Não' não está visível")
                return False
        else:
            # PASSO 11: Tratar caso "Sim" (não implementado)
            # Para veículos já segurados, seria necessário implementar
            # lógica específica de renovação
            exibir_mensagem("⚠️ Lógica para 'Sim' não implementada")
            return False
            
    except Exception as e:
        # PASSO 12: Tratar exceções durante a execução
        exibir_mensagem(f"❌ ERRO na Tela 4: {str(e)}")
        return False


def navegar_tela_5_playwright(page):
    """
    ================================================================================
    FUNÇÃO: navegar_tela_5_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Implementa a navegação da Tela 5 - Estimativa Inicial com captura de dados.
        Esta é a tela mais complexa do fluxo, onde o sistema calcula estimativas
        de preço para diferentes tipos de cobertura e exibe os resultados em cards.
        Além da navegação, esta função captura dados estruturados dos cards.
    
    ELEMENTOS IDENTIFICADOS:
        - Cards de cobertura: "div.bg-primary"
        - Valores monetários: "p.text-primary.underline"
        - Benefícios: "div.gap-3.flex.flex-col.pl-4.mt-3"
        - Botão continuar: "#gtm-telaEstimativaContinuarParaCotacaoFinal"
    
    ESTRATÉGIA DE IMPLEMENTAÇÃO:
        1. Aguardar carregamento inicial (5 segundos)
        2. Loop de tentativas para aguardar elementos dinâmicos (30 tentativas)
        3. Verificar múltiplos indicadores de carregamento
        4. Capturar dados estruturados dos cards
        5. Clicar no botão "Continuar" para prosseguir
        6. Retornar status da operação
    
    DESAFIOS SUPERADOS:
        - Elementos dinâmicos que demoram a carregar
        - Captura precisa de valores monetários
        - Estruturação de dados complexa
        - Timeout configurável para estabilidade
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        bool: True se navegação e captura bem-sucedidas, False caso contrário
    
    LOGS:
        - "📱 TELA 5: Estimativa Inicial - Aguardando cálculo da estimativa..."
        - "🔄 Tentativa {X}/{30} - Aguardando cards de cobertura..."
        - "✅ Elemento de estimativa encontrado: {X} cards"
        - "📊 Dados capturados: {X} coberturas"
        - "💰 Valores encontrados: {X}"
        - "✅ Navegação da Tela 5 concluída"
        - "❌ Timeout: Elementos da Tela 5 não apareceram"
        - "❌ ERRO na Tela 5: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 5
        exibir_mensagem("📱 TELA 5: Estimativa Inicial - Aguardando cálculo da estimativa...")
        
        # PASSO 2: Aguardar carregamento inicial da página
        # Este delay é maior que as outras telas porque a Tela 5
        # precisa calcular estimativas em tempo real
        time.sleep(5)
        
        # PASSO 3: Configurar loop de tentativas para elementos dinâmicos
        # A Tela 5 tem elementos que demoram a carregar devido ao cálculo
        # de estimativas em tempo real
        max_tentativas = 30
        tentativa = 0
        
        # PASSO 4: Loop principal para aguardar carregamento dos elementos
        while tentativa < max_tentativas:
            # PASSO 4.1: Exibir progresso das tentativas
            exibir_mensagem(f"🔄 Tentativa {tentativa + 1}/{max_tentativas} - Aguardando cards de cobertura...")
            
            # PASSO 4.2: Verificar se os cards de cobertura apareceram
            # O seletor "div.bg-primary" foi identificado como o container
            # principal dos cards de estimativa
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                exibir_mensagem(f"✅ Elemento de estimativa encontrado: {elemento_estimativa.count()} cards")
                break
            
            # PASSO 4.3: Verificar se há elementos com preços (fallback)
            # Se os cards não apareceram, verificar se há valores monetários
            elementos_preco = page.locator("text=R$")
            if elementos_preco.count() > 0:
                exibir_mensagem(f"✅ Elementos com preços encontrados: {elementos_preco.count()}")
                break
            
            # PASSO 4.4: Verificar se o botão "Continuar" apareceu (fallback)
            # Último indicador de que a página carregou
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            if botao_continuar.count() > 0:
                exibir_mensagem("✅ Botão 'Continuar' encontrado")
                break
            
            # PASSO 4.5: Aguardar 1 segundo antes da próxima tentativa
            time.sleep(1)
            tentativa += 1
        
        # PASSO 5: Verificar se o timeout foi atingido
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Timeout: Elementos da Tela 5 não apareceram")
            return False
        
        # PASSO 6: Capturar dados estruturados dos cards de cobertura
        # Esta é a funcionalidade principal da Tela 5
        dados_capturados = capturar_dados_carrossel_estimativas_playwright(page)
        
        # PASSO 7: Exibir resumo dos dados capturados
        if dados_capturados:
            exibir_mensagem(f"📊 Dados capturados: {len(dados_capturados.get('coberturas_detalhadas', []))} coberturas")
            exibir_mensagem(f"💰 Valores encontrados: {dados_capturados.get('valores_encontrados', 0)}")
        
        # PASSO 8: Navegar para a próxima tela clicando no botão "Continuar"
        try:
            # PASSO 8.1: Localizar o botão "Continuar"
            botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal")
            
            # PASSO 8.2: Verificar se o botão está disponível
            if botao_continuar.count() > 0:
                # PASSO 8.3: Exibir mensagem de navegação
                exibir_mensagem("🔄 Clicando no botão 'Continuar' da Tela 5")
                
                # PASSO 8.4: Clicar no botão para prosseguir
                botao_continuar.click()
                
                # PASSO 8.5: Aguardar transição para próxima tela
                time.sleep(3)
                
                # PASSO 8.6: Confirmar sucesso da navegação
                exibir_mensagem("✅ Navegação da Tela 5 concluída")
                
                # PASSO 8.7: Retornar sucesso
                return True
            else:
                # PASSO 8.8: Tratar caso onde botão não está disponível
                exibir_mensagem("❌ Botão 'Continuar' não encontrado na Tela 5")
                return False
                
        except Exception as e:
            # PASSO 8.9: Tratar exceções durante o clique no botão
            exibir_mensagem(f"❌ ERRO ao clicar no botão 'Continuar': {str(e)}")
            return False
            
    except Exception as e:
        # PASSO 9: Tratar exceções gerais durante a execução
        exibir_mensagem(f"❌ ERRO na Tela 5: {str(e)}")
        return False


def capturar_dados_carrossel_estimativas_playwright(page):
    """
    ================================================================================
    FUNÇÃO: capturar_dados_carrossel_estimativas_playwright()
    ================================================================================
    
    DESCRIÇÃO:
        Captura dados estruturados do carrossel de estimativas da Tela 5.
        Esta função é o coração da captura de dados, extraindo informações
        detalhadas de cada card de cobertura, incluindo valores monetários,
        benefícios e metadados.
    
    ELEMENTOS CAPTURADOS:
        - Nome da cobertura: "button p.text-white"
        - Valores monetários: "p.text-primary.underline"
        - Benefícios: "div.gap-3.flex.flex-col.pl-4.mt-3"
        - Texto completo: Conteúdo total do card
    
    ESTRATÉGIA DE CAPTURA:
        1. Localizar todos os cards de cobertura
        2. Para cada card:
           a. Extrair nome da cobertura
           b. Parsear valores "De R$ X até R$ Y"
           c. Capturar lista de benefícios
           d. Estruturar dados em JSON
        3. Salvar dados em arquivo temporário
        4. Retornar estrutura completa
    
    TÉCNICAS UTILIZADAS:
        - Regex patterns para parsing de valores monetários
        - Seletores CSS específicos para cada elemento
        - Estruturação hierárquica de dados
        - Fallbacks para casos de erro
    
    PARÂMETROS:
        page (Page): Objeto page do Playwright
    
    RETORNO:
        dict: Estrutura JSON com dados capturados ou None se erro
    
    ESTRUTURA DE RETORNO:
        {
            "timestamp": "2025-09-02T03:45:30.523994",
            "tela": 5,
            "nome_tela": "Estimativa Inicial",
            "coberturas_detalhadas": [
                {
                    "indice": 1,
                    "cobertura": "Cobertura Compreensiva",
                    "valores": {"de": "R$ 1.600,00", "ate": "R$ 2.200,00"},
                    "beneficios": [{"nome": "Colisão e Acidentes", "status": "incluido"}]
                }
            ],
            "valores_encontrados": 6,
            "beneficios_gerais": [...],
            "seguradoras": [...],
            "elementos_detectados": [...]
        }
    
    LOGS:
        - "🔍 Encontrados {X} cards de cobertura (bg-primary)"
        - "📋 Card {X}: {cobertura} - De {valor} até {valor}"
        - "💾 DADOS SALVOS: {caminho_arquivo}"
        - "📊 RESUMO: {X} coberturas detalhadas, {X} benefícios gerais"
        - "❌ ERRO na captura de dados: {erro}"
    ================================================================================
    """
    try:
        # PASSO 1: Inicializar estrutura de dados do carrossel
        # Esta estrutura segue o padrão definido no exemplo_json_retorno.json
        dados_carrossel = {
            "timestamp": datetime.now().isoformat(),  # Timestamp ISO para rastreamento
            "tela": 5,                                # Número da tela atual
            "nome_tela": "Estimativa Inicial",        # Nome descritivo da tela
            "url": str(page.url),                     # URL atual da página
            "titulo": str(page.title),                # Título da página
            "coberturas_detalhadas": [],              # Lista de coberturas capturadas
            "beneficios_gerais": [],                  # Benefícios encontrados na página
            "valores_encontrados": 0,                 # Contador de valores monetários
            "seguradoras": [],                        # Seguradoras detectadas
            "elementos_detectados": []                # Elementos especiais detectados
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
