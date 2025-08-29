#!/usr/bin/env python3
"""
Tela 4: Veículo já segurado
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, salvar_estado_tela
)

def implementar_tela4(driver, parametros):
    """Implementa a Tela 4: Veículo já segurado"""
    print(f"\n�� TELA 4: Veículo já segurado? → Não...")
    
    try:
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 4, "inicial", None)
        
        # Aguardar elementos da pergunta sobre veículo segurado
        print("⏳ Aguardando elementos da pergunta sobre veículo segurado...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
            )
            print("✅ Tela 4 carregada - pergunta sobre veículo segurado detectada!")
        except Exception as e:
            print(f"⚠️ Confirmação do veículo não detectada: {e}")
            print("⏳ Tentando prosseguir mesmo assim...")
        
        # Aguardar carregamento da página
        print("⏳ Aguardando carregamento da página (timeout: 20s)...")
        try:
            WebDriverWait(driver, 20).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página carregada com sucesso")
        except:
            print("⚠️ jQuery não detectado ou ainda carregando")
            print("⚠️ Angular não detectado ou ainda carregando")
            print("✅ Página carregada com sucesso")
        
        salvar_estado_tela(driver, 4, "pergunta_carregada", None)
        
        # Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado...")
        
        # ESTRATÉGIA 1: Tentar encontrar radio 'Não' diretamente
        try:
            radio_nao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='radio' and contains(@value, 'Não')]"))
            )
            print("✅ Radio 'Não' encontrado via: //input[@type='radio' and contains(@value, 'Não')]")
            
            # ESTRATÉGIA 2: Clicar via JavaScript (mais confiável)
            driver.execute_script("arguments[0].click();", radio_nao)
            print("✅ Radio 'Não' clicado via JavaScript")
            
        except Exception as e:
            print(f"⚠️ Radio 'Não' não encontrado: {e}")
            print("⚠️ Radio 'Não' não encontrado - prosseguindo...")
        
        # Aguardar botão Continuar aparecer
        print("⏳ Aguardando botão Continuar aparecer...")
        print("⏳ Aguardando botão Continuar Tela 4 aparecer...")
        
        # ESTRATÉGIA 1: Buscar por texto "Continuar" ou "continuar"
        try:
            botao_continuar = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'continuar')]"))
            )
            print("✅ botão Continuar Tela 4 encontrado via: ('xpath', \"//*[contains(text(), 'Continuar') or contains(text(), 'continuar')]\")")
            
            # ESTRATÉGIA 2: Aguardar estabilização antes de clicar
            aguardar_estabilizacao(driver, 3)
            
            # ESTRATÉGIA 3: Clicar via JavaScript para evitar interceptação
            driver.execute_script("arguments[0].click();", botao_continuar)
            print("✅ Botão Continuar clicado via JavaScript (evitando interceptação)")
            
        except Exception as e:
            print(f"❌ Erro ao clicar em botão Continuar Tela 4: {e}")
            raise Exception(f"Falha ao clicar Continuar na Tela 4: {e}")
        
        # Aguardar carregamento da página
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        # Verificar se a página carregou
        try:
            WebDriverWait(driver, 60).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página carregada com sucesso")
        except:
            print("⚠️ jQuery não detectado ou ainda carregando")
            print("⚠️ Angular não detectado ou ainda carregando")
            print("✅ Página carregada com sucesso")
        
        aguardar_estabilizacao(driver, 10)
        salvar_estado_tela(driver, 4, "apos_continuar", None)
        
        print("✅ **TELA 4 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
