#!/usr/bin/env python3
"""
RPA Tô Segurado - FLUXO CORRIGIDO
Implementa o fluxo correto conforme especificação do usuário
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
                driver.execute_script(f"document.querySelector('{by}={value}').value = '{texto}';")
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
    print(f"�� Ação: {acao}")
    print(f"�� Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def navegar_ate_tela3(driver):
    """Navega o RPA até a Tela 3 com fluxo correto"""
    print("🚀 **NAVEGANDO ATÉ TELA 3 COM FLUXO CORRETO**")
    
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
    
    print("✅ **NAVEGAÇÃO ATÉ TELA 3 CONCLUÍDA COM SUCESSO!**")
    return True

def implementar_tela3_corrigida(driver):
    """Implementa a Tela 3 CORRETA: Confirmação do veículo ECOSPORT"""
    print("\n�� **INICIANDO TELA 3 CORRIGIDA: Confirmação do veículo ECOSPORT**")
    
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
        print("✅ **TELA 3 CORRIGIDA IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 3 corrigida: {e}")
        return False

def implementar_tela4_corrigida(driver):
    """Implementa a Tela 4 CORRETA: Veículo já está segurado?"""
    print("\n�� **INICIANDO TELA 4 CORRIGIDA: Veículo já está segurado?""")
    
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
        print("✅ **TELA 4 CORRIGIDA IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 4 corrigida: {e}")
        return False

def implementar_tela5_corrigida(driver):
    """Implementa a Tela 5 CORRETA: Estimativa inicial (carrossel de coberturas)"""
    print("\n�� **INICIANDO TELA 5 CORRIGIDA: Estimativa inicial**")
    
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
        
        # CAPTURAR DADOS DA ESTIMATIVA INICIAL
        print("📊 CAPTURANDO DADOS DA ESTIMATIVA INICIAL...")
        
        # Salvar dados específicos
        try:
            # Procurar por preços ou coberturas
            precos = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$') or contains(text(), 'reais')]")
            if precos:
                print(f"�� Preços encontrados: {len(precos)}")
                for i, preco in enumerate(precos[:5]):  # Primeiros 5
                    print(f"   {i+1}: {preco.text}")
            
            # Procurar por nomes de seguradoras
            seguradoras = driver.find_elements(By.XPATH, "//*[contains(text(), 'Seguradora') or contains(text(), 'seguro')]")
            if seguradoras:
                print(f"�� Seguradoras encontradas: {len(seguradoras)}")
                for i, seguradora in enumerate(seguradoras[:5]):  # Primeiros 5
                    print(f"   {i+1}: {seguradora.text}")
                    
        except Exception as e:
            print(f"⚠️ Erro ao capturar dados: {e}")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 5"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 5")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        print("✅ **TELA 5 CORRIGIDA IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5 corrigida: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - FLUXO CORRIGIDO**")
    print("=" * 80)
    print("🎯 OBJETIVO: Implementar fluxo CORRETO conforme especificação")
    print("🔧 MÉTODO: Delays extremos + fluxo correto de telas")
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
        
        # Navegar até Tela 3
        if not navegar_ate_tela3(driver):
            print("❌ Erro: Falha ao navegar até Tela 3")
            return
        
        # Implementar Tela 3 CORRIGIDA
        if not implementar_tela3_corrigida(driver):
            print("❌ Erro: Falha ao implementar Tela 3 corrigida")
            return
        
        # Implementar Tela 4 CORRIGIDA
        if not implementar_tela4_corrigida(driver):
            print("❌ Erro: Falha ao implementar Tela 4 corrigida")
            return
        
        # Implementar Tela 5 CORRIGIDA (Estimativa inicial)
        if not implementar_tela5_corrigida(driver):
            print("❌ Erro: Falha ao implementar Tela 5 corrigida")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO! FLUXO CORRETO IMPLEMENTADO!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 5")
        print(f"✅ Tela 1: Seleção Carro")
        print(f"✅ Tela 2: Inserção placa KVA-1791")
        print(f"✅ Tela 3: Confirmação ECOSPORT → Sim")
        print(f"✅ Tela 4: Veículo segurado → Não")
        print(f"✅ Tela 5: Estimativa inicial (DADOS CAPTURADOS)")
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
