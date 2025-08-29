#!/usr/bin/env python3
"""
Diagnóstico Específico da Tela 9 - Endereço onde o carro passa a noite
Investiga exatamente o que está acontecendo na transição Tela 8 → Tela 9
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

def navegar_ate_tela8(driver):
    """Navega até a Tela 8 (tipo de combustível)"""
    print("🚀 **NAVEGANDO ATÉ TELA 8...**")
    
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
    
    # Clicar em Continuar na Tela 7
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 7")
    
    # Aguardar Tela 8 carregar (tipo de combustível)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tipo de Combustível')]"))
    )
    print("✅ Tela 8 carregada - tipo de combustível")
    
    return True

def investigar_transicao_tela8_9_detalhada(driver):
    """Investiga detalhadamente a transição da Tela 8 para Tela 9"""
    print("\n🔍 **INVESTIGANDO TRANSIÇÃO TELA 8 → TELA 9 (DETALHADA)...**")
    
    try:
        # Selecionar Flex na Tela 8
        flex_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Flex')]"))
        )
        driver.execute_script("arguments[0].click();", flex_radio)
        print("✅ Flex selecionado na Tela 8")
        
        # Salvar estado ANTES de clicar em Continuar
        with open("/opt/imediatoseguros-rpa/temp/tela8_antes_continuar_detalhado.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML da Tela 8 (antes) salvo")
        
        # Verificar se há botão Continuar
        try:
            continuar_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
            )
            print("✅ Botão Continuar encontrado e clicável")
            
            # Verificar se o botão está visível
            if continuar_btn.is_displayed():
                print("✅ Botão Continuar está visível")
            else:
                print("⚠️ Botão Continuar NÃO está visível")
                
        except Exception as e:
            print(f"❌ Erro ao encontrar botão Continuar: {e}")
            return False
        
        # Clicar em Continuar na Tela 8
        try:
            continuar_btn.click()
            print("✅ Continuar clicado na Tela 8")
        except Exception as e:
            print(f"❌ Erro ao clicar em Continuar: {e}")
            # Tentar com JavaScript
            try:
                driver.execute_script("arguments[0].click();", continuar_btn)
                print("✅ Continuar clicado com JavaScript")
            except Exception as e2:
                print(f"❌ Erro também com JavaScript: {e2}")
                return False
        
        # Monitorar a transição por 30 segundos
        print("⏳ Monitorando transição por 30 segundos...")
        
        for i in range(30):
            time.sleep(1)
            
            try:
                current_url = driver.current_url
                current_title = driver.title
                page_source = driver.page_source
                
                # Verificar se apareceu Tela 9
                if "onde o carro passa a noite" in page_source.lower() or "endereço" in page_source.lower():
                    print(f"🎉 TELA 9 DETECTADA no segundo {i+1}!")
                    
                    # Salvar HTML da Tela 9
                    with open(f"/opt/imediatoseguros-rpa/temp/tela9_detectada_segundo_{i+1}_detalhado.html", "w", encoding="utf-8") as f:
                        f.write(page_source)
                    print(f" HTML da Tela 9 salvo: segundo_{i+1}_detalhado.html")
                    
                    return True
                
                # Verificar se ainda está na Tela 8
                if "Tipo de Combustível" in page_source:
                    print(f"⏳ Ainda na Tela 8... ({i+1}s)")
                    continue
                
                # Verificar se apareceu erro
                if "erro" in page_source.lower() or "error" in page_source.lower():
                    print(f"❌ ERRO DETECTADO no segundo {i+1}!")
                    
                    # Salvar HTML com erro
                    with open(f"/opt/imediatoseguros-rpa/temp/erro_segundo_{i+1}_detalhado.html", "w", encoding="utf-8") as f:
                        f.write(page_source)
                    print(f"📄 HTML com erro salvo: erro_segundo_{i+1}_detalhado.html")
                    
                    return False
                
                # Verificar mudanças na URL ou título
                if i > 0:
                    print(f" Segundo {i+1}: URL={current_url[:50]}... | Título={current_title[:50]}...")
                
            except Exception as e:
                print(f"⚠️ Erro durante monitoramento: {e}")
        
        print("⏰ Timeout de 30 segundos atingido")
        return False
        
    except Exception as e:
        print(f"❌ Erro durante investigação: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🔍 **DIAGNÓSTICO ESPECÍFICO TELA 9 - TÔ SEGURADO**")
        print("=" * 70)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 8
        if not navegar_ate_tela8(driver):
            print("❌ Falha ao navegar até Tela 8")
            return
        
        # Investigar transição Tela 8 → Tela 9 detalhadamente
        sucesso = investigar_transicao_tela8_9_detalhada(driver)
        
        if sucesso:
            print("\n✅ **TELA 9 CARREGADA COM SUCESSO!**")
            print("📁 Verifique os arquivos salvos em /opt/imediatoseguros-rpa/temp/")
        else:
            print("\n❌ **PROBLEMA IDENTIFICADO NA TRANSIÇÃO!**")
            print("📁 Verifique os arquivos de erro salvos")
        
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
