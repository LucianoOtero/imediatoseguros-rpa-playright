#!/usr/bin/env python3
"""
INVESTIGADOR COMPLETO TELA 5 - ANÁLISE DETALHADA
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

def investigar_completo_tela5():
    print("🔍 **INVESTIGADOR COMPLETO TELA 5**")
    print("=" * 50)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="investigar_completo_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # Navegar até Tela 5
        print("\n **Navegando até Tela 5...**")
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
        
        print("   ✅ Tela 5 carregada")
        
        # INVESTIGAÇÃO COMPLETA
        print("\n **INVESTIGAÇÃO COMPLETA:**")
        
        # 1. Verificar se o elemento existe
        print("\n1️⃣ **VERIFICANDO EXISTÊNCIA DO ELEMENTO:**")
        try:
            sim_radio = driver.find_element(By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']")
            print("   ✅ Elemento 'Sim' encontrado na página")
            print(f"   �� Atributos: value='{sim_radio.get_attribute('value')}', type='{sim_radio.get_attribute('type')}', name='{sim_radio.get_attribute('name')}'")
            print(f"   📋 Visible: {sim_radio.is_displayed()}, Enabled: {sim_radio.is_enabled()}")
        except Exception as e:
            print(f"   ❌ Elemento 'Sim' NÃO encontrado: {e}")
        
        # 2. Verificar se está clicável
        print("\n2️⃣ **VERIFICANDO SE ESTÁ CLICÁVEL:**")
        try:
            sim_radio_clicavel = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']"
            )))
            print("   ✅ Elemento 'Sim' está clicável")
        except Exception as e:
            print(f"   ❌ Elemento 'Sim' NÃO está clicável: {e}")
        
        # 3. Verificar se está visível
        print("\n3️⃣ **VERIFICANDO VISIBILIDADE:**")
        try:
            sim_radio_visivel = wait.until(EC.visibility_of_element_located((
                By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']"
            )))
            print("   ✅ Elemento 'Sim' está visível")
        except Exception as e:
            print(f"   ❌ Elemento 'Sim' NÃO está visível: {e}")
        
        # 4. Tentar clicar com JavaScript
        print("\n4️⃣ **TENTANDO CLICAR COM JAVASCRIPT:**")
        try:
            sim_radio = driver.find_element(By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']")
            driver.execute_script("arguments[0].click();", sim_radio)
            print("   ✅ Clique com JavaScript executado")
            
            # Verificar se foi selecionado
            if sim_radio.is_selected():
                print("   ✅ Radio button 'Sim' foi selecionado com sucesso!")
            else:
                print("   ❌ Radio button 'Sim' NÃO foi selecionado")
                
        except Exception as e:
            print(f"   ❌ Erro ao clicar com JavaScript: {e}")
        
        # 5. Salvar arquivos para análise
        print("\n5️⃣ **SALVANDO ARQUIVOS:**")
        html_path = "/opt/imediatoseguros-rpa/temp/investigacao_completa_tela5.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"   📄 HTML salvo: {html_path}")
        
        screenshot_path = "/opt/imediatoseguros-rpa/temp/investigacao_completa_tela5.png"
        driver.save_screenshot(screenshot_path)
        print(f"   📸 Screenshot salvo: {screenshot_path}")
        
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
    investigar_completo_tela5()
