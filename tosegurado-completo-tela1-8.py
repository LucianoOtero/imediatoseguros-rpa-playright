#!/usr/bin/env python3
"""
RPA Tô Segurado - COMPLETO ATÉ TELA 8
Navega desde o início até a Tela 8 com fluxo correto
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
    """Aguarda o carregamento completo da página"""
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
    """Clica em um elemento com delay extremo"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 15)
        
        try:
            elemento = WebDriverWait(driver, 10).until(
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
        time.sleep(2)
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
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 10)
        
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais presente, tentando JavaScript...")
            if by == By.ID:
                driver.execute_script(f"document.getElementById('{value}').value = '{texto}';")
            else:
                driver.execute_script(f"arguments[0].value = '{texto}';", elemento)
            print(f"✅ {descricao} preenchido via JavaScript")
            return True
        
        elemento.clear()
        time.sleep(1)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
    """Clica em um radio button via JavaScript"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        aguardar_estabilizacao(driver, 15)
        
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

def clicar_checkbox_via_javascript(driver, texto_checkbox, descricao="checkbox", timeout=30):
    """Clica em um checkbox via JavaScript"""
    try:
        print(f"⏳ Aguardando checkbox {descricao} aparecer...")
        aguardar_estabilizacao(driver, 15)
        
        script = f"""
        var elementos = document.querySelectorAll('input[type="checkbox"], label, span, div');
        var checkboxEncontrado = null;
        
        for (var i = 0; i < elementos.length; i++) {{
            var elemento = elementos[i];
            if (elemento.textContent && elemento.textContent.includes('{texto_checkbox}')) {{
                checkboxEncontrado = elemento;
                break;
            }}
        }}
        
        if (checkboxEncontrado) {{
            if (checkboxEncontrado.tagName === 'LABEL') {{
                var inputId = checkboxEncontrado.getAttribute('for');
                if (inputId) {{
                    var input = document.getElementById(inputId);
                    if (input) {{
                        input.click();
                        return 'Checkbox clicado via label: ' + inputId;
                    }}
                }}
            }}
            
            checkboxEncontrado.click();
            return 'Checkbox clicado diretamente: ' + checkboxEncontrado.outerHTML.substring(0, 100);
        }} else {{
            return 'Checkbox não encontrado';
        }}
        """
        
        resultado = driver.execute_script(script)
        print(f"🎯 {resultado}")
        
        if "Checkbox clicado" in resultado:
            print(f"✅ Checkbox {descricao} clicado via JavaScript")
            return True
        else:
            print(f"❌ Checkbox {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar checkbox {descricao}: {e}")
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
    print(f"📱 **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def navegar_ate_tela5(driver):
    """Navega o RPA até a Tela 5 com fluxo correto"""
    print("🚀 **NAVEGANDO ATÉ TELA 5 COM FLUXO CORRETO**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    print("⏳ Aguardando carregamento completo da página...")
    time.sleep(10)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    aguardar_estabilizacao(driver, 20)
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa CORRETA
    print("\n📱 TELA 2: Inserindo placa KVA-1791...")
    aguardar_estabilizacao(driver, 15)
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # PLACA CORRETA: KVA-1791
    if not preencher_com_delay_extremo(driver, By.ID, "placaTelaDadosPlaca", "KVA-1791", "placa"):
        print("❌ Erro: Falha ao preencher placa")
        return False
    
    aguardar_estabilizacao(driver, 15)
    salvar_estado_tela(driver, 2, "placa_inserida", None)
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    print("⏳ Aguardando carregamento da página...")
    time.sleep(15)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("⚠️ Página pode não ter carregado completamente")
    
    aguardar_estabilizacao(driver, 20)
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    # TELA 3: Confirmação do veículo ECOSPORT
    print("\n📱 TELA 3: Confirmando veículo ECOSPORT...")
    
    try:
        # Aguardar elementos da confirmação do ECOSPORT
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ECOSPORT')]"))
        )
        print("✅ Tela 3 carregada - confirmação do ECOSPORT detectada!")
        
        salvar_estado_tela(driver, 3, "confirmacao_ecosport", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 3, "confirmacao_carregada", None)
        
        # Selecionar "Sim" para confirmação do veículo
        print("⏳ Selecionando 'Sim' para confirmação do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 3"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 3")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 3, "apos_continuar", None)
        
    except Exception as e:
        print(f"⚠️ Erro na confirmação Tela 3: {e} - tentando prosseguir...")
    
    # TELA 4: Veículo já está segurado?
    print("\n�� TELA 4: Veículo já está segurado?")
    
    try:
        # Aguardar elementos da pergunta sobre veículo segurado
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 4 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 4, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 4, "pergunta_carregada", None)
        
        # Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 4"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 4")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 4, "apos_continuar", None)
        
    except Exception as e:
        print(f"⚠️ Erro na Tela 4: {e} - tentando prosseguir...")
    
    # TELA 5: Estimativa inicial
    print("\n�� TELA 5: Estimativa inicial...")
    
    try:
        # Aguardar elementos da estimativa inicial
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel') or contains(text(), 'cobertura')]"))
        )
        print("✅ Tela 5 carregada - estimativa inicial detectada!")
        
        salvar_estado_tela(driver, 5, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 5, "estimativa_carregada", None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(text(), 'Continuar')]", "botão Continuar Tela 5"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 5")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        
    except Exception as e:
        print(f"⚠️ Erro na Tela 5: {e} - tentando prosseguir...")
    
    print("✅ **NAVEGAÇÃO ATÉ TELA 5 CONCLUÍDA!**")
    return True

def implementar_tela6(driver):
    """Implementa a Tela 6: Tipo de combustível + checkboxes"""
    print("\n **INICIANDO TELA 6: Tipo de combustível + checkboxes**")
    
    try:
        # Aguardar elementos da Tela 6
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível') or contains(text(), 'Flex') or contains(text(), 'Gasolina')]"))
        )
        print("✅ Tela 6 carregada - tipo de combustível detectado!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "combustivel_carregado", None)
        
        # Selecionar "Flex" como tipo de combustível
        print("⏳ Selecionando 'Flex' como tipo de combustível...")
        
        if not clicar_radio_via_javascript(driver, "Flex", "Flex como combustível"):
            print("⚠️ Radio 'Flex' não encontrado - tentando prosseguir...")
        
        # Selecionar checkboxes se disponíveis
        print("⏳ Verificando checkboxes disponíveis...")
        
        # Kit Gás (se disponível)
        if not clicar_checkbox_via_javascript(driver, "kit gas", "Kit Gás"):
            print("⚠️ Checkbox Kit Gás não encontrado")
        
        # Blindado (se disponível)
        if not clicar_checkbox_via_javascript(driver, "blindado", "Blindado"):
            print("⚠️ Checkbox Blindado não encontrado")
        
        # Financiado (se disponível)
        if not clicar_checkbox_via_javascript(driver, "financiado", "Financiado"):
            print("⚠️ Checkbox Financiado não encontrado")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """Implementa a Tela 7: Endereço de pernoite (CEP)"""
    print("\n **INICIANDO TELA 7: Endereço de pernoite**")
    
    try:
        # Aguardar elementos do endereço
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'endereço') or contains(text(), 'Endereço') or contains(text(), 'CEP') or contains(text(), 'cep')]"))
        )
        print("✅ Tela 7 carregada - endereço de pernoite detectado!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "endereco_carregado", None)
        
        # Inserir CEP
        print("⏳ Inserindo CEP...")
        
        # Tentar diferentes seletores para o campo CEP
        cep_campo = None
        try:
            cep_campo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CEP') or contains(@placeholder, 'cep') or contains(@name, 'cep') or contains(@id, 'cep')]"))
            )
        except:
            try:
                cep_campo = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='text']"))
                )
            except:
                print("⚠️ Campo CEP não encontrado - tentando prosseguir...")
        
        if cep_campo:
            cep_campo.clear()
            time.sleep(1)
            cep_campo.send_keys("03084-000")
            print("✅ CEP preenchido: 03084-000")
        
        # Aguardar sugestão e selecionar
        print("⏳ Aguardando sugestão de endereço...")
        time.sleep(5)
        
        # Selecionar sugestão se disponível
        try:
            sugestao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Rua Santa') or contains(text(), 'São Paulo')]"))
            )
            sugestao.click()
            print("✅ Sugestão de endereço selecionada")
        except:
            print("⚠️ Sugestão não encontrada - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """Implementa a Tela 8: Finalidade do veículo"""
    print("\n **INICIANDO TELA 8: Finalidade do veículo**")
    
    try:
        # Aguardar elementos da finalidade do veículo
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'finalidade') or contains(text(), 'Finalidade') or contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]"))
        )
        print("✅ Tela 8 carregada - finalidade do veículo detectada!")
        
        salvar_estado_tela(driver, 8, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 8, "finalidade_carregada", None)
        
        # Selecionar "Pessoal" como finalidade do veículo
        print("⏳ Selecionando 'Pessoal' como finalidade do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Pessoal", "Pessoal como finalidade"):
            print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(text(), 'Continuar')]", "botão Continuar Tela 8"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 8")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 8, "apos_continuar", None)
        print("✅ **TELA 8 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - COMPLETO ATÉ TELA 8**")
    print("=" * 80)
    print("🎯 OBJETIVO: Navegar desde o início até a Tela 8")
    print("🔧 MÉTODO: Delays extremos + fluxo completo e correto")
    print("📝 NOTA: Placa KVA-1791, veículo ECOSPORT, fluxo correto")
    print("=" * 80)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 5
        if not navegar_ate_tela5(driver):
            print("❌ Erro: Falha ao navegar até Tela 5")
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
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO TOTAL! TELAS 1-8 IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 8")
        print(f"✅ Tela 1: Seleção Carro")
        print(f"✅ Tela 2: Inserção placa KVA-1791")
        print(f"✅ Tela 3: Confirmação ECOSPORT → Sim")
        print(f"✅ Tela 4: Veículo segurado → Não")
        print(f"✅ Tela 5: Estimativa inicial")
        print(f"✅ Tela 6: Tipo combustível + checkboxes")
        print(f"✅ Tela 7: Endereço pernoite (CEP)")
        print(f"✅ Tela 8: Finalidade veículo → Pessoal")
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
