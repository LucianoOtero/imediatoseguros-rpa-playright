#!/usr/bin/env python3
"""
Executa todas as 12 telas da cotação de seguro
"""

import time
import json
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import aguardar_estabilizacao

from telas.tela1_selecao import implementar_tela1
# Importar todas as telas
from telas.tela2_placa import implementar_tela2
from telas.tela3_confirmacao import implementar_tela3
from telas.tela4_segurado import implementar_tela4
from telas.tela5_estimativa import implementar_tela5
from telas.tela6_combustivel import implementar_tela6
from telas.tela7_endereco import implementar_tela7
from telas.tela8_finalidade import implementar_tela8
from telas.tela9_dados import implementar_tela9
from telas.tela10_contato import implementar_tela10
from telas.tela11_coberturas import implementar_tela11
from telas.tela12_finalizacao import implementar_tela12

def configurar_driver():
    """Configura o driver do Chrome com configuração que funcionou"""
    print("🔧 Configurando Chrome...")
    
    # Criar diretório temporário único para cada execução
    temp_dir = tempfile.mkdtemp()
    
    chrome_options = Options()
    
    # CONFIGURAÇÕES QUE FUNCIONARAM
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # CONFIGURAÇÕES ADICIONAIS PARA ESTABILIDADE
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-css")
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    chrome_options.add_argument("--disable-background-timer-throttling")
    chrome_options.add_argument("--disable-backgrounding-occluded-windows")
    chrome_options.add_argument("--disable-renderer-backgrounding")
    
    try:
        # Usar ChromeDriver local que já baixamos
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            print("✅ Usando ChromeDriver local...")
            service = Service(chromedriver_path)
        else:
            print("📥 ChromeDriver local não encontrado, baixando automaticamente...")
            service = Service(ChromeDriverManager().install())
        
        print(" Criando driver do Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Executar script para evitar detecção
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver configurado com sucesso")
        return driver
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        raise e

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            parametros = json.load(f)
            print("✅ Parâmetros carregados com sucesso:")
            print(f"   �� URL Base: {parametros.get('url_base', 'N/A')}")
            print(f"   Placa: {parametros.get('placa', 'N/A')}")
            print(f"   Marca: {parametros.get('marca', 'N/A')}")
            print(f"   🚙 Modelo: {parametros.get('modelo', 'N/A')}")
            print(f"   Email: {parametros.get('email', 'N/A')}")
            print(f"   📱 Celular: {parametros.get('celular', 'N/A')}")
            return parametros
    except FileNotFoundError:
        print("❌ Arquivo parametros.json não encontrado")
        return None
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar JSON")
        return None

def executar_todas_telas():
    """Executa todas as 12 telas"""
    print(" INICIANDO EXECUÇÃO DE TODAS AS 12 TELAS!")
    print("=" * 60)
    
    driver = None
    
    try:
        # Configurar driver
        driver = configurar_driver()
        
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            print("❌ Falha ao carregar parâmetros")
            return False
        
        # Verificar se os parâmetros essenciais estão presentes
        parametros_essenciais = ['url_base', 'placa', 'marca', 'modelo', 'email', 'celular']
        for param in parametros_essenciais:
            if not parametros.get(param):
                print(f"❌ Parâmetro essencial '{param}' não encontrado no JSON")
                return False
        
        print(f"\n EXECUTANDO COM DADOS REAIS:")
        print(f"   �� URL Base: {parametros['url_base']}")
        print(f"   Placa: {parametros['placa']}")
        print(f"   Marca: {parametros['marca']}")
        print(f"   🚙 Modelo: {parametros['modelo']}")
        print(f"   Email: {parametros['email']}")
        print(f"   📱 Celular: {parametros['celular']}")
        print("=" * 60)
        
        # Abrir página inicial usando URL do JSON
        print(f"🌐 Abrindo página inicial: {parametros['url_base']}")
        print("⏳ Aguardando carregamento...")
        
        driver.get(parametros['url_base'])
        
        # Aguardar carregamento da página
        time.sleep(5)
        
        # Verificar se a página carregou corretamente
        if "tosegurado" not in driver.current_url.lower():
            print("❌ Página não carregou corretamente")
            print(f"   URL esperada: {parametros['url_base']}")
            print(f"   URL atual: {driver.current_url}")
            return False
        
        print("✅ Página inicial carregada com sucesso")
        print(f"   🌐 URL carregada: {driver.current_url}")
        
        # Aguardar estabilização inicial
        print("⏳ Aguardando estabilização inicial...")
        aguardar_estabilizacao(driver, 5)
        
        # Executar Tela 1
        print("\n📱 INICIANDO TELA 1...")
        if not implementar_tela1(driver, parametros):
            print("❌ Falha na Tela 1")
            return False
        
        # Executar Tela 1 (já implementada no main.py)
        print("\n📱 TELA 1: Página inicial (já implementada)")
        
        # Executar Tela 2
        print(f"\n📱 INICIANDO TELA 2: Inserindo placa {parametros['placa']}...")
        if not implementar_tela2(driver, parametros):
            print("❌ Falha na Tela 2")
            return False
        
        # Executar Tela 3
        print(f"\n📱 INICIANDO TELA 3: Confirmando {parametros['marca']} {parametros['modelo']}...")
        if not implementar_tela3(driver, parametros):
            print("❌ Falha na Tela 3")
            return False
        
        # Executar Tela 4
        print(f"\n📱 INICIANDO TELA 4: Veículo já segurado? → {parametros.get('veiculo_segurado', 'Não')}...")
        if not implementar_tela4(driver, parametros):
            print("❌ Falha na Tela 4")
            return False
        
        # Executar Tela 5
        print("\n📱 INICIANDO TELA 5: Estimativa inicial...")
        if not implementar_tela5(driver, parametros):
            print("❌ Falha na Tela 5")
            return False
        
        # Executar Tela 6
        print(f"\n📱 INICIANDO TELA 6: Tipo de combustível → {parametros.get('combustivel', 'Flex')}...")
        if not implementar_tela6(driver, parametros):
            print("❌ Falha na Tela 6")
            return False
        
        # Executar Tela 7
        print(f"\n📱 INICIANDO TELA 7: Endereço de pernoite → CEP {parametros.get('cep', 'N/A')}...")
        if not implementar_tela7(driver, parametros):
            print("❌ Falha na Tela 7")
            return False
        
        # Executar Tela 8
        print(f"\n📱 INICIANDO TELA 8: Finalidade do veículo → {parametros.get('uso_veiculo', 'Particular')}...")
        if not implementar_tela8(driver, parametros):
            print("❌ Falha na Tela 8")
            return False
        
        # Executar Tela 9
        print(f"\n📱 INICIANDO TELA 9: Dados pessoais → {parametros.get('nome', 'N/A')}...")
        if not implementar_tela9(driver, parametros):
            print("❌ Falha na Tela 9")
            return False
        
        # Executar Tela 10
        print(f"\n�� INICIANDO TELA 10: Contato → {parametros.get('email', 'N/A')}...")
        if not implementar_tela10(driver, parametros):
            print("❌ Falha na Tela 10")
            return False
        
        # Executar Tela 11
        print("\n�� INICIANDO TELA 11: Coberturas adicionais...")
        if not implementar_tela11(driver, parametros):
            print("❌ Falha na Tela 11")
            return False
        
        # Executar Tela 12
        print("\n�� INICIANDO TELA 12: Finalização...")
        if not implementar_tela12(driver, parametros):
            print("❌ Falha na Tela 12")
            return False
        
        print("\n🎉 TODAS AS 12 TELAS EXECUTADAS COM SUCESSO!")
        print("=" * 60)
        print(f"✅ Dados utilizados:")
        print(f"   �� URL Base: {parametros['url_base']}")
        print(f"   Placa: {parametros['placa']}")
        print(f"   Marca: {parametros['marca']}")
        print(f"   🚙 Modelo: {parametros['modelo']}")
        print(f"   Email: {parametros['email']}")
        print(f"   📱 Celular: {parametros['celular']}")
        
        # Aguardar resultado final
        print("⏳ Aguardando resultado final...")
        time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False
        
    finally:
        if driver:
            print(" Fechando driver...")
            try:
                driver.quit()
                print("✅ Driver fechado com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao fechar driver: {e}")

if __name__ == "__main__":
    executar_todas_telas()
