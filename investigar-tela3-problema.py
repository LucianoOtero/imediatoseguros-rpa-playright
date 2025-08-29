#!/usr/bin/env python3
"""
Investigação específica da Tela 3 após selecionar 'Sim'
"""

import time
import tempfile
import shutil
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções otimizadas"""
    print("🔧 Configurando Chrome...")
    
    temp_dir = tempfile.mkdtemp()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver, temp_dir

def aguardar_carregamento_pagina(driver, timeout=30):
    """Aguarda o carregamento completo da página"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def aguardar_estabilizacao(driver, segundos=5):
    """Aguarda a estabilização da página"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)

def clicar_com_delay(driver, by, value, descricao="elemento", timeout=20):
    """Clica em um elemento com delay"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 3)
        
        try:
            elemento = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').click();")
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(1)
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay(driver, by, value, texto, descricao="campo", timeout=20):
    """Preenche um campo com delay"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 2)
        
        elemento.clear()
        time.sleep(0.5)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio"):
    """Clica em um radio button via JavaScript"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        aguardar_estabilizacao(driver, 3)
        
        script = f"""
        var elementos = document.querySelectorAll('input[type="radio"], label, span, div');
        var radioEncontrado = null;
        
        for (var i = 0; i < elementos.length; i++) {{
            var elemento = elementos[i];
            if (elemento.textContent && elemento.textContent.includes('{texto_radio}')) {{
                radioEncontrado = elemento;
                break;
            }}
        }}
        
        if (radioEncontrado) {{
            if (radioEncontrado.tagName === 'LABEL') {{
                var inputId = radioEncontrado.getAttribute('for');
                if (inputId) {{
                    var input = document.getElementById(inputId);
                    if (input) {{
                        input.click();
                        return 'Radio clicado via label: ' + inputId;
                    }}
                }}
            }}
            
            radioEncontrado.click();
            return 'Radio clicado diretamente: ' + radioEncontrado.outerHTML.substring(0, 100);
        }} else {{
            return 'Radio não encontrado';
        }}
        """
        
        resultado = driver.execute_script(script)
        print(f"🎯 {resultado}")
        
        if "Radio clicado" in resultado:
            print(f"✅ Radio {descricao} clicado via JavaScript")
            return True
        else:
            print(f"❌ Radio {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar radio {descricao}: {e}")
        return False

