#!/usr/bin/env python3
"""
RPA Tô Segurado - DELAYS EXTREMOS
Solução para o problema de stale element reference
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

def aguardar_estabilizacao(driver, segundos=10):
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
            driver.execute_script(f"document.getElementById('{value}').value = '{texto}';")
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

def navegar_ate_tela5(driver):
    """Navega o RPA até a Tela 5 com delays extremos"""
    print("🚀 **NAVEGANDO ATÉ TELA 5 COM DELAYS EXTREMOS**")
    
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
    
    # INVESTIGAR O QUE CARREGOU
    print("\n🔍 **INVESTIGANDO O QUE CARREGOU APÓS TELA 3:**")
    print("=" * 60)
    
    # Salvar estado atual
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    # Verificar URL e título
    print(f" URL Atual: {driver.current_url}")
    print(f"📄 Título Atual: {driver.title}")
    
    # Procurar por elementos específicos
    print("\n🔍 **PROCURANDO ELEMENTOS ESPECÍFICOS:**")
    
    # Procurar por confirmação de veículo
    try:
        confirmacao_elements = driver.find_elements(By.NAME, "confirmacaoVeiculo")
        print(f"✅ Elementos 'confirmacaoVeiculo' encontrados: {len(confirmacao_elements)}")
        
        for i, elem in enumerate(confirmacao_elements):
            print(f"   Elemento {i+1}: {elem.get_attribute('outerHTML')[:200]}...")
    except:
        print("❌ Erro ao procurar 'confirmacaoVeiculo'")
    
    # Procurar por texto COROLLA
    try:
        corolla_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'COROLLA')]")
        print(f"✅ Elementos 'COROLLA' encontrados: {len(corolla_elements)}")
        
        for i, elem in enumerate(corolla_elements):
            print(f"   Elemento {i+1}: {elem.text[:100]}...")
    except:
        print("❌ Erro ao procurar 'COROLLA'")
    
    # Procurar por botões Continuar
    try:
        continuar_elements = driver.find_elements(By.XPATH, "//button[contains(., 'Continuar')]")
        print(f"✅ Botões 'Continuar' encontrados: {len(continuar_elements)}")
        
        for i, elem in enumerate(continuar_elements):
            print(f"   Botão {i+1}: {elem.get_attribute('outerHTML')[:200]}...")
    except:
        print("❌ Erro ao procurar botões 'Continuar'")
    
    print("\n **INVESTIGAÇÃO CONCLUÍDA!**")
    print("📁 Verifique os arquivos salvos para análise detalhada")
    
    return True

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - DELAYS EXTREMOS**")
    print("=" * 60)
    print(" OBJETIVO: Investigar Tela 5 com delays extremos")
    print("🔧 SOLUÇÃO: Delays muito maiores para evitar stale element")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        if navegar_ate_tela5(driver):
            print("\n **INVESTIGAÇÃO CONCLUÍDA COM SUCESSO!**")
        else:
            print("\n❌ **FALHA NA INVESTIGAÇÃO**")
    
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
