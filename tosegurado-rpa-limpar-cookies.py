#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - LIMPANDO COOKIES E SESSÃO
===============================================================================
🎯 OBJETIVO: Limpar cookies para evitar redirecionamento automático
⚡ MÉTODO: Chrome com dados limpos + nova sessão
📊 RESULTADO: Navegação limpa sem interferência de sessões anteriores
===============================================================================
"""

import time
import tempfile
import shutil
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome_limpo():
    """Configura o Chrome SEM cookies e dados de sessão"""
    print("🔧 Configurando Chrome LIMPO (sem cookies)...")
    
    temp_dir = tempfile.mkdtemp()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--disable-features=VizDisplayCompositor")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # LIMPAR TODOS OS COOKIES E DADOS
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--disable-application-cache")
    chrome_options.add_argument("--disable-offline-load-stale-cache")
    chrome_options.add_argument("--disk-cache-size=0")
    chrome_options.add_argument("--media-cache-size=0")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Limpar cookies via JavaScript
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver, temp_dir

def limpar_cookies_manualmente(driver):
    """Limpa cookies manualmente via JavaScript"""
    print("🧹 Limpando cookies manualmente...")
    
    try:
        # Limpar todos os cookies
        driver.delete_all_cookies()
        
        # Limpar localStorage e sessionStorage
        driver.execute_script("window.localStorage.clear();")
        driver.execute_script("window.sessionStorage.clear();")
        
        # Limpar cache
        driver.execute_script("""
            if ('caches' in window) {
                caches.keys().then(function(names) {
                    for (let name of names) caches.delete(name);
                });
            }
        """)
        
        print("✅ Cookies e dados limpos!")
        return True
        
    except Exception as e:
        print(f"⚠️ Erro ao limpar cookies: {e}")
        return False

def testar_navegacao_limpa():
    """Testa navegação com cookies limpos"""
    print("🧪 **TESTANDO NAVEGAÇÃO COM COOKIES LIMPOS**")
    print("=" * 80)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome limpo
        driver, temp_dir = configurar_chrome_limpo()
        print("✅ Chrome limpo configurado")
        
        # Navegar para o site
        print("\n🌐 Navegando para o site...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        # Limpar cookies manualmente
        limpar_cookies_manualmente(driver)
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        
        botao_carro = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        botao_carro.click()
        print("✅ Carro selecionado")
        
        time.sleep(10)
        
        # Tela 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        
        campo_placa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys("EED3D56")
        print("✅ Placa inserida: EED3D56")
        
        time.sleep(5)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        
        botao_continuar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        botao_continuar.click()
        print("✅ Continuar clicado")
        
        # AGUARDAR TRANSIÇÃO
        print("\n⏳ Aguardando transição para Tela 4...")
        time.sleep(15)
        
        # Verificar se mudou para Tela 4
        print(f"�� URL atual: {driver.current_url}")
        print(f"📄 Título atual: {driver.title}")
        
        # Procurar por elementos da Tela 4
        elementos_segurado = driver.find_elements(By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]")
        print(f"🎯 Elementos 'segurado' encontrados: {len(elementos_segurado)}")
        
        if elementos_segurado:
            print("✅ TELA 4 DETECTADA! Cookies limpos funcionaram!")
        else:
            print("❌ TELA 4 ainda não detectada")
            
        # Salvar estado final
        timestamp = datetime.now().strftime("%H:%M:%S")
        os.makedirs("temp/teste_cookies_limpos", exist_ok=True)
        
        with open("temp/teste_cookies_limpos/resultado.txt", "w", encoding="utf-8") as f:
            f.write(f"TESTE COOKIES LIMPOS - {timestamp}\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Elementos segurado: {len(elementos_segurado)}\n")
        
        print("\n✅ **TESTE CONCLUÍDO!**")
        print("�� Resultado salvo em: temp/teste_cookies_limpos/")
        
    except Exception as e:
        print(f"❌ **ERRO DURANTE TESTE:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    testar_navegacao_limpa()
