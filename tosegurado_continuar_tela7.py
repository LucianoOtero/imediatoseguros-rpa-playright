#!/usr/bin/env python3
"""
RPA Tô Segurado - Continuando da Tela 7
Continua o fluxo a partir da Tela 7 (estimativa inicial)
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

def navegar_ate_tela7(driver):
    """Navega até a Tela 7 (estimativa inicial)"""
    print("🚀 **NAVEGANDO ATÉ TELA 7...**")
    
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
    
    # Clicar em Continuar na Tela 6
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 6")
    
    # Aguardar Tela 7 carregar (estimativa inicial)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa inicial')]"))
    )
    print("✅ Tela 7 carregada - estimativa inicial")
    
    return True

def extrair_dados_tela7(driver):
    """Extrai os dados da Tela 7"""
    print("\n📊 **EXTRAINDO DADOS DA TELA 7...**")
    
    try:
        # Salvar HTML da Tela 7
        with open("/opt/imediatoseguros-rpa/temp/tela7_estimativa.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("�� HTML da Tela 7 salvo")
        
        # Extrair valores das coberturas
        coberturas = []
        
        # Buscar por valores
        valores = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
        for valor in valores:
            if "De" in valor.text or "até" in valor.text:
                coberturas.append(valor.text.strip())
        
        # Buscar por tipos de cobertura
        tipos = driver.find_elements(By.XPATH, "//*[contains(text(), 'Cobertura')]")
        
        print(f"💰 Valores encontrados: {len(coberturas)}")
        print(f"🛡️ Tipos de cobertura: {len(tipos)}")
        
        # Salvar dados da Tela 7
        with open("/opt/imediatoseguros-rpa/temp/dados_tela7.txt", "w", encoding="utf-8") as f:
            f.write("=== DADOS DA TELA 7 (ESTIMATIVA INICIAL) ===\n\n")
            f.write("COBERTURAS:\n")
            for tipo in tipos:
                f.write(f"- {tipo.text}\n")
            f.write("\nVALORES:\n")
            for cobertura in coberturas:
                f.write(f"- {cobertura}\n")
        
        print("📝 Dados da Tela 7 salvos")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados da Tela 7: {e}")
        return False

def continuar_tela7(driver):
    """Continua para a próxima tela (Tela 8)"""
    print("\n�� **CONTINUANDO PARA TELA 8...**")
    
    try:
        # Procurar botão Continuar na Tela 7
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 7")
        
        # Aguardar carregamento da próxima tela
        time.sleep(5)
        
        # Verificar se carregou a Tela 8 (tipo de combustível)
        if "Tipo de Combustível" in driver.page_source:
            print("✅ Tela 8 carregada - tipo de combustível")
            return True
        elif "Flex" in driver.page_source and "Gasolina" in driver.page_source:
            print("✅ Tela 8 carregada - opções de combustível detectadas")
            return True
        else:
            print("❌ Tela 8 não carregou como esperado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao continuar da Tela 7: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🚀 **RPA TÔ SEGURADO - CONTINUANDO DA TELA 7**")
        print("=" * 60)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 7
        if not navegar_ate_tela7(driver):
            print("❌ Falha ao navegar até Tela 7")
            return
        
        # Extrair dados da Tela 7
        extrair_dados_tela7(driver)
        
        # Continuar para Tela 8
        if continuar_tela7(driver):
            print("\n�� **TELA 7 CONCLUÍDA COM SUCESSO!**")
            print("✅ Dados extraídos e salvos")
            print("✅ Navegou para Tela 8")
        else:
            print("\n❌ **FALHA AO CONTINUAR PARA TELA 8**")
        
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
