#!/usr/bin/env python3
"""
Debug usando Chrome do sistema - Sem webdriver-manager
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def debug_tosegurado_system():
    try:
        print("🚀 Iniciando debug com Chrome do sistema...")
        
        # Configurações mínimas
        chrome_options = Options()
# flags auto-add
chrome_options.add_argument("--remote-debugging-port=0")
# flags auto-add
chrome_options.add_argument("--no-default-browser-check")
# flags auto-add
chrome_options.add_argument("--no-first-run")
# flags auto-add
chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        
        print("🔧 Iniciando Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("�� Navegando para ToSegurado...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        
        print("⏳ Aguardando carregamento...")
        time.sleep(10)
        
        print("📸 Capturando screenshot...")
        driver.save_screenshot("/opt/imediatoseguros-rpa/screenshots/debug_system.png")
        
        print("⏸️ Pausa para análise - Pressione Enter para continuar...")
        input()
        
        print("✅ Debug concluído!")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    debug_tosegurado_system()
