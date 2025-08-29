#!/usr/bin/env python3
"""
Diagnóstico Detalhado do Erro na Cotação
Analisa exatamente o que está acontecendo na página
"""

import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções headless"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Criar diretório temporário único
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def navegar_ate_tela6(driver):
    """Navega até a Tela 6 (veículo já segurado)"""
    print("🚀 **NAVEGANDO ATÉ TELA 6...**")
    
    # Tela 1: Selecionar Carro
    driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
    time.sleep(3)
    
    carro_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
    )
    carro_btn.click()
    print("✅ Tela 1: Carro selecionado")
    
    # Tela 2: Inserir placa
    placa_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']"))
    )
    placa_input.clear()
    placa_input.send_keys("EED3D56")
    print("✅ Tela 2: Placa EED3D56 inserida")
    
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Tela 3: Continuar clicado")
    
    # Tela 4: Aguardar carregamento
    time.sleep(3)
    
    # Tela 5: Confirmar veículo
    sim_radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
    )
    driver.execute_script("arguments[0].click();", sim_radio)
    print("✅ Tela 5: Veículo confirmado")
    
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Tela 6: Continuar clicado")
    
    # Aguardar Tela 6 carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'já está segurado')]"))
    )
    print("✅ Tela 6 carregada - veículo já segurado")
    
    return True

def investigar_erro_detalhado(driver):
    """Investiga detalhadamente o que está acontecendo"""
    print("\n🔍 **INVESTIGANDO ERRO DETALHADAMENTE...**")
    
    # Clicar em Continuar na Tela 6
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 6")
    
    # Monitorar a página por 30 segundos
    print("⏳ Monitorando página por 30 segundos...")
    
    for i in range(30):
        time.sleep(1)
        
        try:
            current_url = driver.current_url
            current_title = driver.title
            page_source = driver.page_source
            
            # Verificar se apareceu erro
            if "erro" in page_source.lower() or "error" in page_source.lower():
                print(f"❌ ERRO DETECTADO no segundo {i+1}!")
                
                # Salvar HTML com erro
                with open(f"/opt/imediatoseguros-rpa/temp/erro_segundo_{i+1}.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
                print(f"📄 HTML com erro salvo: erro_segundo_{i+1}.html")
                
                # Extrair texto da página
                page_text = driver.find_element(By.TAG_NAME, "body").text
                with open(f"/opt/imediatoseguros-rpa/temp/erro_segundo_{i+1}.txt", "w", encoding="utf-8") as f:
                    f.write(page_text)
                print(f"📝 Texto da página salvo: erro_segundo_{i+1}.txt")
                
                return True
            
            # Verificar se carregou a cotação
            if "Parabéns, chegamos ao resultado final" in page_source:
                print(f"🎉 COTAÇÃO CARREGOU no segundo {i+1}!")
                return False
            
            # Verificar se ainda está carregando
            if "Aguarde! Estamos buscando" in page_source:
                print(f"⏳ Ainda carregando... ({i+1}s)")
                continue
            
            # Verificar mudanças na URL ou título
            if i > 0:
                print(f"�� Segundo {i+1}: URL={current_url[:50]}... | Título={current_title[:50]}...")
            
        except Exception as e:
            print(f"⚠️ Erro durante monitoramento: {e}")
    
    print("⏰ Timeout de 30 segundos atingido")
    return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🔍 **DIAGNÓSTICO DETALHADO DO ERRO - TÔ SEGURADO**")
        print("=" * 60)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        if not navegar_ate_tela6(driver):
            print("❌ Falha ao navegar até Tela 6")
            return
        
        # Investigar erro detalhadamente
        erro_encontrado = investigar_erro_detalhado(driver)
        
        if erro_encontrado:
            print("\n❌ **ERRO IDENTIFICADO E DOCUMENTADO!**")
            print("📁 Verifique os arquivos salvos em /opt/imediatoseguros-rpa/temp/")
        else:
            print("\n✅ **NENHUM ERRO DETECTADO**")
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
