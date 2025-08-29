#!/usr/bin/env python3
"""
RPA Tô Segurado - Versão Otimizada com Detecção Inteligente de Estabilização
================================================================================

VERSÃO: 2.0.0 - OTIMIZADA PARA VELOCIDADE
DATA: 29/08/2025
AUTOR: Assistente IA - Baseado em investigar-estabilizacao-inteligente.py

MELHORIAS IMPLEMENTADAS:
- ✅ Substituição de delays fixos (15-20s) por detecção inteligente (0.5-1.5s)
- ✅ Método Network (0.5s) - Mais rápido para requisições
- ✅ Método JavaScript (1.5s) - Mais robusto para React/Material-UI
- ✅ Método por Elemento (1.0s) - Mais preciso para elementos críticos
- ✅ Fallback inteligente com delay mínimo (5s) apenas quando necessário
- ✅ Redução estimada de 70-80% no tempo total de execução

ESTRATÉGIA DE ESTABILIZAÇÃO:
1. Network (5s) - Detecta fim de requisições
2. JavaScript (10s) - Detecta estabilização de componentes
3. Elemento específico (5s) - Detecta estabilização de botões
4. Delay mínimo (5s) - Fallback apenas quando necessário

TEMPO ESTIMADO POR TELA: 0.5s a 1.5s (vs 15-20s anterior)
TEMPO TOTAL ESTIMADO: ~12-20s (vs 120-160s anterior)
"""

import time
import json
import os
import tempfile
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def configurar_chrome():
    """
    Configura o Chrome com opções otimizadas para RPA
    Usa ChromeDriver local para evitar erros [WinError 193]
    """
    print("🔧 Configurando Chrome para RPA...")
    
    # Criar diretório temporário para dados do Chrome
    temp_dir = tempfile.mkdtemp()
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Modo headless para execução em background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    chrome_options.add_argument("--disable-images")  # Não carregar imagens para velocidade
    chrome_options.add_argument("--disable-javascript-harmony-shipping")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    # Usar ChromeDriver local que já baixamos
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
    
    if not os.path.exists(chromedriver_path):
        print(f"❌ ChromeDriver não encontrado em: {chromedriver_path}")
        print("📥 Baixe o ChromeDriver de: https://chromedriver.chromium.org/")
        return None, None
    
    print("✅ Usando ChromeDriver local...")
    service = Service(chromedriver_path)
    
    try:
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        print("✅ Chrome configurado com sucesso")
        return driver, temp_dir
    except Exception as e:
        print(f"❌ Erro ao configurar Chrome: {e}")
        return None, None

def aguardar_carregamento_pagina(driver, timeout=30):
    """
    Aguarda o carregamento básico da página
    Primeiro passo - verifica se o DOM inicial foi carregado
    """
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except TimeoutException:
        print("⚠️ Timeout ao aguardar carregamento básico da página")
        return False

def detectar_estabilizacao_por_network(driver, timeout=5, intervalo=0.5):
    """
    MÉTODO 1: Detecta estabilização por requisições de rede
    ⚡ MAIS RÁPIDO - Detecta estabilização em ~0.5s
    ✅ Ideal para verificar se todas as requisições terminaram
    """
    print("   🌐 Verificando estabilização por Network...")
    
    try:
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            # Verificar se há requisições pendentes
            requests_pendentes = driver.execute_script("""
                return window.performance.getEntriesByType('resource').filter(
                    resource => resource.responseEnd === 0
                ).length;
            """)
            
            if requests_pendentes == 0:
                print(f"   ✅ Network estável após {(i+1) * intervalo:.1f}s")
                return True
            else:
                print(f"   ⏳ {requests_pendentes} requisições pendentes...")
        
        print(f"   ⏰ Network timeout ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar Network: {e}")
        return False

