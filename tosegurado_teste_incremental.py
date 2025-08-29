#!/usr/bin/env python3
"""
RPA TESTE INCREMENTAL - TÔ SEGURADO - TESTE TELA POR TELA
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

def test_tela_por_tela():
    print("🚀 **TESTE INCREMENTAL - TELA POR TELA**")
    print("=" * 50)
    
    try:
        # Configurar Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        temp_dir = tempfile.mkdtemp(prefix="tosegurado_incremental_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # TELA 1: Navegar para página inicial
        print("\n **Tela 1:** Navegando para página inicial")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        
        if "Qual seguro você deseja cotar?" not in driver.page_source:
            print("   ❌ Página inicial não carregou")
            return False
        print("   ✅ Página inicial carregada")
        
        # TELA 2: Clicar no botão "Carro"
        print("\n **Tela 2:** Clicando no botão 'Carro'")
        carro_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("   ✅ Botão 'Carro' clicado")
        time.sleep(3)
        
        # TELA 3: Verificar formulário de placa
        print("\n **Tela 3:** Verificando formulário de placa")
        if "Qual é a placa do carro?" not in driver.page_source:
            print("   ❌ Tela de placa não carregou")
            return False
        print("   ✅ Tela de placa carregada")
        
        # Preencher placa
        placa_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("   ✅ Placa preenchida: EED3D56")
        
        # TELA 4: TESTE - Tentar clicar em Continuar
        print("\n **Tela 4:** TESTE - Tentando clicar em Continuar")
        
        try:
            # Procurar por diferentes seletores do botão Continuar
            seletores_continuar = [
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(., 'Continuar')]",
                "//button[text()='Continuar']",
                "//button[@type='submit']",
                "//input[@type='submit']"
            ]
            
            continuar_button = None
            for i, seletor in enumerate(seletores_continuar, 1):
                try:
                    print(f"   �� Tentativa {i}: {seletor}")
                    continuar_button = driver.find_element(By.XPATH, seletor)
                    print(f"   ✅ Botão encontrado com seletor: {seletor}")
                    break
                except Exception as e:
                    print(f"   ❌ Seletor {i} falhou: {e}")
                    continue
            
            if continuar_button:
                # Verificar se está clicável
                print("   �� Verificando se botão está clicável...")
                if wait.until(EC.element_to_be_clickable((By.XPATH, seletor))):
                    print("   ✅ Botão está clicável")
                    
                    # Scroll para o elemento
                    driver.execute_script("arguments[0].scrollIntoView(true);", continuar_button)
                    time.sleep(1)
                    
                    # Tentar clicar
                    print("   �� Tentando clicar...")
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado com sucesso!")
                    
                    # Aguardar e verificar próxima tela
                    time.sleep(5)
                    if "O veículo COROLLA XEI" in driver.page_source:
                        print("   ✅ Tela 4 carregou - Confirmação do veículo")
                    else:
                        print("   ⚠️ Próxima tela não identificada")
                        
                else:
                    print("   ❌ Botão não está clicável")
            else:
                print("   ❌ Nenhum botão 'Continuar' encontrado")
                
                # Salvar HTML para análise
                html_path = "/opt/imediatoseguros-rpa/temp/tela_3_erro.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(driver.page_source)
                print(f"   📄 HTML salvo para análise: {html_path}")
                
                # Salvar screenshot
                screenshot_path = "/opt/imediatoseguros-rpa/temp/tela_3_erro.png"
                driver.save_screenshot(screenshot_path)
                print(f"   📸 Screenshot salvo: {screenshot_path}")
                
        except Exception as e:
            print(f"   ❌ Erro ao tentar clicar em Continuar: {e}")
            
            # Salvar HTML para análise
            html_path = "/opt/imediatoseguros-rpa/temp/tela_3_erro_detalhado.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"   �� HTML detalhado salvo: {html_path}")
        
        print("\n✅ **TESTE INCREMENTAL CONCLUÍDO**")
        print("Verifique os arquivos salvos para análise")
        
        return True
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL:** {e}")
        return False
        
    finally:
        # Fechar navegador
        if 'driver' in locals():
            driver.quit()
            print("🔒 Navegador fechado")
            
        # Limpar diretório temporário
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    test_tela_por_tela()
