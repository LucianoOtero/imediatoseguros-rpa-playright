#!/usr/bin/env python3
"""
Automação RPA SIMPLES para ToSegurado - SEM user-data-dir
Sistema de cotação de seguros automotivos - Versão Simples
"""

import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class ToSeguradoSimpleAutomation:
    def __init__(self, headless=False):  # FALSE para debug visual
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configurar Chrome Driver SEM user-data-dir"""
        chrome_options = Options()
# flags auto-add
chrome_options.add_argument("--remote-debugging-port=0")
# flags auto-add
chrome_options.add_argument("--headless=new")
        
        if self.headless:
            chrome_options.add_argument('--headless')
        
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-images')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        
        # NÃO usar --user-data-dir para evitar conflitos
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("✅ Chrome Driver iniciado com sucesso (SEM user-data-dir)")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar Chrome Driver: {e}")
            return False
    
    def navigate_to_tosegurado(self):
        """Navegar para ToSegurado"""
        try:
            logger.info(" Navegando para ToSegurado...")
            self.driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
            time.sleep(5)
            logger.info("✅ Página inicial carregada")
            
            # Capturar screenshot da página inicial
            self.capture_screenshot("homepage")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao navegar para ToSegurado: {e}")
            return False
    
    def capture_screenshot(self, name):
        """Capturar screenshot para debug"""
        try:
            screenshot_path = f"/opt/imediatoseguros-rpa/screenshots/simple_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot salvo: {screenshot_path}")
        except:
            logger.warning("⚠️ Não foi possível salvar screenshot")
    
    def run_simple_test(self):
        """Executar teste simples"""
        try:
            logger.info("🧪 Executando teste simples (SEM user-data-dir)...")
            
            # Setup do driver
            if not self.setup_driver():
                return None
            
            # Navegar para ToSegurado
            if not self.navigate_to_tosegurado():
                return None
            
            # Aguardar um pouco para visualizar
            logger.info("⏳ Aguardando para visualização...")
            time.sleep(10)
            
            # Fechar driver
            if self.driver:
                self.driver.quit()
            
            return {
                'success': True,
                'message': 'Teste simples executado com sucesso (SEM user-data-dir)'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no teste simples: {e}")
            if self.driver:
                self.driver.quit()
            return {
                'success': False,
                'error': str(e)
            }

# Função para executar teste simples
def execute_simple_test():
    """Executar teste simples no ToSegurado (SEM user-data-dir)"""
    automation = ToSeguradoSimpleAutomation(headless=False)  # FALSE para debug visual
    return automation.run_simple_test()

if __name__ == "__main__":
    # Teste simples da automação
    result = execute_simple_test()
    print("Resultado:", result)