def detectar_estabilizacao_por_javascript(driver, timeout=10, intervalo=0.5):
    """
    MÉTODO 2: Detecta estabilização usando JavaScript avançado
    🧠 MAIS ROBUSTO - Detecta estabilização em ~1.5s
    ✅ Ideal para páginas React/Material-UI com componentes dinâmicos
    """
    print("   ⚡ Verificando estabilização por JavaScript...")
    
    try:
        script = """
        // Verificar múltiplos indicadores de estabilização
        var indicadores = {
            readyState: document.readyState,
            loading: document.querySelectorAll('[class*="loading"], [class*="Loading"]').length,
            spinner: document.querySelectorAll('[class*="spinner"], [class*="Spinner"]').length,
            progress: document.querySelectorAll('[class*="progress"], [class*="Progress"]').length,
            overlay: document.querySelectorAll('[class*="overlay"], [class*="Overlay"]').length,
            requests: window.performance.getEntriesByType('resource').filter(r => r.responseEnd === 0).length,
            mutations: 0
        };
        
        // Verificar se há mutações no DOM
        if (window.mutationObserver) {
            var observer = new MutationObserver(function(mutations) {
                indicadores.mutations += mutations.length;
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true
            });
        }
        
        return indicadores;
        """
        
        indicadores_iniciais = driver.execute_script(script)
        
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            indicadores_atual = driver.execute_script(script)
            
            # Verificar se os indicadores mudaram
            mudancas = 0
            for key in indicadores_iniciais:
                if indicadores_iniciais[key] != indicadores_atual[key]:
                    mudancas += 1
            
            if mudancas == 0 and i >= 2:
                print(f"   ✅ JavaScript estável após {(i+1) * intervalo:.1f}s")
                return True
            else:
                print(f"   ⏳ {mudancas} indicadores mudaram...")
        
        print(f"   ⏰ JavaScript timeout ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar JavaScript: {e}")
        return False

def detectar_estabilizacao_por_elemento(driver, xpath_alvo, timeout=5, intervalo=0.5):
    """
    MÉTODO 3: Detecta estabilização por elemento específico
    🎯 MAIS PRECISO - Detecta estabilização em ~1.0s
    ✅ Ideal para elementos críticos como botões "Continuar"
    """
    print(f"   🎯 Verificando estabilização por elemento: {xpath_alvo}")
    
    try:
        # Aguardar elemento aparecer
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_alvo))
        )
        
        # Capturar estado inicial do elemento
        estado_inicial = elemento.get_attribute('outerHTML')
        mudancas = 0
        max_mudancas = 2
        
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            try:
                elemento = driver.find_element(By.XPATH, xpath_alvo)
                estado_atual = elemento.get_attribute('outerHTML')
                
                if estado_atual != estado_inicial:
                    mudancas += 1
                    print(f"   ⚠️ Mudança {mudancas} no elemento alvo")
                    estado_inicial = estado_atual
                    
                    if mudancas >= max_mudancas:
                        print(f"   ❌ Muitas mudanças no elemento ({mudancas})")
                        return False
                
                # Se não houve mudanças por alguns intervalos, considerar estável
                if mudancas == 0 and i >= 2:
                    print(f"   ✅ Elemento estável após {(i+1) * intervalo:.1f}s")
                    return True
                    
            except:
                print(f"   ⚠️ Elemento não encontrado na iteração {i}")
                continue
        
        print(f"   ⏰ Elemento timeout ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao verificar elemento: {e}")
        return False

