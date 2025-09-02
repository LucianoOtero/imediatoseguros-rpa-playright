#!/usr/bin/env python3
"""
TESTE TELAS 1 A 8 SEQUENCIAL - IMPLEMENTAÇÃO COMPLETA
Teste das Telas 1-8 usando Playwright com implementação da Tela 8

DESCRIÇÃO:
- Tela 1: Seleção do tipo de seguro (Carro)
- Tela 2: Inserção da placa
- Tela 3: Confirmação do veículo
- Tela 4: Veículo segurado
- Tela 5: Estimativa inicial (captura de dados)
- Tela 6: Itens do carro (combustível e checkboxes)
- Tela 7: Endereço de pernoite (CEP)
- Tela 8: Finalidade do veículo (uso do veículo)

AUTOR: Luciano Otero
DATA: 2025-09-02
VERSÃO: 1.2.0
STATUS: Implementação completa das Telas 1-8
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

def main():
    """
    Função principal que executa o teste das Telas 1-8 sequencialmente
    
    FLUXO:
        1. Carrega parâmetros do JSON
        2. Configura browser Playwright
        3. Executa Tela 1 → Tela 2 → Tela 3 → Tela 4 → Tela 5 → Tela 6 → Tela 7 → Tela 8
        4. Exibe resultados de cada tela
        5. Fecha browser
    
    RETORNO:
        int: 0 se sucesso, 1 se falha
    """
    try:
        # Carregar parâmetros
        with open('config/parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        exibir_mensagem("🚀 INICIANDO TESTE TELAS 1 A 8 SEQUENCIAL")
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
            
            # Resultado final
            exibir_mensagem("\n" + "="*60)
            exibir_mensagem("🎉 TESTE TELAS 1 A 8 CONCLUÍDO COM SUCESSO!")
            exibir_mensagem(f"✅ Total de telas executadas: {telas_executadas}/8")
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
