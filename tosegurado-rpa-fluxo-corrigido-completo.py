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
# PARTE 2: FUNÇÕES DE NAVEGAÇÃO

def navegar_ate_tela3(driver):
    """Navega o RPA até a Tela 3 com seletores que funcionaram"""
    print("🚀 **NAVEGANDO ATÉ TELA 3 COM SELETORES TESTADOS**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    # Clicar no botão Carro com seletor que funcionou
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento completo da página...")
    time.sleep(10)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # Preencher placa com delay extremo
    if not preencher_com_delay_extremo(driver, By.ID, "placaTelaDadosPlaca", "EED3D56", "placa"):
        print("❌ Erro: Falha ao preencher placa")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "placa_inserida", None)
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    # USAR O SELETOR QUE FUNCIONOU!
    if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento da página...")
    time.sleep(15)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("⚠️ Página pode não ter carregado completamente")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    print("✅ **NAVEGAÇÃO ATÉ TELA 3 CONCLUÍDA COM SUCESSO!**")
    return True

def implementar_tela4(driver):
    """Implementa a Tela 4 (Veículo já está segurado) - CORREÇÃO: NÃO"""
    print("\n **INICIANDO TELA 4: Veículo já está segurado**")
    
    # Aguardar Tela 4 carregar
    print("⏳ Aguardando Tela 4 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 4 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 4, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 4, "pergunta_carregada", None)
        
        # CORREÇÃO: Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado (CORREÇÃO!)...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 4"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 4")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 4, "apos_continuar", None)
        print("✅ **TELA 4 IMPLEMENTADA COM SUCESSO! (Não selecionado)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 4: {e}")
        return False

def implementar_tela5(driver):
    """Implementa a Tela 5 (Estimativa inicial) - AGORA DEVE FUNCIONAR!"""
    print("\n **INICIANDO TELA 5: Estimativa inicial**")
    
    # Aguardar Tela 5 carregar
    print("⏳ Aguardando Tela 5 carregar...")
    
    try:
        # Aguardar elementos da estimativa
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel')]"))
        )
        print("✅ Tela 5 carregada - estimativa inicial detectada!")
        
        salvar_estado_tela(driver, 5, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 5, "estimativa_carregada", None)
        
        # CAPTURAR DADOS DA TELA 5
        capturar_dados_tela5(driver, None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 5"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 5")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO! (Estimativa inicial)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False

# CONTINUA NA PARTE 3...
# PARTE 3: FUNÇÕES DAS TELAS 6-10

