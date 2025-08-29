#!/usr/bin/env python3
"""
RPA COMPLETO HEADLESS - TÔ SEGURADO - COTAÇÃO DE SEGURO AUTO
Navega por todas as 15 telas em modo headless
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import re
import tempfile
import shutil

class ToSeguradoRPAHeadless:
    def __init__(self):
        self.driver = None
        self.wait = None
        self.cotacao_data = {}
        self.current_step = 0
        self.temp_dir = None
        
    def setup_driver(self):
        """Configura o Chrome WebDriver em modo headless"""
        print("🔧 Configurando Chrome WebDriver HEADLESS...")
        
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
        self.temp_dir = tempfile.mkdtemp(prefix="tosegurado_rpa_")
        chrome_options.add_argument(f"--user-data-dir={self.temp_dir}")
        chrome_options.add_argument(f"--data-path={self.temp_dir}")
        chrome_options.add_argument(f"--homedir={self.temp_dir}")
        
        print(f"📁 Diretório temporário criado: {self.temp_dir}")
        
        try:
            # Instalar e configurar ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Configurar timeout
            self.driver.set_page_load_timeout(30)
            self.driver.implicitly_wait(10)
            self.wait = WebDriverWait(self.driver, 20)
            
            print("✅ Chrome WebDriver HEADLESS configurado com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao configurar Chrome: {e}")
            return False
        
    def log_step(self, step, action, details=""):
        """Registra cada passo do processo"""
        self.current_step = step
        print(f" **Tela {step}:** {action}")
        if details:
            print(f"   📝 {details}")
        print()
        
    def save_screenshot(self, step):
        """Salva screenshot de cada tela"""
        try:
            filename = f"/opt/imediatoseguros-rpa/temp/tela_{step:02d}.png"
            self.driver.save_screenshot(filename)
            print(f"   📸 Screenshot salvo: {filename}")
        except Exception as e:
            print(f"   ⚠️ Erro ao salvar screenshot: {e}")
            
    def wait_for_element(self, by, value, timeout=20):
        """Aguarda elemento aparecer na tela"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return element
        except Exception as e:
            print(f"   ⚠️ Elemento não encontrado: {value}")
            return None
            
    def wait_for_text(self, text, timeout=20):
        """Aguarda texto aparecer na tela"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda driver: text in driver.page_source
            )
            return True
        except Exception as e:
            print(f"   ⚠️ Texto não encontrado: {text}")
            return False
            
    def execute_complete_flow(self):
        """Executa o fluxo completo das 15 telas"""
        try:
            print("🚀 **INICIANDO RPA COMPLETO HEADLESS - TÔ SEGURADO**")
            print("=" * 70)
            
            # Configurar driver
            if not self.setup_driver():
                return False
                
            # TELA 1: Seleção do tipo de seguro
            self.log_step(1, "Navegando para página inicial")
            self.driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
            self.save_screenshot(1)
            
            # Aguardar página carregar
            if not self.wait_for_text("Qual seguro você deseja cotar?"):
                print("   ❌ Página inicial não carregou corretamente")
                return False
                
            print("   ✅ Página inicial carregada")
            
            # TELA 2: Clicar no botão "Carro"
            self.log_step(2, "Clicando no botão 'Carro'")
            carro_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Carro')]")
            if carro_button:
                carro_button.click()
                print("   ✅ Botão 'Carro' clicado")
                time.sleep(3)
                self.save_screenshot(2)
            else:
                print("   ❌ Botão 'Carro' não encontrado")
                return False
                
            # TELA 3: Formulário de placa
            self.log_step(3, "Preenchendo formulário de placa")
            if not self.wait_for_text("Qual é a placa do carro?"):
                print("   ❌ Tela de placa não carregou")
                return False
                
            # Preencher placa
            placa_input = self.wait_for_element(By.XPATH, "//input[@placeholder='ABC-1D34']")
            if placa_input:
                placa_input.clear()
                placa_input.send_keys("EED3D56")
                print("   ✅ Placa preenchida: EED3D56")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(3)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Campo de placa não encontrado")
                return False
                
            # TELA 4: Confirmação do veículo
            self.log_step(4, "Confirmando dados do veículo")
            if not self.wait_for_text("O veículo COROLLA XEI"):
                print("   ❌ Tela de confirmação não carregou")
                return False
                
            # Selecionar "Sim"
            sim_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Sim']")
            if sim_button:
                sim_button.click()
                print("   ✅ 'Sim' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(4)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Sim' não encontrado")
                return False
                
            # TELA 5: Veículo já segurado
            self.log_step(5, "Respondendo sobre seguro vigente")
            if not self.wait_for_text("Esse veículo já está segurado?"):
                print("   ❌ Tela de seguro vigente não carregou")
                return False
                
            # Selecionar "Não"
            nao_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Não']")
            if nao_button:
                nao_button.click()
                print("   ✅ 'Não' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(5)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Não' não encontrado")
                return False
                
            # TELA 6: Carrossel de coberturas
            self.log_step(6, "Pulando carrossel de coberturas")
            time.sleep(5)  # Aguardar carrossel carregar
            
            # Clicar em Continuar
            continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
            if continuar_button:
                continuar_button.click()
                print("   ✅ Carrossel pulado")
                time.sleep(3)
                self.save_screenshot(6)
            else:
                print("   ❌ Botão 'Continuar' não encontrado")
                return False
                
            # TELA 7: Questionário do veículo
            self.log_step(7, "Preenchendo questionário do veículo")
            if not self.wait_for_text("O carro possui alguns desses itens?"):
                print("   ❌ Questionário do veículo não carregou")
                return False
                
            # Selecionar "Flex"
            flex_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Flex']")
            if flex_button:
                flex_button.click()
                print("   ✅ 'Flex' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(7)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Flex' não encontrado")
                return False
                
            # TELA 8: Endereço noturno
            self.log_step(8, "Preenchendo endereço noturno")
            if not self.wait_for_text("Onde o carro passa a noite?"):
                print("   ❌ Tela de endereço não carregou")
                return False
                
            # Preencher CEP
            endereco_input = self.wait_for_element(By.XPATH, "//input[@placeholder*='CEP']")
            if endereco_input:
                endereco_input.clear()
                endereco_input.send_keys("03317000")
                print("   ✅ CEP preenchido: 03317000")
                time.sleep(3)
                
                # Selecionar endereço no balão
                endereco_sugestao = self.wait_for_element(By.XPATH, "//div[contains(text(), 'Rua Serra de Botucatu')]")
                if endereco_sugestao:
                    endereco_sugestao.click()
                    print("   ✅ Endereço selecionado")
                    
                    # Clicar em Continuar
                    continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                    if continuar_button:
                        continuar_button.click()
                        print("   ✅ Botão 'Continuar' clicado")
                        time.sleep(3)
                        self.save_screenshot(8)
                    else:
                        print("   ❌ Botão 'Continuar' não encontrado")
                        return False
                else:
                    print("   ❌ Sugestão de endereço não encontrada")
                    return False
            else:
                print("   ❌ Campo de endereço não encontrado")
                return False
                
            # TELA 9: Uso do veículo
            self.log_step(9, "Selecionando uso do veículo")
            if not self.wait_for_text("Qual é o uso do veículo?"):
                print("   ❌ Tela de uso do veículo não carregou")
                return False
                
            # Selecionar "Pessoal"
            pessoal_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Pessoal']")
            if pessoal_button:
                pessoal_button.click()
                print("   ✅ 'Pessoal' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(9)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Pessoal' não encontrado")
                return False
                
            # TELA 10: Dados pessoais
            self.log_step(10, "Preenchendo dados pessoais")
            if not self.wait_for_text("Nessa etapa, precisamos dos seus dados pessoais"):
                print("   ❌ Tela de dados pessoais não carregou")
                return False
                
            # Preencher dados (se não estiverem preenchidos)
            # Nome, CPF, Data, etc. podem estar preenchidos automaticamente
            
            # Clicar em Continuar
            continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
            if continuar_button:
                continuar_button.click()
                print("   ✅ Botão 'Continuar' clicado")
                time.sleep(3)
                self.save_screenshot(10)
            else:
                print("   ❌ Botão 'Continuar' não encontrado")
                return False
                
            # TELA 11: Condutor principal
            self.log_step(11, "Confirmando condutor principal")
            if not self.wait_for_text("Você será o condutor principal do veículo?"):
                print("   ❌ Tela de condutor principal não carregou")
                return False
                
            # Selecionar "Sim"
            sim_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Sim']")
            if sim_button:
                sim_button.click()
                print("   ✅ 'Sim' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(11)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Sim' não encontrado")
                return False
                
            # TELA 12: Local trabalho/estudo
            self.log_step(12, "Selecionando local trabalho/estudo")
            if not self.wait_for_text("O veículo é utilizado para ir ao local de trabalho"):
                print("   ❌ Tela de local trabalho/estudo não carregou")
                return False
                
            # Selecionar "Local de trabalho"
            trabalho_checkbox = self.wait_for_element(By.XPATH, "//input[@type='checkbox' and @value='Local de trabalho']")
            if trabalho_checkbox:
                trabalho_checkbox.click()
                print("   ✅ 'Local de trabalho' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(12)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Checkbox 'Local de trabalho' não encontrado")
                return False
                
            # TELA 13: Garagem e portão
            self.log_step(13, "Selecionando garagem e portão")
            if not self.wait_for_text("Você possui uma garagem na sua residência?"):
                print("   ❌ Tela de garagem e portão não carregou")
                return False
                
            # Selecionar "Sim" para garagem
            sim_garagem = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Sim']")
            if sim_garagem:
                sim_garagem.click()
                print("   ✅ 'Sim' para garagem selecionado")
                
                # Selecionar "Eletrônico" para portão
                eletronico_portao = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Eletrônico']")
                if eletronico_portao:
                    eletronico_portao.click()
                    print("   ✅ 'Eletrônico' para portão selecionado")
                    
                    # Clicar em Continuar
                    continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                    if continuar_button:
                        continuar_button.click()
                        print("   ✅ Botão 'Continuar' clicado")
                        time.sleep(3)
                        self.save_screenshot(13)
                    else:
                        print("   ❌ Botão 'Continuar' não encontrado")
                        return False
                else:
                    print("   ❌ Radio button 'Eletrônico' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Sim' para garagem não encontrado")
                return False
                
            # TELA 14: Reside com 18-26 anos
            self.log_step(14, "Respondendo sobre residentes 18-26 anos")
            if not self.wait_for_text("Você reside com alguém entre 18 e 26 anos?"):
                print("   ❌ Tela de residentes 18-26 anos não carregou")
                return False
                
            # Selecionar "Não"
            nao_button = self.wait_for_element(By.XPATH, "//input[@type='radio' and @value='Não']")
            if nao_button:
                nao_button.click()
                print("   ✅ 'Não' selecionado")
                
                # Clicar em Continuar
                continuar_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Continuar')]")
                if continuar_button:
                    continuar_button.click()
                    print("   ✅ Botão 'Continuar' clicado")
                    time.sleep(3)
                    self.save_screenshot(14)
                else:
                    print("   ❌ Botão 'Continuar' não encontrado")
                    return False
            else:
                print("   ❌ Radio button 'Não' não encontrado")
                return False
                
            # TELA 15: Aguardar cálculo automático
            self.log_step(15, "Aguardando cálculo automático")
            if not self.wait_for_text("Por favor, aguarde. Estamos realizando o cálculo para você!"):
                print("   ❌ Tela de cálculo não carregou")
                return False
                
            print("   ⏳ Aguardando cálculo automático...")
            time.sleep(15)  # Aguardar início do cálculo
            
            # Aguardar resultado final
            if not self.wait_for_text("Parabéns, chegamos ao resultado final da cotação!", timeout=180):
                print("   ❌ Resultado final não carregou")
                return False
                
            print("   ✅ Cálculo concluído!")
            self.save_screenshot(15)
            
            # Extrair dados das cotações
            self.extract_cotacao_data()
            
            # Finalizar clicando em "Agora não"
            agora_nao_button = self.wait_for_element(By.XPATH, "//button[contains(text(), 'Agora não')]")
            if agora_nao_button:
                agora_nao_button.click()
                print("   ✅ 'Agora não' clicado - Finalizado!")
            else:
                print("   ⚠️ Botão 'Agora não' não encontrado")
                
            return True
            
        except Exception as e:
            print(f"❌ Erro durante execução: {e}")
            return False
            
    def extract_cotacao_data(self):
        """Extrai dados das cotações"""
        print("📊 Extraindo dados das cotações...")
        
        try:
            # Procurar por valores de cotação
            page_source = self.driver.page_source
            
            # Padrões para encontrar valores
            price_patterns = [
                r'R\$\s*([\d.,]+)',
                r'([\d.,]+)\s*anual',
                r'R\$\s*([\d.,]+)\s*anual'
            ]
            
            cotacoes = []
            for pattern in price_patterns:
                matches = re.findall(pattern, page_source)
                for match in matches:
                    try:
                        valor = float(match.replace('.', '').replace(',', '.'))
                        cotacoes.append(valor)
                    except ValueError:
                        continue
                        
            # Procurar por coberturas
            coberturas = []
            cobertura_keywords = ['Franquia', 'Valor de Mercado', 'Assistência', 'Vidros', 'Carro Reserva', 
                                 'Danos Materiais', 'Danos Corporais', 'Danos Morais', 'Morte/Invalidez']
            
            for keyword in cobertura_keywords:
                if keyword in page_source:
                    coberturas.append(keyword)
                    
            self.cotacao_data = {
                'cotacoes': cotacoes,
                'coberturas': coberturas,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
            print(f"   ✅ {len(cotacoes)} cotações encontradas")
            print(f"   ✅ {len(coberturas)} coberturas encontradas")
            
            # Salvar dados
            json_path = "/opt/imediatoseguros-rpa/temp/dados_cotacao.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.cotacao_data, f, indent=2, ensure_ascii=False)
            print(f"   Dados salvos em: {json_path}")
            
        except Exception as e:
            print(f"   ❌ Erro ao extrair dados: {e}")
            
    def close(self):
        """Fecha o navegador e limpa diretório temporário"""
        if self.driver:
            self.driver.quit()
            print("🔒 Navegador fechado")
            
        # Limpar diretório temporário
        if self.temp_dir:
            try:
                shutil.rmtree(self.temp_dir, ignore_errors=True)
                print(f"🗑️ Diretório temporário removido: {self.temp_dir}")
            except Exception as e:
                print(f"⚠️ Erro ao remover diretório temporário: {e}")

def main():
    """Função principal"""
    rpa = ToSeguradoRPAHeadless()
    
    try:
        # Executar fluxo completo
        success = rpa.execute_complete_flow()
        
        if success:
            print("\n🎉 **SUCESSO! FLUXO COMPLETO EXECUTADO!**")
            print("=" * 70)
            print("✅ Todas as 15 telas navegadas com sucesso!")
            print("✅ Dados das cotações extraídos!")
            print("✅ Processo finalizado!")
        else:
            print("\n❌ **FALHA NO FLUXO**")
            print("=" * 70)
            print("❌ Ocorreu um erro durante a execução")
            print("❌ Verifique os logs acima para identificar o problema")
            
    except Exception as e:
        print(f"\n❌ **ERRO CRÍTICO:** {e}")
        
    finally:
        # Fechar navegador e limpar
        rpa.close()

if __name__ == "__main__":
    main()
