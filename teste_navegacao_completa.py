#!/usr/bin/env python3
"""
Teste de navegação completa até a Tela 6
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    """Configura o driver do Chrome"""
    print("🔧 Configurando Chrome...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            print("✅ Usando ChromeDriver local...")
            service = Service(chromedriver_path)
        else:
            print("❌ ChromeDriver local não encontrado")
            return None
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver configurado com sucesso")
        return driver
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        return None

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return None

def navegar_ate_tela6(driver, parametros):
    """Navega desde o início até a Tela 6"""
    print("\n🧭 NAVEGAÇÃO COMPLETA ATÉ TELA 6")
    print("=" * 50)
    
    try:
        # TELA 1: Página inicial
        print("\n📱 TELA 1: Página inicial...")
        driver.get(parametros['url_base'])
        time.sleep(5)
        
        # Clicar em "Carro"
        print("⏳ Clicando em 'Carro'...")
        try:
            botao_carro = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Carro')]"))
            )
            botao_carro.click()
            print("✅ Botão Carro clicado")
        except Exception as e:
            print(f"❌ Erro ao clicar em Carro: {e}")
            return False
        
        time.sleep(5)
        print(f"📍 URL após Tela 1: {driver.current_url}")
        
        # TELA 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        try:
            campo_placa = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
            )
            campo_placa.clear()
            campo_placa.send_keys(parametros['placa'])
            print(f"✅ Placa {parametros['placa']} inserida")
        except Exception as e:
            print(f"❌ Erro na Tela 2: {e}")
            return False
        
        time.sleep(3)
        print(f"📍 URL após Tela 2: {driver.current_url}")
        
        # TELA 3: Confirmar veículo
        print("\n📱 TELA 3: Confirmando veículo...")
        try:
            # Aguardar carregamento
            time.sleep(5)
            
            # Procurar botão Continuar
            botao_continuar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
            )
            botao_continuar.click()
            print("✅ Botão Continuar clicado na Tela 3")
        except Exception as e:
            print(f"❌ Erro na Tela 3: {e}")
            return False
        
        time.sleep(10)
        print(f"📍 URL após Tela 3: {driver.current_url}")
        
        # TELA 4: Veículo segurado
        print("\n📱 TELA 4: Veículo já segurado...")
        try:
            # Aguardar carregamento
            time.sleep(5)
            
            # Selecionar "Não"
            radio_nao = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//input[@type='radio' and contains(@value, 'Não')]"))
            )
            radio_nao.click()
            print("✅ Radio 'Não' selecionado")
            
            # Clicar Continuar
            botao_continuar = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
            )
            botao_continuar.click()
            print("✅ Botão Continuar clicado na Tela 4")
        except Exception as e:
            print(f"❌ Erro na Tela 4: {e}")
            return False
        
        time.sleep(10)
        print(f"📍 URL após Tela 4: {driver.current_url}")
        
        # TELA 5: Estimativa
        print("\n📱 TELA 5: Estimativa inicial...")
        try:
            # Aguardar carregamento
            time.sleep(5)
            
            # Clicar Continuar
            botao_continuar = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
            )
            botao_continuar.click()
            print("✅ Botão Continuar clicado na Tela 5")
        except Exception as e:
            print(f"❌ Erro na Tela 5: {e}")
            return False
        
        time.sleep(10)
        print(f"📍 URL após Tela 5: {driver.current_url}")
        
        # TELA 6: Combustível
        print("\n📱 TELA 6: Tipo de combustível...")
        try:
            # Aguardar carregamento
            time.sleep(5)
            
            # Verificar se chegamos na Tela 6
            html = driver.page_source
            if "combustível" in html.lower() or "combustivel" in html.lower():
                print("✅ TELA 6 ALCANÇADA! Texto 'combustível' encontrado!")
                
                # Listar textos da Tela 6
                elementos = driver.find_elements(By.XPATH, "//*[text()]")
                textos = [elem.text.strip() for elem in elementos if elem.text.strip()]
                print(f"📝 Textos da Tela 6 ({len(textos)}):")
                for i, texto in enumerate(textos[:15]):  # Primeiros 15
                    print(f"   {i+1}: {texto}")
                
                return True
            else:
                print("❌ TELA 6 NÃO ALCANÇADA!")
                print("📝 Últimos textos encontrados:")
                elementos = driver.find_elements(By.XPATH, "//*[text()]")
                textos = [elem.text.strip() for elem in elementos if elem.text.strip()]
                for i, texto in enumerate(textos[-10:]):  # Últimos 10
                    print(f"   {i+1}: {texto}")
                return False
                
        except Exception as e:
            print(f"❌ Erro na Tela 6: {e}")
            return False
        
    except Exception as e:
        print(f"❌ Erro geral na navegação: {e}")
        return False

def main():
    """Função principal"""
    print("🧭 TESTE DE NAVEGAÇÃO COMPLETA ATÉ TELA 6")
    print("=" * 50)
    
    # Configurar driver
    driver = configurar_driver()
    if not driver:
        return
    
    try:
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            return
        
        # Navegar até Tela 6
        sucesso = navegar_ate_tela6(driver, parametros)
        
        if sucesso:
            print("\n🎉 NAVEGAÇÃO ATÉ TELA 6 CONCLUÍDA COM SUCESSO!")
        else:
            print("\n❌ NAVEGAÇÃO ATÉ TELA 6 FALHOU!")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("✅ Driver fechado")

if __name__ == "__main__":
    main()