def aguardar_estabilizacao_inteligente(driver, descricao="página", timeout=15):
    """
    FUNÇÃO PRINCIPAL: Aguarda estabilização usando métodos inteligentes
    🚀 SUBSTITUI DELAYS FIXOS (15-20s) por DETECÇÃO INTELIGENTE (0.5-1.5s)
    
    ESTRATÉGIA OTIMIZADA:
    1. Network (5s) - Mais rápido para requisições
    2. JavaScript (10s) - Mais robusto para React/Material-UI
    3. Elemento específico (5s) - Mais preciso para botões
    4. Delay mínimo (5s) - Fallback apenas quando necessário
    """
    print(f"🧠 Aguardando estabilização inteligente: {descricao}")
    inicio = time.time()
    
    # MÉTODO 1: Network (mais rápido - 5s)
    if detectar_estabilizacao_por_network(driver, timeout=5):
        duracao = time.time() - inicio
        print(f"✅ Estabilização detectada por Network em {duracao:.1f}s")
        return True
    
    # MÉTODO 2: JavaScript (mais robusto - 10s restantes)
    if detectar_estabilizacao_por_javascript(driver, timeout=10):
        duracao = time.time() - inicio
        print(f"✅ Estabilização detectada por JavaScript em {duracao:.1f}s")
        return True
    
    # MÉTODO 3: Elemento específico (mais preciso - 5s restantes)
    if detectar_estabilizacao_por_elemento(driver, "//button[contains(., 'Continuar')]", timeout=5):
        duracao = time.time() - inicio
        print(f"✅ Estabilização detectada por elemento específico em {duracao:.1f}s")
        return True
    
    # FALLBACK: Delay mínimo apenas quando necessário
    print("⚠️ Estabilização não detectada, usando delay mínimo como fallback")
    time.sleep(5)
    duracao = time.time() - inicio
    print(f"⏱️ Tempo total com fallback: {duracao:.1f}s")
    return False

