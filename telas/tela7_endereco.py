#!/usr/bin/env python3
"""
Tela 7: Endereço de pernoite (CEP)
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, salvar_estado_tela
)

def implementar_tela7(driver, parametros):
    """Implementa a Tela 7: Endereço de pernoite"""
    print(f"\n **INICIANDO TELA 7: Endereço de pernoite**")
    
    try:
        # Aguardar elementos do endereço (ESTRATÉGIA QUE FUNCIONOU)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'endereço') or contains(text(), 'Endereço') or contains(text(), 'CEP') or contains(text(), 'cep')]"))
        )
        print("✅ Tela 7 carregada - endereço de pernoite detectado!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        # Aguardar carregamento da página (ESTRATÉGIA QUE FUNCIONOU)
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "endereco_carregado", None)
        
        # Inserir CEP (ESTRATÉGIA QUE FUNCIONOU)
        print("⏳ Inserindo CEP...")
        
        # Tentar diferentes seletores para o campo CEP
        cep_campo = None
        try:
            cep_campo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CEP') or contains(@placeholder, 'cep') or contains(@name, 'cep') or contains(@id, 'cep')]"))
            )
        except:
            try:
                cep_campo = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
            except:
                print("⚠️ Campo CEP não encontrado - tentando prosseguir...")
        
        if cep_campo:
            cep_campo.clear()
            time.sleep(1)
            cep_campo.send_keys("03084-000")
            print("✅ CEP preenchido: 03084-000")
        
        # Aguardar sugestão e selecionar (ESTRATÉGIA QUE FUNCIONOU)
        print("⏳ Aguardando sugestão de endereço...")
        time.sleep(5)
        
        # Selecionar sugestão se disponível
        try:
            sugestao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rua Santa') or contains(text(), 'São Paulo')]"))
            )
            sugestao.click()
            print("✅ Sugestão de endereço selecionada")
        except:
            print("⚠️ Sugestão não encontrada - tentando prosseguir...")
        
        # Clicar em Continuar (ESTRATÉGIA QUE FUNCIONOU)
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página (ESTRATÉGIA QUE FUNCIONOU)"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def clicar_com_delay_extremo(driver, by, value, descricao="elemento", timeout=30):
    """Clica em um elemento com delay extremo (ESTRATÉGIA QUE FUNCIONOU)"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 15)
        
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').click();")
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(2)
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False
