#!/usr/bin/env python3
"""
RPA Tô Segurado - COMPLETO FINAL
Implementa todas as telas restantes (5-12) usando delays extremos
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
    print(f"️  **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def navegar_ate_tela3(driver):
    """Navega o RPA até a Tela 3 com delays extremos"""
    print("🚀 **NAVEGANDO ATÉ TELA 3 COM DELAYS EXTREMOS**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    # Clicar no botão Carro com delay extremo
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

def implementar_tela5(driver):
    """Implementa a Tela 5 (Confirmação do veículo)"""
    print("\n **INICIANDO TELA 5: Confirmação do veículo**")
    
    # Aguardar Tela 5 carregar
    print("⏳ Aguardando Tela 5 carregar...")
    
    try:
        # Aguardar elementos da confirmação
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        print("✅ Tela 5 carregada - confirmação do veículo detectada!")
        
        salvar_estado_tela(driver, 5, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 5, "confirmacao_carregada", None)
        
        # Selecionar "Sim" para confirmação do veículo
        print("⏳ Selecionando 'Sim' para confirmação do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
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
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False

def implementar_tela6(driver):
    """Implementa a Tela 6 (Veículo já está segurado)"""
    print("\n **INICIANDO TELA 6: Veículo já está segurado**")
    
    # Aguardar Tela 6 carregar
    print("⏳ Aguardando Tela 6 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 6 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "pergunta_carregada", None)
        
        # Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
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
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """Implementa a Tela 7 (Confirmação que veículo não está segurado)"""
    print("\n **INICIANDO TELA 7: Confirmação que veículo não está segurado**")
    
    # Aguardar Tela 7 carregar
    print("⏳ Aguardando Tela 7 carregar...")
    
    try:
        # Aguardar elementos da confirmação
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        print("✅ Tela 7 carregada - confirmação detectada!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "confirmacao_carregada", None)
        
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
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """Implementa a Tela 8 (Estimativa inicial)"""
    print("\n **INICIANDO TELA 8: Estimativa inicial**")
    
    # Aguardar Tela 8 carregar
    print("⏳ Aguardando Tela 8 carregar...")
    
    try:
        # Aguardar elementos da estimativa
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel')]"))
        )
        print("✅ Tela 8 carregada - estimativa inicial detectada!")
        
        salvar_estado_tela(driver, 8, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 8, "estimativa_carregada", None)
        
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
        print("✅ **TELA 8 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def implementar_tela9(driver):
    """Implementa a Tela 9 (Tipo de combustível)"""
    print("\n **INICIANDO TELA 9: Tipo de combustível**")
    
    # Aguardar Tela 9 carregar
    print("⏳ Aguardando Tela 9 carregar...")
    
    try:
        # Aguardar elementos do tipo de combustível
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível') or contains(text(), 'Flex')]"))
        )
        print("✅ Tela 9 carregada - tipo de combustível detectado!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 9, "combustivel_carregado", None)
        
        # Selecionar "Flex" como tipo de combustível
        print("⏳ Selecionando 'Flex' como tipo de combustível...")
        
        if not clicar_radio_via_javascript(driver, "Flex", "Flex como combustível"):
            print("⚠️ Radio 'Flex' não encontrado - tentando prosseguir...")
        
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
        print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False

def implementar_tela10(driver):
    """Implementa a Tela 10 (Endereço de pernoite)"""
    print("\n **INICIANDO TELA 10: Endereço de pernoite**")
    
    # Aguardar Tela 10 carregar
    print("⏳ Aguardando Tela 10 carregar...")
    
    try:
        # Aguardar elementos do endereço
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'endereço') or contains(text(), 'Endereço') or contains(text(), 'CEP')]"))
        )
        print("✅ Tela 10 carregada - endereço de pernoite detectado!")
        
        salvar_estado_tela(driver, 10, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 10, "endereco_carregado", None)
        
        # Inserir CEP
        print("⏳ Inserindo CEP...")
        
        if not preencher_com_delay_extremo(driver, By.ID, "enderecoTelaEndereco", "03084-000", "CEP"):
            print("❌ Erro: Falha ao preencher CEP")
            return False
        
        # Aguardar sugestão e selecionar
        print("⏳ Aguardando sugestão de endereço...")
        time.sleep(5)
        
        # Selecionar sugestão
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Rua Santa')]", "sugestão de endereço"):
            print("⚠️ Sugestão não encontrada - tentando prosseguir...")
        
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
        print("✅ **TELA 10 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False

def implementar_tela11(driver):
    """Implementa a Tela 11 (Uso do veículo)"""
    print("\n **INICIANDO TELA 11: Uso do veículo**")
    
    # Aguardar Tela 11 carregar
    print("⏳ Aguardando Tela 11 carregar...")
    
    try:
        # Aguardar elementos do uso do veículo
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]"))
        )
        print("✅ Tela 11 carregada - uso do veículo detectado!")
        
        salvar_estado_tela(driver, 11, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 11, "uso_veiculo_carregado", None)
        
        # Selecionar "Pessoal" como uso do veículo
        print("⏳ Selecionando 'Pessoal' como uso do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Pessoal", "Pessoal como uso"):
            print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 11"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 11")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 11, "apos_continuar", None)
        print("✅ **TELA 11 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 11: {e}")
        return False

def implementar_tela12(driver):
    """Implementa a Tela 12 (Dados Pessoais)"""
    print("\n **INICIANDO TELA 12: Dados pessoais**")
    
    # Aguardar Tela 12 carregar
    print("⏳ Aguardando Tela 12 carregar...")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Nome') or contains(text(), 'CPF') or contains(text(), 'nascimento')]"))
        )
        print("✅ Tela 12 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 12, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 12, "dados_pessoais_carregados", None)
        
        # Preencher Nome Completo
        print("⏳ Preenchendo Nome Completo...")
        try:
            nome_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Nome') or contains(@placeholder, 'nome')]"))
            )
            nome_input.clear()
            nome_input.send_keys("LUCIANO OTERO")
            print("✅ Nome Completo preenchido")
        except:
            print("⚠️ Campo Nome não encontrado - tentando prosseguir...")
        
        # Preencher CPF
        print("⏳ Preenchendo CPF...")
        try:
            cpf_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CPF') or contains(@placeholder, 'cpf')]"))
            )
            cpf_input.clear()
            cpf_input.send_keys("085.546.078-48")
            print("✅ CPF preenchido")
        except:
            print("⚠️ Campo CPF não encontrado - tentando prosseguir...")
        
        # Preencher Data de Nascimento
        print("⏳ Preenchendo Data de Nascimento...")
        try:
            data_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Data') or contains(@placeholder, 'nascimento') or contains(@placeholder, 'Nascimento')]"))
            )
            data_input.clear()
            data_input.send_keys("09/02/1965")
            print("✅ Data de Nascimento preenchida")
        except:
            print("⚠️ Campo Data não encontrado - tentando prosseguir...")
        
        # Selecionar Sexo
        print("⏳ Selecionando Sexo...")
        if not clicar_radio_via_javascript(driver, "masculino", "masculino"):
            print("⚠️ Radio masculino não encontrado - tentando prosseguir...")
        
        # Selecionar Estado Civil
        print("⏳ Selecionando Estado Civil...")
        if not clicar_radio_via_javascript(driver, "casado", "casado"):
            print("⚠️ Radio casado não encontrado - tentando prosseguir...")
        
        # Preencher E-mail
        print("⏳ Preenchendo E-mail...")
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'E-mail') or contains(@placeholder, 'email') or contains(@type, 'email')]"))
            )
            email_input.clear()
            email_input.send_keys("lrotero@gmail.com")
            print("✅ E-mail preenchido")
        except:
            print("⚠️ Campo E-mail não encontrado - tentando prosseguir...")
        
        # Preencher Celular
        print("⏳ Preenchendo Celular...")
        try:
            celular_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Celular') or contains(@placeholder, 'celular') or contains(@placeholder, 'Telefone')]"))
            )
            celular_input.clear()
            celular_input.send_keys("(11) 97668-7668")
            print("✅ Celular preenchido")
        except:
            print("⚠️ Campo Celular não encontrado - tentando prosseguir...")
        
        salvar_estado_tela(driver, 12, "configuracao_completa", None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 12"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 12")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 12, "apos_continuar", None)
        print("✅ **TELA 12 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 12: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - COMPLETO FINAL**")
    print("=" * 80)
    print("🎯 OBJETIVO: Implementar TODAS as telas restantes (5-12)")
    print("🔧 MÉTODO: Delays extremos para evitar stale element reference")
    print("📝 NOTA: Navegação completa do fluxo de cotação")
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
        
        # Implementar Tela 5
        if not implementar_tela5(driver):
            print("❌ Erro: Falha ao implementar Tela 5")
            return
        
        # Implementar Tela 6
        if not implementar_tela6(driver):
            print("❌ Erro: Falha ao implementar Tela 6")
            return
        
        # Implementar Tela 7
        if not implementar_tela7(driver):
            print("❌ Erro: Falha ao implementar Tela 7")
            return
        
        # Implementar Tela 8
        if not implementar_tela8(driver):
            print("❌ Erro: Falha ao implementar Tela 8")
            return
        
        # Implementar Tela 9
        if not implementar_tela9(driver):
            print("❌ Erro: Falha ao implementar Tela 9")
            return
        
        # Implementar Tela 10
        if not implementar_tela10(driver):
            print("❌ Erro: Falha ao implementar Tela 10")
            return
        
        # Implementar Tela 11
        if not implementar_tela11(driver):
            print("❌ Erro: Falha ao implementar Tela 11")
            return
        
        # Implementar Tela 12
        if not implementar_tela12(driver):
            print("❌ Erro: Falha ao implementar Tela 12")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO TOTAL! TODAS AS TELAS IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 12")
        print(f"✅ Tela 5: Confirmação do veículo")
        print(f"✅ Tela 6: Veículo já segurado")
        print(f"✅ Tela 7: Confirmação não segurado")
        print(f"✅ Tela 8: Estimativa inicial")
        print(f"✅ Tela 9: Tipo de combustível")
        print(f"✅ Tela 10: Endereço de pernoite")
        print(f"✅ Tela 11: Uso do veículo")
        print(f"✅ Tela 12: Dados pessoais")
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
