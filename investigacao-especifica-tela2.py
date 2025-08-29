#!/usr/bin/env python3
"""
Investigação Específica da Tela 2 - Por que o campo placa não aparece?
Investiga detalhadamente o que está na Tela 2 após selecionar Carro
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

def investigar_tela2_detalhadamente(driver):
    """Investiga a Tela 2 detalhadamente"""
    print("🔍 **INVESTIGANDO TELA 2 DETALHADAMENTE...**")
    
    # Navegar até Tela 1
    print("�� Navegando até Tela 1...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    time.sleep(5)
    
    # Selecionar Carro
    carro_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
    )
    print("✅ Botão Carro encontrado")
    
    # Salvar estado antes do clique
    with open("/opt/imediatoseguros-rpa/temp/tela1_antes_carro.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML da Tela 1 (antes) salvo")
    
    # Clicar no Carro
    carro_button.click()
    print("✅ Carro selecionado")
    time.sleep(10)  # Aguardar mais tempo
    
    # Salvar estado após clique
    with open("/opt/imediatoseguros-rpa/temp/tela2_apos_carro.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("�� HTML da Tela 2 (após) salvo")
    
    # Salvar screenshot
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela2_apos_carro.png")
    print(" Screenshot da Tela 2 salvo")
    
    # Verificar informações da página
    print(f"\n�� URL atual: {driver.current_url}")
    print(f"📄 Título atual: {driver.title}")
    
    # Procurar por elementos relacionados à placa
    print("\n🔍 **PROCURANDO ELEMENTOS RELACIONADOS À PLACA...**")
    
    # Procurar por input com id "placaTelaPlaca"
    try:
        placa_input = driver.find_element(By.ID, "placaTelaPlaca")
        print("✅ Campo de placa encontrado por ID!")
        print(f"   Tag: {placa_input.tag_name}")
        print(f"   Classes: {placa_input.get_attribute('class')}")
        print(f"   Placeholder: {placa_input.get_attribute('placeholder')}")
        print(f"   Visível: {placa_input.is_displayed()}")
        print(f"   Habilitado: {placa_input.is_enabled()}")
    except:
        print("❌ Campo de placa NÃO encontrado por ID")
    
    # Procurar por qualquer input
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n🔍 Total de inputs encontrados: {len(inputs)}")
        
        for i, input_elem in enumerate(inputs[:10]):  # Mostrar apenas os 10 primeiros
            try:
                id_attr = input_elem.get_attribute("id")
                name_attr = input_elem.get_attribute("name")
                placeholder = input_elem.get_attribute("placeholder")
                tipo = input_elem.get_attribute("type")
                classes = input_elem.get_attribute("class")
                
                print(f"   Input {i+1}: ID='{id_attr}' Name='{name_attr}' Type='{tipo}'")
                print(f"      Placeholder: {placeholder}")
                print(f"      Classes: {classes}")
                print(f"      Visível: {input_elem.is_displayed()}")
            except:
                print(f"   Input {i+1}: Erro ao analisar")
    except:
        print("❌ Erro ao procurar inputs")
    
    # Procurar por formulários
    try:
        forms = driver.find_elements(By.TAG_NAME, "form")
        print(f"\n🔍 Total de formulários encontrados: {len(forms)}")
        
        for i, form in enumerate(forms):
            try:
                id_attr = form.get_attribute("id")
                action = form.get_attribute("action")
                method = form.get_attribute("method")
                classes = form.get_attribute("class")
                
                print(f"   Form {i+1}: ID='{id_attr}' Action='{action}' Method='{method}'")
                print(f"      Classes: {classes}")
            except:
                print(f"   Form {i+1}: Erro ao analisar")
    except:
        print("❌ Erro ao procurar formulários")
    
    # Procurar por botões
    try:
        botoes = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n🔍 Total de botões encontrados: {len(botoes)}")
        
        for i, botao in enumerate(botoes[:5]):  # Mostrar apenas os 5 primeiros
            try:
                texto = botao.text
                id_attr = botao.get_attribute("id")
                classes = botao.get_attribute("class")
                
                print(f"   Botão {i+1}: ID='{id_attr}' Texto='{texto[:50]}...'")
                print(f"      Classes: {classes}")
                print(f"      Visível: {botao.is_displayed()}")
            except:
                print(f"   Botão {i+1}: Erro ao analisar")
    except:
        print("❌ Erro ao procurar botões")
    
    # Procurar por mensagens de erro
    print("\n🔍 **PROCURANDO MENSAGENS DE ERRO...**")
    try:
        erros = driver.find_elements(By.XPATH, "//*[contains(text(), 'erro') or contains(text(), 'Erro') or contains(text(), 'ERRO') or contains(text(), 'falha') or contains(text(), 'Falha')]")
        if erros:
            print(f"⚠️ {len(erros)} mensagens de erro encontradas:")
            for i, erro in enumerate(erros[:5], 1):
                print(f"   Erro {i}: {erro.text}")
        else:
            print("✅ Nenhuma mensagem de erro encontrada")
    except:
        print("❌ Erro ao procurar mensagens de erro")
    
    # Procurar por texto relacionado à placa
    print("\n�� **PROCURANDO TEXTO RELACIONADO À PLACA...**")
    try:
        textos_placa = driver.find_elements(By.XPATH, "//*[contains(text(), 'placa') or contains(text(), 'Placa') or contains(text(), 'PLACA')]")
        if textos_placa:
            print(f"✅ {len(textos_placa)} textos relacionados à placa encontrados:")
            for i, texto in enumerate(textos_placa[:5], 1):
                print(f"   Texto {i}: {texto.text}")
        else:
            print("⚠️ Nenhum texto relacionado à placa encontrado")
    except:
        print("❌ Erro ao procurar textos relacionados à placa")
    
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
    except:
        print("❌ Erro ao procurar iframes")
    
    # Verificar console do navegador
    print("\n🔍 **VERIFICANDO CONSOLE DO NAVEGADOR...**")
    try:
        logs = driver.get_log("browser")
        if logs:
            print(f"✅ {len(logs)} logs do console encontrados:")
            for log in logs[:5]:
                print(f"   {log['level']}: {log['message']}")
        else:
            print("ℹ️ Nenhum log do console encontrado")
    except Exception as e:
        print(f"❌ Erro ao verificar console: {e}")

def main():
    """Função principal"""
    print("�� **INVESTIGAÇÃO ESPECÍFICA TELA 2 - TÔ SEGURADO**")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Investigar Tela 2
        investigar_tela2_detalhadamente(driver)
        
        print("\n✅ **INVESTIGAÇÃO CONCLUÍDA!**")
        print("📁 Verifique os arquivos salvos em /opt/imediatoseguros-rpa/temp/")
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-investigacao-tela2.png")
            print(" Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
