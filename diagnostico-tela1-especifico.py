#!/usr/bin/env python3
"""
Diagnóstico Específico da Tela 1 - Seleção do tipo de seguro
Investiga exatamente o que está acontecendo na Tela 1
"""

import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções otimizadas"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Criar diretório temporário único
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def investigar_tela1(driver):
    """Investiga a Tela 1 detalhadamente"""
    print("🔍 **INVESTIGANDO TELA 1 DETALHADAMENTE...**")
    
    # Navegar para a página
    print("🌐 Navegando para https://www.app.tosegurado.com.br/cotacao...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    time.sleep(5)
    
    # Salvar HTML inicial
    with open("/opt/imediatoseguros-rpa/temp/tela1-inicial.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML inicial da Tela 1 salvo")
    
    # Salvar screenshot inicial
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela1-inicial.png")
    print("�� Screenshot inicial da Tela 1 salvo")
    
    # Verificar título da página
    titulo = driver.title
    print(f"📄 Título da página: {titulo}")
    
    # Verificar URL
    url = driver.current_url
    print(f"🌐 URL atual: {url}")
    
    # Procurar por elementos relacionados ao carro
    print("\n🔍 **PROCURANDO ELEMENTOS RELACIONADOS AO CARRO...**")
    
    # Tentar diferentes seletores
    seletores = [
        "//button[contains(., 'Carro')]",
        "//button[contains(text(), 'Carro')]",
        "//*[contains(text(), 'Carro')]",
        "//button[contains(@class, 'carro')]",
        "//div[contains(text(), 'Carro')]",
        "//p[contains(text(), 'Carro')]"
    ]
    
    for i, seletor in enumerate(seletores, 1):
        try:
            elementos = driver.find_elements(By.XPATH, seletor)
            print(f"🔍 Seletor {i}: {seletor}")
            print(f"   ✅ Encontrados: {len(elementos)} elementos")
            
            if elementos:
                for j, elemento in enumerate(elementos[:3]):  # Mostrar apenas os 3 primeiros
                    try:
                        texto = elemento.text
                        classes = elemento.get_attribute("class")
                        tag = elemento.tag_name
                        print(f"      Elemento {j+1}: <{tag}> - Classes: {classes}")
                        print(f"         Texto: {texto[:100]}...")
                    except:
                        print(f"      Elemento {j+1}: Erro ao analisar")
        except Exception as e:
            print(f"   ❌ Erro com seletor {i}: {e}")
    
    # Procurar por botões em geral
    print("\n�� **PROCURANDO TODOS OS BOTÕES...**")
    try:
        botoes = driver.find_elements(By.TAG_NAME, "button")
        print(f"✅ Total de botões encontrados: {len(botoes)}")
        
        for i, botao in enumerate(botoes[:5]):  # Mostrar apenas os 5 primeiros
            try:
                texto = botao.text
                classes = botao.get_attribute("class")
                id_attr = botao.get_attribute("id")
                print(f"   Botão {i+1}: ID='{id_attr}' - Classes: {classes}")
                print(f"      Texto: {texto[:50]}...")
            except:
                print(f"   Botão {i+1}: Erro ao analisar")
    except Exception as e:
        print(f"❌ Erro ao procurar botões: {e}")
    
    # Procurar por divs com texto
    print("\n🔍 **PROCURANDO DIVS COM TEXTO...**")
    try:
        divs = driver.find_elements(By.TAG_NAME, "div")
        divs_com_texto = [d for d in divs if d.text.strip()]
        print(f"✅ Total de divs com texto: {len(divs_com_texto)}")
        
        for i, div in enumerate(divs_com_texto[:5]):  # Mostrar apenas os 5 primeiros
            try:
                texto = div.text
                classes = div.get_attribute("class")
                print(f"   Div {i+1}: Classes: {classes}")
                print(f"      Texto: {texto[:100]}...")
            except:
                print(f"   Div {i+1}: Erro ao analisar")
    except Exception as e:
        print(f"❌ Erro ao procurar divs: {d}")
    
    # Verificar se há iframe
    print("\n🔍 **VERIFICANDO IFRAMES...**")
    try:
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        print(f"✅ Total de iframes: {len(iframes)}")
        
        for i, iframe in enumerate(iframes):
            try:
                src = iframe.get_attribute("src")
                print(f"   Iframe {i+1}: src='{src}'")
            except:
                print(f"   Iframe {i+1}: Erro ao analisar")
    except Exception as e:
        print(f"❌ Erro ao procurar iframes: {e}")
    
    # Verificar console do navegador
    print("\n🔍 **VERIFICANDO CONSOLE DO NAVEGADOR...**")
    try:
        logs = driver.get_log("browser")
        if logs:
            print(f"✅ Logs do console encontrados: {len(logs)}")
            for log in logs[:5]:  # Mostrar apenas os 5 primeiros
                print(f"   {log['level']}: {log['message']}")
        else:
            print("ℹ️ Nenhum log do console encontrado")
    except Exception as e:
        print(f"❌ Erro ao verificar console: {e}")

def main():
    """Função principal"""
    print("🔍 **DIAGNÓSTICO ESPECÍFICO TELA 1 - TÔ SEGURADO**")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Investigar Tela 1
        investigar_tela1(driver)
        
        print("\n✅ **DIAGNÓSTICO CONCLUÍDO!**")
        print("📁 Verifique os arquivos salvos em /opt/imediatoseguros-rpa/temp/")
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-diagnostico-tela1.png")
            print("�� Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
