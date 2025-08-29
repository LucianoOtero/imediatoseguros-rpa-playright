#!/usr/bin/env python3
"""
INVESTIGADOR TRANSIÇÃO TELA 6 → TELA 7
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

def investigar_transicao_tela6_7():
    print("🔍 **INVESTIGANDO TRANSIÇÃO TELA 6 → TELA 7**")
    print("=" * 60)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="investigar_transicao_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        print("\n **Navegando até Tela 6...**")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        
        carro_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]")))
        carro_button.click()
        time.sleep(3)
        
        placa_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']")))
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        
        continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
        continuar_button.click()
        time.sleep(3)
        
        # TELA 5: Confirmar veículo
        if "COROLLA" in driver.page_source:
            print("   ✅ Tela 5 carregada - confirmando veículo...")
            sim_radio = driver.find_element(By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']")
            driver.execute_script("arguments[0].click();", sim_radio)
            print("   ✅ Veículo confirmado")
            
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            time.sleep(3)
        
        # TELA 6: Verificar e selecionar "Não"
        if "Esse veículo já está segurado?" in driver.page_source:
            print("   ✅ Tela 6 carregada")
            
            # Selecionar "Não"
            nao_radio = driver.find_element(By.XPATH, "//input[@value='nao' and @name='jaSeguradoTelaRenovacao']")
            if not nao_radio.is_selected():
                driver.execute_script("arguments[0].click();", nao_radio)
                print("   ✅ Radio 'Não' selecionado")
            else:
                print("   ✅ Radio 'Não' já estava selecionado")
            
            # INVESTIGAR TRANSIÇÃO
            print("\n **INVESTIGANDO TRANSIÇÃO TELA 6 → TELA 7:**")
            
            # Antes de clicar em Continuar
            print("   �� ANTES de clicar em Continuar:")
            print(f"      🌐 URL: {driver.current_url}")
            print(f"      📄 Título: {driver.title}")
            
            # Clicar em Continuar
            print("\n   ��️ Clicando em 'Continuar'...")
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            print("   ✅ Continuar clicado")
            
            # Monitorar transição em tempo real
            print("\n   �� MONITORANDO TRANSIÇÃO:")
            for i in range(1, 16):  # Monitorar por 15 segundos
                time.sleep(1)
                current_url = driver.current_url
                page_title = driver.title
                page_source = driver.page_source
                
                print(f"      ⏳ {i:2d}s - URL: {current_url}")
                print(f"           Título: {page_title}")
                
                # Verificar se chegamos na Tela 7
                if "estimativa inicial" in page_source.lower():
                    print("      ✅ TELA 7 DETECTADA!")
                    break
                elif "combustível" in page_source.lower():
                    print("      ✅ TELA 8 DETECTADA (pulou Tela 7)!")
                    break
                elif "erro" in page_source.lower():
                    print("      ❌ ERRO detectado na página!")
                    break
                elif i == 15:
                    print("      ⚠️ Timeout - página não carregou completamente")
            
            # Salvar arquivos para análise
            html_path = "/opt/imediatoseguros-rpa/temp/investigacao_transicao_tela6_7.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"\n📄 HTML salvo: {html_path}")
            
            screenshot_path = "/opt/imediatoseguros-rpa/temp/investigacao_transicao_tela6_7.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot salvo: {screenshot_path}")
            
            return True
        else:
            print("   ❌ Tela 6 NÃO carregou")
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
    investigar_transicao_tela6_7()
