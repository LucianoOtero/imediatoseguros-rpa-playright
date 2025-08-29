#!/usr/bin/env python3
"""
RPA CONTINUANDO DA TELA 7 - TÔ SEGURADO
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

def continuar_da_tela7():
    print("🚀 **CONTINUANDO RPA DA TELA 7**")
    print("=" * 50)
    
    try:
        # Configurar Chrome
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        temp_dir = tempfile.mkdtemp(prefix="continuar_tela7_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # Navegar até Tela 7
        print("\n **Navegando até Tela 7...**")
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
        
        # TELA 5: Confirmar veículo com JavaScript
        if "COROLLA" in driver.page_source:
            print("   ✅ Tela 5 carregada - confirmando veículo...")
            sim_radio = driver.find_element(By.XPATH, "//input[@value='Sim' and @name='confirmarVeiculoTelaInformacoesVeiculo']")
            driver.execute_script("arguments[0].click();", sim_radio)
            print("   ✅ Veículo confirmado")
            
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            time.sleep(3)
        
        # TELA 6: Selecionar "Não" para seguro vigente
        if "Esse veículo já está segurado?" in driver.page_source:
            print("   ✅ Tela 6 carregada - selecionando 'Não'...")
            nao_radio = driver.find_element(By.XPATH, "//input[@value='nao' and @name='jaSeguradoTelaRenovacao']")
            if not nao_radio.is_selected():
                driver.execute_script("arguments[0].click();", nao_radio)
                print("   ✅ Radio 'Não' selecionado")
            else:
                print("   ✅ Radio 'Não' já estava selecionado")
            
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            time.sleep(3)
        
        # TELA 7: Verificar se carregou
        if "estimativa inicial para o seu seguro carro" in driver.page_source:
            print("   ✅ Tela 7 carregada!")
            print("   📊 Carrossel de coberturas exibido")
            
            # Clicar em Continuar para ir para Tela 8
            print("\n **Tela 7:** Clicando em 'Continuar' para próxima tela...")
            continuar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']")))
            continuar_button.click()
            print("   ✅ Continuar clicado")
            
            # TELA 8: Aguardar próxima tela
            print("\n **Tela 8:** Aguardando próxima tela...")
            time.sleep(5)
            
            print(f"\n URL atual: {driver.current_url}")
            print(f"📄 Título da página: {driver.title}")
            
            # Salvar arquivos para análise
            html_path = "/opt/imediatoseguros-rpa/temp/tela_8_continuacao.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"\n📄 HTML salvo: {html_path}")
            
            screenshot_path = "/opt/imediatoseguros-rpa/temp/tela_8_continuacao.png"
            driver.save_screenshot(screenshot_path)
            print(f"📸 Screenshot salvo: {screenshot_path}")
            
            print("\n🎉 **RPA EXECUTADO COM SUCESSO!**")
            print("✅ Navegou pelas 8 primeiras telas")
            print("✅ Confirmou o veículo COROLLA XEI")
            print("✅ Selecionou 'Não' para seguro vigente")
            print("✅ Visualizou carrossel de coberturas")
            print("✅ Avançou para a Tela 8")
            
            return True
        else:
            print("   ❌ Tela 7 NÃO carregou")
            return False
        
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
    continuar_da_tela7()
