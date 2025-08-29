#!/usr/bin/env python3
"""
Teste específico da Tela 6 para identificar o erro
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    """Configura o driver do Chrome"""
    print("🔧 Configurando Chrome...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        # Usar ChromeDriver local
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            print("✅ Usando ChromeDriver local...")
            service = Service(chromedriver_path)
        else:
            print("❌ ChromeDriver local não encontrado")
            return None
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver configurado com sucesso")
        return driver
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        return None

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return None

def testar_tela6(driver, parametros):
    """Testa especificamente a Tela 6"""
    print("\n🧪 TESTANDO TELA 6 ESPECIFICAMENTE")
    print("=" * 50)
    
    try:
        # Abrir página inicial
        print(f"🌐 Abrindo: {parametros['url_base']}")
        driver.get(parametros['url_base'])
        time.sleep(5)
        
        # Simular navegação até Tela 6 (pular telas 1-5)
        print("⏭️ Simulando navegação até Tela 6...")
        
        # Aguardar elementos da Tela 6
        print("⏳ Aguardando elementos da Tela 6...")
        
        try:
            # Teste 1: Aguardar elemento com texto "combustível"
            print("🔍 Teste 1: Procurando texto 'combustível'...")
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível')]"))
            )
            print("✅ Elemento 'combustível' encontrado!")
            
        except Exception as e:
            print(f"❌ Teste 1 falhou: {e}")
            
            # Teste 2: Verificar HTML da página
            print("🔍 Teste 2: Verificando HTML da página...")
            html = driver.page_source
            if "combustível" in html.lower():
                print("✅ Texto 'combustível' encontrado no HTML")
            else:
                print("❌ Texto 'combustível' NÃO encontrado no HTML")
            
            # Teste 3: Listar todos os textos visíveis
            print("🔍 Teste 3: Listando textos visíveis...")
            elementos = driver.find_elements(By.XPATH, "//*[text()]")
            textos = [elem.text.strip() for elem in elementos if elem.text.strip()]
            print(f"📝 Textos encontrados ({len(textos)}):")
            for i, texto in enumerate(textos[:10]):  # Primeiros 10
                print(f"   {i+1}: {texto}")
            if len(textos) > 10:
                print(f"   ... e mais {len(textos) - 10} textos")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro geral na Tela 6: {e}")
        return False

def main():
    """Função principal"""
    print("🧪 TESTE ESPECÍFICO DA TELA 6")
    print("=" * 50)
    
    # Configurar driver
    driver = configurar_driver()
    if not driver:
        return
    
    try:
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            return
        
        # Testar Tela 6
        sucesso = testar_tela6(driver, parametros)
        
        if sucesso:
            print("\n✅ Teste da Tela 6 concluído!")
        else:
            print("\n❌ Teste da Tela 6 falhou!")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("✅ Driver fechado")

if __name__ == "__main__":
    main()
