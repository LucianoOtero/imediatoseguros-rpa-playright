#!/usr/bin/env python3
"""
RPA SIMPLES E ESTÁVEL - TÔ SEGURADO
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import shutil

def main():
    print("🚀 **RPA SIMPLES E ESTÁVEL - TÔ SEGURADO**")
    print("=" * 50)
    
    try:
        # Configurar Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        temp_dir = tempfile.mkdtemp(prefix="tosegurado_simples_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # TELA 1: Navegar para página inicial
        print("\n **Tela 1:** Navegando para página inicial")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        
        # Verificar se carregou
        if "Qual seguro você deseja cotar?" not in driver.page_source:
            print("   ❌ Página inicial não carregou")
            return False
            
        print("   ✅ Página inicial carregada")
        
        # TELA 2: Clicar no botão "Carro" - COM PROTEÇÃO STALE
        print("\n **Tela 2:** Clicando no botão 'Carro'")
        
        # Aguardar elemento estar presente E clicável
        carro_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", carro_button)
        time.sleep(1)
        
        # Clicar no elemento
        carro_button.click()
        print("   ✅ Botão 'Carro' clicado")
        time.sleep(3)
        
        # TELA 3: Verificar se formulário de placa carregou
        print("\n **Tela 3:** Verificando formulário de placa")
        
        if "Qual é a placa do carro?" not in driver.page_source:
            print("   ❌ Tela de placa não carregou")
            return False
            
        print("   ✅ Tela de placa carregada")
        
        # Preencher placa
        placa_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']"))
        )
        
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("   ✅ Placa preenchida: EED3D56")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 4: Verificar confirmação do veículo
        print("\n **Tela 4:** Verificando confirmação do veículo")
        
        if "O veículo COROLLA XEI" not in driver.page_source:
            print("   ❌ Tela de confirmação não carregou")
            return False
            
        print("   ✅ Tela de confirmação carregada")
        
        # Selecionar "Sim"
        sim_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        sim_button.click()
        print("   ✅ 'Sim' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 5: Verificar veículo já segurado
        print("\n **Tela 5:** Verificando veículo já segurado")
        
        if "Esse veículo já está segurado?" not in driver.page_source:
            print("   ❌ Tela de seguro vigente não carregou")
            return False
            
        print("   ✅ Tela de seguro vigente carregada")
        
        # Selecionar "Não"
        nao_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        nao_button.click()
        print("   ✅ 'Não' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 6: Pular carrossel de coberturas
        print("\n **Tela 6:** Pulando carrossel de coberturas")
        time.sleep(5)
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Carrossel pulado")
        time.sleep(3)
        
        # TELA 7: Verificar questionário do veículo
        print("\n **Tela 7:** Verificando questionário do veículo")
        
        if "O carro possui alguns desses itens?" not in driver.page_source:
            print("   ❌ Questionário do veículo não carregou")
            return False
            
        print("   ✅ Questionário do veículo carregado")
        
        # Selecionar "Flex"
        flex_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        flex_button.click()
        print("   ✅ 'Flex' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 8: Verificar endereço noturno
        print("\n **Tela 8:** Verificando endereço noturno")
        
        if "Onde o carro passa a noite?" not in driver.page_source:
            print("   ❌ Tela de endereço não carregou")
            return False
            
        print("   ✅ Tela de endereço carregada")
        
        # Preencher CEP
        endereco_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text']"))
        )
        
        endereco_input.clear()
        endereco_input.send_keys("03317000")
        print("   ✅ CEP preenchido: 03317000")
        time.sleep(3)
        
        # Selecionar endereço no balão
        endereco_sugestao = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Rua Serra de Botucatu')]"))
        )
        endereco_sugestao.click()
        print("   ✅ Endereço selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 9: Verificar uso do veículo
        print("\n **Tela 9:** Verificando uso do veículo")
        
        if "Qual é o uso do veículo?" not in driver.page_source:
            print("   ❌ Tela de uso do veículo não carregou")
            return False
            
        print("   ✅ Tela de uso do veículo carregada")
        
        # Selecionar "Pessoal"
        pessoal_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        pessoal_button.click()
        print("   ✅ 'Pessoal' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 10: Verificar dados pessoais
        print("\n **Tela 10:** Verificando dados pessoais")
        
        if "Nessa etapa, precisamos dos seus dados pessoais" not in driver.page_source:
            print("   ❌ Tela de dados pessoais não carregou")
            return False
            
        print("   ✅ Tela de dados pessoais carregada")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 11: Verificar condutor principal
        print("\n **Tela 11:** Verificando condutor principal")
        
        if "Você será o condutor principal do veículo?" not in driver.page_source:
            print("   ❌ Tela de condutor principal não carregou")
            return False
            
        print("   ✅ Tela de condutor principal carregada")
        
        # Selecionar "Sim"
        sim_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        sim_button.click()
        print("   ✅ 'Sim' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 12: Verificar local trabalho/estudo
        print("\n **Tela 12:** Verificando local trabalho/estudo")
        
        if "O veículo é utilizado para ir ao local de trabalho" not in driver.page_source:
            print("   ❌ Tela de local trabalho/estudo não carregou")
            return False
            
        print("   ✅ Tela de local trabalho/estudo carregada")
        
        # Selecionar "Local de trabalho"
        trabalho_checkbox = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox'][1]"))
        )
        trabalho_checkbox.click()
        print("   ✅ 'Local de trabalho' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 13: Verificar garagem e portão
        print("\n **Tela 13:** Verificando garagem e portão")
        
        if "Você possui uma garagem na sua residência?" not in driver.page_source:
            print("   ❌ Tela de garagem e portão não carregou")
            return False
            
        print("   ✅ Tela de garagem e portão carregada")
        
        # Selecionar "Sim" para garagem
        sim_garagem = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        sim_garagem.click()
        print("   ✅ 'Sim' para garagem selecionado")
        
        # Selecionar "Eletrônico" para portão
        eletronico_portao = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][2]"))
        )
        eletronico_portao.click()
        print("   ✅ 'Eletrônico' para portão selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 14: Verificar residentes 18-26 anos
        print("\n **Tela 14:** Verificando residentes 18-26 anos")
        
        if "Você reside com alguém entre 18 e 26 anos?" not in driver.page_source:
            print("   ❌ Tela de residentes 18-26 anos não carregou")
            return False
            
        print("   ✅ Tela de residentes 18-26 anos carregada")
        
        # Selecionar "Não"
        nao_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='radio'][1]"))
        )
        nao_button.click()
        print("   ✅ 'Não' selecionado")
        
        # Clicar em Continuar
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
        )
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado")
        time.sleep(3)
        
        # TELA 15: Aguardar cálculo automático
        print("\n **Tela 15:** Aguardando cálculo automático")
        
        if "Por favor, aguarde. Estamos realizando o cálculo para você!" not in driver.page_source:
            print("   ❌ Tela de cálculo não carregou")
            return False
            
        print("   ⏳ Aguardando cálculo automático...")
        time.sleep(15)
        
        # Aguardar resultado final
        if not wait.until(lambda d: "Parabéns, chegamos ao resultado final da cotação!" in d.page_source):
            print("   ❌ Resultado final não carregou")
            return False
            
        print("   ✅ Cálculo concluído!")
        
        # Finalizar clicando em "Agora não"
        agora_nao_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agora não')]"))
        )
        agora_nao_button.click()
        print("   ✅ 'Agora não' clicado - Finalizado!")
        
        print("\n🎉 **SUCESSO! FLUXO COMPLETO EXECUTADO!**")
        print("✅ Todas as 15 telas navegadas com sucesso!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ **ERRO:** {e}")
        return False
        
    finally:
        # Fechar navegador
        if 'driver' in locals():
            driver.quit()
            print("🔒 Navegador fechado")
            
        # Limpar diretório temporário
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
