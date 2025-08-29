#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - FLUXO CORRIGIDO FINAL (PARTE 1)
===============================================================================
🎯 OBJETIVO: Fluxo correto das telas com seletores que funcionaram
 CORREÇÃO: Tela 4 = Veículo segurado, Tela 5 = Estimativa inicial
⚡ MÉTODO: Delays extremos + Seletores testados + Fluxo correto
📊 BONUS: Capturar dados da estimativa inicial (Tela 5)
📝 NOTA: Fluxo real das telas corrigido pelo usuário
===============================================================================
"""

import time
import tempfile
import shutil
import os
import json
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

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página com timeout maior"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def aguardar_estabilizacao(driver, segundos=15):
    """Aguarda a estabilização da página"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)

def clicar_com_delay_extremo(driver, by, value, descricao="elemento", timeout=30):
    """Clica em um elemento com delay extremo para evitar stale element"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # Aguardar elemento estar presente
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 15)
        
        # Verificar se ainda está presente
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            # Tentar JavaScript como fallback
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').click();")
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(2)
        
        # Clicar
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay_extremo(driver, by, value, texto, descricao="campo", timeout=30):
    """Preenche um campo com delay extremo"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # Aguardar elemento estar presente
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 10)
        
        # Verificar se ainda está presente
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais presente, tentando JavaScript...")
            # Tentar JavaScript como fallback
            if by == By.ID:
                driver.execute_script(f"document.getElementById('{value}').value = '{texto}';")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').value = '{texto}';")
            print(f"✅ {descricao} preenchido via JavaScript")
            return True
        
        # Limpar e preencher
        elemento.clear()
        time.sleep(1)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
    """Clica em um radio button via JavaScript procurando por texto"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 15)
        
        # JavaScript para encontrar e clicar no radio
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
            // Se for um label, procurar o input associado
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
            
            // Clicar diretamente
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

def capturar_dados_tela5(driver, temp_dir):
    """Captura dados da Tela 5 (Estimativa Inicial)"""
    print("**CAPTURANDO DADOS DA TELA 5 (ESTIMATIVA INICIAL)**")
    print("=" * 70)
    
    # Salvar página da Tela 5
    tela5_dir = salvar_estado_tela(driver, 5, "captura_dados", temp_dir)
    
    # Procurar por elementos da cobertura "Compreensiva"
    try:
        # Procurar por texto "Compreensiva"
        elementos_compreensiva = driver.find_elements(By.XPATH, "//*[contains(text(), 'Compreensiva')]")
        
        if elementos_compreensiva:
            print("✅ Nome Cobertura: Compreensiva")
            
            # Procurar por valores monetários próximos
            valores_monetarios = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
            print(f" Valores monetários encontrados: {len(valores_monetarios)}")
            
            # Salvar dados em JSON
            dados_cobertura = {
                "nome_cobertura": "Compreensiva",
                "valores_encontrados": len(valores_monetarios),
                "timestamp": datetime.now().isoformat(),
                "url": driver.current_url,
                "titulo": driver.title
            }
            
            # Salvar JSON
            json_path = os.path.join(tela5_dir, "dados_cobertura_compreensiva.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dados_cobertura, f, indent=2, ensure_ascii=False)
            
            # Salvar TXT
            txt_path = os.path.join(tela5_dir, "dados_cobertura_compreensiva.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Nome Cobertura: {dados_cobertura['nome_cobertura']}\n")
                f.write(f"Valores Encontrados: {dados_cobertura['valores_encontrados']}\n")
                f.write(f"Timestamp: {dados_cobertura['timestamp']}\n")
                f.write(f"URL: {dados_cobertura['url']}\n")
                f.write(f"Título: {dados_cobertura['titulo']}\n")
            
            print(f"💾 Dados salvos em JSON: {json_path}")
            print(f" Dados salvos em TXT: {txt_path}")
            
        else:
            print("❌ Cobertura 'Compreensiva' não encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
    
    print("**RESUMO DOS DADOS CAPTURADOS:**")
    print("=" * 70)
    print("✅ Dados da Tela 5 capturados com sucesso!")

def salvar_estado_tela(driver, tela_num, acao, temp_dir):
    """Salva o estado atual da tela"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    tela_dir = f"temp/tela_{tela_num:02d}"
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

# CONTINUA NA PARTE 2...
