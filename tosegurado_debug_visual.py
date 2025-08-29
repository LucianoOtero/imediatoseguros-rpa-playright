#!/usr/bin/env python3
"""
Automação RPA VISUAL para ToSegurado - MODO DEBUG
Sistema de cotação de seguros automotivos com Chrome visível para debug
"""

import time
import logging
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

class ToSeguradoVisualDebug:
    def __init__(self, headless=False):
        self.headless = headless
        self.driver = None
        self.wait = None

    def setup_driver(self):
        """Configurar Chrome Driver em modo visual para debug"""
        chrome_options = Options()
# flags auto-add
chrome_options.add_argument("--remote-debugging-port=0")
# flags auto-add
chrome_options.add_argument("--headless=new")

        # MODO VISUAL para debug
        if self.headless:
            chrome_options.add_argument('--headless')
        else:
            # Configurações para modo visual
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)

        # Configurações de estabilidade
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-extensions')
        chrome_options.add_argument('--disable-plugins')
        chrome_options.add_argument('--disable-web-security')
        chrome_options.add_argument('--allow-running-insecure-content')
        chrome_options.add_argument('--remote-debugging-port=9222')

        # Diretório único para evitar conflitos
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')

        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            
            # Remover indicadores de automação
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("✅ Chrome Driver iniciado em modo visual para debug")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar Chrome Driver: {e}")
            return False

    def navigate_to_tosegurado(self):
        """Navegar para ToSegurado e aguardar carregamento"""
        try:
            logger.info("�� Navegando para ToSegurado...")
            self.driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
            
            # Aguardar carregamento completo
            time.sleep(8)
            
            # Capturar screenshot da página inicial
            self.capture_debug_screenshot("homepage_loaded")
            
            logger.info("✅ Página inicial carregada")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao navegar para ToSegurado: {e}")
            self.capture_debug_screenshot("navigation_error")
            return False

    def analyze_page_structure(self):
        """Analisar estrutura da página para identificar elementos"""
        try:
            logger.info("🔍 Analisando estrutura da página...")
            
            # Capturar HTML da página
            page_source = self.driver.page_source
            
            # Salvar HTML para análise
            html_path = f"/opt/imediatoseguros-rpa/temp/page_source_{int(time.time())}.html"
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page_source)
            logger.info(f"�� HTML da página salvo em: {html_path}")
            
            # Procurar por elementos relacionados a carro/seguro
            car_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Carro') or contains(text(), 'carro')]")
            auto_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Auto') or contains(text(), 'auto')]")
            seguro_elements = self.driver.find_elements(By.XPATH, "//*[contains(text(), 'Seguro') or contains(text(), 'seguro')]")
            
            logger.info(f"🔍 Elementos encontrados:")
            logger.info(f"   - Carro: {len(car_elements)} elementos")
            logger.info(f"   - Auto: {len(auto_elements)} elementos")
            logger.info(f"   - Seguro: {len(auto_elements)} elementos")
            
            # Capturar screenshot após análise
            self.capture_debug_screenshot("page_analysis")
            
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao analisar página: {e}")
            self.capture_debug_screenshot("analysis_error")
            return False

    def capture_debug_screenshot(self, name):
        """Capturar screenshot para debug"""
        try:
            screenshot_path = f"/opt/imediatoseguros-rpa/screenshots/debug_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot de debug salvo: {screenshot_path}")
        except:
            logger.warning("⚠️ Não foi possível salvar screenshot de debug")

    def run_visual_debug(self):
        """Executar debug visual completo"""
        try:
            logger.info("🧪 Executando debug visual do ToSegurado...")

            # Setup do driver
            if not self.setup_driver():
                return None

            # Navegar para ToSegurado
            if not self.navigate_to_tosegurado():
                return None

            # Analisar estrutura da página
            if not self.analyze_page_structure():
                return None

            # Aguardar interação manual se necessário
            logger.info("⏳ Pausa para análise visual - Pressione Enter para continuar...")
            input()

            # Fechar driver
            if self.driver:
                self.driver.quit()

            return {
                'success': True,
                'message': 'Debug visual executado com sucesso',
                'screenshots': 'Verificar diretório /opt/imediatoseguros-rpa/screenshots/',
                'html': 'Verificar diretório /opt/imediatoseguros-rpa/temp/'
            }

        except Exception as e:
            logger.error(f"❌ Erro no debug visual: {e}")
            if self.driver:
                self.driver.quit()
            return {
                'success': False,
                'error': str(e)
            }

# Função para executar debug visual
def execute_visual_debug():
    """Executar debug visual no ToSegurado"""
    automation = ToSeguradoVisualDebug(headless=False)  # False para modo visual
    return automation.run_visual_debug()

if __name__ == "__main__":
    # Debug visual da automação
    result = execute_visual_debug()
    print("Resultado:", result)
