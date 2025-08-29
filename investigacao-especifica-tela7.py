#!/usr/bin/env python3
"""
Investigação Específica da Tela 7 - Por que não carrega a estimativa?
Investiga detalhadamente o que está acontecendo na Tela 7
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

def navegar_ate_tela6(driver):
    """Navega até a Tela 6 (seguro vigente)"""
    print("🚀 **NAVEGANDO ATÉ TELA 6...**")
    
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
    
    # Procurar e clicar no radio "Sim"
    sim_radio = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
    )
    driver.execute_script("arguments[0].click();", sim_radio)
    print("✅ Veículo confirmado via JavaScript")
    time.sleep(3)
    
    # Tela 6: Aguardar carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "confirmarVeiculoTelaInformacoesVeiculo"))
    )
    print("✅ Tela 6 carregada - radio buttons detectados")
    time.sleep(3)
    
    # Verificar se "Não" está selecionado
    try:
        nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
        if not nao_radio.is_selected():
            driver.execute_script("arguments[0].click();", nao_radio)
            print("✅ Radio 'Não' selecionado")
            time.sleep(2)
    except:
        print("⚠️ Radio 'Não' não encontrado")
    
    # Salvar estado da Tela 6
    with open("/opt/imediatoseguros-rpa/temp/tela6_antes_continuar.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML da Tela 6 (antes) salvo")
    
    # Salvar screenshot
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela6_antes_continuar.png")
    print(" Screenshot da Tela 6 (antes) salvo")

def investigar_transicao_tela6_tela7(driver):
    """Investiga a transição da Tela 6 para Tela 7"""
    print("\n🔍 **INVESTIGANDO TRANSIÇÃO TELA 6 → TELA 7...**")
    
    # Verificar estado atual
    print(f" URL atual: {driver.current_url}")
    print(f"📄 Título atual: {driver.title}")
    
    # Clicar em Continuar na Tela 6
    print("⏳ Clicando em Continuar na Tela 6...")
    continuar_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "gtm-telaInfosAutoContinuar"))
    )
    continuar_button.click()
    print("✅ Continuar clicado na Tela 6")
    
    # Aguardar transição com timeout muito maior
    print("⏳ Aguardando transição para Tela 7 (timeout: 120s)...")
    
    # Monitorar mudanças na página
    for i in range(120):
        try:
            # Procurar por elementos da Tela 7
            elementos_tela7 = driver.find_elements(By.XPATH, "//*[contains(text(), 'estimativa inicial') or contains(text(), 'carregando') or contains(text(), 'aguarde') or contains(text(), 'calculando')]")
            
            if elementos_tela7:
                print(f" **TELA 7 DETECTADA no segundo {i+1}!**")
                
                # Salvar HTML da Tela 7
                with open("/opt/imediatoseguros-rpa/temp/tela7_detectada.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print(" HTML da Tela 7 salvo")
                
                # Salvar screenshot da Tela 7
                driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela7_detectada.png")
                print(" Screenshot da Tela 7 salvo")
                
                # Analisar elementos encontrados
                print(f"✅ {len(elementos_tela7)} elementos da Tela 7 encontrados:")
                for j, elemento in enumerate(elementos_tela7[:5], 1):
                    print(f"   Elemento {j}: {elemento.text[:100]}...")
                
                return True
            
            # Aguardar 1 segundo
            time.sleep(1)
            
            # A cada 15 segundos, salvar estado intermediário
            if (i + 1) % 15 == 0:
                print(f"⏳ {i+1}s - Aguardando...")
                
                # Salvar HTML intermediário
                with open(f"/opt/imediatoseguros-rpa/temp/tela6_intermediario_{i+1}s.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                
                # Salvar screenshot intermediário
                driver.save_screenshot(f"/opt/imediatoseguros-rpa/temp/tela6_intermediario_{i+1}s.png")
        
        except Exception as e:
            print(f"⚠️ Erro durante monitoramento no segundo {i+1}: {e}")
    
    print("❌ **TIMEOUT - TELA 7 NÃO CARREGOU EM 120 SEGUNDOS**")
    
    # Salvar estado final
    with open("/opt/imediatoseguros-rpa/temp/tela6_timeout_final.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    print("📄 HTML final (timeout) salvo")
    
    # Salvar screenshot final
    driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela6_timeout_final.png")
    print(" Screenshot final (timeout) salvo")
    
    return False

def analisar_conteudo_pagina(driver):
    """Analisa o conteúdo da página para entender o que está acontecendo"""
    print("\n **ANALISANDO CONTEÚDO DA PÁGINA...**")
    
    # Procurar por textos relacionados à estimativa
    try:
        textos_estimativa = driver.find_elements(By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'Estimativa') or contains(text(), 'ESTIMATIVA') or contains(text(), 'carregando') or contains(text(), 'aguarde')]")
        if textos_estimativa:
            print(f"✅ {len(textos_estimativa)} textos relacionados à estimativa encontrados:")
            for i, texto in enumerate(textos_estimativa[:5], 1):
                print(f"   Texto {i}: {texto.text}")
        else:
            print("⚠️ Nenhum texto relacionado à estimativa encontrado")
    except:
        print("❌ Erro ao procurar textos relacionados à estimativa")
    
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
        erros = driver.find_elements(By.XPATH, "//*[contains(text(), 'erro') or contains(text(), 'Erro') or contains(text(), 'ERRO') or contains(text(), 'falha') or contains(text(), 'Falha') or contains(text(), 'timeout') or contains(text(), 'Timeout')]")
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

def main():
    """Função principal"""
    print(" **INVESTIGAÇÃO ESPECÍFICA TELA 7 - TÔ SEGURADO**")
    print("=" * 60)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        navegar_ate_tela6(driver)
        
        # Investigar transição Tela 6 → Tela 7
        sucesso = investigar_transicao_tela6_tela7(driver)
        
        if sucesso:
            print("\n✅ **TELA 7 CARREGOU COM SUCESSO!**")
            print("📁 Verifique os arquivos salvos")
        else:
            print("\n❌ **TELA 7 NÃO CARREGOU**")
            print("📁 Verifique os arquivos de timeout")
        
        # Analisar conteúdo da página
        analisar_conteudo_pagina(driver)
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-investigacao-tela7.png")
            print(" Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
