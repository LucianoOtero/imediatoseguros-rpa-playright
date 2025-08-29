#!/usr/bin/env python3
"""
INVESTIGAÇÃO ESPECÍFICA DA TRANSIÇÃO TELA 3 → TELA 4
===============================================================================
🎯 OBJETIVO: Identificar por que a Tela 4 não carrega após Tela 3
⚡ MÉTODO: Aguardar mais tempo + Verificar elementos + Debug detalhado
📊 RESULTADO: Capturar estado exato da transição
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
    print(f"📱 **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def investigar_transicao_tela3_tela4():
    """Investiga a transição da Tela 3 para Tela 4"""
    print("🔍 **INVESTIGANDO TRANSIÇÃO TELA 3 → TELA 4**")
    print("=" * 80)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 3
        print("\n�� Navegando até Tela 3...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        time.sleep(5)
        
        botao_carro = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        botao_carro.click()
        print("✅ Carro selecionado")
        
        time.sleep(10)
        salvar_estado_tela(driver, 1, "apos_carro", temp_dir)
        
        # Tela 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        time.sleep(5)
        
        campo_placa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys("EED3D56")
        print("✅ Placa inserida")
        
        time.sleep(5)
        salvar_estado_tela(driver, 2, "placa_inserida", temp_dir)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        time.sleep(5)
        
        botao_continuar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        botao_continuar.click()
        print("✅ Continuar clicado")
        
        # AGUARDAR MAIS TEMPO PARA TRANSIÇÃO
        print("\n⏳ AGUARDANDO TRANSIÇÃO PARA TELA 4...")
        print("⏰ Aguardando 30 segundos para transição completa...")
        
        for i in range(30):
            print(f"⏳ Aguardando... {i+1}/30 segundos")
            time.sleep(1)
            
            # Verificar se mudou para Tela 4
            try:
                # Procurar por elementos da Tela 4
                elementos_tela4 = driver.find_elements(By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]")
                if elementos_tela4:
                    print(f"🎯 TELA 4 DETECTADA no segundo {i+1}!")
                    salvar_estado_tela(driver, 4, "detectada_automaticamente", temp_dir)
                    break
            except:
                pass
        
        # Salvar estado final
        print("\n📸 Salvando estado final...")
        salvar_estado_tela(driver, 3, "estado_final_apos_continuar", temp_dir)
        
        # Verificar elementos da página atual
        print("\n�� ANALISANDO ELEMENTOS DA PÁGINA ATUAL...")
        print(f"�� URL atual: {driver.current_url}")
        print(f"📄 Título atual: {driver.title}")
        
        # Procurar por elementos específicos
        elementos_segurado = driver.find_elements(By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]")
        print(f"🎯 Elementos 'segurado' encontrados: {len(elementos_segurado)}")
        
        if elementos_segurado:
            for i, elem in enumerate(elementos_segurado[:3]):  # Primeiros 3
                print(f"  {i+1}. Texto: {elem.text[:100]}...")
        
        # Procurar por botões
        botoes = driver.find_elements(By.TAG_NAME, "button")
        print(f"�� Botões encontrados: {len(botoes)}")
        
        for i, botao in enumerate(botoes[:5]):  # Primeiros 5
            try:
                texto = botao.text.strip()
                if texto:
                    print(f"  {i+1}. Botão: '{texto}'")
            except:
                pass
        
        print("\n✅ **INVESTIGAÇÃO CONCLUÍDA!**")
        print("📁 Verifique os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        
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
    investigar_transicao_tela3_tela4()
