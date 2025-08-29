#!/usr/bin/env python3
"""
Automação RPA com DEBUG VISUAL para ToSegurado
Sistema de cotação de seguros automotivos - Versão Debug
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

class ToSeguradoDebugAutomation:
    def __init__(self, headless=False):  # FALSE para debug visual
        self.headless = headless
        self.driver = None
        self.wait = None
        
    def setup_driver(self):
        """Configurar Chrome Driver com debug visual"""
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
        
        # Adicionar diretório único para evitar conflitos
        chrome_options.add_argument(f'--user-data-dir=/tmp/chrome_profile_{int(time.time())}')
        chrome_options.add_argument('--no-first-run')
        chrome_options.add_argument('--no-default-browser-check')
        
        try:
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            logger.info("✅ Chrome Driver iniciado com sucesso")
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
    
    def select_car_insurance(self):
        """Selecionar seguro de carro"""
        try:
            logger.info("🚗 Selecionando seguro de carro...")
            time.sleep(3)
            
            # Capturar screenshot antes da seleção
            self.capture_screenshot("before_car_selection")
            
            # Procurar por botão ou link de carro
            car_selectors = [
                "//div[contains(text(), 'Carro')]",
                "//button[contains(text(), 'Carro')]",
                "//a[contains(text(), 'Carro')]",
                "//div[contains(@class, 'car')]",
                "//div[contains(@class, 'auto')]",
                "//div[contains(@class, 'icon') and contains(@class, 'car')]",
                "//div[contains(@class, 'insurance-type')]//div[contains(text(), 'Carro')]",
                "//div[contains(@class, 'option')]//div[contains(text(), 'Carro')]",
                "//div[contains(@class, 'card')]//div[contains(text(), 'Carro')]"
            ]
            
            for selector in car_selectors:
                try:
                    car_element = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    car_element.click()
                    logger.info("✅ Seguro de carro selecionado")
                    time.sleep(5)
                    
                    # Capturar screenshot após seleção
                    self.capture_screenshot("after_car_selection")
                    return True
                except:
                    continue
            
            logger.error("❌ Não foi possível selecionar seguro de carro")
            self.capture_screenshot("car_selection_failed")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao selecionar seguro de carro: {e}")
            self.capture_screenshot("car_selection_error")
            return False
    
    def enter_license_plate(self, plate):
        """Inserir placa do veículo com debug visual"""
        try:
            logger.info(f" Inserindo placa: {plate}")
            
            # Capturar screenshot antes de inserir placa
            self.capture_screenshot("before_plate_input")
            
            # Aguardar campo de placa
            plate_selectors = [
                "//input[@placeholder*='placa' or @placeholder*='Placa']",
                "//input[contains(@name, 'placa')]",
                "//input[@id*='placa']",
                "//input[@type='text']",
                "//input[contains(@class, 'plate')]",
                "//input[contains(@class, 'license')]",
                "//input[@placeholder*='FPG' or @placeholder*='ABC']"
            ]
            
            plate_input = None
            for selector in plate_selectors:
                try:
                    plate_input = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    logger.info(f"✅ Campo de placa encontrado com seletor: {selector}")
                    break
                except:
                    continue
            
            if not plate_input:
                logger.error("❌ Campo de placa não encontrado")
                self.capture_screenshot("plate_field_not_found")
                return False
            
            # Limpar e inserir placa
            plate_input.clear()
            plate_input.send_keys(plate)
            logger.info(f"✅ Placa {plate} inserida")
            time.sleep(2)
            
            # Capturar screenshot após inserir placa
            self.capture_screenshot("after_plate_input")
            
            # Clicar em continuar
            continue_selectors = [
                "//button[contains(text(), 'Continuar')]",
                "//button[contains(text(), 'continuar')]",
                "//a[contains(text(), 'Continuar')]",
                "//button[contains(@class, 'continue')]",
                "//button[contains(@class, 'btn') and contains(@class, 'primary')]",
                "//button[contains(@class, 'submit')]",
                "//button[@type='submit']",
                "//input[@type='submit']",
                "//button[contains(@class, 'next')]",
                "//button[contains(@class, 'proceed')]"
            ]
            
            for selector in continue_selectors:
                try:
                    continue_btn = self.driver.find_element(By.XPATH, selector)
                    continue_btn.click()
                    logger.info(f"✅ Botão continuar clicado com seletor: {selector}")
                    time.sleep(5)
                    
                    # Capturar screenshot após clicar continuar
                    self.capture_screenshot("after_continue_click")
                    return True
                except:
                    continue
            
            logger.error("❌ Botão continuar não encontrado")
            self.capture_screenshot("continue_button_not_found")
            return False
            
        except Exception as e:
            logger.error(f"❌ Erro ao inserir placa: {e}")
            self.capture_screenshot("plate_error")
            return False
    
    def capture_screenshot(self, name):
        """Capturar screenshot para debug"""
        try:
            screenshot_path = f"/opt/imediatoseguros-rpa/screenshots/debug_{name}_{int(time.time())}.png"
            self.driver.save_screenshot(screenshot_path)
            logger.info(f"📸 Screenshot de debug salvo: {screenshot_path}")
        except:
            logger.warning("⚠️ Não foi possível salvar screenshot de debug")
    
    def run_debug_test(self):
        """Executar teste com debug visual"""
        try:
            logger.info("🧪 Executando teste com debug visual...")
            
            # Setup do driver
            if not self.setup_driver():
                return None
            
            # Navegar para ToSegurado
            if not self.navigate_to_tosegurado():
                return None
            
            # Selecionar seguro de carro
            if not self.select_car_insurance():
                return None
            
            # Inserir placa
            if not self.enter_license_plate("FPG-8D63"):
                return None
            
            # Aguardar um pouco para visualizar
            logger.info("⏳ Aguardando para visualização...")
            time.sleep(10)
            
            # Fechar driver
            if self.driver:
                self.driver.quit()
            
            return {
                'success': True,
                'message': 'Teste com debug visual executado com sucesso'
            }
            
        except Exception as e:
            logger.error(f"❌ Erro no teste com debug visual: {e}")
            if self.driver:
                self.driver.quit()
            return {
                'success': False,
                'error': str(e)
            }

# Função para executar teste com debug visual
def execute_debug_test():
    """Executar teste com debug visual no ToSegurado"""
    automation = ToSeguradoDebugAutomation(headless=False)  # FALSE para debug visual
    return automation.run_debug_test()

if __name__ == "__main__":
    # Teste com debug visual
    result = execute_debug_test()
    print("Resultado:", result)
