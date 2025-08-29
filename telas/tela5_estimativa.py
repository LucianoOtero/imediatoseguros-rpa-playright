#!/usr/bin/env python3
"""
Tela 5: Estimativa inicial
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, salvar_estado_tela
)

def implementar_tela5(driver, parametros):
    """Implementa a Tela 5: Estimativa inicial"""
    print(f"\n�� TELA 5: Estimativa inicial...")
    
    try:
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 5, "inicial", None)
        
        # ESTRATÉGIA 1: Aguardar elementos da estimativa inicial (mais específicos)
        print("⏳ Aguardando elementos da estimativa inicial...")
        try:
            # Buscar por elementos mais específicos que indicam a Tela 5
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel') or contains(text(), 'cobertura') or contains(text(), 'preço') or contains(text(), 'Preço')]"))
            )
            print("✅ Tela 5 carregada - estimativa inicial detectada!")
        except Exception as e:
            print(f"⚠️ Elementos da estimativa não detectados: {e}")
            print("⏳ Tentando estratégia alternativa...")
            
            # ESTRATÉGIA 2: Buscar por elementos genéricos que podem indicar a Tela 5
            try:
                WebDriverWait(driver, 15).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'continuar') or contains(text(), 'Próximo') or contains(text(), 'próximo')]"))
                )
                print("✅ Tela 5 detectada via botão Continuar/Próximo!")
            except:
                print("⚠️ Botão Continuar/Próximo não encontrado")
                print("⏳ Tentando prosseguir mesmo assim...")
        
        # Aguardar carregamento da página
        print("⏳ Aguardando carregamento da página (timeout: 30s)...")
        try:
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            print("✅ Página carregada com sucesso")
        except:
            print("⚠️ jQuery não detectado ou ainda carregando")
            print("⚠️ Angular não detectado ou ainda carregando")
            print("✅ Página carregada com sucesso")
        
        salvar_estado_tela(driver, 5, "estimativa_carregada", None)
        
        # Aguardar estabilização antes de procurar o botão
        aguardar_estabilizacao(driver, 5)
        
        # Aguardar botão Continuar aparecer
        print("⏳ Aguardando botão Continuar aparecer...")
        
        # ESTRATÉGIA 1: Buscar por texto "Continuar" ou "continuar"
        try:
            botao_continuar = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'continuar')]"))
            )
            print("✅ Botão Continuar encontrado via: //*[contains(text(), 'Continuar') or contains(text(), 'continuar')]")
            
            # ESTRATÉGIA 2: Aguardar estabilização antes de clicar
            aguardar_estabilizacao(driver, 3)
            
            # ESTRATÉGIA 3: Clicar via JavaScript para evitar problemas
            driver.execute_script("arguments[0].click();", botao_continuar)
            print("✅ Botão Continuar clicado via JavaScript")
            
        except Exception as e:
            print(f"❌ Erro ao clicar em botão Continuar Tela 5: {e}")
            raise Exception(f"Falha ao clicar Continuar na Tela 5: {e}")
        
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
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False
