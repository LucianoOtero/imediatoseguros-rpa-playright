#!/usr/bin/env python3
"""
Tela 1: Seleção do tipo de seguro
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, clicar_com_delay_otimizado, 
    salvar_estado_tela
)

def implementar_tela1(driver, parametros):
    """Implementa a Tela 1: Seleção do tipo de seguro"""
    print(f"\n📱 TELA 1: Selecionando tipo de seguro...")
    
    try:
        aguardar_estabilizacao(driver, 3)
        salvar_estado_tela(driver, 1, "inicial", None)
        
        # Aguardar elementos da página carregarem
        print("⏳ Aguardando elementos da página carregarem...")
        time.sleep(5)
        
        # Verificar se estamos na tela correta
        try:
            # Aguardar elementos de seleção de seguro aparecerem
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Carro') or contains(text(), 'car') or contains(text(), 'Moto') or contains(text(), 'Vida')]"))
            )
            print("✅ Tela de seleção de seguro detectada!")
        except:
            print("❌ Tela de seleção de seguro não detectada")
            salvar_estado_tela(driver, 1, "tela_incorreta", None)
            return False
        
        # Selecionar "Carro" como tipo de seguro
        print("⏳ Selecionando 'Carro' como tipo de seguro...")
        
        # Tentar diferentes estratégias para encontrar o botão Carro
        estrategias_carro = [
            (By.XPATH, "//button[contains(text(), 'Carro')]"),
            (By.XPATH, "//*[contains(text(), 'Carro')]"),
            (By.XPATH, "//div[contains(text(), 'Carro')]"),
            (By.XPATH, "//span[contains(text(), 'Carro')]"),
            (By.CSS_SELECTOR, "[data-tipo='carro']"),
            (By.CSS_SELECTOR, ".carro, .car, .veiculo-carro")
        ]
        
        botao_carro = None
        for estrategia in estrategias_carro:
            try:
                print(f"⏳ Tentando estratégia para Carro: {estrategia[0]} = {estrategia[1]}")
                botao_carro = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(estrategia)
                )
                print(f"✅ Botão Carro encontrado via: {estrategia[0]} = {estrategia[1]}")
                break
            except:
                continue
        
        if not botao_carro:
            print("❌ Botão Carro não encontrado")
            salvar_estado_tela(driver, 1, "botao_nao_encontrado", None)
            return False
        
        # Clicar no botão Carro
        print("⏳ Clicando no botão Carro...")
        try:
            botao_carro.click()
            print("✅ Botão Carro clicado com sucesso")
        except Exception as e:
            print(f"⚠️ Erro ao clicar via método normal: {e}")
            # Tentar via JavaScript
            try:
                driver.execute_script("arguments[0].click();", botao_carro)
                print("✅ Botão Carro clicado via JavaScript")
            except Exception as e2:
                print(f"❌ Falha também via JavaScript: {e2}")
                return False
        
        # Aguardar carregamento da próxima página
        print("⏳ Aguardando carregamento da página de cotação...")
        time.sleep(10)
        
        # Verificar se a página mudou
        try:
            # Aguardar elementos da página de cotação
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'placa') or contains(text(), 'Placa') or contains(text(), 'veículo') or contains(text(), 'Veículo')]"))
            )
            print("✅ Página de cotação carregada com sucesso!")
        except:
            print("⚠️ Página de cotação pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 1, "carro_selecionado", None)
        
        print("✅ **TELA 1 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 1: {e}")
        return False
