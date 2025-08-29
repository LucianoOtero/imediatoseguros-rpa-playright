#!/usr/bin/env python3
"""
Investigação Específica da Tela 6 - Por que não carrega?
Investiga detalhadamente o que está acontecendo na Tela 6
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

def navegar_ate_tela5(driver):
    """Navega até a Tela 5 (confirmação do veículo)"""
    print("🚀 **NAVEGANDO ATÉ TELA 5...**")
    
    # Tela 1: Selecionar Carro
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    time.sleep(5)
    
    carro_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
    )
    carro_button.click()
    print("✅ Tela 1: Carro selecionado")
    time.sleep(3)
    
    # Tela 2: Inserir placa
    placa_input = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
    )
    placa_input.clear()
    placa_input.send_keys("EED3D56")
    print("✅ Tela 2: Placa EED3D56 inserida")
    time.sleep(2)
    
    # Tela 3: Clicar Continuar
    continuar_button = WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
    )
    continuar_button.click()
    print("✅ Tela 3: Continuar clicado")
    time.sleep(5)
    
    # Tela 5: Confirmar veículo
    WebDriverWait(driver, 40).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
    )
    print("✅ Tela 5 carregada - veículo COROLLA detectado")
    time.sleep(3)
    
    # Salvar estado da Tela 5
    with open("/opt/imediatoseguros-rpa/temp/tela5_antes_confirmar.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML da Tela 5 (antes) salvo")
    
    # Procurar e clicar no radio "Sim"
    sim_radio = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
    )
    print("✅ Radio 'Sim' encontrado")
    
    # Clicar via JavaScript
    driver.execute_script("arguments[0].click();", sim_radio)
    print("✅ Veículo confirmado via JavaScript")
    time.sleep(3)
    
    # Salvar estado após confirmação
    with open("/opt/imediatoseguros-rpa/temp/tela5_apos_confirmar.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("�� HTML da Tela 5 (após) salvo")
    
    # Salvar screenshot
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela5_apos_confirmar.png")
    print(" Screenshot da Tela 5 (após) salvo")

def investigar_transicao_tela5_tela6(driver):
    """Investiga a transição da Tela 5 para Tela 6"""
    print("\n🔍 **INVESTIGANDO TRANSIÇÃO TELA 5 → TELA 6...**")
    
    # Verificar estado atual
    print(f"�� URL atual: {driver.current_url}")
    print(f"📄 Título atual: {driver.title}")
    
    # Aguardar transição com timeout muito maior
    print("⏳ Aguardando transição para Tela 6 (timeout: 60s)...")
    
    # Monitorar mudanças na página
    for i in range(60):
        try:
            # Procurar por elementos da Tela 6
            elementos_tela6 = driver.find_elements(By.XPATH, "//*[contains(text(), 'já está segurado') or contains(text(), 'seguro vigente') or contains(text(), 'Não') or contains(text(), 'Sim')]")
            
            if elementos_tela6:
                print(f"�� **TELA 6 DETECTADA no segundo {i+1}!**")
                
                # Salvar HTML da Tela 6
                with open("/opt/imediatoseguros-rpa/temp/tela6_detectada.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print("�� HTML da Tela 6 salvo")
                
                # Salvar screenshot da Tela 6
                driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela6_detectada.png")
                print(" Screenshot da Tela 6 salvo")
                
                # Analisar elementos encontrados
                print(f"✅ {len(elementos_tela6)} elementos da Tela 6 encontrados:")
                for j, elemento in enumerate(elementos_tela6[:5], 1):
                    print(f"   Elemento {j}: {elemento.text[:100]}...")
                
                return True
            
            # Aguardar 1 segundo
            time.sleep(1)
            
            # A cada 10 segundos, salvar estado intermediário
            if (i + 1) % 10 == 0:
                print(f"⏳ {i+1}s - Aguardando...")
                
                # Salvar HTML intermediário
                with open(f"/opt/imediatoseguros-rpa/temp/tela5_intermediario_{i+1}s.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                
                # Salvar screenshot intermediário
                driver.save_screenshot(f"/opt/imediatoseguros-rpa/temp/tela5_intermediario_{i+1}s.png")
        
        except Exception as e:
            print(f"⚠️ Erro durante monitoramento no segundo {i+1}: {e}")
    
    print("❌ **TIMEOUT - TELA 6 NÃO CARREGOU EM 60 SEGUNDOS**")
    
    # Salvar estado final
    with open("/opt/imediatoseguros-rpa/temp/tela5_timeout_final.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML final (timeout) salvo")
    
    # Salvar screenshot final
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela5_timeout_final.png")
    print(" Screenshot final (timeout) salvo")
    
    return False

def analisar_conteudo_pagina(driver):
    """Analisa o conteúdo da página para entender o que está acontecendo"""
    print("\n�� **ANALISANDO CONTEÚDO DA PÁGINA...**")
    
    # Procurar por textos relacionados ao seguro
    try:
        textos_seguro = driver.find_elements(By.XPATH, "//*[contains(text(), 'seguro') or contains(text(), 'Seguro') or contains(text(), 'SEGURO')]")
        if textos_seguro:
            print(f"✅ {len(textos_seguro)} textos relacionados ao seguro encontrados:")
            for i, texto in enumerate(textos_seguro[:5], 1):
                print(f"   Texto {i}: {texto.text}")
        else:
            print("⚠️ Nenhum texto relacionado ao seguro encontrado")
    except:
        print("❌ Erro ao procurar textos relacionados ao seguro")
    
    # Procurar por botões
    try:
        botoes = driver.find_elements(By.TAG_NAME, "button")
        print(f"\n🔍 Total de botões encontrados: {len(botoes)}")
        
        for i, botao in enumerate(botoes[:5]):
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
    
    # Procurar por inputs
    try:
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"\n🔍 Total de inputs encontrados: {len(inputs)}")
        
        for i, input_elem in enumerate(inputs[:5]):
            try:
                id_attr = input_elem.get_attribute("id")
                name_attr = input_elem.get_attribute("name")
                tipo = input_elem.get_attribute("type")
                value = input_elem.get_attribute("value")
                
                print(f"   Input {i+1}: ID='{id_attr}' Name='{name_attr}' Type='{tipo}' Value='{value}'")
            except:
                print(f"   Input {i+1}: Erro ao analisar")
    except:
        print("❌ Erro ao procurar inputs")
    
    # Verificar se há mensagens de erro
    print("\n�� **VERIFICANDO MENSAGENS DE ERRO...**")
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
    print("�� **INVESTIGAÇÃO ESPECÍFICA TELA 6 - TÔ SEGURADO**")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 5
        navegar_ate_tela5(driver)
        
        # Investigar transição Tela 5 → Tela 6
        sucesso = investigar_transicao_tela5_tela6(driver)
        
        if sucesso:
            print("\n✅ **TELA 6 CARREGOU COM SUCESSO!**")
            print("📁 Verifique os arquivos salvos")
        else:
            print("\n❌ **TELA 6 NÃO CARREGOU**")
            print("📁 Verifique os arquivos de timeout")
        
        # Analisar conteúdo da página
        analisar_conteudo_pagina(driver)
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-investigacao-tela6.png")
            print(" Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
