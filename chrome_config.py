#!/usr/bin/env python3
"""
Configuração do Chrome para RPA Tô Segurado
Módulo separado para evitar erros de 'driver' não definido
"""

import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """
    Configura o Chrome com opções otimizadas
    
    Returns:
        tuple: (driver, temp_dir) - driver configurado e diretório temporário
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Criar diretório temporário único
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    # Configurar o driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def limpar_chrome(driver, temp_dir):
    """
    Limpa recursos do Chrome
    
    Args:
        driver: WebDriver do Chrome
        temp_dir: Diretório temporário criado
    """
    if driver:
        driver.quit()
    if temp_dir:
        shutil.rmtree(temp_dir)
        print(f"🗑️ Diretório temporário removido: {temp_dir}")

# Funções utilitárias adicionais
def aguardar_carregamento_pagina(driver, timeout=30):
    """
    Aguarda a página carregar completamente
    
    Args:
        driver: WebDriver do Chrome
        timeout: Timeout em segundos
    """
    print(f"⏳ Aguardando carregamento da página (timeout: {timeout}s)...")
    
    # Aguardar até que a página esteja pronta
    from selenium.webdriver.support.ui import WebDriverWait
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
    # Aguardar um pouco mais para garantir que tudo carregou
    import time
    time.sleep(3)
    print("✅ Página carregada completamente")

def criar_diretorio_tela(numero_tela):
    """
    Cria diretório para salvar arquivos da tela
    
    Args:
        numero_tela: Número da tela
        
    Returns:
        str: Caminho do diretório criado
    """
    import os
    diretorio = f"/opt/imediatoseguros-rpa/temp/tela_{numero_tela:02d}"
    os.makedirs(diretorio, exist_ok=True)
    return diretorio

def salvar_estado_tela(driver, numero_tela, descricao, sufixo=""):
    """
    Salva o estado completo da tela
    
    Args:
        driver: WebDriver do Chrome
        numero_tela: Número da tela
        descricao: Descrição do estado
        sufixo: Sufixo opcional para o nome do arquivo
        
    Returns:
        str: Caminho do diretório onde os arquivos foram salvos
    """
    import os
    from datetime import datetime
    
    diretorio = criar_diretorio_tela(numero_tela)
    
    # Salvar HTML
    nome_html = f"tela_{numero_tela:02d}_{descricao}{sufixo}.html"
    caminho_html = os.path.join(diretorio, nome_html)
    with open(caminho_html, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # Salvar screenshot
    nome_screenshot = f"tela_{numero_tela:02d}_{descricao}{sufixo}.png"
    caminho_screenshot = os.path.join(diretorio, nome_screenshot)
    driver.save_screenshot(caminho_screenshot)
    
    # Salvar informações da página
    nome_info = f"tela_{numero_tela:02d}_{descricao}{sufixo}.txt"
    caminho_info = os.path.join(diretorio, nome_info)
    with open(caminho_info, "w", encoding="utf-8") as f:
        f.write(f"TELA {numero_tela:02d}: {descricao}\n")
        f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"URL: {driver.current_url}\n")
        f.write(f"Título: {driver.title}\n")
        f.write(f"HTML salvo em: {caminho_html}\n")
        f.write(f"Screenshot salvo em: {caminho_screenshot}\n")
    
    return diretorio

def log_tela(driver, numero_tela, descricao, acao=""):
    """
    Registra log detalhado da tela
    
    Args:
        driver: WebDriver do Chrome
        numero_tela: Número da tela
        descricao: Descrição da tela
        acao: Ação sendo executada (opcional)
        
    Returns:
        str: Caminho do diretório onde os arquivos foram salvos
    """
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    url = driver.current_url
    titulo = driver.title
    
    print(f"\n{'='*80}")
    print(f"️  **TELA {numero_tela:02d}: {descricao}** - {timestamp}")
    print(f"{'='*80}")
    print(f"🌐 URL: {url}")
    print(f"📄 Título: {titulo}")
    
    if acao:
        print(f"🎯 Ação: {acao}")
    
    # Salvar estado da tela
    diretorio = salvar_estado_tela(driver, numero_tela, descricao)
    print(f" Arquivos salvos em: {diretorio}")
    
    return diretorio
