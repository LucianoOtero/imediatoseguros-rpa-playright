#!/usr/bin/env python3
"""
Executa todas as 12 telas da cotação de seguro - Versão alternativa
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
    """Configura o driver do Chrome usando ChromeDriver direto"""
    print("🔧 Configurando driver do Chrome (versão alternativa)...")
    
    chrome_options = Options()
    
    # CONFIGURAÇÕES ESSENCIAIS PARA SERVIDOR UBUNTU
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    
    # CONFIGURAÇÕES ADICIONAIS DE ESTABILIDADE
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")
    chrome_options.add_argument("--disable-javascript")
    chrome_options.add_argument("--disable-css")
    
    # CONFIGURAÇÕES DE MEMÓRIA
    chrome_options.add_argument("--memory-pressure-off")
    chrome_options.add_argument("--max_old_space_size=4096")
    
    # CONFIGURAÇÕES DE REDE
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--ignore-ssl-errors")
    
    # CONFIGURAÇÕES DE IDIOMA
    chrome_options.add_argument("--lang=pt-BR")
    
    # CONFIGURAÇÕES EXPERIMENTAIS
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        print(" Usando ChromeDriver instalado diretamente...")
        
        # Usar ChromeDriver instalado diretamente
        service = Service('/usr/local/bin/chromedriver')
        
        print(" Criando driver do Chrome...")
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Configurações básicas do driver
        driver.set_page_load_timeout(60)
        driver.implicitly_wait(10)
        
        print("✅ Driver configurado com sucesso (versão alternativa)")
        return driver
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        
        # Tentar com caminho alternativo
        try:
            print(" Tentando caminho alternativo...")
            service = Service('./chromedriver')
            driver = webdriver.Chrome(service=service, options=chrome_options)
            
            driver.set_page_load_timeout(60)
            driver.implicitly_wait(10)
            
            print("✅ Driver configurado com caminho alternativo")
            return driver
            
        except Exception as e2:
            print(f"❌ Erro no caminho alternativo: {e2}")
            raise e2

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
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
        
        # Abrir página inicial
        print("🌐 Abrindo página inicial...")
        print("⏳ Aguardando carregamento...")
        
        driver.get("https://cotacaoseguroonline.com.br/")
        
        # Aguardar carregamento da página
        time.sleep(5)
        
        # Verificar se a página carregou
        if "cotacaoseguroonline" not in driver.current_url.lower():
            print("❌ Página não carregou corretamente")
            return False
        
        print("✅ Página inicial carregada com sucesso")
        
        # Aguardar estabilização inicial
        print("⏳ Aguardando estabilização inicial...")
        aguardar_estabilizacao(driver, 5)
        
        # Executar Tela 1 (já implementada no main.py)
        print("\n📱 TELA 1: Página inicial (já implementada)")
        
        # Executar Tela 2
        print("\n📱 INICIANDO TELA 2...")
        if not implementar_tela2(driver, parametros):
            print("❌ Falha na Tela 2")
            return False
        
        # Executar Tela 3
        print("\n📱 INICIANDO TELA 3...")
        if not implementar_tela3(driver, parametros):
            print("❌ Falha na Tela 3")
            return False
        
        # Executar Tela 4
        print("\n📱 INICIANDO TELA 4...")
        if not implementar_tela4(driver, parametros):
            print("❌ Falha na Tela 4")
            return False
        
        # Executar Tela 5
        print("\n📱 INICIANDO TELA 5...")
        if not implementar_tela5(driver, parametros):
            print("❌ Falha na Tela 5")
            return False
        
        # Executar Tela 6
        print("\n📱 INICIANDO TELA 6...")
        if not implementar_tela6(driver, parametros):
            print("❌ Falha na Tela 6")
            return False
        
        # Executar Tela 7
        print("\n📱 INICIANDO TELA 7...")
        if not implementar_tela7(driver, parametros):
            print("❌ Falha na Tela 7")
            return False
        
        # Executar Tela 8
        print("\n📱 INICIANDO TELA 8...")
        if not implementar_tela8(driver, parametros):
            print("❌ Falha na Tela 8")
            return False
        
        # Executar Tela 9
        print("\n📱 INICIANDO TELA 9...")
        if not implementar_tela9(driver, parametros):
            print("❌ Falha na Tela 9")
            return False
        
        # Executar Tela 10
        print("\n📱 INICIANDO TELA 10...")
        if not implementar_tela10(driver, parametros):
            print("❌ Falha na Tela 10")
            return False
        
        # Executar Tela 11
        print("\n📱 INICIANDO TELA 11...")
        if not implementar_tela11(driver, parametros):
            print("❌ Falha na Tela 11")
            return False
        
        # Executar Tela 12
        print("\n📱 INICIANDO TELA 12...")
        if not implementar_tela12(driver, parametros):
            print("❌ Falha na Tela 12")
            return False
        
        print("\n🎉 TODAS AS 12 TELAS EXECUTADAS COM SUCESSO!")
        print("=" * 60)
        
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
