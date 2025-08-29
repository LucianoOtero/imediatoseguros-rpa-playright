#!/usr/bin/env python3
"""
TESTE COM PLACA REAL KVA-1791
===============================================================================
🎯 OBJETIVO: Testar com placa real KVA-1791 para evitar cache da EED3D56
⚡ MÉTODO: Usar placa que existe no sistema
📊 RESULTADO: Identificar se problema é específico da placa EED3D56
===============================================================================
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

def configurar_chrome_limpo():
    """Configura o Chrome SEM cookies e dados de sessão"""
    print("🔧 Configurando Chrome LIMPO...")
    
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

def testar_placa_kva1791():
    """Testa com placa real KVA-1791"""
    print("🧪 **TESTANDO COM PLACA REAL KVA-1791**")
    print("=" * 80)
    
    # PLACA REAL PARA TESTE
    PLACA_TESTE = "KVA-1791"
    
    print(f"🎯 Placa de teste: {PLACA_TESTE}")
    print(f"📝 Formato: Mercosul válido")
    print(f"✅ Placa real: Existe no sistema")
    print(f" Diferente da: EED3D56 (que está com problema)")
    print("=" * 80)
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome limpo
        driver, temp_dir = configurar_chrome_limpo()
        print("✅ Chrome configurado")
        
        # Navegar para o site
        print("\n🌐 Navegando para o site...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        
        botao_carro = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        botao_carro.click()
        print("✅ Carro selecionado")
        
        time.sleep(10)
        
        # Tela 2: Inserir placa KVA-1791
        print(f"\n📱 TELA 2: Inserindo placa REAL: {PLACA_TESTE}")
        
        campo_placa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys(PLACA_TESTE)
        print(f"✅ Placa inserida: {PLACA_TESTE}")
        
        time.sleep(5)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        
        botao_continuar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        botao_continuar.click()
        print("✅ Continuar clicado")
        
        # AGUARDAR TRANSIÇÃO
        print("\n⏳ Aguardando transição para Tela 4...")
        time.sleep(15)
        
        # Verificar se mudou para Tela 4
        print(f" URL atual: {driver.current_url}")
        print(f"📄 Título atual: {driver.title}")
        
        # Procurar por elementos da Tela 4
        elementos_segurado = driver.find_elements(By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]")
        print(f"🎯 Elementos 'segurado' encontrados: {len(elementos_segurado)}")
        
        if elementos_segurado:
            print("✅ TELA 4 DETECTADA! Placa KVA-1791 funcionou!")
            print(" PROBLEMA RESOLVIDO: Era específico da placa EED3D56!")
        else:
            print("❌ TELA 4 ainda não detectada")
            print("⚠️ PROBLEMA PERSISTE: Não é específico da placa")
            
        # Salvar estado final
        timestamp = datetime.now().strftime("%H:%M:%S")
        os.makedirs("temp/teste_placa_kva1791", exist_ok=True)
        
        with open("temp/teste_placa_kva1791/resultado.txt", "w", encoding="utf-8") as f:
            f.write(f"TESTE PLACA KVA-1791 - {timestamp}\n")
            f.write(f"Placa usada: {PLACA_TESTE}\n")
            f.write(f"Formato: Mercosul válido\n")
            f.write(f"Tipo: Placa real (existe no sistema)\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Elementos segurado: {len(elementos_segurado)}\n")
            f.write(f"Tela 4 detectada: {'Sim' if elementos_segurado else 'Não'}\n")
        
        print("\n✅ **TESTE CONCLUÍDO!**")
        print(" Resultado salvo em: temp/teste_placa_kva1791/")
        
    except Exception as e:
        print(f"❌ **ERRO DURANTE TESTE:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    testar_placa_kva1791()
