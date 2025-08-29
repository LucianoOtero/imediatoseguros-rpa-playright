#!/usr/bin/env python3
"""
RPA CONTINUANDO - TELA 5 EM DIANTE
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import shutil

def continuar_rpa():
    print("🚀 **CONTINUANDO RPA - TELA 5**")
    print("=" * 40)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="continuar_rpa_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # Navegar até Tela 5 (confirmação do veículo)
        print("\n **Tela 1:** Navegando...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        
        print("\n **Tela 2:** Clicando em Carro...")
        carro_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]")))
        carro_button.click()
        time.sleep(3)
        
        print("\n **Tela 3:** Preenchendo placa...")
        placa_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']")))
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("   ✅ Placa preenchida")
        
        print("\n **Tela 4:** Clicando em Continuar...")
        continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
        continuar_button.click()
        print("   ✅ Continuar clicado")
        
        # Aguardar redirecionamento e carregamento da Tela 5
        print("\n **Tela 5:** Aguardando confirmação do veículo...")
        time.sleep(5)
        
        # Verificar se estamos na tela de confirmação do veículo
        if "COROLLA XEI" in driver.page_source:
            print("   ✅ Tela de confirmação do veículo carregada!")
            
            # Confirmar o veículo (clicar em "Sim")
            print("\n **Tela 5:** Confirmando veículo...")
            sim_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Sim']")))
            sim_radio.click()
            print("   ✅ Veículo confirmado (Sim)")
            
            # Clicar em Continuar
            print("\n **Tela 5:** Clicando em Continuar...")
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            print("   ✅ Continuar clicado")
            
            # Aguardar próxima tela
            print("\n **Tela 6:** Aguardando próxima tela...")
            time.sleep(5)
            
            print(f"\n�� URL atual: {driver.current_url}")
            print(f"📄 Título: {driver.title}")
            
            # Salvar arquivos
            html_path = "/opt/imediatoseguros-rpa/temp/tela_6_continuacao.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"\n📄 HTML salvo: {html_path}")
            
            screenshot_path = "/opt/imediatoseguros-rpa/temp/tela_6_continuacao.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot salvo: {screenshot_path}")
            
            return True
        else:
            print("   ❌ Tela de confirmação do veículo NÃO carregou")
            return False
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    continuar_rpa()
