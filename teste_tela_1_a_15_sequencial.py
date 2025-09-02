#!/usr/bin/env python3
"""
TESTE TELAS 1 A 15 SEQUENCIAL - IMPLEMENTAÇÃO COMPLETA
Teste das Telas 1-15 usando Playwright com implementação da Tela 15 (carregamento demorado)

DESCRIÇÃO:
- Tela 1: Seleção do tipo de seguro (Carro)
- Tela 2: Inserção da placa
- Tela 3: Confirmação do veículo
- Tela 4: Veículo segurado
- Tela 5: Estimativa inicial (captura de dados)
- Tela 6: Itens do carro (combustível e checkboxes)
- Tela 7: Endereço de pernoite (CEP)
- Tela 8: Finalidade do veículo (uso do veículo)
- Tela 9: Dados pessoais do segurado
- Tela 10: Condutor principal
- Tela 11: Atividade do veículo (local de trabalho/estudo)
- Tela 12: Garagem na residência
- Tela 13: Residência com menores de 18-26 anos
- Tela 14: Corretor anterior (CONDICIONAL)
- Tela 15: Resultado final (CARREGAMENTO DEMORADO)

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 1.12.0
STATUS: Implementação completa das Telas 1-15 (Tela 14 condicional, Tela 15 demorada)
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
        
        # PASSO 2: Aguardar carregamento inicial da tela
        time.sleep(2)
        
        # PASSO 3: Aguardar até que o elemento específico apareça (máximo 30 segundos)
        max_tentativas = 30
        tentativa = 0
        
        while tentativa < max_tentativas:
            elemento_estimativa = page.locator("div.bg-primary")
            if elemento_estimativa.count() > 0:
                break
            time.sleep(1)
            tentativa += 1
        
        # PASSO 4: Verificar se encontrou elementos
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Elementos da estimativa não carregaram")
            return False
        
        # PASSO 5: Confirmar carregamento
        exibir_mensagem("✅ Estimativa carregada com sucesso")
        
        # PASSO 6: Localizar e clicar no botão "Continuar"
        botao_continuar = page.locator("#gtm-telaEstimativaContinuarParaCotacaoFinal").first
        botao_continuar.click()
        
        # PASSO 7: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 8: Aguardar transição
        time.sleep(3)
        
        # PASSO 9: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 10: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 5: {str(e)}")
        return False

def navegar_tela_6_playwright(page, combustivel, kit_gas, blindado, financiado):
    """
    TELA 6: Itens do carro - SELEÇÃO DE COMBUSTÍVEL E CHECKBOXES
    
    DESCRIÇÃO:
        Seleciona o tipo de combustível, marca/desmarca checkboxes e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS:
        - Seleção de combustível: Radio buttons com name="tipoCombustivelTelaItens"
        - Checkbox Kit Gas: input[value="Kit Gás"]
        - Checkbox Blindado: input[value="Blindado"]
        - Checkbox Financiado: input[value="Financiado"]
        - Botão continuar: #gtm-telaItensAutoContinuar
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 6
        2. Seleciona o combustível baseado no parâmetro
        3. Marca/desmarca checkboxes baseado nos parâmetros
        4. Localiza o botão "Continuar"
        5. Clica no botão
        6. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
        combustivel (str): Tipo de combustível ("Flex", "Gasolina", "Etanol", etc.)
        kit_gas (bool): Se deve marcar checkbox Kit Gas
        blindado (bool): Se deve marcar checkbox Blindado
        financiado (bool): Se deve marcar checkbox Financiado
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 6: Aguardando carregamento..."
        - "📱 TELA 6: Selecionando combustível {combustivel}..."
        - "✅ Combustível {combustivel} selecionado com sucesso"
        - "📱 TELA 6: Configurando checkboxes..."
        - "✅ Checkbox Kit Gas: {estado}"
        - "✅ Checkbox Blindado: {estado}"
        - "✅ Checkbox Financiado: {estado}"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Tela 6 não carregou" (se falhar)
        - "❌ ERRO na Tela 6: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 6
        exibir_mensagem("📱 TELA 6: Aguardando carregamento...")
        
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
        
        # PASSO 5: Selecionar combustível
        exibir_mensagem(f"📱 TELA 6: Selecionando combustível {combustivel}...")
        
        # PASSO 6: Mapear combustível para valor do radio button
        mapeamento_combustivel = {
            "Flex": "1",
            "Gasolina": "2", 
            "Alcool": "3",
            "Etanol": "3",  # Alcool e Etanol são o mesmo
            "Diesel": "4",
            "Híbrido": "5",
            "Elétrico": "6"
        }
        
        # PASSO 7: Obter valor do radio button para o combustível
        valor_radio = mapeamento_combustivel.get(combustivel)
        combustivel_selecionado = False
        
        if valor_radio:
            # PASSO 8: Localizar e clicar no radio button específico
            try:
                radio_combustivel = page.locator(f"input[name='tipoCombustivelTelaItens'][value='{valor_radio}']").first
                if radio_combustivel.is_visible():
                    radio_combustivel.click()
                    combustivel_selecionado = True
                    exibir_mensagem(f"✅ Combustível {combustivel} selecionado com sucesso (valor={valor_radio})")
                else:
                    exibir_mensagem(f"⚠️ Radio button para {combustivel} (valor={valor_radio}) não está visível")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao selecionar {combustivel}: {str(e)}")
        else:
            exibir_mensagem(f"⚠️ Combustível '{combustivel}' não mapeado")
        
        # PASSO 9: Verificar se conseguiu selecionar
        if not combustivel_selecionado:
            exibir_mensagem(f"⚠️ Combustível {combustivel} não encontrado, continuando sem seleção")
        
        # PASSO 10: Configurar checkboxes
        exibir_mensagem("📱 TELA 6: Configurando checkboxes...")
        
        # PASSO 11: Configurar checkbox Kit Gas
        try:
            checkbox_kit_gas = page.locator('input[value="Kit Gás"]').first
            if checkbox_kit_gas.is_visible():
                if kit_gas and not checkbox_kit_gas.is_checked():
                    checkbox_kit_gas.check()
                    exibir_mensagem("✅ Checkbox Kit Gas: MARCADO")
                elif not kit_gas and checkbox_kit_gas.is_checked():
                    checkbox_kit_gas.uncheck()
                    exibir_mensagem("✅ Checkbox Kit Gas: DESMARCADO")
                else:
                    estado = "MARCADO" if kit_gas else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Kit Gas: {estado} (já estava correto)")
            else:
                exibir_mensagem("⚠️ Checkbox Kit Gas não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao configurar Kit Gas: {str(e)}")
        
        # PASSO 12: Configurar checkbox Blindado
        try:
            checkbox_blindado = page.locator('input[value="Blindado"]').first
            if checkbox_blindado.is_visible():
                if blindado and not checkbox_blindado.is_checked():
                    checkbox_blindado.check()
                    exibir_mensagem("✅ Checkbox Blindado: MARCADO")
                elif not blindado and checkbox_blindado.is_checked():
                    checkbox_blindado.uncheck()
                    exibir_mensagem("✅ Checkbox Blindado: DESMARCADO")
                else:
                    estado = "MARCADO" if blindado else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Blindado: {estado} (já estava correto)")
            else:
                exibir_mensagem("⚠️ Checkbox Blindado não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao configurar Blindado: {str(e)}")
        
        # PASSO 13: Configurar checkbox Financiado
        try:
            checkbox_financiado = page.locator('input[value="Financiado"]').first
            if checkbox_financiado.is_visible():
                if financiado and not checkbox_financiado.is_checked():
                    checkbox_financiado.check()
                    exibir_mensagem("✅ Checkbox Financiado: MARCADO")
                elif not financiado and checkbox_financiado.is_checked():
                    checkbox_financiado.uncheck()
                    exibir_mensagem("✅ Checkbox Financiado: DESMARCADO")
                else:
                    estado = "MARCADO" if financiado else "DESMARCADO"
                    exibir_mensagem(f"✅ Checkbox Financiado: {estado} (já estava correto)")
            else:
                exibir_mensagem("⚠️ Checkbox Financiado não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao configurar Financiado: {str(e)}")
        
        # PASSO 14: Clicar no botão "Continuar"
        botao_continuar.first.click()
        
        # PASSO 15: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 16: Aguardar transição
        time.sleep(3)
        
        # PASSO 17: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 18: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 6: {str(e)}")
        return False

