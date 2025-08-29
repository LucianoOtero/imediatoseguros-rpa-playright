#!/usr/bin/env python3
"""
ANALISADOR - Encontrar o botão 'Carro' correto
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import tempfile
import shutil

def analisar_botao_carro():
    """Analisa a página para encontrar o botão 'Carro'"""
    print("�� **ANALISANDO BOTÃO 'CARRO'**")
    print("=" * 50)
    
    try:
        # Configurar Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        temp_dir = tempfile.mkdtemp(prefix="analise_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome configurado")
        
        # Navegar para página
        print("�� Navegando para ToSegurado...")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(5)
        
        # Salvar HTML para análise
        html_path = "/opt/imediatoseguros-rpa/temp/pagina_analise.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 HTML salvo em: {html_path}")
        
        # Procurar por diferentes seletores
        seletores = [
            "//button[contains(text(), 'Carro')]",
            "//button[contains(., 'Carro')]",
            "//*[contains(text(), 'Carro')]",
            "//div[contains(text(), 'Carro')]",
            "//span[contains(text(), 'Carro')]",
            "//p[contains(text(), 'Carro')]",
            "//button[contains(@class, 'carro')]",
            "//div[contains(@class, 'carro')]"
        ]
        
        print("\n�� **PROCURANDO BOTÃO 'CARRO':**")
        for i, seletor in enumerate(seletores, 1):
            try:
                elementos = driver.find_elements(By.XPATH, seletor)
                if elementos:
                    print(f"   {i}. ✅ {seletor}: {len(elementos)} elementos encontrados")
                    for j, elem in enumerate(elementos):
                        texto = elem.text.strip()
                        classes = elem.get_attribute('class')
                        tag = elem.tag_name
                        print(f"      Elemento {j+1}: Tag={tag}, Texto='{texto}', Classes='{classes}'")
                else:
                    print(f"   {i}. ❌ {seletor}: Nenhum elemento encontrado")
            except Exception as e:
                print(f"   {i}. ⚠️ {seletor}: Erro - {e}")
        
        # Procurar por texto "Carro" em qualquer lugar
        print("\n�� **PROCURANDO TEXTO 'CARRO':**")
        page_source = driver.page_source.lower()
        if 'carro' in page_source:
            print("   ✅ Texto 'carro' encontrado na página")
            
            # Encontrar posição aproximada
            pos = page_source.find('carro')
            inicio = max(0, pos - 100)
            fim = min(len(page_source), pos + 100)
            contexto = page_source[inicio:fim]
            print(f"   📍 Contexto: ...{contexto}...")
        else:
            print("   ❌ Texto 'carro' NÃO encontrado na página")
            
        # Verificar título da página
        print(f"\n�� **TÍTULO DA PÁGINA:** {driver.title}")
        
        # Verificar URL atual
        print(f"🌐 **URL ATUAL:** {driver.current_url}")
        
        # Salvar screenshot
        screenshot_path = "/opt/imediatoseguros-rpa/temp/analise_botao_carro.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        driver.quit()
        shutil.rmtree(temp_dir, ignore_errors=True)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    analisar_botao_carro()
