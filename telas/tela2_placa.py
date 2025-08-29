#!/usr/bin/env python3
"""
Tela 2: Inserção de placa
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, preencher_com_delay_otimizado, 
    salvar_estado_tela
)

def implementar_tela2(driver, parametros):
    """Implementa a Tela 2: Inserção da placa"""
    print(f"\n📱 TELA 2: Inserindo placa {parametros['placa']}...")
    
    try:
        aguardar_estabilizacao(driver, 3)
        salvar_estado_tela(driver, 2, "inicial", None)
        
        # Aguardar elementos da página carregarem
        print("⏳ Aguardando elementos da página carregarem...")
        time.sleep(5)
        
        # Tentar diferentes estratégias para encontrar o campo da placa
        campo_placa = None
        estrategias = [
            # Estratégia 1: Campo com ID específico
            (By.ID, "placaTelaDadosPlaca"),
            # Estratégia 2: Campo com placeholder contendo "placa"
            (By.XPATH, "//input[contains(@placeholder, 'placa') or contains(@placeholder, 'Placa')]"),
            # Estratégia 3: Campo com name contendo "placa"
            (By.XPATH, "//input[contains(@name, 'placa') or contains(@name, 'Placa')]"),
            # Estratégia 4: Campo com label contendo "placa"
            (By.XPATH, "//label[contains(text(), 'placa') or contains(text(), 'Placa')]/following-sibling::input"),
            # Estratégia 5: Campo de texto genérico
            (By.CSS_SELECTOR, "input[type='text']"),
            # Estratégia 6: Campo com atributo data específico
            (By.XPATH, "//input[@data-field='placa' or @data-field='Placa']"),
            # Estratégia 7: Campo com classe específica
            (By.CSS_SELECTOR, "input.placa, input.placa-input, input.plate-input"),
            # Estratégia 8: Campo com aria-label contendo "placa"
            (By.XPATH, "//input[contains(@aria-label, 'placa') or contains(@aria-label, 'Placa')]")
        ]
        
        for estrategia in estrategias:
            try:
                print(f"⏳ Tentando estratégia: {estrategia[0]} = {estrategia[1]}")
                campo_placa = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(estrategia)
                )
                print(f"✅ Campo da placa encontrado via: {estrategia[0]} = {estrategia[1]}")
                break
            except:
                continue
        
        if not campo_placa:
            print("❌ Campo da placa não encontrado com nenhuma estratégia")
            
            # Salvar estado para debug
            salvar_estado_tela(driver, 2, "campo_nao_encontrado", None)
            
            # Tentar encontrar qualquer campo de input para debug
            try:
                todos_campos = driver.find_elements(By.TAG_NAME, "input")
                print(f"🔍 Total de campos input encontrados: {len(todos_campos)}")
                for i, campo in enumerate(todos_campos[:5]):  # Mostrar apenas os primeiros 5
                    try:
                        campo_info = f"Campo {i+1}: type={campo.get_attribute('type')}, id={campo.get_attribute('id')}, name={campo.get_attribute('name')}, placeholder={campo.get_attribute('placeholder')}"
                        print(f"   {campo_info}")
                    except:
                        pass
            except:
                pass
            
            return False
        
        # Preencher a placa
        print(f"⏳ Preenchendo placa: {parametros['placa']}")
        
        try:
            # Limpar o campo
            campo_placa.clear()
            time.sleep(0.5)
            
            # Preencher caractere por caractere para simular digitação humana
            for char in parametros['placa']:
                campo_placa.send_keys(char)
                time.sleep(0.1)
            
            print(f"✅ Placa preenchida com sucesso: {parametros['placa']}")
            
        except Exception as e:
            print(f"❌ Erro ao preencher placa: {e}")
            
            # Tentar via JavaScript como fallback
            try:
                driver.execute_script(f"arguments[0].value = '{parametros['placa']}';", campo_placa)
                print(f"✅ Placa preenchida via JavaScript: {parametros['placa']}")
            except Exception as e2:
                print(f"❌ Falha também via JavaScript: {e2}")
                return False
        
        aguardar_estabilizacao(driver, 3)
        salvar_estado_tela(driver, 2, "placa_inserida", None)
        
        print("✅ **TELA 2 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 2: {e}")
        return False