def navegar_tela_7_playwright(page, cep):
    """
    TELA 7: Endereço de pernoite (CEP)
    
    DESCRIÇÃO:
        Preenche o campo CEP, aguarda carregamento do endereço e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Campo CEP: id=enderecoTelaEndereco
        - Sugestão de endereço: css=.overflow-hidden
        - Botão continuar: id=gtm-telaPernoiteVeiculoContinuar
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 7
        2. Localiza o campo CEP
        3. Preenche o CEP
        4. Aguarda carregamento do endereço baseado no CEP
        5. Clica no endereço sugerido
        6. Clica no botão "Continuar"
        7. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
        cep (str): CEP do endereço (ex: "03317-000")
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 7: Aguardando carregamento..."
        - "✅ Tela 7 carregada com sucesso"
        - "📱 TELA 7: Preenchendo CEP..."
        - "✅ CEP preenchido com sucesso"
        - "⏳ Aguardando carregamento do endereço..."
        - "✅ Endereço sugerido selecionado"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Tela 7 não carregou" (se falhar)
        - "❌ ERRO na Tela 7: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 7
        exibir_mensagem("📱 TELA 7: Aguardando carregamento...")
        
        # PASSO 2: Aguardar carregamento da Tela 7 (máximo 20 segundos)
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            campo_endereco = page.locator("#enderecoTelaEndereco")
            if campo_endereco.count() > 0 and campo_endereco.first.is_visible():
                break
            time.sleep(1)
            tentativa += 1
        
        # PASSO 3: Verificar se encontrou o campo
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Tela 7 não carregou")
            return False
        
        # PASSO 4: Confirmar carregamento
        exibir_mensagem("✅ Tela 7 carregada com sucesso")
        
        # PASSO 5: Preencher CEP
        exibir_mensagem("📱 TELA 7: Preenchendo CEP...")
        
        # PASSO 6: Preencher o CEP no campo
        campo_endereco.first.fill(cep)
        exibir_mensagem(f"✅ CEP preenchido: {cep}")
        time.sleep(1)
        
        # PASSO 7: Aguardar carregamento do endereço baseado no CEP (5 segundos)
        exibir_mensagem("⏳ Aguardando carregamento do endereço...")
        time.sleep(5)
        
        # PASSO 8: Tentar selecionar endereço sugerido
        try:
            sugestao_endereco = page.locator("css=.overflow-hidden").first
            if sugestao_endereco.is_visible():
                sugestao_endereco.click()
                exibir_mensagem("✅ Endereço sugerido selecionado")
                time.sleep(1)
            else:
                exibir_mensagem("⚠️ Endereço sugerido não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao selecionar endereço: {str(e)}")
        
        # PASSO 9: Localizar e clicar no botão "Continuar"
        botao_continuar = page.locator("#gtm-telaPernoiteVeiculoContinuar").first
        botao_continuar.click()
        
        # PASSO 10: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 11: Aguardar transição
        time.sleep(3)
        
        # PASSO 12: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 14: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 7: {str(e)}")
        return False

def navegar_tela_8_playwright(page, uso_veiculo):
    """
    TELA 8: Finalidade do veículo (Uso do veículo)
    
    DESCRIÇÃO:
        Seleciona o tipo de uso do veículo baseado no parâmetro e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS (baseado na gravação e Selenium):
        - Detecção da tela: XPATH com texto "finalidade", "Finalidade", "uso", "Uso", "veículo"
        - Botão continuar: id=gtm-telaUsoVeiculoContinuar
        - Radio buttons: Seleção baseada no parâmetro uso_veiculo
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 8
        2. Detecta elementos da tela usando XPATH
        3. Seleciona o tipo de uso baseado no parâmetro
        4. Clica no botão "Continuar"
        5. Aguarda transição
    
    PARÂMETROS:
        page: Objeto page do Playwright
        uso_veiculo (str): Tipo de uso do veículo ("Pessoal", "Profissional", "Motorista de aplicativo", "Taxi")
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "📱 TELA 8: Aguardando carregamento..."
        - "✅ Tela 8 carregada com sucesso"
        - "📱 TELA 8: Selecionando uso do veículo..."
        - "✅ Uso '{uso_veiculo}' selecionado com sucesso"
        - "✅ Botão 'Continuar' clicado com sucesso"
        - "❌ Tela 8 não carregou" (se falhar)
        - "❌ ERRO na Tela 8: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 8
        exibir_mensagem("📱 TELA 8: Aguardando carregamento...")
        
        # PASSO 2: Aguardar carregamento da Tela 8 (máximo 20 segundos)
        max_tentativas = 20
        tentativa = 0
        
        while tentativa < max_tentativas:
            # Procurar por elementos que indicam a Tela 8
            elementos_tela8 = page.locator("xpath=//*[contains(text(), 'finalidade') or contains(text(), 'Finalidade') or contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]")
            if elementos_tela8.count() > 0:
                break
            time.sleep(1)
            tentativa += 1
        
        # PASSO 3: Verificar se encontrou elementos da Tela 8
        if tentativa >= max_tentativas:
            exibir_mensagem("❌ Tela 8 não carregou")
            return False
        
        # PASSO 4: Confirmar carregamento
        exibir_mensagem("✅ Tela 8 carregada com sucesso")
        
        # PASSO 5: Selecionar uso do veículo
        exibir_mensagem(f"📱 TELA 8: Selecionando uso do veículo...")
        
        # PASSO 6: Selecionar o radio button baseado no parâmetro
        try:
            # Mapear uso_veiculo para os valores corretos dos radio buttons
            mapeamento_uso = {
                "Pessoal": "Particular",
                "Profissional": "Profissional", 
                "Motorista de aplicativo": "Motorista de App",
                "Motorista de App": "Motorista de App",
                "Taxi": "Taxi",
                "Táxi": "Taxi"  # Alternativa com acento
            }
            
            valor_radio = mapeamento_uso.get(uso_veiculo, uso_veiculo)
            
            # Localizar e clicar no radio button específico
            seletor_radio = f'input[value="{valor_radio}"][name="finalidadeVeiculoTelaUsoVeiculo"]'
            radio_button = page.locator(seletor_radio).first
            
            if radio_button.is_visible():
                radio_button.click()
                exibir_mensagem(f"✅ Uso '{uso_veiculo}' selecionado com sucesso (valor={valor_radio})")
            else:
                exibir_mensagem(f"⚠️ Radio button para '{uso_veiculo}' (valor={valor_radio}) não está visível")
                
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao selecionar uso do veículo: {str(e)}")
        
        # PASSO 7: Localizar e clicar no botão "Continuar"
        botao_continuar = page.locator("#gtm-telaUsoVeiculoContinuar").first
        botao_continuar.click()
        
        # PASSO 8: Confirmar clique
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 9: Aguardar transição
        time.sleep(3)
        
        # PASSO 10: Retornar sucesso
        return True
        
    except Exception as e:
        # PASSO 11: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 8: {str(e)}")
        return False

def navegar_tela_9_playwright(page, nome, cpf, data_nascimento, sexo, estado_civil, email, celular):
    """
    TELA 9: Dados pessoais do segurado
    
    DESCRIÇÃO:
        Preenche todos os campos de dados pessoais do segurado e clica em "Continuar"
    
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Nome: id=nomeTelaSegurado
        - CPF: id=cpfTelaSegurado
        - Data Nascimento: id=dataNascimentoTelaSegurado
        - Sexo: Dropdown MUI (seleção)
        - Estado Civil: Dropdown MUI (seleção)
        - Email: id=emailTelaSegurado
        - Celular: id=celularTelaSegurado
        - Botão continuar: id=gtm-telaDadosSeguradoContinuar
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 9
        2. Detecta elementos da tela usando XPATH
        3. Preenche todos os campos de entrada
        4. Seleciona sexo e estado civil via dropdowns
        5. Clica em "Continuar"
    
    PARÂMETROS:
        page: Página Playwright
        nome: Nome completo do segurado
        cpf: CPF do segurado
        data_nascimento: Data de nascimento
        sexo: Sexo (Masculino/Feminino)
        estado_civil: Estado civil
        email: Email do segurado
        celular: Celular do segurado
    
    RETORNO:
        bool: True se sucesso, False se falha
    """
    try:
        # PASSO 1: Aguardar carregamento da Tela 9
        exibir_mensagem("📱 TELA 9: Aguardando carregamento...")
        
        # Aguardar até 20 segundos para detectar elementos da tela
        for tentativa in range(20):
            try:
                # Detectar elementos da Tela 9 usando XPATH
                elementos_tela = page.locator("xpath=//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]")
                if elementos_tela.count() > 0:
                    exibir_mensagem("✅ Tela 9 carregada com sucesso")
                    break
            except:
                pass
            
            if tentativa == 19:
                exibir_mensagem("❌ ERRO: Tela 9 não foi detectada após 20 segundos")
                return False
            
            time.sleep(1)
        
        # PASSO 2: Preencher Nome Completo
        exibir_mensagem("📱 TELA 9: Preenchendo nome...")
        try:
            nome_campo = page.locator("#nomeTelaSegurado")
            nome_campo.click()
            nome_campo.fill(nome)
            exibir_mensagem(f"✅ Nome preenchido: {nome}")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao preencher nome: {str(e)}")
        
        # PASSO 3: Preencher CPF
        exibir_mensagem("📱 TELA 9: Preenchendo CPF...")
        try:
            cpf_campo = page.locator("#cpfTelaSegurado")
            cpf_campo.click()
            cpf_campo.fill(cpf)
            exibir_mensagem(f"✅ CPF preenchido: {cpf}")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao preencher CPF: {str(e)}")
        
        # PASSO 4: Preencher Data de Nascimento
        exibir_mensagem("📱 TELA 9: Preenchendo data de nascimento...")
        try:
            data_campo = page.locator("#dataNascimentoTelaSegurado")
            data_campo.click()
            data_campo.fill(data_nascimento)
            exibir_mensagem(f"✅ Data de nascimento preenchida: {data_nascimento}")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao preencher data de nascimento: {str(e)}")
        
        # PASSO 5: Selecionar Sexo
        exibir_mensagem("📱 TELA 9: Selecionando sexo...")
        try:
            # Localizar o campo de sexo
            campo_sexo = page.locator("#sexoTelaSegurado")
            if campo_sexo.is_visible():
                # Clicar no campo para abrir o dropdown
                campo_sexo.click()
                time.sleep(1)
                
                # Aguardar até 5 segundos para o dropdown aparecer
                for tentativa in range(5):
                    try:
                        # Procurar por elementos de lista que contenham o texto do sexo
                        opcoes_sexo = page.locator("xpath=//li[contains(text(), '" + sexo + "')]")
                        if opcoes_sexo.count() > 0:
                            opcoes_sexo.first.click()
                            exibir_mensagem(f"✅ Sexo selecionado: {sexo}")
                            break
                    except:
                        pass
                    
                    if tentativa == 4:
                        exibir_mensagem(f"⚠️ Sexo '{sexo}' não encontrado no dropdown")
                    
                    time.sleep(1)
            else:
                exibir_mensagem("⚠️ Campo de sexo não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao selecionar sexo: {str(e)}")
        
        # PASSO 6: Selecionar Estado Civil
        exibir_mensagem("📱 TELA 9: Selecionando estado civil...")
        try:
            # Localizar o campo de estado civil
            campo_estado_civil = page.locator("#estadoCivilTelaSegurado")
            if campo_estado_civil.is_visible():
                # Clicar no campo para abrir o dropdown
                campo_estado_civil.click()
                time.sleep(1)
                
                # Mapear estado civil do JSON para possíveis variações na tela
                mapeamento_estado_civil = {
                    "Casado ou Uniao Estavel": ["Casado ou União Estável", "Casado ou Uniao Estavel", "Casado ou União Estavel", "Casado ou Uniao Estável"],
                    "Solteiro": ["Solteiro", "Solteiro(a)"],
                    "Divorciado": ["Divorciado", "Divorciado(a)"],
                    "Viuvo": ["Viúvo", "Viuvo", "Viúvo(a)", "Viuvo(a)"],
                    "Separado": ["Separado", "Separado(a)"]
                }
                
                # Obter possíveis variações para o estado civil
                variacoes_estado_civil = mapeamento_estado_civil.get(estado_civil, [estado_civil])
                
                # Aguardar até 5 segundos para o dropdown aparecer
                estado_civil_selecionado = False
                for tentativa in range(5):
                    try:
                        # Tentar cada variação possível
                        for variacao in variacoes_estado_civil:
                            opcoes_estado_civil = page.locator("xpath=//li[contains(text(), '" + variacao + "')]")
                            if opcoes_estado_civil.count() > 0:
                                opcoes_estado_civil.first.click()
                                exibir_mensagem(f"✅ Estado civil selecionado: {estado_civil} (encontrado como '{variacao}')")
                                estado_civil_selecionado = True
                                break
                        
                        if estado_civil_selecionado:
                            break
                    except:
                        pass
                    
                    if tentativa == 4 and not estado_civil_selecionado:
                        exibir_mensagem(f"⚠️ Estado civil '{estado_civil}' não encontrado no dropdown (tentou: {', '.join(variacoes_estado_civil)})")
                    
                    time.sleep(1)
            else:
                exibir_mensagem("⚠️ Campo de estado civil não encontrado")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao selecionar estado civil: {str(e)}")
        
        # PASSO 7: Preencher Email
        exibir_mensagem("📱 TELA 9: Preenchendo email...")
        try:
            email_campo = page.locator("#emailTelaSegurado")
            email_campo.click()
            email_campo.fill(email)
            exibir_mensagem(f"✅ Email preenchido: {email}")
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao preencher email: {str(e)}")
        
        # PASSO 8: Preencher Celular
        exibir_mensagem("📱 TELA 9: Preenchendo celular...")
        try:
            celular_campo = page.locator("#celularTelaSegurado")
            celular_campo.click()
            
            # Limpar o campo primeiro
            celular_campo.clear()
            time.sleep(0.5)
            
            # Preencher caractere por caractere para evitar problemas com máscara
            for digito in celular:
                celular_campo.type(digito)
                time.sleep(0.1)
            
            # Aguardar um pouco para a máscara processar
            time.sleep(1)
            
            # Verificar se foi preenchido corretamente
            valor_preenchido = celular_campo.input_value()
            exibir_mensagem(f"✅ Celular preenchido: {celular} (valor no campo: {valor_preenchido})")
            
            if valor_preenchido != celular:
                exibir_mensagem(f"⚠️ ATENÇÃO: Valor no campo ({valor_preenchido}) diferente do esperado ({celular})")
                
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao preencher celular: {str(e)}")
        
        # PASSO 9: Clicar em "Continuar"
        exibir_mensagem("📱 TELA 9: Clicando em 'Continuar'...")
        try:
            botao_continuar = page.locator("#gtm-telaDadosSeguradoContinuar")
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            time.sleep(3)  # Aguardar transição
        except Exception as e:
            exibir_mensagem(f"⚠️ Erro ao clicar em 'Continuar': {str(e)}")
        
        exibir_mensagem("✅ TELA 9 CONCLUÍDA!")
        return True
        
    except Exception as e:
        # PASSO 10: Tratar exceções
        exibir_mensagem(f"❌ ERRO na Tela 9: {str(e)}")
        return False

