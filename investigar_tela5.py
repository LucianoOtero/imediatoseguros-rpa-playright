#!/usr/bin/env python3
"""
INVESTIGADOR TELA 5 - O QUE ACONTECEU?
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

def investigar_tela5():
    print("🔍 **INVESTIGANDO TELA 5**")
    print("=" * 40)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="investigar_tela5_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # Navegar até Tela 4
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
        
        # INVESTIGAR TELA 5
        print("\n **Tela 5:** INVESTIGANDO...")
        
        # Aguardar e verificar
        for i in range(1, 11):
            print(f"   ⏳ Aguardando {i}s...")
            time.sleep(1)
            
            current_url = driver.current_url
            page_title = driver.title
            page_source = driver.page_source
            
            print(f"   🌐 URL: {current_url}")
            print(f"   📄 Título: {page_title}")
            
            # Verificar se estamos na tela correta
            if "COROLLA" in page_source:
                print("   ✅ Texto 'COROLLA' encontrado!")
                break
            elif "cotacao" in current_url.lower():
                print("   ⚠️ Redirecionado para página de cotação")
                break
            else:
                print("   🔍 Procurando elementos...")
        
        # Salvar arquivos para análise
        html_path = "/opt/imediatoseguros-rpa/temp/investigacao_tela5.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"\n📄 HTML salvo: {html_path}")
        
        screenshot_path = "/opt/imediatoseguros-rpa/temp/investigacao_tela5.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    investigar_tela5()