def salvar_estado_tela(driver, tela_num, acao, temp_dir):
    """Salva o estado atual da tela"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    tela_dir = f"temp/investigacao_tela3_problema"
    os.makedirs(tela_dir, exist_ok=True)
    
    html_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.html"
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    screenshot_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.png"
    driver.save_screenshot(screenshot_file)
    
    info_file = f"{tela_dir}/tela_{tela_num:02d}_{acao}.txt"
    with open(info_file, 'w', encoding='utf-8') as f:
        f.write(f"TELA {tela_num:02d}: {acao}\n")
        f.write(f"Timestamp: {timestamp}\n")
        f.write(f"URL: {driver.current_url}\n")
        f.write(f"Título: {driver.title}\n")
        f.write(f"Arquivos salvos em: {os.path.abspath(tela_dir)}\n")
    
    print(f"==================================================================================")
    print(f"📱 **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def investigar_tela3():
    """Investiga especificamente a Tela 3 após selecionar 'Sim'"""
    print("🔍 **INVESTIGANDO PROBLEMA NA TELA 3**")
    print("=" * 80)
    print("🎯 OBJETIVO: Verificar o que acontece após selecionar 'Sim'")
    print("🔧 MÉTODO: Navegar até Tela 3 e analisar estado após seleção")
    print("=" * 80)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # TELA 1: Seleção do tipo de seguro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou")
            return False
        
        salvar_estado_tela(driver, 1, "inicial", None)
        aguardar_estabilizacao(driver, 5)
        
        # Clicar no botão Carro
        if not clicar_com_delay(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
            print("❌ Erro: Falha ao clicar no botão Carro")
            return False
        
        print("⏳ Aguardando carregamento completo da página...")
        time.sleep(5)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou após selecionar Carro")
            return False
        
        aguardar_estabilizacao(driver, 5)
        
        # TELA 2: Inserção da placa
        print("\n📱 TELA 2: Inserindo placa...")
        aguardar_estabilizacao(driver, 3)
        salvar_estado_tela(driver, 2, "inicial", None)
        
        # Preencher placa
        if not preencher_com_delay(driver, By.ID, "placaTelaDadosPlaca", "KVA-1791", "placa"):
            print("❌ Erro: Falha ao preencher placa")
            return False
        
        aguardar_estabilizacao(driver, 3)
        salvar_estado_tela(driver, 2, "placa_inserida", None)
        
        # TELA 3: Clicar em Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        
        if not clicar_com_delay(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 3")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 3, "apos_clique", None)
        
        # TELA 3: Confirmação do veículo
        print("\n📱 TELA 3: Confirmando veículo...")
        
        try:
            # Aguardar elementos da confirmação do veículo
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ECOSPORT')]"))
            )
            print("✅ Tela 3 carregada - confirmação do ECOSPORT detectada!")
            
            salvar_estado_tela(driver, 3, "confirmacao_veiculo", None)
            
            if not aguardar_carregamento_pagina(driver, 20):
                print("❌ Erro: Página não carregou completamente")
                return False
            
            salvar_estado_tela(driver, 3, "confirmacao_carregada", None)
            
            # Selecionar "Sim" para confirmação do veículo
            print("⏳ Selecionando 'Sim' para confirmação do veículo...")
            
            if not clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
                print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
            
            # AGUARDAR MUITO MAIS TEMPO APÓS SELECIONAR 'SIM'
            print("⏳ Aguardando estabilização após selecionar 'Sim'...")
            time.sleep(10)
            
            salvar_estado_tela(driver, 3, "apos_selecionar_sim", None)
            
            # ANALISAR ESTADO ATUAL DA PÁGINA
            print("\n🔍 ANALISANDO ESTADO ATUAL DA PÁGINA...")
            print(f"URL atual: {driver.current_url}")
            print(f"Título atual: {driver.title}")
            
            # Procurar por botões disponíveis
            try:
                botoes = driver.find_elements(By.TAG_NAME, "button")
                print(f"�� Botões encontrados: {len(botoes)}")
                for i, botao in enumerate(botoes):
                    try:
                        texto = botao.text.strip()
                        if texto:
                            print(f"   {i+1}. Botão: '{texto}'")
                    except:
                        pass
            except:
                print("⚠️ Não foi possível listar botões")
            
            # Procurar por elementos de texto
            try:
                elementos_texto = driver.find_elements(By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'continuar')]")
                print(f"�� Elementos 'Continuar' encontrados: {len(elementos_texto)}")
                for i, elem in enumerate(elementos_texto):
                    try:
                        texto = elem.text.strip()
                        if texto:
                            print(f"   {i+1}. Elemento: '{texto}' (tag: {elem.tag_name})")
                    except:
                        pass
            except:
                print("⚠️ Não foi possível listar elementos 'Continuar'")
            
            # Tentar clicar em Continuar com diferentes estratégias
            print("\n🔧 TENTANDO DIFERENTES ESTRATÉGIAS PARA CONTINUAR...")
            
            # Estratégia 1: Botão com texto "Continuar"
            try:
                print("🎯 Estratégia 1: Botão com texto 'Continuar'")
                botao_continuar = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continuar')]"))
                )
                botao_continuar.click()
                print("✅ Estratégia 1 funcionou!")
                return True
            except:
                print("❌ Estratégia 1 falhou")
            
            # Estratégia 2: Elemento p com texto "Continuar"
            try:
                print("🎯 Estratégia 2: Elemento p com texto 'Continuar'")
                elemento_continuar = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
                )
                elemento_continuar.click()
                print("✅ Estratégia 2 funcionou!")
                return True
            except:
                print("❌ Estratégia 2 falhou")
            
            # Estratégia 3: JavaScript genérico
            try:
                print("🎯 Estratégia 3: JavaScript genérico")
                resultado = driver.execute_script("""
                    var elementos = document.querySelectorAll('button, p, div, span');
                    var continuarEncontrado = null;
                    
                    for (var i = 0; i < elementos.length; i++) {
                        var elemento = elementos[i];
                        if (elemento.textContent && elemento.textContent.includes('Continuar')) {
                            continuarEncontrado = elemento;
                            break;
                        }
                    }
                    
                    if (continuarEncontrado) {
                        continuarEncontrado.click();
                        return 'Continuar clicado via JavaScript: ' + continuarEncontrado.outerHTML.substring(0, 100);
                    } else {
                        return 'Continuar não encontrado';
                    }
                """)
                print(f"🎯 {resultado}")
                
                if "Continuar clicado" in resultado:
                    print("✅ Estratégia 3 funcionou!")
                    return True
                else:
                    print("❌ Estratégia 3 falhou")
            except Exception as e:
                print(f"❌ Estratégia 3 falhou: {e}")
            
            print("❌ Todas as estratégias falharam")
            return False
            
        except Exception as e:
            print(f"❌ Erro na confirmação Tela 3: {e}")
            return False
        
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE INVESTIGAÇÃO:** {e}")
        return False
    
    finally:
        # Limpeza
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    investigar_tela3()