def navegar_tela_10_playwright(page, condutor_principal, nome_condutor=None, cpf_condutor=None, data_nascimento_condutor=None, sexo_condutor=None, estado_civil_condutor=None):
    """
    TELA 10: Condutor principal
    
    DESCRIÇÃO:
        Navega para a Tela 10 e seleciona se será o condutor principal ou não.
        Se não for o condutor principal, preenche os dados do condutor.
    
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim: input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Radio Não: input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]
        - Botão Continuar: #gtm-telaCondutorPrincipalContinuar
        - Nome Condutor: #nomeTelaCondutorPrincipal (quando "Não" selecionado)
        - CPF Condutor: #cpfTelaCondutorPrincipal (quando "Não" selecionado)
        - Data Nascimento: #dataNascimentoTelaCondutorPrincipal (quando "Não" selecionado)
        - Sexo Condutor: #sexoTelaCondutorPrincipal (quando "Não" selecionado)
        - Estado Civil: #estadoCivilTelaCondutorPrincipal (quando "Não" selecionado)
    
    IMPLEMENTAÇÃO:
        1. Aguarda carregamento da Tela 10
        2. Seleciona radio button baseado no parâmetro condutor_principal
        3. Se "Não" selecionado, preenche campos adicionais do condutor
        4. Clica em "Continuar"
        5. Aguarda transição para próxima tela
    
    PARÂMETROS:
        page: Objeto page do Playwright
        condutor_principal: bool - True se será condutor principal, False se não
        nome_condutor: str - Nome do condutor (quando condutor_principal=False)
        cpf_condutor: str - CPF do condutor (quando condutor_principal=False)
        data_nascimento_condutor: str - Data de nascimento (quando condutor_principal=False)
        sexo_condutor: str - Sexo do condutor (quando condutor_principal=False)
        estado_civil_condutor: str - Estado civil do condutor (quando condutor_principal=False)
    
    RETORNO:
        bool: True se sucesso, False se falha
    
    LOGS ESPERADOS:
        - "👥 TELA 10: Condutor principal..."
        - "✅ Tela 10 carregada - condutor principal detectado!"
        - "⏳ Selecionando 'Sim' para condutor principal..."
        - "⏳ Selecionando 'Não' para não condutor principal..."
        - "⏳ Preenchendo dados do condutor..."
        - "✅ TELA 10 IMPLEMENTADA COM SUCESSO!"
        - "❌ ERRO na Tela 10: {erro}" (se exceção)
    """
    try:
        # PASSO 1: Exibir mensagem de início da Tela 10
        exibir_mensagem("👥 TELA 10: Condutor principal...")
        
        # PASSO 2: Aguardar carregamento da Tela 10
        # Aguardar o botão continuar da Tela 10 aparecer
        page.wait_for_selector("#gtm-telaCondutorPrincipalContinuar", timeout=20000)
        exibir_mensagem("✅ Tela 10 carregada - condutor principal detectado!")
        
        # PASSO 3: Aguardar estabilização da página
        time.sleep(2)
        
        # PASSO 4: Selecionar opção baseada no parâmetro condutor_principal
        if condutor_principal:
            # CENÁRIO 1: Selecionar "Sim" (Condutor Principal)
            exibir_mensagem("⏳ Selecionando 'Sim' para condutor principal...")
            
            # Localizar e clicar no radio button "Sim"
            radio_sim = page.locator('input[value="sim"][name="condutorPrincipalTelaCondutorPrincipal"]')
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("✅ Radio 'Sim' selecionado com sucesso")
            else:
                exibir_mensagem("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        else:
            # CENÁRIO 2: Selecionar "Não" (Não Condutor Principal)
            exibir_mensagem("⏳ Selecionando 'Não' para não condutor principal...")
            
            # Localizar e clicar no radio button "Não"
            radio_nao = page.locator('input[value="nao"][name="condutorPrincipalTelaCondutorPrincipal"]')
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("✅ Radio 'Não' selecionado com sucesso")
                
                # PASSO 5: Aguardar campos do condutor aparecerem
                time.sleep(2)
                
                # PASSO 6: Preencher campos do condutor
                exibir_mensagem("⏳ Preenchendo dados do condutor...")
                
                # Nome do condutor
                if nome_condutor:
                    nome_campo = page.locator("#nomeTelaCondutorPrincipal")
                    if nome_campo.is_visible():
                        nome_campo.fill(nome_condutor)
                        exibir_mensagem(f"✅ Nome do condutor preenchido: {nome_condutor}")
                    else:
                        exibir_mensagem("⚠️ Campo nome do condutor não encontrado")
                
                # CPF do condutor
                if cpf_condutor:
                    cpf_campo = page.locator("#cpfTelaCondutorPrincipal")
                    if cpf_campo.is_visible():
                        cpf_campo.fill(cpf_condutor)
                        exibir_mensagem(f"✅ CPF do condutor preenchido: {cpf_condutor}")
                    else:
                        exibir_mensagem("⚠️ Campo CPF do condutor não encontrado")
                
                # Data de nascimento do condutor
                if data_nascimento_condutor:
                    data_campo = page.locator("#dataNascimentoTelaCondutorPrincipal")
                    if data_campo.is_visible():
                        data_campo.fill(data_nascimento_condutor)
                        exibir_mensagem(f"✅ Data de nascimento do condutor preenchida: {data_nascimento_condutor}")
                    else:
                        exibir_mensagem("⚠️ Campo data de nascimento do condutor não encontrado")
                
                # Sexo do condutor (dropdown MUI)
                if sexo_condutor:
                    sexo_campo = page.locator("#sexoTelaCondutorPrincipal")
                    if sexo_campo.is_visible():
                        # Clicar no campo para abrir o dropdown
                        sexo_campo.click()
                        time.sleep(1)
                        
                        # Aguardar a lista aparecer e clicar na opção
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            opcao_sexo = page.locator(f'xpath=//li[contains(text(), "{sexo_condutor}")]')
                            if opcao_sexo.is_visible():
                                opcao_sexo.click()
                                exibir_mensagem(f"✅ Sexo do condutor selecionado: {sexo_condutor}")
                            else:
                                exibir_mensagem(f"⚠️ Opção de sexo '{sexo_condutor}' não encontrada")
                        except:
                            exibir_mensagem("⚠️ Erro ao selecionar sexo do condutor")
                    else:
                        exibir_mensagem("⚠️ Campo sexo do condutor não encontrado")
                
                # Estado civil do condutor (dropdown MUI)
                if estado_civil_condutor:
                    estado_civil_campo = page.locator("#estadoCivilTelaCondutorPrincipal")
                    if estado_civil_campo.is_visible():
                        # Clicar no campo para abrir o dropdown
                        estado_civil_campo.click()
                        time.sleep(1)
                        
                        # Aguardar a lista aparecer e clicar na opção
                        try:
                            page.wait_for_selector("ul", timeout=5000)
                            
                            # Mapeamento para variações de acento
                            mapeamento_estado_civil = {
                                "Casado ou Uniao Estavel": "Casado ou União Estável"
                            }
                            
                            texto_busca = mapeamento_estado_civil.get(estado_civil_condutor, estado_civil_condutor)
                            opcao_estado_civil = page.locator(f'xpath=//li[contains(text(), "{texto_busca}")]')
                            
                            if opcao_estado_civil.is_visible():
                                opcao_estado_civil.click()
                                exibir_mensagem(f"✅ Estado civil do condutor selecionado: {estado_civil_condutor}")
                            else:
                                exibir_mensagem(f"⚠️ Opção de estado civil '{estado_civil_condutor}' não encontrada")
                        except:
                            exibir_mensagem("⚠️ Erro ao selecionar estado civil do condutor")
                    else:
                        exibir_mensagem("⚠️ Campo estado civil do condutor não encontrado")
            else:
                exibir_mensagem("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # PASSO 7: Aguardar estabilização após seleção
        time.sleep(2)
        
        # PASSO 8: Clicar em "Continuar"
        exibir_mensagem("⏳ Clicando em 'Continuar'...")
        
        botao_continuar = page.locator("#gtm-telaCondutorPrincipalContinuar")
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
            
            # PASSO 9: Aguardar transição para próxima tela
            time.sleep(3)
            
            # PASSO 10: Confirmar sucesso
            exibir_mensagem("✅ TELA 10 IMPLEMENTADA COM SUCESSO!")
            return True
        else:
            exibir_mensagem("❌ Botão 'Continuar' não encontrado")
            return False
            
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 10: {str(e)}")
        return False

def navegar_tela_11_playwright(page, local_de_trabalho, estacionamento_proprio_local_de_trabalho, local_de_estudo, estacionamento_proprio_local_de_estudo):
    """
    TELA 11: Atividade do veículo
    
    DESCRIÇÃO:
        Navega para a Tela 11 e seleciona se o veículo é utilizado para ir ao local de trabalho e/ou estudo.
        Se selecionar local de trabalho, aparece checkbox de estacionamento próprio do trabalho.
        Se selecionar local de estudo, aparece checkbox de estacionamento próprio do estudo.
        
    ELEMENTOS IDENTIFICADOS:
        - Checkbox Local de Trabalho: input[type="checkbox"][value="trabalho"]
        - Checkbox Local de Estudo: input[type="checkbox"][value="estudo"]
        - Checkbox Estacionamento Local de Trabalho: input[type="checkbox"][data-gtm-form-interact-field-id="10"]
        - Checkbox Estacionamento Local de Estudo: input[type="checkbox"][data-gtm-form-interact-field-id="11"]
        - Botão Continuar: #gtm-telaAtividadeVeiculoContinuar
        
    PARÂMETROS:
        - local_de_trabalho: bool - Se o veículo é usado para ir ao trabalho
        - estacionamento_proprio_local_de_trabalho: bool - Se há estacionamento próprio no trabalho
        - local_de_estudo: bool - Se o veículo é usado para ir ao estudo
        - estacionamento_proprio_local_de_estudo: bool - Se há estacionamento próprio no estudo
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🎯 TELA 11: ATIVIDADE DO VEÍCULO")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 11
        exibir_mensagem("⏳ Aguardando carregamento da Tela 11...")
        page.wait_for_selector("#gtm-telaAtividadeVeiculoContinuar", timeout=10000)
        time.sleep(2)  # Aguarda estabilização
        
        exibir_mensagem("✅ Tela 11 carregada - atividade do veículo detectada!")
        
        # PASSO 1: Seleciona checkbox Local de Trabalho se necessário
        if local_de_trabalho:
            exibir_mensagem("📋 Marcando checkbox 'Local de Trabalho'...")
            checkbox_trabalho = page.locator('input[type="checkbox"][value="trabalho"]')
            if not checkbox_trabalho.is_checked():
                checkbox_trabalho.check()
                exibir_mensagem("✅ Checkbox 'Local de Trabalho' marcado!")
                time.sleep(1)  # Aguarda aparecimento do checkbox de estacionamento
            else:
                exibir_mensagem("ℹ️ Checkbox 'Local de Trabalho' já estava marcado")
        else:
            exibir_mensagem("ℹ️ Local de Trabalho: Não selecionado")
        
        # PASSO 2: Seleciona checkbox Local de Estudo se necessário
        if local_de_estudo:
            exibir_mensagem("📋 Marcando checkbox 'Local de Estudo'...")
            checkbox_estudo = page.locator('input[type="checkbox"][value="estudo"]')
            if not checkbox_estudo.is_checked():
                checkbox_estudo.check()
                exibir_mensagem("✅ Checkbox 'Local de Estudo' marcado!")
                time.sleep(1)  # Aguarda aparecimento do checkbox de estacionamento
            else:
                exibir_mensagem("ℹ️ Checkbox 'Local de Estudo' já estava marcado")
        else:
            exibir_mensagem("ℹ️ Local de Estudo: Não selecionado")
        
        # PASSO 3: Configurar estacionamento do trabalho (se local_de_trabalho = true)
        if local_de_trabalho:
            exibir_mensagem("🅿️ Configurando estacionamento do trabalho...")
            try:
                checkbox_estacionamento_trabalho = page.locator('input[type="checkbox"][data-gtm-form-interact-field-id="10"]')
                if checkbox_estacionamento_trabalho.is_visible():
                    if estacionamento_proprio_local_de_trabalho and not checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.check()
                        exibir_mensagem("✅ Estacionamento próprio do trabalho: MARCADO")
                    elif not estacionamento_proprio_local_de_trabalho and checkbox_estacionamento_trabalho.is_checked():
                        checkbox_estacionamento_trabalho.uncheck()
                        exibir_mensagem("✅ Estacionamento próprio do trabalho: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_trabalho else "DESMARCADO"
                        exibir_mensagem(f"✅ Estacionamento próprio do trabalho: {estado} (já estava correto)")
                else:
                    exibir_mensagem("⚠️ Checkbox estacionamento do trabalho não encontrado")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao configurar estacionamento do trabalho: {str(e)}")
        
        # PASSO 4: Configurar estacionamento do estudo (se local_de_estudo = true)
        if local_de_estudo:
            exibir_mensagem("🅿️ Configurando estacionamento do estudo...")
            try:
                checkbox_estacionamento_estudo = page.locator('input[type="checkbox"][data-gtm-form-interact-field-id="11"]')
                if checkbox_estacionamento_estudo.is_visible():
                    if estacionamento_proprio_local_de_estudo and not checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.check()
                        exibir_mensagem("✅ Estacionamento próprio do estudo: MARCADO")
                    elif not estacionamento_proprio_local_de_estudo and checkbox_estacionamento_estudo.is_checked():
                        checkbox_estacionamento_estudo.uncheck()
                        exibir_mensagem("✅ Estacionamento próprio do estudo: DESMARCADO")
                    else:
                        estado = "MARCADO" if estacionamento_proprio_local_de_estudo else "DESMARCADO"
                        exibir_mensagem(f"✅ Estacionamento próprio do estudo: {estado} (já estava correto)")
                else:
                    exibir_mensagem("⚠️ Checkbox estacionamento do estudo não encontrado")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao configurar estacionamento do estudo: {str(e)}")
        
        # PASSO 5: Aguardar estabilização após todas as configurações
        time.sleep(2)
        
        # PASSO 6: Clica no botão Continuar
        exibir_mensagem("🔄 Clicando em 'Continuar'...")
        botao_continuar = page.locator("#gtm-telaAtividadeVeiculoContinuar")
        botao_continuar.click()
        
        # PASSO 7: Aguarda navegação
        time.sleep(2)
        exibir_mensagem("✅ Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 11: {str(e)}")
        return False

def navegar_tela_12_playwright(page, garagem_residencia, portao_eletronico):
    """
    TELA 12: Garagem na Residência
    
    DESCRIÇÃO:
        Navega para a Tela 12 e seleciona se possui garagem na residência e tipo de portão.
        
    ELEMENTOS IDENTIFICADOS:
        - Radio Sim: input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Não: input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]
        - Radio Eletrônico: input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]
        - Radio Manual: input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer (texto "Continuar")
        
    PARÂMETROS:
        - garagem_residencia: bool - Se possui garagem na residência
        - portao_eletronico: str - Tipo de portão ("Eletronico", "Manual", "Não possui")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🏠 TELA 12: GARAGEM NA RESIDÊNCIA")
        exibir_mensagem("="*50)
        
        # Aguarda o carregamento da Tela 12
        exibir_mensagem("⏳ Aguardando carregamento da Tela 12...")
        page.wait_for_selector('p.font-semibold.font-workSans.cursor-pointer', timeout=10000)
        time.sleep(2)  # Aguarda estabilização
        
        exibir_mensagem("✅ Tela 12 carregada - garagem na residência detectada!")
        
        # Seleciona Sim ou Não para garagem
        if garagem_residencia:
            exibir_mensagem("📋 Selecionando 'Sim' para garagem na residência...")
            
            # Localizar e clicar no radio button "Sim"
            radio_sim = page.locator('input[value="sim"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_sim.is_visible():
                radio_sim.click()
                exibir_mensagem("✅ Radio 'Sim' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("⚠️ Radio 'Sim' para garagem não encontrado")
                return False
            
            # Aguarda campo de portão aparecer
            exibir_mensagem("⏳ Aguardando campo de portão aparecer...")
            time.sleep(2)
            
            # Seleciona tipo de portão
            if portao_eletronico == "Eletronico":
                exibir_mensagem("📋 Selecionando 'Eletrônico' para portão...")
                
                radio_eletronico = page.locator('input[value="eletronico"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_eletronico.is_visible():
                    radio_eletronico.click()
                    exibir_mensagem("✅ Radio 'Eletrônico' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("⚠️ Radio 'Eletrônico' para portão não encontrado")
                    return False
                    
            elif portao_eletronico == "Manual":
                exibir_mensagem("📋 Selecionando 'Manual' para portão...")
                
                radio_manual = page.locator('input[value="manual"][name="tipoPortaoTelaGaragemResidencia"]')
                if radio_manual.is_visible():
                    radio_manual.click()
                    exibir_mensagem("✅ Radio 'Manual' para portão selecionado com sucesso")
                else:
                    exibir_mensagem("⚠️ Radio 'Manual' para portão não encontrado")
                    return False
            else:
                exibir_mensagem("ℹ️ Tipo de portão: Não possui")
        else:
            exibir_mensagem("📋 Selecionando 'Não' para garagem na residência...")
            
            # Localizar e clicar no radio button "Não"
            radio_nao = page.locator('input[value="nao"][name="possuiGaragemTelaGaragemResidencia"]')
            if radio_nao.is_visible():
                radio_nao.click()
                exibir_mensagem("✅ Radio 'Não' para garagem selecionado com sucesso")
            else:
                exibir_mensagem("⚠️ Radio 'Não' para garagem não encontrado")
                return False
        
        # Aguarda estabilização após seleções
        time.sleep(2)
        
        # Clica no botão Continuar
        exibir_mensagem("🔄 Clicando em 'Continuar'...")
        botao_continuar = page.locator('p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")')
        if botao_continuar.is_visible():
            botao_continuar.click()
            exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        else:
            exibir_mensagem("⚠️ Botão 'Continuar' não encontrado")
            return False
        
        # Aguarda navegação
        time.sleep(2)
        exibir_mensagem("✅ Navegação para próxima tela realizada!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 12: {str(e)}")
        return False


def navegar_tela_13_playwright(page, reside_18_26, sexo_do_menor, faixa_etaria_menor_mais_novo):
    """
    TELA 13: Residência com Menores de 18-26 anos
    
    DESCRIÇÃO:
        Navega para a Tela 13 e seleciona se reside com alguém entre 18 e 26 anos.
        Se sim, seleciona o sexo e faixa etária do mais novo.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Radio principal: Você reside com alguém entre 18 e 26 anos?
            - Não
            - Sim, mas não utilizam o veículo
            - Sim e utilizam o veículo
        - Radio condicional Sexo (só aparece se "Sim e utilizam o veículo"):
            - Feminino
            - Masculino
            - Ambos
        - Radio condicional Faixa etária (só aparece se "Sim e utilizam o veículo"):
            - 18 a 24 anos
            - 25 anos
        - Botão Continuar: p.font-semibold.font-workSans.cursor-pointer:has-text("Continuar")
        
    PARÂMETROS:
        - reside_18_26: str - Resposta principal ("Não", "Sim, mas não utilizam o veículo", "Sim e utilizam o veículo")
        - sexo_do_menor: str - Sexo do menor ("Feminino", "Masculino", "Ambos", "N/A")
        - faixa_etaria_menor_mais_novo: str - Faixa etária ("18 a 24 anos", "25 anos", "N/A")
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("👥 TELA 13: RESIDÊNCIA COM MENORES DE 18-26 ANOS")
        exibir_mensagem("="*50)
        
        # PASSO 1: Aguardar carregamento da tela
        exibir_mensagem("⏳ Aguardando carregamento da Tela 13...")
        page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=10000)
        exibir_mensagem("✅ Tela 13 carregada - residência com menores detectada!")
        
        # PASSO 2: Selecionar resposta principal
        exibir_mensagem(f"👥 Selecionando resposta principal: '{reside_18_26}'...")
        
        # Mapear valores para os selectors da gravação
        if reside_18_26 == "Não":
            # Selecionar "Não"
            page.locator("input[type='radio'][value='nao']").first.check()
            exibir_mensagem("✅ Radio 'Não' selecionado com sucesso")
            
        elif reside_18_26 == "Sim, mas não utilizam o veículo":
            # Selecionar "Sim, mas não utilizam o veículo"
            page.locator("input[type='radio'][value='sim_nao_utilizam']").check()
            exibir_mensagem("✅ Radio 'Sim, mas não utilizam o veículo' selecionado com sucesso")
            
        elif reside_18_26 == "Sim e utilizam o veículo":
            # Selecionar "Sim e utilizam o veículo"
            page.locator("input[type='radio'][value='sim_utilizam']").check()
            exibir_mensagem("✅ Radio 'Sim e utilizam o veículo' selecionado com sucesso")
            
            # PASSO 3: Se "Sim e utilizam o veículo", selecionar campos condicionais
            if sexo_do_menor != "N/A":
                exibir_mensagem(f"👤 Selecionando sexo do menor: '{sexo_do_menor}'...")
                
                if sexo_do_menor == "Feminino":
                    page.locator("input[type='radio'][value='feminino']").check()
                    exibir_mensagem("✅ Radio 'Feminino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Masculino":
                    page.locator("input[type='radio'][value='masculino']").check()
                    exibir_mensagem("✅ Radio 'Masculino' para sexo selecionado com sucesso")
                elif sexo_do_menor == "Ambos":
                    page.locator("input[type='radio'][value='ambos']").check()
                    exibir_mensagem("✅ Radio 'Ambos' para sexo selecionado com sucesso")
            
            if faixa_etaria_menor_mais_novo != "N/A":
                exibir_mensagem(f"📅 Selecionando faixa etária: '{faixa_etaria_menor_mais_novo}'...")
                
                if faixa_etaria_menor_mais_novo == "18 a 24 anos":
                    page.locator("input[type='radio'][value='18_24']").check()
                    exibir_mensagem("✅ Radio '18 a 24 anos' para faixa etária selecionado com sucesso")
                elif faixa_etaria_menor_mais_novo == "25 anos":
                    page.locator("input[type='radio'][value='25']").check()
                    exibir_mensagem("✅ Radio '25 anos' para faixa etária selecionado com sucesso")
        else:
            exibir_mensagem("⚠️ Resposta não reconhecida, usando 'Não'")
            page.locator("input[type='radio'][value='nao']").first.check()
        
        # PASSO 4: Clicar no botão Continuar
        exibir_mensagem("⏳ Aguardando botão 'Continuar'...")
        page.wait_for_selector("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')", timeout=5000)
        
        exibir_mensagem("🔄 Clicando no botão 'Continuar'...")
        page.locator("p.font-semibold.font-workSans.cursor-pointer:has-text('Continuar')").click()
        exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
        
        # PASSO 5: Aguardar transição para próxima tela
        exibir_mensagem("⏳ Aguardando transição para próxima tela...")
        time.sleep(2)
        exibir_mensagem("✅ TELA 13 CONCLUÍDA!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 13: {str(e)}")
        return False

def navegar_tela_14_playwright(page, continuar_com_corretor_anterior):
    """
    TELA 14: Corretor Anterior (CONDICIONAL)
    
    DESCRIÇÃO:
        Tela condicional que só aparece quando já existe uma cotação para o cliente.
        Pergunta se deseja continuar com o corretor anterior ou não.
        
    ELEMENTOS IDENTIFICADOS (baseado na gravação):
        - Botão Continuar: id=gtm-telaCorretorAnteriorContinuar
        - Elementos de seleção: css=.flex > .min-h-\[39rem\] .mb-6 > .flex > .flex > .text-primary
        - Checkbox/Radio: css=.flex > .md\3Aw-80 > div:nth-child(2) > .flex > .flex .text-primary:nth-child(1)
        
    CARACTERÍSTICAS IMPORTANTES:
        - Tela condicional: Só aparece quando já existe uma cotação para o cliente
        - Lógica de detecção: Precisa verificar se a tela aparece antes de processar
        - Elementos simples: Parece ser uma tela de confirmação/opção
        
    PARÂMETROS:
        - continuar_com_corretor_anterior: bool - Se deve continuar com o corretor anterior
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("👨‍💼 TELA 14: CORRETOR ANTERIOR (CONDICIONAL)")
        exibir_mensagem("="*50)
        
        # PASSO 1: Verificar se a Tela 14 aparece (é condicional)
        exibir_mensagem("🔍 Verificando se a Tela 14 (Corretor Anterior) aparece...")
        
        # Aguardar um tempo para ver se a tela aparece
        time.sleep(3)
        
        # Tentar localizar elementos da Tela 14
        try:
            # Tentar encontrar o botão da Tela 14
            botao_tela14 = page.locator("#gtm-telaCorretorAnteriorContinuar")
            if botao_tela14.count() > 0 and botao_tela14.first.is_visible():
                exibir_mensagem("✅ Tela 14 detectada - Corretor Anterior aparece!")
                
                # PASSO 2: Processar a Tela 14
                exibir_mensagem(f"👨‍💼 Processando Tela 14: continuar_com_corretor_anterior = {continuar_com_corretor_anterior}")
                
                # Selecionar opção baseada no parâmetro
                if continuar_com_corretor_anterior:
                    exibir_mensagem("✅ Selecionando 'Continuar com corretor anterior'...")
                    # Tentar seletores mais simples e robustos
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Continuar com corretor anterior").first.click()
                        exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='sim']").first.click()
                            exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Continuar')").first.click()
                            exibir_mensagem("✅ Opção 'Continuar com corretor anterior' selecionada por label")
                else:
                    exibir_mensagem("✅ Selecionando 'Não continuar com corretor anterior'...")
                    try:
                        # Primeiro tentar por texto
                        page.locator("text=Não continuar com corretor anterior").first.click()
                        exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por texto")
                    except:
                        try:
                            # Tentar por radio button
                            page.locator("input[type='radio'][value='nao']").first.click()
                            exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por radio")
                        except:
                            # Tentar por label
                            page.locator("label:has-text('Não')").first.click()
                            exibir_mensagem("✅ Opção 'Não continuar com corretor anterior' selecionada por label")
                
                # PASSO 3: Clicar no botão Continuar
                exibir_mensagem("🔄 Clicando no botão 'Continuar'...")
                botao_continuar = page.locator('p.font-semibold.font-workSans.cursor-pointer.text-sm.leading-6:has-text("Continuar")')
                if botao_continuar.is_visible():
                    botao_continuar.click()
                    exibir_mensagem("✅ Botão 'Continuar' clicado com sucesso")
                else:
                    exibir_mensagem("⚠️ Botão 'Continuar' não encontrado")
                    return False
                
                # PASSO 4: Aguardar transição para próxima tela
                exibir_mensagem("⏳ Aguardando transição para próxima tela...")
                time.sleep(2)
                exibir_mensagem("✅ TELA 14 CONCLUÍDA!")
                
                return True
            else:
                exibir_mensagem("ℹ️ Tela 14 não aparece - não há cotação anterior para este cliente")
                exibir_mensagem("ℹ️ Pulando para próxima tela...")
                return True  # Retorna True mesmo não aparecendo, pois é condicional
                
        except Exception as e:
            exibir_mensagem(f"ℹ️ Tela 14 não detectada: {str(e)}")
            exibir_mensagem("ℹ️ Pulando para próxima tela...")
            return True  # Retorna True mesmo não aparecendo, pois é condicional
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 14: {str(e)}")
        return False


def navegar_tela_15_playwright(page, email_login, senha_login):
    """
    TELA 15: Resultado Final (DUAS FASES)
    
    DESCRIÇÃO:
        Implementa as duas fases da Tela 15:
        FASE 1: Mapa + Timer regressivo (2:43 minutos)
        FASE 2: Tela de cálculo + Modal de login + Modal CPF divergente
        
    ELEMENTOS IDENTIFICADOS:
        FASE 1:
        - Modal timer: text=Por favor, aguarde. Estamos buscando o corretor ideal para você!
        - Timer: text=Tempo estimado em 02:43
        
        FASE 2:
        - Modal login: MuiBackdrop-root
        - Email: #emailTelaLogin
        - Senha: #senhaTelaLogin
        - Botão Acessar: #gtm-telaLoginBotaoAcessar
        - Modal CPF divergente: text=CPF informado não corresponde à conta
        - Botão "Logar com outra conta": #logarComOutraContaModalAssociarUsuario
        
    PARÂMETROS:
        page: Objeto page do Playwright
        email_login: Email para login
        senha_login: Senha para login
        
    RETORNO:
        bool: True se sucesso, False se falha
    """
    try:
        exibir_mensagem("\n" + "="*50)
        exibir_mensagem("🎯 TELA 15: RESULTADO FINAL (DUAS FASES)")
        exibir_mensagem("="*50)
        
        # ========================================
        # FASE 1: MAPA + TIMER REGRESSIVO
        # ========================================
        exibir_mensagem("🔄 FASE 1: Aguardando mapa e timer regressivo...")
        
        # PASSO 1: Aguardar modal com timer aparecer
        exibir_mensagem("⏳ Aguardando modal com timer...")
        
        try:
            # Aguardar até 30 segundos para o modal aparecer
            modal_timer = page.locator("text=Por favor, aguarde. Estamos buscando o corretor ideal para você!")
            modal_timer.wait_for(timeout=30000)
            exibir_mensagem("✅ Modal com timer detectado!")
        except Exception as e:
            exibir_mensagem(f"⚠️ Modal com timer não detectado: {str(e)}")
            exibir_mensagem("ℹ️ Continuando para Fase 2...")
        
        # PASSO 2: Aguardar timer regressivo (aproximadamente 2:43 minutos)
        exibir_mensagem("⏳ Aguardando timer regressivo (2:43 minutos)...")
        
        # Aguardar aproximadamente 2:43 minutos (163 segundos)
        tempo_timer = 163
        tempo_inicio_timer = time.time()
        
        while (time.time() - tempo_inicio_timer) < tempo_timer:
            try:
                # Verificar se ainda está no timer
                timer_atual = page.locator("text=Tempo estimado em")
                if timer_atual.count() > 0:
                    tempo_decorrido = int(time.time() - tempo_inicio_timer)
                    tempo_restante = tempo_timer - tempo_decorrido
                    exibir_mensagem(f"⏳ Timer em andamento... ({tempo_restante}s restantes)")
                else:
                    exibir_mensagem("✅ Timer concluído!")
                    break
            except:
                pass
            
            time.sleep(10)  # Verificar a cada 10 segundos
        
        exibir_mensagem("✅ FASE 1 CONCLUÍDA!")
        
        # ========================================
        # FASE 2: TELA DE CÁLCULO + MODAL LOGIN
        # ========================================
        exibir_mensagem("🔄 FASE 2: Aguardando tela de cálculo e modal de login...")
        
        # PASSO 3: Aguardar tela de cálculo aparecer
        exibir_mensagem("⏳ Aguardando tela de cálculo...")
        time.sleep(5)
        
        # PASSO 4: Aguardar modal de login aparecer
        exibir_mensagem("⏳ Aguardando modal de login...")
        
        try:
            # Aguardar até 30 segundos para o modal de login aparecer
            modal_login = page.locator("text=Acesse sua conta para visualizar o resultado final")
            modal_login.wait_for(timeout=30000)
            exibir_mensagem("✅ Modal de login detectado!")
        except Exception as e:
            exibir_mensagem(f"⚠️ Modal de login não detectado: {str(e)}")
            return False
        
        # PASSO 5: Preencher email
        exibir_mensagem("📧 Preenchendo email...")
        
        try:
            campo_email = page.locator("#emailTelaLogin")
            campo_email.fill(email_login)
            exibir_mensagem(f"✅ Email preenchido: {email_login}")
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao preencher email: {str(e)}")
            return False
        
        # PASSO 6: Preencher senha
        exibir_mensagem("🔒 Preenchendo senha...")
        
        try:
            campo_senha = page.locator("#senhaTelaLogin")
            campo_senha.fill(senha_login)
            exibir_mensagem("✅ Senha preenchida")
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao preencher senha: {str(e)}")
            return False
        
        # PASSO 7: CAPTURA DE TELA E LOGS DETALHADOS DO MODAL
        exibir_mensagem("📸 CAPTURANDO TELA DO MODAL DE LOGIN...")
        
        try:
            # Capturar screenshot do modal
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            screenshot_path = f"modal_login_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            exibir_mensagem(f"📸 Screenshot salvo: {screenshot_path}")
            
            # Verificar se os campos estão realmente preenchidos
            valor_email_campo = campo_email.input_value()
            valor_senha_campo = campo_senha.input_value()
            
            exibir_mensagem(f"🔍 VERIFICAÇÃO DOS CAMPOS:")
            exibir_mensagem(f"   📧 Email no campo: '{valor_email_campo}'")
            exibir_mensagem(f"   🔒 Senha no campo: '{valor_senha_campo}'")
            exibir_mensagem(f"   📧 Email esperado: '{email_login}'")
            exibir_mensagem(f"   🔒 Senha esperada: '{senha_login}'")
            
            # Verificar se os campos estão corretos
            if valor_email_campo == email_login:
                exibir_mensagem("✅ Email preenchido corretamente!")
            else:
                exibir_mensagem("❌ Email NÃO foi preenchido corretamente!")
            
            if valor_senha_campo == senha_login:
                exibir_mensagem("✅ Senha preenchida corretamente!")
            else:
                exibir_mensagem("❌ Senha NÃO foi preenchida corretamente!")
            
            # Verificar se o botão "Acessar" está visível
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            if botao_acessar.is_visible():
                exibir_mensagem("✅ Botão 'Acessar' está visível e pronto para clicar!")
                texto_botao = botao_acessar.text_content()
                exibir_mensagem(f"   📝 Texto do botão: '{texto_botao}'")
            else:
                exibir_mensagem("❌ Botão 'Acessar' NÃO está visível!")
            
            # Verificar se o modal está realmente presente
            modal_presente = page.locator("text=Acesse sua conta para visualizar o resultado final")
            if modal_presente.count() > 0:
                exibir_mensagem("✅ Modal de login está presente na tela!")
            else:
                exibir_mensagem("❌ Modal de login NÃO está presente na tela!")
            
            # Capturar HTML do modal para debug
            try:
                modal_html = page.locator(".MuiBackdrop-root").inner_html()
                exibir_mensagem(f"🔍 HTML do modal capturado (primeiros 200 chars): {modal_html[:200]}...")
            except Exception as e:
                exibir_mensagem(f"⚠️ Erro ao capturar HTML do modal: {str(e)}")
            
        except Exception as e:
            exibir_mensagem(f"❌ Erro durante captura de tela/logs: {str(e)}")
        
        # PASSO 8: Clicar em "Acessar"
        exibir_mensagem("🔄 Clicando em 'Acessar'...")
        
        try:
            botao_acessar = page.locator("#gtm-telaLoginBotaoAcessar")
            if botao_acessar.is_visible():
                botao_acessar.click()
                exibir_mensagem("✅ Botão 'Acessar' clicado com sucesso!")
                
                # Aguardar possível redirecionamento ou modal CPF divergente
                exibir_mensagem("⏳ Aguardando resposta do login...")
                time.sleep(5)
                
                # Verificar se apareceu modal CPF divergente
                try:
                    modal_cpf = page.locator("text=CPF informado não corresponde à conta")
                    if modal_cpf.count() > 0:
                        exibir_mensagem("✅ Modal CPF divergente detectado!")
                        
                        # Clicar no botão "Manter Login atual"
                        try:
                            exibir_mensagem("🔍 Procurando botão 'Manter Login atual'...")
                            
                            # Tentar pelo ID específico
                            botao_manter_login = page.locator("#manterLoginAtualModalAssociarUsuario")
                            if botao_manter_login.is_visible():
                                botao_manter_login.click()
                                exibir_mensagem("✅ Botão 'Manter Login atual' clicado pelo ID!")
                                time.sleep(3)
                            else:
                                # Tentar pelo texto
                                botao_manter_login = page.locator("text=Manter Login atual")
                                if botao_manter_login.is_visible():
                                    botao_manter_login.click()
                                    exibir_mensagem("✅ Botão 'Manter Login atual' clicado pelo texto!")
                                    time.sleep(3)
                                else:
                                    exibir_mensagem("⚠️ Botão 'Manter Login atual' não encontrado")
                        except Exception as e:
                            exibir_mensagem(f"⚠️ Erro ao clicar no botão 'Manter Login atual': {str(e)}")
                    else:
                        exibir_mensagem("ℹ️ Modal CPF divergente não apareceu - login pode ter sido bem-sucedido")
                except Exception as e:
                    exibir_mensagem(f"⚠️ Erro ao verificar modal CPF: {str(e)}")
                
            else:
                exibir_mensagem("❌ Botão 'Acessar' não está visível!")
                return False
        except Exception as e:
            exibir_mensagem(f"❌ Erro ao clicar em 'Acessar': {str(e)}")
            return False
        
        exibir_mensagem("✅ LOGIN CONCLUÍDO!")
        
        # ========================================
        # CAPTURA DE DADOS DOS PLANOS DE SEGURO
        # ========================================
        exibir_mensagem("📊 INICIANDO CAPTURA DE DADOS DOS PLANOS...")
        
        # Aguardar carregamento dos planos
        time.sleep(5)
        
        # Capturar dados dos planos
        dados_planos = capturar_dados_planos_seguro(page)
        
        if dados_planos:
            exibir_mensagem("✅ DADOS DOS PLANOS CAPTURADOS COM SUCESSO!")
            exibir_mensagem("📋 RESUMO DOS DADOS CAPTURADOS:")
            exibir_mensagem(f"   📊 Plano Recomendado: {dados_planos['plano_recomendado'].get('valor', 'N/A')}")
            exibir_mensagem(f"   📊 Plano Alternativo: {dados_planos['plano_alternativo'].get('valor', 'N/A')}")
        else:
            exibir_mensagem("⚠️ FALHA NA CAPTURA DE DADOS DOS PLANOS")
        
        exibir_mensagem("🎯 TELA 15 FINALIZADA COM SUCESSO!")
        
        return True
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na Tela 15: {str(e)}")
        return False

def capturar_dados_planos_seguro(page):
    """
    CAPTURA DADOS DOS PLANOS DE SEGURO
    
    DESCRIÇÃO:
        Captura os dados dos planos de seguro (Recomendado e Alternativo) na Tela 15.
        Extrai valores, características e coberturas de cada plano.
        
    ELEMENTOS IDENTIFICADOS:
        PLANO RECOMENDADO (Primeira Coluna):
        - Label: label.font-workSans.font-semibold (texto "Plano recomendado")
        - Valor do Seguro: p.md\\:font-bold (texto "R$ 2.516,60")
        - Forma de Pagamento: label.text-primary.text-xs.font-normal.mb-2 (texto "anual")
        - Parcelamento: div.text-primary.text-xs.font-bold (texto "Crédito em até 1x...")
        - Valor da Franquia: p.md\\:font-bold (texto "R$ 2.516,60")
        - Valor de Mercado: p.mb-1 (texto "100% da tabela FIPE")
        - Assistência: img[src="/icone-ok.svg"] (verificar se existe)
        - Vidros: img[src="/icone-ok.svg"] (verificar se existe)
        - Carro Reserva: img[src="/icone-ok.svg"] (verificar se existe)
        - Danos Materiais: div.items-center.justify-center.flex.flex-col.md\\:flex-row (texto "R$ 50.000,00")
        - Danos Corporais: div.items-center.justify-center.flex.flex-col.md\\:flex-row (texto "R$ 50.000,00")
        - Danos Morais: div.items-center.justify-center.flex.flex-col.md\\:flex-row (texto "R$ 50.000,00")
        - Morte/Invalidez: div.items-center.justify-center.flex.flex-col.md\\:flex-row (texto "R$ 5.000,00")
        
        PLANO ALTERNATIVO (Segunda Coluna):
        - Mesmos elementos, exceto "Plano recomendado"
        
    RETORNO:
        dict: Dicionário com os dados dos planos estruturados
    """
    try:
        exibir_mensagem("📊 CAPTURANDO DADOS DOS PLANOS DE SEGURO...")
        
        # Aguardar carregamento dos planos
        time.sleep(3)
        
        dados_planos = {
            "plano_recomendado": {},
            "plano_alternativo": {}
        }
        
        # ========================================
        # CAPTURA PLANO RECOMENDADO (Primeira Coluna)
        # ========================================
        exibir_mensagem("🔍 Capturando dados do Plano Recomendado...")
        
        # Label do plano
        try:
            label_plano = page.locator("label.font-workSans.font-semibold").first
            if label_plano.is_visible():
                dados_planos["plano_recomendado"]["plano"] = label_plano.text_content().strip()
                exibir_mensagem(f"✅ Plano: {dados_planos['plano_recomendado']['plano']}")
            else:
                dados_planos["plano_recomendado"]["plano"] = "Plano recomendado"
                exibir_mensagem("⚠️ Label do plano não encontrado, usando padrão")
        except Exception as e:
            dados_planos["plano_recomendado"]["plano"] = "Plano recomendado"
            exibir_mensagem(f"⚠️ Erro ao capturar label do plano: {str(e)}")
        
        # Valor do Seguro
        try:
            valor_seguro = page.locator("p.md\\:font-bold").first
            if valor_seguro.is_visible():
                dados_planos["plano_recomendado"]["valor"] = valor_seguro.text_content().strip()
                exibir_mensagem(f"✅ Valor: {dados_planos['plano_recomendado']['valor']}")
            else:
                dados_planos["plano_recomendado"]["valor"] = "N/A"
                exibir_mensagem("⚠️ Valor do seguro não encontrado")
        except Exception as e:
            dados_planos["plano_recomendado"]["valor"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor: {str(e)}")
        
        # Forma de Pagamento
        try:
            forma_pagamento = page.locator("label.text-primary.text-xs.font-normal.mb-2").first
            if forma_pagamento.is_visible():
                dados_planos["plano_recomendado"]["forma_pagamento"] = forma_pagamento.text_content().strip()
                exibir_mensagem(f"✅ Forma de Pagamento: {dados_planos['plano_recomendado']['forma_pagamento']}")
            else:
                dados_planos["plano_recomendado"]["forma_pagamento"] = "N/A"
                exibir_mensagem("⚠️ Forma de pagamento não encontrada")
        except Exception as e:
            dados_planos["plano_recomendado"]["forma_pagamento"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar forma de pagamento: {str(e)}")
        
        # Parcelamento
        try:
            parcelamento = page.locator("div.text-primary.text-xs.font-bold").first
            if parcelamento.is_visible():
                dados_planos["plano_recomendado"]["parcelamento"] = parcelamento.text_content().strip()
                exibir_mensagem(f"✅ Parcelamento: {dados_planos['plano_recomendado']['parcelamento']}")
            else:
                dados_planos["plano_recomendado"]["parcelamento"] = "N/A"
                exibir_mensagem("⚠️ Parcelamento não encontrado")
        except Exception as e:
            dados_planos["plano_recomendado"]["parcelamento"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar parcelamento: {str(e)}")
        
        # Valor da Franquia
        try:
            franquia = page.locator("p.md\\:font-bold").nth(1)  # Segundo elemento
            if franquia.is_visible():
                dados_planos["plano_recomendado"]["valor_franquia"] = franquia.text_content().strip()
                exibir_mensagem(f"✅ Valor da Franquia: {dados_planos['plano_recomendado']['valor_franquia']}")
            else:
                dados_planos["plano_recomendado"]["valor_franquia"] = "N/A"
                exibir_mensagem("⚠️ Valor da franquia não encontrado")
        except Exception as e:
            dados_planos["plano_recomendado"]["valor_franquia"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor da franquia: {str(e)}")
        
        # Valor de Mercado
        try:
            valor_mercado = page.locator("p.mb-1").first
            if valor_mercado.is_visible():
                dados_planos["plano_recomendado"]["valor_mercado"] = valor_mercado.text_content().strip()
                exibir_mensagem(f"✅ Valor de Mercado: {dados_planos['plano_recomendado']['valor_mercado']}")
            else:
                dados_planos["plano_recomendado"]["valor_mercado"] = "N/A"
                exibir_mensagem("⚠️ Valor de mercado não encontrado")
        except Exception as e:
            dados_planos["plano_recomendado"]["valor_mercado"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor de mercado: {str(e)}")
        
        # Coberturas (Assistência, Vidros, Carro Reserva)
        coberturas = ["assistencia", "vidros", "carro_reserva"]
        for i, cobertura in enumerate(coberturas):
            try:
                # Procurar por ícone de OK para cada cobertura
                icone_ok = page.locator(f"img[src='/icone-ok.svg']").nth(i)
                if icone_ok.is_visible():
                    dados_planos["plano_recomendado"][cobertura] = True
                    exibir_mensagem(f"✅ {cobertura.title()}: True")
                else:
                    dados_planos["plano_recomendado"][cobertura] = False
                    exibir_mensagem(f"❌ {cobertura.title()}: False")
            except Exception as e:
                dados_planos["plano_recomendado"][cobertura] = False
                exibir_mensagem(f"⚠️ Erro ao capturar {cobertura}: {str(e)}")
        
        # Danos (Materiais, Corporais, Morais, Morte/Invalidez)
        danos = ["danos_materiais", "danos_corporais", "danos_morais", "morte_invalidez"]
        for i, dano in enumerate(danos):
            try:
                # Procurar por div com classe específica
                elemento_dano = page.locator("div.items-center.justify-center.flex.flex-col.md\\:flex-row").nth(i)
                if elemento_dano.is_visible():
                    # Extrair o valor (texto dentro do segundo p)
                    valor_dano = elemento_dano.locator("p.mb-1").nth(1).text_content().strip()
                    dados_planos["plano_recomendado"][dano] = valor_dano
                    exibir_mensagem(f"✅ {dano.replace('_', ' ').title()}: {valor_dano}")
                else:
                    dados_planos["plano_recomendado"][dano] = "N/A"
                    exibir_mensagem(f"⚠️ {dano.replace('_', ' ').title()} não encontrado")
            except Exception as e:
                dados_planos["plano_recomendado"][dano] = "N/A"
                exibir_mensagem(f"⚠️ Erro ao capturar {dano}: {str(e)}")
        
        # ========================================
        # CAPTURA PLANO ALTERNATIVO (Segunda Coluna)
        # ========================================
        exibir_mensagem("🔍 Capturando dados do Plano Alternativo...")
        
        # Para o plano alternativo, não há label "Plano recomendado"
        dados_planos["plano_alternativo"]["plano"] = "Plano alternativo"
        
        # Capturar os mesmos elementos, mas da segunda coluna
        # Valor do Seguro (segunda coluna)
        try:
            valor_seguro_alt = page.locator("p.md\\:font-bold").nth(2)  # Terceiro elemento
            if valor_seguro_alt.is_visible():
                dados_planos["plano_alternativo"]["valor"] = valor_seguro_alt.text_content().strip()
                exibir_mensagem(f"✅ Valor (Alternativo): {dados_planos['plano_alternativo']['valor']}")
            else:
                dados_planos["plano_alternativo"]["valor"] = "N/A"
                exibir_mensagem("⚠️ Valor do seguro alternativo não encontrado")
        except Exception as e:
            dados_planos["plano_alternativo"]["valor"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor alternativo: {str(e)}")
        
        # Forma de Pagamento (segunda coluna)
        try:
            forma_pagamento_alt = page.locator("label.text-primary.text-xs.font-normal.mb-2").nth(1)  # Segundo elemento
            if forma_pagamento_alt.is_visible():
                dados_planos["plano_alternativo"]["forma_pagamento"] = forma_pagamento_alt.text_content().strip()
                exibir_mensagem(f"✅ Forma de Pagamento (Alternativo): {dados_planos['plano_alternativo']['forma_pagamento']}")
            else:
                dados_planos["plano_alternativo"]["forma_pagamento"] = "N/A"
                exibir_mensagem("⚠️ Forma de pagamento alternativo não encontrada")
        except Exception as e:
            dados_planos["plano_alternativo"]["forma_pagamento"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar forma de pagamento alternativo: {str(e)}")
        
        # Parcelamento (segunda coluna)
        try:
            parcelamento_alt = page.locator("div.text-primary.text-xs.font-bold").nth(1)  # Segundo elemento
            if parcelamento_alt.is_visible():
                dados_planos["plano_alternativo"]["parcelamento"] = parcelamento_alt.text_content().strip()
                exibir_mensagem(f"✅ Parcelamento (Alternativo): {dados_planos['plano_alternativo']['parcelamento']}")
            else:
                dados_planos["plano_alternativo"]["parcelamento"] = "N/A"
                exibir_mensagem("⚠️ Parcelamento alternativo não encontrado")
        except Exception as e:
            dados_planos["plano_alternativo"]["parcelamento"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar parcelamento alternativo: {str(e)}")
        
        # Valor da Franquia (segunda coluna)
        try:
            franquia_alt = page.locator("p.md\\:font-bold").nth(3)  # Quarto elemento
            if franquia_alt.is_visible():
                dados_planos["plano_alternativo"]["valor_franquia"] = franquia_alt.text_content().strip()
                exibir_mensagem(f"✅ Valor da Franquia (Alternativo): {dados_planos['plano_alternativo']['valor_franquia']}")
            else:
                dados_planos["plano_alternativo"]["valor_franquia"] = "N/A"
                exibir_mensagem("⚠️ Valor da franquia alternativo não encontrado")
        except Exception as e:
            dados_planos["plano_alternativo"]["valor_franquia"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor da franquia alternativo: {str(e)}")
        
        # Valor de Mercado (segunda coluna)
        try:
            valor_mercado_alt = page.locator("p.mb-1").nth(1)  # Segundo elemento
            if valor_mercado_alt.is_visible():
                dados_planos["plano_alternativo"]["valor_mercado"] = valor_mercado_alt.text_content().strip()
                exibir_mensagem(f"✅ Valor de Mercado (Alternativo): {dados_planos['plano_alternativo']['valor_mercado']}")
            else:
                dados_planos["plano_alternativo"]["valor_mercado"] = "N/A"
                exibir_mensagem("⚠️ Valor de mercado alternativo não encontrado")
        except Exception as e:
            dados_planos["plano_alternativo"]["valor_mercado"] = "N/A"
            exibir_mensagem(f"⚠️ Erro ao capturar valor de mercado alternativo: {str(e)}")
        
        # Coberturas do plano alternativo (ícones de OK)
        for i, cobertura in enumerate(coberturas):
            try:
                # Procurar por ícone de OK para cada cobertura (segunda coluna)
                icone_ok_alt = page.locator(f"img[src='/icone-ok.svg']").nth(i + 3)  # Pular os 3 primeiros
                if icone_ok_alt.is_visible():
                    dados_planos["plano_alternativo"][cobertura] = True
                    exibir_mensagem(f"✅ {cobertura.title()} (Alternativo): True")
                else:
                    dados_planos["plano_alternativo"][cobertura] = False
                    exibir_mensagem(f"❌ {cobertura.title()} (Alternativo): False")
            except Exception as e:
                dados_planos["plano_alternativo"][cobertura] = False
                exibir_mensagem(f"⚠️ Erro ao capturar {cobertura} alternativo: {str(e)}")
        
        # Danos do plano alternativo
        for i, dano in enumerate(danos):
            try:
                # Procurar por div com classe específica (segunda coluna)
                elemento_dano_alt = page.locator("div.items-center.justify-center.flex.flex-col.md\\:flex-row").nth(i + 4)  # Pular os 4 primeiros
                if elemento_dano_alt.is_visible():
                    # Extrair o valor (texto dentro do segundo p)
                    valor_dano_alt = elemento_dano_alt.locator("p.mb-1").nth(1).text_content().strip()
                    dados_planos["plano_alternativo"][dano] = valor_dano_alt
                    exibir_mensagem(f"✅ {dano.replace('_', ' ').title()} (Alternativo): {valor_dano_alt}")
                else:
                    dados_planos["plano_alternativo"][dano] = "N/A"
                    exibir_mensagem(f"⚠️ {dano.replace('_', ' ').title()} alternativo não encontrado")
            except Exception as e:
                dados_planos["plano_alternativo"][dano] = "N/A"
                exibir_mensagem(f"⚠️ Erro ao capturar {dano} alternativo: {str(e)}")
        
        # Salvar dados em arquivo JSON
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        json_path = f"dados_planos_seguro_{timestamp}.json"
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(dados_planos, f, indent=2, ensure_ascii=False)
        
        exibir_mensagem(f"💾 Dados salvos em: {json_path}")
        exibir_mensagem("📊 CAPTURA DE DADOS CONCLUÍDA!")
        
        return dados_planos
        
    except Exception as e:
        exibir_mensagem(f"❌ ERRO na captura de dados: {str(e)}")
        return None

def main():
    """
    Função principal que executa o teste das Telas 1-9 sequencialmente
    
    FLUXO:
        1. Carrega parâmetros do JSON
        2. Configura browser Playwright
        3. Executa Tela 1 → Tela 2 → Tela 3 → Tela 4 → Tela 5 → Tela 6 → Tela 7 → Tela 8 → Tela 9
        4. Exibe resultados de cada tela
        5. Fecha browser
    
    RETORNO:
        int: 0 se sucesso, 1 se falha
    """
    try:
        # Carregar parâmetros
        with open('config/parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 15 SEQUENCIAL")
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
            if navegar_tela_6_playwright(page, parametros['combustivel'], parametros['kit_gas'], parametros['blindado'], parametros['financiado']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 6 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 6 FALHOU!")
                return 1
            
            # TELA 7
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_7_playwright(page, parametros['cep']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 7 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 7 FALHOU!")
                return 1
            
            # TELA 8
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_8_playwright(page, parametros['uso_veiculo']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 8 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 8 FALHOU!")
                return 1
            
            # TELA 9
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_9_playwright(page, parametros['nome'], parametros['cpf'], parametros['data_nascimento'], parametros['sexo'], parametros['estado_civil'], parametros['email'], parametros['celular']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 9 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 9 FALHOU!")
                return 1
            
            # TELA 10
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_10_playwright(page, parametros['condutor_principal'], parametros['nome_condutor'], parametros['cpf_condutor'], parametros['data_nascimento_condutor'], parametros['sexo_condutor'], parametros['estado_civil_condutor']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 10 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 10 FALHOU!")
                return 1
            
            # TELA 11
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_11_playwright(page, parametros['local_de_trabalho'], parametros['estacionamento_proprio_local_de_trabalho'], parametros['local_de_estudo'], parametros['estacionamento_proprio_local_de_estudo']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 11 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 11 FALHOU!")
                return 1
            
            # TELA 12
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_12_playwright(page, parametros['garagem_residencia'], parametros['portao_eletronico']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 12 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 12 FALHOU!")
                return 1
            
            # TELA 13
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_13_playwright(page, parametros['reside_18_26'], parametros['sexo_do_menor'], parametros['faixa_etaria_menor_mais_novo']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 13 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 13 FALHOU!")
                return 1
            
            # TELA 14 (CONDICIONAL)
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_14_playwright(page, parametros['continuar_com_corretor_anterior']):
                # Não incrementa telas_executadas pois é condicional
                exibir_mensagem("✅ TELA 14 PROCESSADA!")
            else:
                exibir_mensagem("❌ TELA 14 FALHOU!")
                return 1
            
            # TELA 15
            exibir_mensagem("\n" + "="*50)
            if navegar_tela_15_playwright(page, parametros['autenticacao']['email_login'], parametros['autenticacao']['senha_login']):
                telas_executadas += 1
                exibir_mensagem("✅ TELA 15 CONCLUÍDA!")
            else:
                exibir_mensagem("❌ TELA 15 FALHOU!")
                return 1
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 TESTE TELAS 1 A 15 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/14 (Tela 14 é condicional)")
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
