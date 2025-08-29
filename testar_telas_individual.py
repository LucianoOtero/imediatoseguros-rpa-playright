#!/usr/bin/env python3
"""
Testa telas individuais para debug
"""

import sys
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from utils.helpers import aguardar_estabilizacao

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
    """Configura o driver do Chrome"""
    print("🔧 Configurando driver do Chrome...")
    
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print("✅ Driver configurado com sucesso")
    return driver

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo parametros.json não encontrado")
        return None

def testar_tela_individual(numero_tela):
    """Testa uma tela específica"""
    print(f"🧪 TESTANDO TELA {numero_tela} INDIVIDUALMENTE")
    print("=" * 50)
    
    driver = configurar_driver()
    
    try:
        parametros = carregar_parametros()
        if not parametros:
            return False
        
        # Abrir página inicial
        print("🌐 Abrindo página inicial...")
        driver.get("https://cotacaoseguroonline.com.br/")
        driver.maximize_window()
        aguardar_estabilizacao(driver, 5)
        
        # Executar telas até a desejada
        telas = {
            2: implementar_tela2,
            3: implementar_tela3,
            4: implementar_tela4,
            5: implementar_tela5,
            6: implementar_tela6,
            7: implementar_tela7,
            8: implementar_tela8,
            9: implementar_tela9,
            10: implementar_tela10,
            11: implementar_tela11,
            12: implementar_tela12
        }
        
        for tela_num, tela_func in telas.items():
            if tela_num <= numero_tela:
                print(f"\n�� Executando Tela {tela_num}...")
                if not tela_func(driver, parametros):
                    print(f"❌ Falha na Tela {tela_num}")
                    return False
                
                if tela_num == numero_tela:
                    print(f"✅ Tela {numero_tela} testada com sucesso!")
                    break
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
        
    finally:
        print("�� Fechando driver...")
        driver.quit()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python testar_telas_individual.py <numero_tela>")
        print("Exemplo: python testar_telas_individual.py 6")
        sys.exit(1)
    
    try:
        numero_tela = int(sys.argv[1])
        if numero_tela < 2 or numero_tela > 12:
            print("❌ Número da tela deve estar entre 2 e 12")
            sys.exit(1)
        
        testar_tela_individual(numero_tela)
        
    except ValueError:
        print("❌ Número da tela deve ser um número inteiro")
        sys.exit(1)