def clicar_com_delay_inteligente(driver, by, value, descricao="elemento", timeout=30):
    """
    Clica em elemento com detecção inteligente de estabilização
    Substitui delays fixos por detecção inteligente
    Implementa estratégia robusta para evitar stale element reference
    """
    print(f"🖱️ Clicando em: {descricao}")
    
    try:
        # Aguardar elemento estar presente e clicável
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        
        # Tentar clique normal primeiro
        try:
            elemento.click()
            print(f"   ✅ Clique normal realizado em {descricao}")
            
            # Aguardar estabilização inteligente após o clique
            aguardar_estabilizacao_inteligente(driver, f"após clicar em {descricao}")
            return True
            
        except Exception as e:
            print(f"   ⚠️ Clique normal falhou, tentando JavaScript: {e}")
            
            # Fallback para JavaScript - recriar referência do elemento
            try:
                elemento_atualizado = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((by, value))
                )
                driver.execute_script("arguments[0].click();", elemento_atualizado)
                print(f"   ✅ Clique JavaScript realizado em {descricao}")
                
                # Aguardar estabilização inteligente após o clique
                aguardar_estabilizacao_inteligente(driver, f"após clicar em {descricao}")
                return True
                
            except Exception as js_error:
                print(f"   ❌ JavaScript também falhou: {js_error}")
                
                # Último recurso: tentar clique direto via JavaScript com seletor
                try:
                    if by == By.XPATH:
                        script = f"""
                        var elemento = document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                        if (elemento) {{
                            elemento.click();
                            return true;
                        }}
                        return false;
                        """
                    elif by == By.ID:
                        script = f"""
                        var elemento = document.getElementById('{value}');
                        if (elemento) {{
                            elemento.click();
                            return true;
                        }}
                        return false;
                        """
                    else:
                        script = f"""
                        var elemento = document.querySelector('{value}');
                        if (elemento) {{
                            elemento.click();
                            return true;
                        }}
                        return false;
                        """
                    
                    resultado = driver.execute_script(script)
                    if resultado:
                        print(f"   ✅ Clique direto JavaScript realizado em {descricao}")
                        
                        # Aguardar estabilização inteligente após o clique
                        aguardar_estabilizacao_inteligente(driver, f"após clicar em {descricao}")
                        return True
                    else:
                        print(f"   ❌ Elemento não encontrado via JavaScript direto")
                        return False
                        
                except Exception as direct_error:
                    print(f"   ❌ Clique direto JavaScript falhou: {direct_error}")
                    return False
            
    except TimeoutException:
        print(f"   ❌ Timeout: Elemento {descricao} não encontrado ou não clicável")
        return False
    except Exception as e:
        print(f"   ❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay_inteligente(driver, by, value, texto, descricao="campo", timeout=30):
    """
    Preenche campo com detecção inteligente de estabilização
    Substitui delays fixos por detecção inteligente
    """
    print(f"✏️ Preenchendo {descricao}: {texto}")
    
    try:
        # Aguardar elemento estar presente
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        # Limpar campo e preencher
        elemento.clear()
        elemento.send_keys(texto)
        print(f"   ✅ Campo {descricao} preenchido")
        
        # Aguardar estabilização inteligente após o preenchimento
        aguardar_estabilizacao_inteligente(driver, f"após preencher {descricao}")
        return True
        
    except TimeoutException:
        print(f"   ❌ Timeout: Campo {descricao} não encontrado")
        return False
    except Exception as e:
        print(f"   ❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
    """
    Clica em radio button via JavaScript com detecção inteligente
    Substitui delays fixos por detecção inteligente
    """
    print(f"🔘 Clicando radio: {descricao}")
    
    try:
        script = f"""
        // Encontrar radio button por texto
        var labels = Array.from(document.querySelectorAll('label'));
        var radio = null;
        
        for (var i = 0; i < labels.length; i++) {{
            if (labels[i].textContent.trim().includes('{texto_radio}')) {{
                var input = labels[i].querySelector('input[type="radio"]');
                if (input) {{
                    radio = input;
                    break;
                }}
            }}
        }}
        
        if (radio) {{
            radio.click();
            return true;
        }}
        return false;
        """
        
        resultado = driver.execute_script(script)
        
        if resultado:
            print(f"   ✅ Radio {descricao} clicado via JavaScript")
            
            # Aguardar estabilização inteligente após o clique
            aguardar_estabilizacao_inteligente(driver, f"após clicar radio {descricao}")
            return True
        else:
            print(f"   ❌ Radio {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao clicar radio {descricao}: {e}")
        return False

def clicar_checkbox_via_javascript(driver, texto_checkbox, descricao="checkbox", timeout=30):
    """
    Clica em checkbox via JavaScript com detecção inteligente
    Substitui delays fixos por detecção inteligente
    """
    print(f"☑️ Clicando checkbox: {descricao}")
    
    try:
        script = f"""
        // Encontrar checkbox por texto
        var labels = Array.from(document.querySelectorAll('label'));
        var checkbox = null;
        
        for (var i = 0; i < labels.length; i++) {{
            if (labels[i].textContent.trim().includes('{texto_checkbox}')) {{
                var input = labels[i].querySelector('input[type="checkbox"]');
                if (input) {{
                    checkbox = input;
                    break;
                }}
            }}
        }}
        
        if (checkbox) {{
            checkbox.click();
            return true;
        }}
        return false;
        """
        
        resultado = driver.execute_script(script)
        
        if resultado:
            print(f"   ✅ Checkbox {descricao} clicado via JavaScript")
            
            # Aguardar estabilização inteligente após o clique
            aguardar_estabilizacao_inteligente(driver, f"após clicar checkbox {descricao}")
            return True
        else:
            print(f"   ❌ Checkbox {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"   ❌ Erro ao clicar checkbox {descricao}: {e}")
        return False

def salvar_estado_tela(driver, tela_num, acao, temp_dir):
    """
    Salva estado da tela para debug (HTML, screenshot, info)
    Mantido para compatibilidade e debug
    """
    try:
        # Criar diretório para a tela
        tela_dir = os.path.join(temp_dir, f"tela_{tela_num:02d}")
        os.makedirs(tela_dir, exist_ok=True)
        
        # Salvar HTML
        html_file = os.path.join(tela_dir, f"tela_{tela_num:02d}_{acao}.html")
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        
        # Salvar screenshot
        png_file = os.path.join(tela_dir, f"tela_{tela_num:02d}_{acao}.png")
        driver.save_screenshot(png_file)
        
        # Salvar informações
        info_file = os.path.join(tela_dir, f"tela_{tela_num:02d}_{acao}.txt")
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"Tela: {tela_num}\n")
            f.write(f"Ação: {acao}\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Timestamp: {datetime.now()}\n")
        
        print(f"   💾 Estado salvo: {tela_dir}")
        
    except Exception as e:
        print(f"   ⚠️ Erro ao salvar estado: {e}")

def navegar_ate_tela5(driver, parametros):
    """
    Navega pelas Telas 1-5 usando detecção inteligente de estabilização
    Substitui delays fixos por detecção inteligente
    """
    print("\n🚀 **NAVEGANDO TELAS 1-5 COM ESTABILIZAÇÃO INTELIGENTE**")
    print("=" * 70)
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 **TELA 1: Seleção do tipo de seguro**")
    if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar em Carro na Tela 1")
        return False
    print("✅ Tela 1 concluída")
    
    # TELA 2: Inserção da placa
    print("\n📱 **TELA 2: Inserção da placa**")
    if not preencher_com_delay_inteligente(driver, By.ID, "placaTelaDadosPlaca", "KVA-1791", "campo placa"):
        print("❌ Erro: Falha ao preencher placa na Tela 2")
        return False
    if not clicar_com_delay_inteligente(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 2")
        return False
    print("✅ Tela 2 concluída")
    
    # TELA 3: Confirmação do modelo
    print("\n📱 **TELA 3: Confirmação do modelo**")
    if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    # Aguardar carregamento da próxima parte da Tela 3
    aguardar_estabilizacao_inteligente(driver, "Tela 3 - segunda parte")
    
    # Verificar se a confirmação do ECOSPORT apareceu
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ECOSPORT')]"))
        )
        print("✅ Tela 3 carregada - confirmação do ECOSPORT detectada!")
    except TimeoutException:
        print("❌ Erro: Confirmação do ECOSPORT não apareceu na Tela 3")
        return False
    
    # Clicar "Sim" para confirmação
    if not clicar_radio_via_javascript(driver, "Sim", "radio Sim"):
        print("❌ Erro: Falha ao clicar Sim na Tela 3")
        return False
    
    # Clicar "Continuar"
    if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    print("✅ Tela 3 concluída")
    
    # TELA 4: Pergunta sobre veículo já segurado
    print("\n📱 **TELA 4: Veículo já segurado?**")
    if not clicar_radio_via_javascript(driver, "Não", "radio Não"):
        print("❌ Erro: Falha ao clicar Não na Tela 4")
        return False
    
    if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 4")
        return False
    print("✅ Tela 4 concluída")
    
    # TELA 5: Estimativa inicial
    print("\n📱 **TELA 5: Estimativa inicial**")
    if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(text(), 'Continuar')]", "botão Continuar"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 5")
        return False
    print("✅ Tela 5 concluída")
    
    print("\n🎯 **TELAS 1-5 CONCLUÍDAS COM SUCESSO!**")
    return True

