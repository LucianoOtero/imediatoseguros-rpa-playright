#!/usr/bin/env python3
"""
Debug SIMPLES do ToSegurado - Sem conflitos
"""

import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def debug_tosegurado():
    try:
        print("🚀 Iniciando debug visual do ToSegurado...")
        
        # Configurações mínimas do Chrome
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
        
        print("🔧 Configurando Chrome Driver...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print("�� Navegando para ToSegurado...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        
        print("⏳ Aguardando carregamento...")
        time.sleep(10)
        
        print("📸 Capturando screenshot...")
        driver.save_screenshot("/opt/imediatoseguros-rpa/screenshots/debug_simple.png")
        
        print("⏸️ Pausa para análise visual - Pressione Enter para continuar...")
        input()
        
        print("✅ Debug concluído!")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    debug_tosegurado()
