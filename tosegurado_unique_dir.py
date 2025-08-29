#!/usr/bin/env python3
"""
Debug com diretório único para cada execução
"""

import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def debug_tosegurado_unique():
    try:
        print("🚀 Iniciando debug com diretório único...")
        
        # Criar diretório único baseado no timestamp
        unique_dir = f"/tmp/chrome_debug_{int(time.time())}"
        os.makedirs(unique_dir, exist_ok=True)
        print(f"📁 Diretório único criado: {unique_dir}")
        
        # Configurações com diretório único
        chrome_options = Options()
# flags auto-add
chrome_options.add_argument("--remote-debugging-port=0")
# flags auto-add
chrome_options.add_argument("--headless=new")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument(f'--user-data-dir={unique_dir}')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        
        print("🔧 Configurando Chrome Driver...")
        
        print("🚀 Iniciando Chrome...")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(" Navegando para ToSegurado...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        
        print("⏳ Aguardando carregamento...")
        time.sleep(10)
        
        print("📸 Capturando screenshot...")
        driver.save_screenshot("/opt/imediatoseguros-rpa/screenshots/debug_unique_dir.png")
        
        print("⏸️ Pausa para análise - Pressione Enter para continuar...")
        input()
        
        print("✅ Debug concluído!")
        driver.quit()
        
        # Limpar diretório único
        os.system(f"rm -rf {unique_dir}")
        print(f"🧹 Diretório único removido: {unique_dir}")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        if 'driver' in locals():
            driver.quit()
        if 'unique_dir' in locals():
            os.system(f"rm -rf {unique_dir}")

if __name__ == "__main__":
    debug_tosegurado_unique()