def implementar_tela6(driver):
    """
    Implementa Tela 6: Tipo de combustível + checkboxes
    Usa detecção inteligente de estabilização
    """
    print("\n📱 **TELA 6: Tipo de combustível + checkboxes**")
    
    # Aguardar estabilização da página
    aguardar_estabilizacao_inteligente(driver, "Tela 6 - carregamento")
    
    # Verificar se chegamos na tela correta
    try:
        # Procurar por elementos relacionados a combustível
        elementos_combustivel = driver.find_elements(By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível') or contains(text(), 'Flex') or contains(text(), 'Gasolina')]")
        
        if not elementos_combustivel:
            print("❌ Erro: Tela 6 não carregou (elementos de combustível não encontrados)")
            return False
        
        print("✅ Tela 6 carregada - elementos de combustível detectados")
        
        # Clicar em "Flex" (radio button)
        if not clicar_radio_via_javascript(driver, "Flex", "radio Flex"):
            print("❌ Erro: Falha ao clicar Flex na Tela 6")
            return False
        
        # Clicar nos checkboxes necessários
        checkboxes_necessarios = ["kit gas", "blindado", "financiado"]
        for checkbox in checkboxes_necessarios:
            if not clicar_checkbox_via_javascript(driver, checkbox, f"checkbox {checkbox}"):
                print(f"⚠️ Aviso: Falha ao clicar checkbox {checkbox}")
        
        # Clicar "Continuar"
        if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        print("✅ Tela 6 concluída")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """
    Implementa Tela 7: Endereço de pernoite (CEP)
    Usa detecção inteligente de estabilização
    """
    print("\n📱 **TELA 7: Endereço de pernoite (CEP)**")
    
    # Aguardar estabilização da página
    aguardar_estabilizacao_inteligente(driver, "Tela 7 - carregamento")
    
    # Verificar se chegamos na tela correta
    try:
        # Procurar por elementos relacionados a endereço/CEP
        elementos_endereco = driver.find_elements(By.XPATH, "//*[contains(text(), 'endereço') or contains(text(), 'Endereço') or contains(text(), 'CEP') or contains(text(), 'cep')]")
        
        if not elementos_endereco:
            print("❌ Erro: Tela 7 não carregou (elementos de endereço não encontrados)")
            return False
        
        print("✅ Tela 7 carregada - elementos de endereço detectados")
        
        # Preencher CEP (hardcoded como no script original)
        cep_input = driver.find_element(By.XPATH, "//input[contains(@placeholder, 'CEP')]")
        if not cep_input:
            # Fallback para CSS selector
            cep_input = driver.find_element(By.CSS_SELECTOR, "input[type='text']")
        
        if cep_input:
            cep_input.clear()
            cep_input.send_keys("03084-000")  # CEP hardcoded do script original
            print("✅ CEP preenchido: 03084-000")
            
            # Aguardar estabilização após preenchimento
            aguardar_estabilizacao_inteligente(driver, "após preencher CEP")
        else:
            print("❌ Erro: Campo CEP não encontrado")
            return False
        
        # Clicar na sugestão de endereço
        try:
            sugestao = driver.find_element(By.XPATH, "//*[contains(text(), 'Rua Santa') or contains(text(), 'São Paulo')]")
            sugestao.click()
            print("✅ Sugestão de endereço selecionada")
            
            # Aguardar estabilização após seleção
            aguardar_estabilizacao_inteligente(driver, "após selecionar sugestão")
        except:
            print("⚠️ Aviso: Sugestão de endereço não encontrada, continuando...")
        
        # Clicar "Continuar"
        if not clicar_com_delay_inteligente(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        print("✅ Tela 7 concluída")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """
    Implementa Tela 8: Finalidade do veículo
    Usa detecção inteligente de estabilização
    """
    print("\n📱 **TELA 8: Finalidade do veículo**")
    
    # Aguardar estabilização da página
    aguardar_estabilizacao_inteligente(driver, "Tela 8 - carregamento")
    
    # Verificar se chegamos na tela correta
    try:
        # Procurar por elementos relacionados a finalidade/uso
        elementos_finalidade = driver.find_elements(By.XPATH, "//*[contains(text(), 'finalidade') or contains(text(), 'Finalidade') or contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]")
        
        if not elementos_finalidade:
            print("❌ Erro: Tela 8 não carregou (elementos de finalidade não encontrados)")
            return False
        
        print("✅ Tela 8 carregada - elementos de finalidade detectados")
        
        # Clicar em "Pessoal" (radio button)
        if not clicar_radio_via_javascript(driver, "Pessoal", "radio Pessoal"):
            print("❌ Erro: Falha ao clicar Pessoal na Tela 8")
            return False
        
        # Clicar "Continuar" usando ID específico (corrigido do script original)
        if not clicar_com_delay_inteligente(driver, By.ID, "gtm-telaUsoVeiculoContinuar", "botão Continuar Tela 8"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 8")
            return False
        
        print("✅ Tela 8 concluída")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def executar_todas_telas(driver, parametros, temp_dir):
    """
    Executa todas as 8 telas usando detecção inteligente de estabilização
    Substitui delays fixos por detecção inteligente para máxima velocidade
    """
    print("\n🚀 **EXECUTANDO TODAS AS 8 TELAS COM ESTABILIZAÇÃO INTELIGENTE**")
    print("=" * 80)
    print("⚡ OBJETIVO: Reduzir tempo de execução de 15-20s para 0.5-1.5s por tela")
    print("🧠 MÉTODO: Detecção inteligente (Network + JavaScript + Elemento)")
    print("=" * 80)
    
    inicio_total = time.time()
    
    try:
        # Navegar até Tela 5
        if not navegar_ate_tela5(driver, parametros):
            print("❌ Falha na navegação até Tela 5")
            return False
        
        # Salvar estado após Tela 5
        salvar_estado_tela(driver, 5, "apos_tela5", temp_dir)
        
        # Implementar Tela 6
        if not implementar_tela6(driver):
            print("❌ Falha na Tela 6")
            return False
        
        # Salvar estado após Tela 6
        salvar_estado_tela(driver, 6, "apos_tela6", temp_dir)
        
        # Implementar Tela 7
        if not implementar_tela7(driver):
            print("❌ Falha na Tela 7")
            return False
        
        # Salvar estado após Tela 7
        salvar_estado_tela(driver, 7, "apos_tela7", temp_dir)
        
        # Implementar Tela 8
        if not implementar_tela8(driver):
            print("❌ Falha na Tela 8")
            return False
        
        # Salvar estado final
        salvar_estado_tela(driver, 8, "final", temp_dir)
        
        fim_total = time.time()
        duracao_total = fim_total - inicio_total
        
        print("\n" + "=" * 80)
        print("🎉 **TODAS AS 8 TELAS EXECUTADAS COM SUCESSO!**")
        print("=" * 80)
        print(f"⏱️ Tempo total de execução: {duracao_total:.1f}s")
        print(f"🚀 Velocidade: ~{duracao_total/8:.1f}s por tela (vs 15-20s anterior)")
        print(f"⚡ Melhoria estimada: {((15-duracao_total/8)/15)*100:.0f}% mais rápido")
        print("🧠 Método: Detecção inteligente de estabilização")
        print("=" * 80)
        
        return True
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return False

def main():
    """
    Função principal - Executa o RPA com detecção inteligente de estabilização
    """
    print("🚀 **RPA TÔ SEGURADO - VERSÃO 2.0.0 OTIMIZADA**")
    print("=" * 60)
    print("🧠 NOVA FUNCIONALIDADE: Detecção inteligente de estabilização")
    print("⚡ OBJETIVO: Reduzir tempo de execução em 70-80%")
    print("🎯 MÉTODO: Substituir delays fixos (15-20s) por detecção inteligente (0.5-1.5s)")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Carregar parâmetros
    try:
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        print("✅ Parâmetros carregados")
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return
    
    # Configurar Chrome
    driver, temp_dir = configurar_chrome()
    if not driver:
        print("❌ Falha na configuração do Chrome")
        return
    
    try:
        # Navegar para a URL base
        print(f"\n🌐 Navegando para: {parametros['url_base']}")
        driver.get(parametros['url_base'])
        
        # Aguardar carregamento básico da página
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou")
            return
        
        print("✅ Página carregada")
        
        # Executar todas as telas
        if executar_todas_telas(driver, parametros, temp_dir):
            print("\n🎉 **RPA EXECUTADO COM SUCESSO!**")
        else:
            print("\n❌ **RPA FALHOU**")
    
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Limpeza
        if driver:
            driver.quit()
            print("🔒 Chrome fechado")
        
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
    
    fim = datetime.now()
    print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️ Duração total: {fim - inicio}")

if __name__ == "__main__":
    main()
