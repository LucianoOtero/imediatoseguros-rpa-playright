#!/usr/bin/env python3
"""
Debug do ToSegurado usando Firefox snap
"""

import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def debug_tosegurado_firefox_snap():
    try:
        print("🚀 Iniciando debug com Firefox snap...")
        
        # Configurações do Firefox com caminho correto
        firefox_options = Options()
# flags auto-add
chrome_options.add_argument("--remote-debugging-port=0")
# flags auto-add
chrome_options.add_argument("--no-default-browser-check")
# flags auto-add
chrome_options.add_argument("--no-first-run")
# flags auto-add
chrome_options.add_argument("--disable-dev-shm-usage")
# flags auto-add
chrome_options.add_argument("--no-sandbox")
# flags auto-add
chrome_options.add_argument("--headless=new")
        firefox_options.binary_location = "/snap/bin/firefox"
        firefox_options.add_argument('--start-maximized')
        firefox_options.add_argument('--disable-extensions')
        
        print("🔧 Iniciando Firefox snap...")
        driver = webdriver.Firefox(options=firefox_options)
        
        print(" Navegando para ToSegurado...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        
        print("⏳ Aguardando carregamento...")
        time.sleep(10)
        
        print("📸 Capturando screenshot...")
        driver.save_screenshot("/opt/imediatoseguros-rpa/screenshots/debug_firefox_snap.png")
        
        print("⏸️ Pausa para análise - Pressione Enter para continuar...")
        input()
        
        print("✅ Debug concluído!")
        driver.quit()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    debug_tosegurado_firefox_snap()
