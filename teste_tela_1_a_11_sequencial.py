#!/usr/bin/env python3
"""
TESTE TELAS 1 A 11 SEQUENCIAL - IMPLEMENTAÇÃO COMPLETA
Teste das Telas 1-11 usando Playwright com implementação da Tela 11

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

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 1.5.0
STATUS: Implementação completa das Telas 1-11
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
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 9 SEQUENCIAL")
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
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 TESTE TELAS 1 A 11 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/11")
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