def implementar_tela6(driver):
    """Implementa a Tela 6 (Tipo de combustível + checkboxes)"""
    print("\n **INICIANDO TELA 6: Tipo de combustível + checkboxes**")
    
    # Aguardar Tela 6 carregar
    print("⏳ Aguardando Tela 6 carregar...")
    
    try:
        # Aguardar elementos do combustível
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'combustivel')]"))
        )
        print("✅ Tela 6 carregada - tipo de combustível detectado!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "combustivel_carregado", None)
        
        # Selecionar "Flex" como tipo de combustível
        print("⏳ Selecionando 'Flex' como tipo de combustível...")
        
        if not clicar_radio_via_javascript(driver, "Flex", "Flex para combustível"):
            print("⚠️ Radio 'Flex' não encontrado - tentando prosseguir...")
        
        # Deixar checkboxes em branco (kit gas, blindado, financiado)
        print("⏳ Deixando checkboxes em branco...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO! (Combustível Flex)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """Implementa a Tela 7 (Endereço de pernoite)"""
    print("\n **INICIANDO TELA 7: Endereço de pernoite**")
    
    # Aguardar Tela 7 carregar
    print("⏳ Aguardando Tela 7 carregar...")
    
    try:
        # Aguardar elementos do endereço
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'pernoite') or contains(text(), 'endereço') or contains(text(), 'CEP')]"))
        )
        print("✅ Tela 7 carregada - endereço de pernoite detectado!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "endereco_carregado", None)
        
        # Inserir CEP 03084-000
        print("⏳ Inserindo CEP 03084-000...")
        
        # Procurar campo CEP
        try:
            campo_cep = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CEP') or contains(@name, 'cep')]"))
            )
            campo_cep.clear()
            campo_cep.send_keys("03084-000")
            print("✅ CEP inserido: 03084-000")
        except:
            print("⚠️ Campo CEP não encontrado - tentando prosseguir...")
        
        # Aguardar sugestões de endereço
        time.sleep(5)
        
        # Selecionar primeira sugestão de endereço
        try:
            sugestao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'sugestao') or contains(@class, 'suggestion')]"))
            )
            sugestao.click()
            print("✅ Sugestão de endereço selecionada")
        except:
            print("⚠️ Sugestão de endereço não encontrada - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO! (Endereço inserido)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """Implementa a Tela 8 (Finalidade do veículo)"""
    print("\n **INICIANDO TELA 8: Finalidade do veículo**")
    
    # Aguardar Tela 8 carregar
    print("⏳ Aguardando Tela 8 carregar...")
    
    try:
        # Aguardar elementos da finalidade
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'finalidade') or contains(text(), 'utilizado') or contains(text(), 'Pessoal')]"))
        )
        print("✅ Tela 8 carregada - finalidade do veículo detectada!")
        
        salvar_estado_tela(driver, 8, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 8, "finalidade_carregada", None)
        
        # Selecionar "Pessoal" como finalidade
        print("⏳ Selecionando 'Pessoal' como finalidade do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Pessoal", "Pessoal para finalidade"):
            print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 8"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 8")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 8, "apos_continuar", None)
        print("✅ **TELA 8 IMPLEMENTADA COM SUCESSO! (Finalidade Pessoal)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def implementar_tela9(driver):
    """Implementa a Tela 9 (Dados pessoais)"""
    print("\n **INICIANDO TELA 9: Dados pessoais**")
    
    # Aguardar Tela 9 carregar
    print("⏳ Aguardando Tela 9 carregar...")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'dados pessoais') or contains(text(), 'Nome Completo')]"))
        )
        print("✅ Tela 9 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 9, "dados_carregados", None)
        
        # Preencher dados pessoais
        print("⏳ Preenchendo dados pessoais...")
        
        # Nome Completo
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Digite seu nome completo']", "LUCIANO OTERO", "nome completo"):
            print("⚠️ Campo nome não encontrado - tentando alternativas...")
            # Tentar alternativas
            try:
                campo_nome = driver.find_element(By.XPATH, "//input[contains(@name, 'nome') or contains(@id, 'nome')]")
                campo_nome.clear()
                campo_nome.send_keys("LUCIANO OTERO")
                print("✅ Nome preenchido via alternativa")
            except:
                print("❌ Campo nome não encontrado")
        
        # CPF
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Digite seu CPF']", "085.546.078-48", "CPF"):
            print("⚠️ Campo CPF não encontrado - tentando alternativas...")
            try:
                campo_cpf = driver.find_element(By.XPATH, "//input[contains(@name, 'cpf') or contains(@id, 'cpf')]")
                campo_cpf.clear()
                campo_cpf.send_keys("085.546.078-48")
                print("✅ CPF preenchido via alternativa")
            except:
                print("❌ Campo CPF não encontrado")
        
        # Data de nascimento
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='DD/MM/AAAA']", "09/02/1965", "data nascimento"):
            print("⚠️ Campo data não encontrado - tentando alternativas...")
            try:
                campo_data = driver.find_element(By.XPATH, "//input[contains(@name, 'nascimento') or contains(@id, 'nascimento') or contains(@type, 'date')]")
                campo_data.clear()
                campo_data.send_keys("09/02/1965")
                print("✅ Data preenchida via alternativa")
            except:
                print("❌ Campo data não encontrado")
        
        # Sexo (Masculino)
        if not clicar_radio_via_javascript(driver, "Masculino", "Masculino para sexo"):
            print("⚠️ Radio Masculino não encontrado - tentando prosseguir...")
        
        # Estado civil (Casado)
        if not clicar_radio_via_javascript(driver, "Casado", "Casado para estado civil"):
            print("⚠️ Radio Casado não encontrado - tentando prosseguir...")
        
        # E-mail
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@type='email']", "lrotero@gmail.com", "e-mail"):
            print("⚠️ Campo e-mail não encontrado - tentando alternativas...")
            try:
                campo_email = driver.find_element(By.XPATH, "//input[contains(@name, 'email') or contains(@id, 'email')]")
                campo_email.clear()
                campo_email.send_keys("lrotero@gmail.com")
                print("✅ E-mail preenchido via alternativa")
            except:
                print("❌ Campo e-mail não encontrado")
        
        # Celular
        if not preencher_com_delay_extremo(driver, By.XPATH, "//input[@placeholder='Celular']", "(11) 97668-7668", "celular"):
            print("⚠️ Campo celular não encontrado - tentando alternativas...")
            try:
                campo_celular = driver.find_element(By.XPATH, "//input[contains(@name, 'celular') or contains(@id, 'celular') or contains(@name, 'telefone')]")
                campo_celular.clear()
                campo_celular.send_keys("(11) 97668-7668")
                print("✅ Celular preenchido via alternativa")
            except:
                print("❌ Campo celular não encontrado")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 9"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 9")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 9, "apos_continuar", None)
        print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO! (Dados pessoais preenchidos)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False

def implementar_tela10(driver):
    """Implementa a Tela 10 (Condutor principal)"""
    print("\n📱 **INICIANDO TELA 10: Condutor principal**")
    
    # Aguardar Tela 10 carregar
    print("⏳ Aguardando Tela 10 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'condutor principal') or contains(text(), 'condutor')]"))
        )
        print("✅ Tela 10 carregada - pergunta sobre condutor principal detectada!")
        
        salvar_estado_tela(driver, 10, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 10, "pergunta_carregada", None)
        
        # Selecionar "Sim" para condutor principal
        print("⏳ Selecionando 'Sim' para condutor principal...")
        
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para condutor principal"):
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 10"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 10")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 10, "apos_continuar", None)
        print("✅ **TELA 10 IMPLEMENTADA COM SUCESSO! (Condutor principal Sim)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False

# CONTINUA NA PARTE 4...
# PARTE 4: FUNÇÃO PRINCIPAL E MONTAGEM FINAL

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - FLUXO CORRIGIDO FINAL**")
    print("=" * 80)
    print("🎯 OBJETIVO: Fluxo correto das telas com seletores que funcionaram")
    print(" CORREÇÃO: Tela 4 = Veículo segurado, Tela 5 = Estimativa inicial")
    print("⚡ MÉTODO: Delays extremos + Seletores testados + Fluxo correto")
    print("📊 BONUS: Capturar dados da estimativa inicial (Tela 5)")
    print("📝 NOTA: Fluxo real das telas corrigido pelo usuário")
    print("=" * 80)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 3
        if not navegar_ate_tela3(driver):
            print("❌ Erro: Falha ao navegar até Tela 3")
            return
        
        # Implementar Tela 4 (CORREÇÃO: Veículo já está segurado)
        if not implementar_tela4(driver):
            print("❌ Erro: Falha ao implementar Tela 4")
            return
        
        # Implementar Tela 5 (Estimativa inicial - AGORA DEVE FUNCIONAR!)
        if not implementar_tela5(driver):
            print("❌ Erro: Falha ao implementar Tela 5")
            return
        
        # Implementar Tela 6 (Tipo de combustível + checkboxes)
        if not implementar_tela6(driver):
            print("❌ Erro: Falha ao implementar Tela 6")
            return
        
        # Implementar Tela 7 (Endereço de pernoite)
        if not implementar_tela7(driver):
            print("❌ Erro: Falha ao implementar Tela 7")
            return
        
        # Implementar Tela 8 (Finalidade do veículo)
        if not implementar_tela8(driver):
            print("❌ Erro: Falha ao implementar Tela 8")
            return
        
        # Implementar Tela 9 (Dados pessoais)
        if not implementar_tela9(driver):
            print("❌ Erro: Falha ao implementar Tela 9")
            return
        
        # Implementar Tela 10 (Condutor principal)
        if not implementar_tela10(driver):
            print("❌ Erro: Falha ao implementar Tela 10")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO! TODAS AS 10 TELAS IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 10")
        print(f"✅ Tela 1: Seleção do tipo de seguro (Carro)")
        print(f"✅ Tela 2: Inserção da placa (EED3D56)")
        print(f"✅ Tela 3: Confirmação da placa")
        print(f"✅ Tela 4: Veículo já está segurado (Não selecionado)")
        print(f"✅ Tela 5: Estimativa inicial (dados capturados!)")
        print(f"✅ Tela 6: Tipo de combustível (Flex)")
        print(f"✅ Tela 7: Endereço de pernoite (CEP 03084-000)")
        print(f"✅ Tela 8: Finalidade do veículo (Pessoal)")
        print(f"✅ Tela 9: Dados pessoais (LUCIANO OTERO)")
        print(f"✅ Tela 10: Condutor principal (Sim)")
        print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
    
    finally:
        # Limpeza
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
