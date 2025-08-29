#!/usr/bin/env python3
"""
Investigação Específica da Tela 5 - Confirmação do Veículo
Para entender por que está falhando após Tela 3
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
    print("🔧 Configurando Chrome...")
    
    temp_dir = tempfile.mkdtemp()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver, temp_dir

def aguardar_carregamento_pagina(driver, timeout=30):
    """Aguarda o carregamento completo da página"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def salvar_estado_tela(driver, tela_num, acao, temp_dir):
    """Salva o estado atual da tela"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    tela_dir = f"temp/tela_{tela_num:02d}"
    os.makedirs(tela_dir, exist_ok=True)
    
    html_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    screenshot_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.png"
    driver.save_screenshot(screenshot_file)
    
    info_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"TELA {tela_num:02d}: {acao}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"URL: {driver.current_url}\n")
        f.write(f"Título: {driver.title}\n")
        f.write(f"Arquivos salvos em: {os.path.abspath(tela_dir)}\n")
    
    print(f"==================================================================================")
    print(f"️  **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def investigar_tela5():
    """Investiga especificamente a Tela 5"""
    print("�� **INVESTIGAÇÃO ESPECÍFICA DA TELA 5**")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # TELA 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou")
            return
        
        salvar_estado_tela(driver, 1, "inicial", None)
        
        # Clicar no botão Carro
        carro_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        salvar_estado_tela(driver, 1, "antes_clique", None)
        carro_btn.click()
        print("✅ Carro selecionado")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após selecionar Carro")
            return
        
        salvar_estado_tela(driver, 1, "apos_clique", None)
        
        # TELA 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        placa_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        salvar_estado_tela(driver, 2, "inicial", None)
        
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        
        salvar_estado_tela(driver, 2, "placa_inserida", None)
        
        # TELA 3: Clicar em Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        salvar_estado_tela(driver, 3, "antes_clique", None)
        continuar_btn.click()
        print("✅ Continuar clicado")
        
        # Aguardar carregamento e investigar
        print("⏳ Aguardando carregamento da página...")
        time.sleep(5)  # Aguardar um pouco mais
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        # INVESTIGAR O QUE CARREGOU
        print("\n🔍 **INVESTIGANDO O QUE CARREGOU APÓS TELA 3:**")
        print("=" * 60)
        
        # Salvar estado atual
        salvar_estado_tela(driver, 3, "apos_clique", None)
        
        # Verificar URL e título
        print(f"�� URL Atual: {driver.current_url}")
        print(f"📄 Título Atual: {driver.title}")
        
        # Procurar por elementos específicos
        print("\n🔍 **PROCURANDO ELEMENTOS ESPECÍFICOS:**")
        
        # Procurar por confirmação de veículo
        try:
            confirmacao_elements = driver.find_elements(By.NAME, "confirmacaoVeiculo")
            print(f"✅ Elementos 'confirmacaoVeiculo' encontrados: {len(confirmacao_elements)}")
            
            for i, elem in enumerate(confirmacao_elements):
                print(f"   Elemento {i+1}: {elem.get_attribute('outerHTML')[:200]}...")
        except:
            print("❌ Erro ao procurar 'confirmacaoVeiculo'")
        
        # Procurar por texto COROLLA
        try:
            corolla_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'COROLLA')]")
            print(f"✅ Elementos 'COROLLA' encontrados: {len(corolla_elements)}")
            
            for i, elem in enumerate(corolla_elements):
                print(f"   Elemento {i+1}: {elem.text[:100]}...")
        except:
            print("❌ Erro ao procurar 'COROLLA'")
        
        # Procurar por botões Continuar
        try:
            continuar_elements = driver.find_elements(By.XPATH, "//button[contains(., 'Continuar')]")
            print(f"✅ Botões 'Continuar' encontrados: {len(continuar_elements)}")
            
            for i, elem in enumerate(continuar_elements):
                print(f"   Botão {i+1}: {elem.get_attribute('outerHTML')[:200]}...")
        except:
            print("❌ Erro ao procurar botões 'Continuar'")
        
        # Procurar por possíveis erros
        try:
            error_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'erro') or contains(text(), 'Erro') or contains(text(), 'error') or contains(text(), 'Error')]")
            print(f"⚠️ Elementos de erro encontrados: {len(error_elements)}")
            
            for i, elem in enumerate(error_elements):
                print(f"   Erro {i+1}: {elem.text[:100]}...")
        except:
            print("✅ Nenhum elemento de erro encontrado")
        
        # Salvar HTML completo para análise
        print("\n💾 **HTML COMPLETO SALVO PARA ANÁLISE:**")
        print(f"�� Arquivo: temp/tela_03/tela_03_apos_clique.html")
        
        print("\n�� **INVESTIGAÇÃO CONCLUÍDA!**")
        print("📁 Verifique os arquivos salvos para análise detalhada")
        
    except Exception as e:
        print(f"❌ **ERRO DURANTE INVESTIGAÇÃO:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    investigar_tela5()
