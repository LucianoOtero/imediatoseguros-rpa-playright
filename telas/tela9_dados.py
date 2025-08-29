#!/usr/bin/env python3
"""
Tela 9: Dados pessoais
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_carregamento_pagina, aguardar_estabilizacao,
    preencher_com_delay_otimizado, clicar_radio_via_javascript,
    clicar_continuar_corrigido, salvar_estado_tela
)

def implementar_tela9(driver, parametros):
    """Implementa a Tela 9: Dados pessoais"""
    print("\n **INICIANDO TELA 9: Dados pessoais**")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'nome') or contains(text(), 'Nome') or contains(text(), 'CPF') or contains(text(), 'cpf')]"))
        )
        print("✅ Tela 9 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 9, "dados_carregados", None)
        
        # Preencher Nome
        print(f"⏳ Preenchendo nome: {parametros['nome']}...")
        
        # Tentar diferentes seletores para o campo nome
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'nome') or contains(@placeholder, 'Nome') or contains(@name, 'nome') or contains(@id, 'nome')]", parametros['nome'], "nome"):
                print("⚠️ Campo nome não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher nome - tentando prosseguir...")
        
        # Preencher CPF
        print(f"⏳ Preenchendo CPF: {parametros['cpf']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'CPF') or contains(@placeholder, 'cpf') or contains(@name, 'cpf') or contains(@id, 'cpf')]", parametros['cpf'], "CPF"):
                print("⚠️ Campo CPF não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher CPF - tentando prosseguir...")
        
        # Preencher Data de Nascimento
        print(f"⏳ Preenchendo data de nascimento: {parametros['data_nascimento']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'nascimento') or contains(@placeholder, 'Nascimento') or contains(@name, 'nascimento') or contains(@id, 'nascimento')]", parametros['data_nascimento'], "data de nascimento"):
                print("⚠️ Campo data de nascimento não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher data de nascimento - tentando prosseguir...")
        
        # Selecionar Sexo
        print(f"⏳ Selecionando sexo: {parametros['sexo']}...")
        
        if not clicar_radio_via_javascript(driver, parametros['sexo'], f"{parametros['sexo']} como sexo"):
            print(f"⚠️ Radio '{parametros['sexo']}' não encontrado - tentando prosseguir...")
        
        # Selecionar Estado Civil
        print(f"⏳ Selecionando estado civil: {parametros['estado_civil']}...")
        
        if not clicar_radio_via_javascript(driver, parametros['estado_civil'], f"{parametros['estado_civil']} como estado civil"):
            print(f"⚠️ Radio '{parametros['estado_civil']}' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 9"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 9")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 9, "apos_continuar", None)
        print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False
