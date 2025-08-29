#!/usr/bin/env python3
"""
RPA Tô Segurado - Continuando da Tela 9 (AUTOCOMPLETE FUNCIONANDO)
Continua o fluxo a partir da Tela 9 com autocomplete automático
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
    """Configura o Chrome com opções otimizadas"""
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

def navegar_ate_tela8(driver):
    """Navega até a Tela 8 (tipo de combustível)"""
    print("🚀 **NAVEGANDO ATÉ TELA 8...**")
    
    # Tela 1: Selecionar Carro
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    time.sleep(3)
    
    carro_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
    )
    carro_button.click()
    print("✅ Tela 1: Carro selecionado")
    time.sleep(2)
    
    # Tela 2: Inserir placa
    placa_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "placaTelaPlaca"))
    )
    placa_input.clear()
    placa_input.send_keys("EED3D56")
    print("✅ Tela 2: Placa EED3D56 inserida")
    time.sleep(2)
    
    # Tela 3: Clicar Continuar
    continuar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_button.click()
    print("✅ Tela 3: Continuar clicado")
    time.sleep(3)
    
    # Tela 5: Confirmar veículo
    sim_radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
    )
    driver.execute_script("arguments[0].click();", sim_radio)
    print("✅ Tela 5: Veículo confirmado")
    time.sleep(2)
    
    # Tela 6: Veículo já segurado
    nao_radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Não']"))
    )
    driver.execute_script("arguments[0].click();", nao_radio)
    print("✅ Tela 6: Continuar clicado")
    time.sleep(2)
    
    # Clicar Continuar na Tela 6
    continuar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
    continuar_button.click()
    print("✅ Continuar clicado na Tela 6")
    time.sleep(3)
    
    # Tela 7: Aguardar carregamento da estimativa
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa inicial')]"))
    )
    print("✅ Tela 7 carregada - estimativa inicial")
    time.sleep(2)
    
    # Clicar Continuar na Tela 7
    continuar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
    continuar_button.click()
    print("✅ Continuar clicado na Tela 7")
    time.sleep(3)
    
    # Tela 8: Tipo de combustível
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tipo de Combustível')]"))
    )
    print("✅ Tela 8 carregada - tipo de combustível")
    time.sleep(2)
    
    # Selecionar Flex
    flex_radio = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Flex']"))
    )
    flex_radio.click()
    print("✅ Flex selecionado na Tela 8")
    time.sleep(2)
    
    # Clicar Continuar na Tela 8
    continuar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
    )
    continuar_button.click()
    print("✅ Continuar clicado na Tela 8")
    time.sleep(3)

def preencher_tela9_autocomplete(driver):
    """Preenche a Tela 9 usando autocomplete automático"""
    print("\n�� **PREENCHENDO TELA 9 COM AUTOCOMPLETE...**")
    
    # Aguardar Tela 9 carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Onde o carro passa a noite')]"))
    )
    print("✅ Tela 9 carregada - endereço onde o carro passa a noite")
    time.sleep(2)
    
    # Encontrar campo CEP
    cep_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "enderecoTelaEndereco"))
    )
    print("✅ Campo CEP encontrado")
    
    # Limpar campo e digitar CEP completo (para ativar autocomplete)
    cep_input.clear()
    cep_input.send_keys("03084-000")  # CEP de São Paulo
    print("✅ CEP 03084-000 digitado")
    time.sleep(3)  # Aguardar autocomplete abrir
    
    # Aguardar sugestões aparecerem
    try:
        sugestao = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'São Paulo')]"))
        )
        print("✅ Sugestão de endereço detectada")
        
        # Clicar na primeira sugestão (geralmente a mais relevante)
        sugestao.click()
        print("✅ Sugestão selecionada")
        time.sleep(2)
        
    except Exception as e:
        print(f"⚠️ Não foi possível selecionar sugestão automaticamente: {e}")
        print("�� Tentando preencher manualmente...")
        
        # Se não conseguir selecionar, preencher manualmente
        cep_input.clear()
        cep_input.send_keys("Rua Serra de Botucatu, Tatuapé - São Paulo/SP")
        print("✅ Endereço preenchido manualmente")
        time.sleep(2)
    
    # Verificar se o endereço foi preenchido
    endereco_preenchido = cep_input.get_attribute("value")
    print(f"📝 Endereço preenchido: {endereco_preenchido}")
    
    # Salvar HTML da Tela 9
    with open("/opt/imediatoseguros-rpa/temp/tela9-endereco-preenchido.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("�� HTML da Tela 9 salvo")
    
    # Clicar em Continuar
    continuar_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "gtm-telaPernoiteVeiculoContinuar"))
    )
    continuar_button.click()
    print("✅ Continuar clicado na Tela 9")
    time.sleep(3)
    
    # Verificar se avançou para próxima tela
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'uso do veículo')]"))
        )
        print("✅ Tela 10 carregada - uso do veículo")
        return True
    except:
        print("❌ Tela 10 não carregou")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - CONTINUANDO DA TELA 9 (AUTOCOMPLETE FUNCIONANDO)**")
    print("=" * 70)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 8
        navegar_ate_tela8(driver)
        
        # Preencher Tela 9 com autocomplete
        sucesso = preencher_tela9_autocomplete(driver)
        
        if sucesso:
            print("\n�� **TELA 9 CONCLUÍDA COM SUCESSO!**")
            print("✅ Endereço preenchido com autocomplete")
            print("✅ Navegou para Tela 10")
        else:
            print("\n❌ **PROBLEMA NA TELA 9**")
            print("❌ Não foi possível avançar para Tela 10")
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-tela9-autocomplete.png")
            print("�� Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
