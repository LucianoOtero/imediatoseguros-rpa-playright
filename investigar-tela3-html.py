#!/usr/bin/env python3
"""
INVESTIGAÇÃO HTML DA TELA 3
===============================================================================
🎯 OBJETIVO: Verificar exatamente o que está na Tela 3
⚡ MÉTODO: Salvar HTML completo + Procurar elementos
📊 RESULTADO: Identificar por que radio 'Sim' não aparece
===============================================================================
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

def configurar_chrome_limpo():
    """Configura o Chrome SEM cookies e dados de sessão"""
    print("🔧 Configurando Chrome LIMPO...")
    
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

def investigar_tela3_html():
    """Investiga o HTML da Tela 3"""
    print("🔍 **INVESTIGANDO HTML DA TELA 3**")
    print("=" * 80)
    print("🎯 OBJETIVO: Verificar exatamente o que está na Tela 3")
    print("⚡ MÉTODO: Salvar HTML + Procurar elementos")
    print("=" * 80)
    
    # PLACA REAL PARA TESTE
    PLACA_TESTE = "KVA-1791"
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome limpo
        driver, temp_dir = configurar_chrome_limpo()
        print("✅ Chrome configurado")
        
        # Navegar para o site
        print("\n🌐 Navegando para o site...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        
        botao_carro = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        botao_carro.click()
        print("✅ Carro selecionado")
        
        time.sleep(10)
        
        # Tela 2: Inserir placa KVA-1791
        print(f"\n📱 TELA 2: Inserindo placa: {PLACA_TESTE}")
        
        campo_placa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys(PLACA_TESTE)
        print(f"✅ Placa inserida: {PLACA_TESTE}")
        
        time.sleep(5)
        
        # TELA 3: INVESTIGAR HTML
        print("\n📱 TELA 3: INVESTIGANDO HTML...")
        
        # Aguardar pergunta sobre o veículo aparecer
        print("⏳ Aguardando pergunta sobre o veículo...")
        time.sleep(15)
        
        # Salvar HTML da Tela 3
        timestamp = datetime.now().strftime("%H:%M:%S")
        os.makedirs("temp/investigacao_tela3", exist_ok=True)
        
        html_file = f"temp/investigacao_tela3/tela3_html_{timestamp}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        screenshot_file = f"temp/investigacao_tela3/tela3_screenshot_{timestamp}.png"
        driver.save_screenshot(screenshot_file)
        
        print(f"✅ HTML salvo: {html_file}")
        print(f"📸 Screenshot salvo: {screenshot_file}")
        
        # ANALISAR ELEMENTOS DA PÁGINA
        print("\n�� ANALISANDO ELEMENTOS DA PÁGINA...")
        print(f" URL atual: {driver.current_url}")
        print(f"📄 Título atual: {driver.title}")
        
        # Procurar por elementos específicos
        print("\n�� PROCURANDO ELEMENTOS ESPECÍFICOS...")
        
        # 1. Procurar por texto "ECOSPORT"
        elementos_ecosport = driver.find_elements(By.XPATH, "//*[contains(text(), 'ECOSPORT')]")
        print(f"🚗 Elementos 'ECOSPORT' encontrados: {len(elementos_ecosport)}")
        
        # 2. Procurar por texto "KVA-1791"
        elementos_placa = driver.find_elements(By.XPATH, "//*[contains(text(), 'KVA-1791')]")
        print(f"�� Elementos 'KVA-1791' encontrados: {len(elementos_placa)}")
        
        # 3. Procurar por radio buttons
        radio_buttons = driver.find_elements(By.CSS_SELECTOR, 'input[type="radio"]')
        print(f"📻 Radio buttons encontrados: {len(radio_buttons)}")
        
        # 4. Procurar por labels
        labels = driver.find_elements(By.TAG_NAME, "label")
        print(f"🏷️ Labels encontrados: {len(labels)}")
        
        # 5. Procurar por botão Continuar
        botao_continuar = driver.find_elements(By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar")
        print(f"▶️ Botão Continuar encontrado: {'Sim' if botao_continuar else 'Não'}")
        
        # 6. Procurar por texto "Sim" e "Não"
        elementos_sim = driver.find_elements(By.XPATH, "//*[contains(text(), 'Sim')]")
        elementos_nao = driver.find_elements(By.XPATH, "//*[contains(text(), 'Não')]")
        print(f"✅ Elementos 'Sim' encontrados: {len(elementos_sim)}")
        print(f"❌ Elementos 'Não' encontrados: {len(elementos_nao)}")
        
        # 7. Procurar por pergunta sobre veículo
        elementos_pergunta = driver.find_elements(By.XPATH, "//*[contains(text(), 'corresponde') or contains(text(), 'placa')]")
        print(f"❓ Elementos de pergunta encontrados: {len(elementos_pergunta)}")
        
        # Salvar resultado da investigação
        resultado_file = f"temp/investigacao_tela3/resultado_investigacao_{timestamp}.txt"
        with open(resultado_file, 'w', encoding='utf-8') as f:
            f.write(f"INVESTIGAÇÃO TELA 3 - {timestamp}\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Elementos ECOSPORT: {len(elementos_ecosport)}\n")
            f.write(f"Elementos KVA-1791: {len(elementos_placa)}\n")
            f.write(f"Radio buttons: {len(radio_buttons)}\n")
            f.write(f"Labels: {len(labels)}\n")
            f.write(f"Botão Continuar: {'Sim' if botao_continuar else 'Não'}\n")
            f.write(f"Elementos 'Sim': {len(elementos_sim)}\n")
            f.write(f"Elementos 'Não': {len(elementos_nao)}\n")
            f.write(f"Elementos pergunta: {len(elementos_pergunta)}\n")
        
        print(f"\n✅ Resultado salvo: {resultado_file}")
        
        print("\n✅ **INVESTIGAÇÃO CONCLUÍDA!**")
        print("📁 Verifique os arquivos em: temp/investigacao_tela3/")
        
    except Exception as e:
        print(f"❌ **ERRO DURANTE INVESTIGAÇÃO:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    investigar_tela3_html()
