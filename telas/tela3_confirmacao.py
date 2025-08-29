#!/usr/bin/env python3
"""
Tela 3: Confirmação do veículo
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_carregamento_pagina, aguardar_estabilizacao,
    clicar_radio_via_javascript, clicar_com_delay_otimizado, 
    clicar_continuar_corrigido, salvar_estado_tela
)

def implementar_tela3(driver, parametros):
    """Implementa a Tela 3: Confirmação do veículo"""
    print(f"\n📱 TELA 3: Confirmando veículo {parametros['marca']} {parametros['modelo']}...")
    
    try:
        # Aguardar estabilização inicial
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 3, "inicial", None)
        
        # Aguardar elementos da confirmação do veículo aparecerem
        print("⏳ Aguardando elementos da confirmação do veículo...")
        time.sleep(10)
        
        try:
            # Aguardar elementos da confirmação do veículo
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, f"//*[contains(text(), '{parametros['modelo']}') or contains(text(), '{parametros['marca']}')]"))
            )
            print(f"✅ Tela 3 carregada - confirmação do {parametros['modelo']} detectada!")
            
            salvar_estado_tela(driver, 3, "confirmacao_veiculo", None)
            
        except Exception as e:
            print(f"⚠️ Confirmação do veículo não detectada: {e}")
            print("⏳ Tentando prosseguir mesmo assim...")
            salvar_estado_tela(driver, 3, "confirmacao_nao_detectada", None)
        
        # Aguardar carregamento da página
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        salvar_estado_tela(driver, 3, "confirmacao_carregada", None)
        
        # Selecionar "Sim" para confirmação do veículo (se disponível)
        print("⏳ Verificando se há opção para confirmar veículo...")
        
        try:
            if clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
                print("✅ Radio 'Sim' selecionado para confirmação")
            else:
                print("⚠️ Radio 'Sim' não encontrado - prosseguindo...")
        except Exception as e:
            print(f"⚠️ Erro ao selecionar 'Sim': {e} - prosseguindo...")
        
        # Aguardar estabilização após seleção
        aguardar_estabilizacao(driver, 5)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        # Tentar diferentes estratégias para o botão Continuar
        estrategias_continuar = [
            (By.XPATH, "//button[contains(text(), 'Continuar')]"),
            (By.XPATH, "//*[contains(text(), 'Continuar')]"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, ".btn-continuar, .btn-primary"),
            (By.ID, "continuar"),
            (By.ID, "btn-continuar")
        ]
        
        botao_continuar = None
        for estrategia in estrategias_continuar:
            try:
                print(f"⏳ Tentando estratégia para Continuar: {estrategia[0]} = {estrategia[1]}")
                botao_continuar = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(estrategia)
                )
                print(f"✅ Botão Continuar encontrado via: {estrategia[0]} = {estrategia[1]}")
                break
            except:
                continue
        
        if not botao_continuar:
            print("❌ Botão Continuar não encontrado")
            salvar_estado_tela(driver, 3, "botao_nao_encontrado", None)
            return False
        
        # Clicar no botão Continuar
        print("⏳ Clicando no botão Continuar...")
        try:
            botao_continuar.click()
            print("✅ Botão Continuar clicado com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao clicar via método normal: {e}")
            # Tentar via JavaScript
            try:
                driver.execute_script("arguments[0].click();", botao_continuar)
                print("✅ Botão Continuar clicado via JavaScript")
            except Exception as e2:
                print(f"❌ Falha também via JavaScript: {e2}")
                return False
        
        # Aguardar carregamento da próxima página
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        # Aguardar carregamento da página
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 10)
        salvar_estado_tela(driver, 3, "apos_continuar", None)
        
        print("✅ **TELA 3 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 3: {e}")
        salvar_estado_tela(driver, 3, "erro", None)
        return False
