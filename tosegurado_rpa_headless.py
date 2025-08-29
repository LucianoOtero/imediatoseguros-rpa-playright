#!/usr/bin/env python3
"""
RPA HEADLESS - TÔ SEGURADO - CONFIGURAÇÕES CORRETAS PARA SERVIDOR
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import shutil

def test_chrome_headless():
    """Teste do Chrome em modo headless"""
    print("🚀 **TESTE CHROME HEADLESS - SERVIDOR**")
    print("=" * 50)
    
    try:
        # Configurações CORRETAS para servidor headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # MODO HEADLESS
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Diretório temporário ÚNICO e COMPLETO
        temp_dir = tempfile.mkdtemp(prefix="chrome_headless_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        chrome_options.add_argument(f"--data-path={temp_dir}")
        chrome_options.add_argument(f"--homedir={temp_dir}")
        
        print(f"📁 Diretório temporário criado: {temp_dir}")
        
        # Instalar ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Criar driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome HEADLESS configurado com sucesso!")
        
        # Teste simples
        print("🌐 Navegando para Google...")
        driver.get("https://www.google.com")
        
        print(f"📄 Título: {driver.title}")
        print(f"📄 URL: {driver.current_url}")
        
        time.sleep(3)
        
        print("✅ Teste headless concluído!")
        
        # Fechar
        driver.quit()
        
        # Limpar diretório temporário
        shutil.rmtree(temp_dir, ignore_errors=True)
        print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_chrome_headless()
    
    if success:
        print("\n🎉 **CHROME HEADLESS FUNCIONANDO!**")
        print("Próximo passo: Criar RPA completo headless")
    else:
        print("\n❌ **PROBLEMA NO CHROME HEADLESS**")
