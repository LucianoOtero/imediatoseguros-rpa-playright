#!/usr/bin/env python3
"""
RPA Tô Segurado - Aguardando Cotação Sem Falso Positivo
Aguarda o carregamento da cotação sem detectar erros incorretamente
"""

import time
import tempfile
import shutil
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções headless"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Criar diretório temporário único
    temp_dir = tempfile.mkdtemp()
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def navegar_ate_tela6(driver):
    """Navega até a Tela 6 (veículo já segurado)"""
    print("🚀 **NAVEGANDO ATÉ TELA 6...**")
    
    # Tela 1: Selecionar Carro
    driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
    time.sleep(3)
    
    carro_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
    )
    carro_btn.click()
    print("✅ Tela 1: Carro selecionado")
    
    # Tela 2: Inserir placa
    placa_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']"))
    )
    placa_input.clear()
    placa_input.send_keys("EED3D56")
    print("✅ Tela 2: Placa EED3D56 inserida")
    
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Tela 3: Continuar clicado")
    
    # Tela 4: Aguardar carregamento
    time.sleep(3)
    
    # Tela 5: Confirmar veículo
    sim_radio = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
    )
    driver.execute_script("arguments[0].click();", sim_radio)
    print("✅ Tela 5: Veículo confirmado")
    
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Tela 6: Continuar clicado")
    
    # Aguardar Tela 6 carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'já está segurado')]"))
    )
    print("✅ Tela 6 carregada - veículo já segurado")
    
    return True

def aguardar_cotacao_sem_erro(driver):
    """Aguarda o carregamento da cotação sem falso positivo"""
    print("\n⏳ **AGUARDANDO CARREGAMENTO DA COTAÇÃO...**")
    
    # Aguardar até que a página de carregamento apareça
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Aguarde! Estamos buscando')]"))
    )
    print("✅ Página de carregamento detectada")
    
    # Aguardar até que os resultados apareçam (máximo 10 minutos)
    max_wait = 600  # 10 minutos
    start_time = time.time()
    
    while time.time() - start_time < max_wait:
        try:
            current_url = driver.current_url
            current_title = driver.title
            page_source = driver.page_source
            
            # Verificar se apareceu texto de resultado (sem falso positivo)
            if "Parabéns, chegamos ao resultado final" in page_source:
                print("🎉 **COTAÇÃO CARREGADA COMPLETAMENTE!**")
                return True
            
            # Verificar se ainda está carregando
            if "Aguarde! Estamos buscando" in page_source:
                elapsed = int(time.time() - start_time)
                print(f"⏳ Aguardando... ({elapsed}s / {max_wait}s)")
                time.sleep(15)  # Verificar a cada 15 segundos
                continue
            
            # Verificar se mudou para outra tela
            if "estimativa" not in page_source.lower() and "buscando" not in page_source.lower():
                print(f"🔄 Mudança detectada na página...")
                time.sleep(5)
                continue
                
        except Exception as e:
            print(f"⚠️ Erro durante verificação: {e}")
            time.sleep(5)
    
    print("⏰ **TIMEOUT - Cotação não carregou em 10 minutos**")
    return False

def extrair_cotacoes(driver):
    """Extrai os dados das cotações"""
    print("\n📊 **EXTRAINDO DADOS DAS COTAÇÕES...**")
    
    try:
        # Salvar HTML para análise
        with open("/opt/imediatoseguros-rpa/temp/cotacao_final.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("📄 HTML salvo: /opt/imediatoseguros-rpa/temp/cotacao_final.html")
        
        # Extrair valores principais
        cotacoes = []
        
        # Buscar por valores de prêmio
        valores = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
        for valor in valores:
            if "anual" in valor.text.lower():
                cotacoes.append(valor.text.strip())
        
        # Buscar por franquias
        franquias = driver.find_elements(By.XPATH, "//*[contains(text(), 'Franquia')]")
        
        # Buscar por coberturas
        coberturas = driver.find_elements(By.XPATH, "//*[contains(text(), 'Danos') or contains(text(), 'Assistência')]")
        
        print(f"💰 Valores encontrados: {len(cotacoes)}")
        print(f"🛡️ Franquias encontradas: {len(franquias)}")
        print(f"🔒 Coberturas encontradas: {len(coberturas)}")
        
        # Salvar dados extraídos
        with open("/opt/imediatoseguros-rpa/temp/dados_cotacao_final.txt", "w", encoding="utf-8") as f:
            f.write("=== COTAÇÕES FINAIS EXTRAÍDAS ===\n\n")
            f.write("VALORES:\n")
            for cotacao in cotacoes:
                f.write(f"- {cotacao}\n")
            f.write("\nFRANQUIAS:\n")
            for franquia in franquias:
                f.write(f"- {franquia.text}\n")
            f.write("\nCOBERTURAS:\n")
            for cobertura in coberturas:
                f.write(f"- {cobertura.text}\n")
        
        print("�� Dados salvos: /opt/imediatoseguros-rpa/temp/dados_cotacao_final.txt")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🚀 **RPA TÔ SEGURADO - AGUARDANDO COTAÇÃO SEM FALSO POSITIVO**")
        print("=" * 70)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        if not navegar_ate_tela6(driver):
            print("❌ Falha ao navegar até Tela 6")
            return
        
        # Clicar em Continuar na Tela 6
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 6")
        
        # Aguardar cotação carregar (sem falso positivo)
        if aguardar_cotacao_sem_erro(driver):
            # Extrair dados
            extrair_cotacoes(driver)
            print("\n🎉 **RPA EXECUTADO COM SUCESSO!**")
        else:
            print("\n❌ **COTAÇÃO NÃO CARREGOU COMPLETAMENTE**")
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE EXECUÇÃO:** {e}")
        
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
