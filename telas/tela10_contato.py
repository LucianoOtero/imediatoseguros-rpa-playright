#!/usr/bin/env python3
"""
Tela 10: Contato
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_carregamento_pagina, aguardar_estabilizacao,
    preencher_com_delay_otimizado, clicar_continuar_corrigido, 
    salvar_estado_tela
)

def implementar_tela10(driver, parametros):
    """Implementa a Tela 10: Contato"""
    print("\n **INICIANDO TELA 10: Contato**")
    
    try:
        # Aguardar elementos de contato
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'email') or contains(text(), 'Email') or contains(text(), 'telefone') or contains(text(), 'Telefone')]"))
        )
        print("✅ Tela 10 carregada - contato detectado!")
        
        salvar_estado_tela(driver, 10, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 10, "contato_carregado", None)
        
        # Preencher Email
        print(f"⏳ Preenchendo email: {parametros['email']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email') or contains(@name, 'email') or contains(@id, 'email')]", parametros['email'], "email"):
                print("⚠️ Campo email não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher email - tentando prosseguir...")
        
        # Preencher Telefone/Celular
        print(f"⏳ Preenchendo celular: {parametros['celular']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'telefone') or contains(@placeholder, 'Telefone') or contains(@placeholder, 'celular') or contains(@name, 'telefone') or contains(@id, 'telefone')]", parametros['celular'], "celular"):
                print("⚠️ Campo celular não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher celular - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 10"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 10")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 10, "apos_continuar", None)
        print("✅ **TELA 10 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False
