#!/usr/bin/env python3
"""
Investigação Detalhada da Tela 7 - RPA Tô Segurado
Analisa o que realmente aconteceu após clicar Continuar na Tela 6
"""

import time
import tempfile
import shutil
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções otimizadas"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Criar diretório temporário único
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    # Configurar o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def navegar_ate_tela6(driver):
    """Navega até a Tela 6 (última tela funcionando)"""
    print("🚀 **NAVEGANDO ATÉ TELA 6 (ÚLTIMA FUNCIONANDO)**")
    
    try:
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        time.sleep(5)
        
        carro_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("✅ Carro selecionado")
        time.sleep(3)
        
        # Tela 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        placa_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        time.sleep(2)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado")
        time.sleep(5)
        
        # Tela 5: Confirmar veículo
        print("\n📱 TELA 5: Confirmando veículo...")
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        
        sim_radio = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
        )
        driver.execute_script("arguments[0].click();", sim_radio)
        print("✅ Veículo confirmado")
        time.sleep(3)
        
        # Tela 6: Veículo segurado
        print("\n📱 TELA 6: Selecionando 'Não' para veículo segurado...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmarVeiculoTelaInformacoesVeiculo"))
        )
        
        nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
        if not nao_radio.is_selected():
            driver.execute_script("arguments[0].click();", nao_radio)
            print("✅ Radio 'Não' selecionado")
            time.sleep(2)
        
        print("✅ TELA 6 CARREGADA COM SUCESSO!")
        return True
        
    except Exception as e:
        print(f"❌ **ERRO AO NAVEGAR ATÉ TELA 6:** {e}")
        return False

def investigar_transicao_tela6_7(driver):
    """Investiga o que acontece na transição da Tela 6 para Tela 7"""
    print("\n🔍 **INVESTIGANDO TRANSIÇÃO TELA 6 → TELA 7**")
    
    try:
        # Salvar estado da Tela 6
        print("�� Salvando estado da Tela 6...")
        with open("/opt/imediatoseguros-rpa/temp/tela_06_investigacao.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_06_investigacao.png")
        print("✅ Estado da Tela 6 salvo")
        
        # Clicar em Continuar na Tela 6
        print("\n🎯 Clicando em Continuar na Tela 6...")
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaInfosAutoContinuar"))
        )
        
        # Salvar estado antes do clique
        print("📸 Estado antes do clique...")
        with open("/opt/imediatoseguros-rpa/temp/tela_06_antes_clique.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_06_antes_clique.png")
        
        # Clicar e monitorar mudanças
        print("🖱️ Clicando em Continuar...")
        continuar_button.click()
        print("✅ Continuar clicado")
        
        # Monitorar mudanças por 30 segundos
        print("\n⏳ Monitorando mudanças por 30 segundos...")
        for i in range(30):
            time.sleep(1)
            current_url = driver.current_url
            current_title = driver.title
            
            print(f"⏱️ {i+1:02d}s - URL: {current_url}")
            print(f"     Título: {current_title}")
            
            # Verificar se apareceu algum texto específico
            page_text = driver.page_source.lower()
            
            if "estimativa" in page_text:
                print("🎯 'ESTIMATIVA' DETECTADO!")
                break
            elif "carrossel" in page_text:
                print("�� 'CARROSSEL' DETECTADO!")
                break
            elif "cobertura" in page_text:
                print("🛡️ 'COBERTURA' DETECTADO!")
                break
            elif "loading" in page_text or "aguarde" in page_text or "calculando" in page_text:
                print("⏳ ELEMENTO DE CARREGAMENTO DETECTADO!")
                break
        
        # Salvar estado final
        print("\n📸 Salvando estado final...")
        with open("/opt/imediatoseguros-rpa/temp/tela_07_investigacao.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_07_investigacao.png")
        
        # Análise final
        print("\n�� **ANÁLISE FINAL:**")
        print(f"URL Final: {driver.current_url}")
        print(f"Título Final: {driver.title}")
        
        page_text = driver.page_source.lower()
        
        print("\n�� **ELEMENTOS DETECTADOS:**")
        if "estimativa" in page_text:
            print("✅ 'estimativa' - POSSÍVEL TELA 7")
        else:
            print("❌ 'estimativa' - NÃO ENCONTRADO")
            
        if "carrossel" in page_text:
            print("✅ 'carrossel' - POSSÍVEL TELA 7")
        else:
            print("❌ 'carrossel' - NÃO ENCONTRADO")
            
        if "cobertura" in page_text:
            print("✅ 'cobertura' - POSSÍVEL TELA 7")
        else:
            print("❌ 'cobertura' - NÃO ENCONTRADO")
            
        if "loading" in page_text or "aguarde" in page_text or "calculando" in page_text:
            print("✅ Elementos de carregamento detectados")
        else:
            print("❌ Elementos de carregamento não encontrados")
        
        # Verificar se houve erro
        if "error" in page_text or "erro" in page_text:
            print("⚠️ POSSÍVEL ERRO DETECTADO NA PÁGINA")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA INVESTIGAÇÃO:** {e}")
        return False

def main():
    """Função principal"""
    print("�� **INVESTIGAÇÃO DETALHADA DA TELA 7**")
    print("=" * 60)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        if not navegar_ate_tela6(driver):
            print("❌ **FALHA AO NAVEGAR ATÉ TELA 6 - PARANDO**")
            return
        
        # Investigar transição Tela 6 → Tela 7
        if not investigar_transicao_tela6_7(driver):
            print("❌ **FALHA NA INVESTIGAÇÃO - PARANDO**")
            return
        
        print(f"\n�� **INVESTIGAÇÃO CONCLUÍDA COM SUCESSO!**")
        print(f"�� Arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"🔍 Verifique os arquivos HTML e screenshots para análise")
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL DURANTE INVESTIGAÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-investigacao.png")
            print(" Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
