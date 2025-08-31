#!/usr/bin/env python3
"""
Script de investigação específico para a tela final
Vai tentar navegar até a tela final e capturar dados com tempos de espera maiores
"""

import json
import time
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_chrome():
    """Configura o Chrome para investigação"""
    try:
        chrome_options = Options()
        # Não usar headless para investigação
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        service = Service(chromedriver_path)
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        return driver
    except Exception as e:
        print(f"❌ Erro ao configurar Chrome: {str(e)}")
        return None

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def investigar_tela_final():
    """Investiga especificamente a tela final"""
    
    print("🔍 **INVESTIGAÇÃO DA TELA FINAL**")
    print("="*50)
    
    # Ler parâmetros
    try:
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        print("✅ Parâmetros carregados")
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {str(e)}")
        return
    
    driver = configurar_chrome()
    if not driver:
        return
    
    try:
        # 1. Navegar para a URL base
        url_base = parametros['url_base']
        print(f"🌐 Navegando para: {url_base}")
        driver.get(url_base)
        
        # Aguardar carregamento inicial
        aguardar_carregamento_pagina(driver, 30)
        time.sleep(5)
        
        print(f"📄 Título atual: {driver.title}")
        print(f"🔗 URL atual: {driver.current_url}")
        
        # 2. Tentar encontrar elementos da tela inicial
        print("\n🔍 **PROCURANDO ELEMENTOS DA TELA INICIAL**")
        
        # Procurar por elementos que indicam que estamos na tela inicial
        elementos_iniciais = [
            "Faça agora sua cotação",
            "cotação de Seguro Auto",
            "Selecione o tipo de veículo",
            "Carro"
        ]
        
        for elemento in elementos_iniciais:
            try:
                elementos = driver.find_elements(By.XPATH, f"//*[contains(text(), '{elemento}')]")
                if elementos:
                    print(f"✅ Encontrado: '{elemento}' ({len(elementos)} elementos)")
                    for i, elem in enumerate(elementos[:3]):  # Mostrar apenas os primeiros 3
                        print(f"   {i+1}. Texto: '{elem.text[:100]}...'")
                else:
                    print(f"❌ Não encontrado: '{elemento}'")
            except Exception as e:
                print(f"⚠️ Erro ao procurar '{elemento}': {str(e)}")
        
        # 3. Verificar se há botões ou links para continuar
        print("\n🔍 **PROCURANDO BOTÕES/LINKS PARA CONTINUAR**")
        
        botoes = driver.find_elements(By.TAG_NAME, "button")
        links = driver.find_elements(By.TAG_NAME, "a")
        
        print(f"📊 Botões encontrados: {len(botoes)}")
        print(f"📊 Links encontrados: {len(links)}")
        
        # Mostrar texto dos botões
        for i, botao in enumerate(botoes[:10]):  # Primeiros 10 botões
            try:
                texto = botao.text.strip()
                if texto:
                    print(f"   Botão {i+1}: '{texto}'")
            except:
                pass
        
        # Mostrar texto dos links
        for i, link in enumerate(links[:10]):  # Primeiros 10 links
            try:
                texto = link.text.strip()
                if texto:
                    print(f"   Link {i+1}: '{texto}'")
            except:
                pass
        
        # 4. Verificar se há formulários
        print("\n🔍 **PROCURANDO FORMULÁRIOS**")
        
        forms = driver.find_elements(By.TAG_NAME, "form")
        inputs = driver.find_elements(By.TAG_NAME, "input")
        selects = driver.find_elements(By.TAG_NAME, "select")
        
        print(f"📊 Formulários: {len(forms)}")
        print(f"📊 Inputs: {len(inputs)}")
        print(f"📊 Selects: {len(selects)}")
        
        # 5. Salvar screenshot e HTML para análise
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Screenshot
        screenshot_path = f"temp/investigacao_tela_final_{timestamp}.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        # HTML
        html_path = f"temp/investigacao_tela_final_{timestamp}.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f"📄 HTML salvo: {html_path}")
        
        # 6. Verificar se há JavaScript executando
        print("\n🔍 **VERIFICANDO JAVASCRIPT**")
        
        try:
            # Verificar se há elementos sendo carregados dinamicamente
            elementos_dinamicos = driver.find_elements(By.XPATH, "//*[contains(@class, 'loading') or contains(@class, 'spinner') or contains(@class, 'skeleton')]")
            if elementos_dinamicos:
                print(f"🔄 Elementos dinâmicos encontrados: {len(elementos_dinamicos)}")
                for elem in elementos_dinamicos[:5]:
                    print(f"   - Classe: {elem.get_attribute('class')}")
            else:
                print("✅ Nenhum elemento dinâmico detectado")
        except Exception as e:
            print(f"⚠️ Erro ao verificar elementos dinâmicos: {str(e)}")
        
        # 7. Tentar aguardar mais tempo para ver se algo carrega
        print("\n⏳ **AGUARDANDO CARREGAMENTO ADICIONAL (30s)**")
        
        for i in range(6):  # 30 segundos em intervalos de 5s
            time.sleep(5)
            print(f"   Aguardando... {i+1}/6")
            
            # Verificar se algo mudou
            try:
                elementos_novos = driver.find_elements(By.XPATH, "//*[contains(text(), 'Parabéns') or contains(text(), 'resultado final')]")
                if elementos_novos:
                    print(f"🎉 **ELEMENTOS DA TELA FINAL DETECTADOS!** ({len(elementos_novos)} elementos)")
                    for elem in elementos_novos:
                        print(f"   - Texto: '{elem.text[:200]}...'")
                    break
            except:
                pass
        
        # 8. Verificação final
        print(f"\n📊 **VERIFICAÇÃO FINAL**")
        print(f"   Título: {driver.title}")
        print(f"   URL: {driver.current_url}")
        print(f"   Elementos na página: {len(driver.find_elements(By.XPATH, '//*'))}")
        
        # Verificar se chegamos à tela final
        if "Parabéns" in driver.page_source or "resultado final" in driver.page_source.lower():
            print("🎉 **SUCESSO: TELA FINAL DETECTADA!**")
        else:
            print("❌ **PROBLEMA: TELA FINAL NÃO DETECTADA**")
            print("   Possíveis causas:")
            print("   - O RPA não chegou até a tela final")
            print("   - A tela final demora muito para carregar")
            print("   - Os elementos da tela final têm nomes diferentes")
            print("   - Há um modal ou popup bloqueando")
        
    except Exception as e:
        print(f"❌ **ERRO NA INVESTIGAÇÃO**: {str(e)}")
    
    finally:
        print("\n🔚 **FINALIZANDO INVESTIGAÇÃO**")
        driver.quit()

if __name__ == "__main__":
    # Criar diretório temp se não existir
    os.makedirs("temp", exist_ok=True)
    
    investigar_tela_final()
