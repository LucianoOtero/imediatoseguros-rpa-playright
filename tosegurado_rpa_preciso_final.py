#!/usr/bin/env python3
"""
RPA PRECISO FINAL - COM ELEMENTO CORRETO
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

def rpa_preciso_final():
    print("🚀 **RPA PRECISO FINAL - TÔ SEGURADO**")
    print("=" * 50)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="rpa_preciso_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # TELA 1: Navegar
        print("\n **Tela 1:** Navegando para página inicial...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        print("   ✅ Página inicial carregada")
        
        # TELA 2: Clicar em Carro
        print("\n **Tela 2:** Clicando no botão 'Carro'...")
        carro_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]")))
        carro_button.click()
        time.sleep(3)
        print("   ✅ Botão 'Carro' clicado")
        
        # TELA 3: Preencher placa
        print("\n **Tela 3:** Preenchendo formulário de placa...")
        placa_input = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']")))
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("   ✅ Placa preenchida: EED3D56")
        
        # TELA 4: Clicar em Continuar
        print("\n **Tela 4:** Clicando em 'Continuar'...")
        continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        
        # TELA 5: Aguardar confirmação do veículo
        print("\n **Tela 5:** Aguardando confirmação do veículo...")
        time.sleep(5)
        
        # Verificar se estamos na tela correta usando o elemento exato
        veiculo_element = wait.until(EC.presence_of_element_located((
            By.XPATH, "//p[contains(text(), 'O veículo') and contains(text(), 'COROLLA XEI')]"
        )))
        print("   ✅ Tela de confirmação do veículo carregada!")
        print(f"   📋 Texto encontrado: {veiculo_element.text}")
        
        # Confirmar o veículo (clicar em "Sim")
        print("\n **Tela 5:** Confirmando veículo...")
        sim_radio = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Sim']")))
        sim_radio.click()
        print("   ✅ Veículo confirmado (Sim)")
        
        # Clicar em Continuar para ir para Tela 6
        print("\n **Tela 5:** Clicando em 'Continuar' para próxima tela...")
        continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
        continuar_button.click()
        print("   ✅ Continuar clicado")
        
        # TELA 6: Aguardar próxima tela
        print("\n **Tela 6:** Aguardando próxima tela...")
        time.sleep(5)
        
        print(f"\n�� URL atual: {driver.current_url}")
        print(f"📄 Título da página: {driver.title}")
        
        # Salvar arquivos para análise
        html_path = "/opt/imediatoseguros-rpa/temp/tela_6_analise.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"\n📄 HTML salvo: {html_path}")
        
        screenshot_path = "/opt/imediatoseguros-rpa/temp/tela_6_analise.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        print("\n🎉 **RPA EXECUTADO COM SUCESSO!**")
        print("✅ Navegou pelas 6 primeiras telas")
        print("✅ Confirmou o veículo COROLLA XEI")
        print("✅ Avançou para a próxima tela")
        
        return True
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:**")
        print(f"   {e}")
        return False
        
    finally:
        if 'driver' in locals():
            driver.quit()
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    rpa_preciso_final()
