#!/usr/bin/env python3
"""
Automação RPA completa para ToSegurado
Sistema de cotação de seguros automotivos
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

class ToSeguradoAutomation:
    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configurar Chrome Driver"""
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
        chrome_options.add_argument('--remote-debugging-port=9222')
        
        # Adicionar diretório único para evitar conflitos
        chrome_options.add_argument(f'--user-data-dir=/tmp/chrome_profile_{int(time.time())}')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 20)
            logger.info("✅ Chrome Driver iniciado com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao iniciar Chrome Driver: {e}")
            return False
    
    def navigate_to_tosegurado(self):
        """Navegar para ToSegurado"""
        try:
            logger.info("�� Navegando para ToSegurado...")
            self.driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
            time.sleep(3)
            logger.info("✅ Página inicial carregada")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao navegar para ToSegurado: {e}")
            return False
    
    def select_car_insurance(self):
        """Selecionar seguro de carro"""
        try:
            logger.info("🚗 Selecionando seguro de carro...")
            # Aguardar carregamento da página
            time.sleep(2)
            
            # Procurar por botão ou link de carro
            car_selectors = [
                "//div[contains(text(), 'Carro')]",
                "//button[contains(text(), 'Carro')]",
                "//a[contains(text(), 'Carro')]",
                "//div[contains(@class, 'car')]",
                "//div[contains(@class, 'auto')]"
            ]
            
            for selector in car_selectors:
                try:
                    car_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    car_element.click()
                    logger.info("✅ Seguro de carro selecionado")
                    time.sleep(3)
                    return True
                except:
                    continue
            
            logger.error("❌ Não foi possível selecionar seguro de carro")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao selecionar seguro de carro: {e}")
            return False
    
    def enter_license_plate(self, plate):
        """Inserir placa do veículo"""
        try:
            logger.info(f"�� Inserindo placa: {plate}")
            
            # Aguardar campo de placa
            plate_selectors = [
                "//input[@placeholder*='placa' or @placeholder*='Placa']",
                "//input[contains(@name, 'placa')]",
                "//input[@id*='placa']"
            ]
            
            plate_input = None
            for selector in plate_selectors:
                try:
                    plate_input = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except:
                    continue
            
            if not plate_input:
                logger.error("❌ Campo de placa não encontrado")
                return False
            
            # Limpar e inserir placa
            plate_input.clear()
            plate_input.send_keys(plate)
            time.sleep(1)
            
            # Clicar em continuar
            continue_selectors = [
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'continuar')]",
                "//a[contains(text(), 'Continuar')]"
            ]
            
            for selector in continue_selectors:
                try:
                    continue_btn = self.driver.find_element(By.XPATH, selector)
                    continue_btn.click()
                    logger.info("✅ Placa inserida e continuar clicado")
                    time.sleep(3)
                    return True
                except:
                    continue
            
            logger.error("❌ Botão continuar não encontrado")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao inserir placa: {e}")
            return False
    
    def run_simple_test(self):
        """Executar teste simples"""
        try:
            logger.info("🧪 Executando teste simples...")
            
            # Setup do driver
            if not self.setup_driver():
                return None
            
            # Navegar para ToSegurado
            if not self.navigate_to_tosegurado():
                return None
            
            # Capturar screenshot da página inicial
            try:
                screenshot_path = f"/opt/imediatoseguros-rpa/screenshots/homepage_{int(time.time())}.png"
                self.driver.save_screenshot(screenshot_path)
                logger.info(f"📸 Screenshot da página inicial salvo: {screenshot_path}")
            except:
                logger.warning("⚠️ Não foi possível salvar screenshot")
            
            # Fechar driver
            if self.driver:
                self.driver.quit()
            
            return {
                'success': True,
                'message': 'Teste simples executado com sucesso'
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
    """Executar teste simples no ToSegurado"""
    automation = ToSeguradoAutomation(headless=True)  # True para evitar conflitos
    return automation.run_simple_test()

if __name__ == "__main__":
    # Teste simples da automação
    result = execute_simple_test()
    print("Resultado:", result)
