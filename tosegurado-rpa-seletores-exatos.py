#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - SELETORES EXATOS
===============================================================================
🎯 OBJETIVO: Usar seletores exatos dos radio buttons
⚡ MÉTODO: Seletores CSS precisos + JavaScript direto
�� RESULTADO: Navegar corretamente para Tela 4
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

def clicar_radio_sim_exato(driver):
    """Clica no radio 'Sim' usando seletor exato"""
    try:
        print("⏳ Procurando radio 'Sim' com seletor exato...")
        
        # MÉTODO 1: Seletor CSS exato
        try:
            radio_sim = driver.find_element(By.CSS_SELECTOR, 'input[value="Sim"][name="confirmarVeiculoTelaInformacoesVeiculo"]')
            radio_sim.click()
            print("✅ Radio 'Sim' clicado via CSS selector")
            return True
        except:
            print("⚠️ CSS selector falhou, tentando JavaScript...")
        
        # MÉTODO 2: JavaScript direto
        script = """
        var radioSim = document.querySelector('input[value="Sim"][name="confirmarVeiculoTelaInformacoesVeiculo"]');
        if (radioSim) {
            radioSim.click();
            return 'Radio Sim clicado via JavaScript';
        } else {
            return 'Radio Sim não encontrado';
        }
        """
        
        resultado = driver.execute_script(script)
        print(f"🎯 {resultado}")
        
        if "Radio Sim clicado" in resultado:
            print("✅ Radio 'Sim' clicado via JavaScript")
            return True
        else:
            print("❌ Radio 'Sim' não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar radio 'Sim': {e}")
        return False

def testar_seletores_exatos():
    """Testa com seletores exatos"""
    print("�� **TESTANDO COM SELETORES EXATOS**")
    print("=" * 80)
    print("🎯 OBJETIVO: Usar seletores CSS precisos dos radio buttons")
    print("⚡ MÉTODO: CSS selector + JavaScript direto")
    print("=" * 80)
    
    # PLACA REAL PARA TESTE
    PLACA_TESTE = "KVA-1791"
    
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
        print(f"\n📱 TELA 2: Inserindo placa: {PLACA_TESTE}")
        
        campo_placa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys(PLACA_TESTE)
        print(f"✅ Placa inserida: {PLACA_TESTE}")
        
        time.sleep(5)
        
        # TELA 3 CORRIGIDA: Selecionar "Sim" com seletor exato
        print("\n📱 TELA 3: Selecionando 'Sim' com seletor exato...")
        
        # Aguardar pergunta sobre o veículo aparecer
        print("⏳ Aguardando pergunta sobre o veículo...")
        time.sleep(10)
        
        # Selecionar "Sim" no radio button com seletor exato
        if clicar_radio_sim_exato(driver):
            print("✅ Radio 'Sim' selecionado com seletor exato")
        else:
            print("❌ Falha ao selecionar radio 'Sim'")
            return
        
        # Aguardar seleção
        time.sleep(3)
        
        # Agora clicar em "Continuar"
        print("\n⏳ Clicando em Continuar após selecionar 'Sim'...")
        
        botao_continuar = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        botao_continuar.click()
        print("✅ Continuar clicado")
        
        # AGUARDAR TRANSIÇÃO PARA TELA 4
        print("\n⏳ Aguardando transição para Tela 4...")
        time.sleep(15)
        
        # Verificar se mudou para Tela 4
        print(f" URL atual: {driver.current_url}")
        print(f"📄 Título atual: {driver.title}")
        
        # Procurar por elementos da Tela 4
        elementos_segurado = driver.find_elements(By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]")
        print(f"🎯 Elementos 'segurado' encontrados: {len(elementos_segurado)}")
        
        if elementos_segurado:
            print("✅ TELA 4 DETECTADA! Seletores exatos funcionaram!")
            print(" PROBLEMA RESOLVIDO: Tela 3 corrigida com seletores precisos!")
        else:
            print("❌ TELA 4 ainda não detectada")
            print("⚠️ PROBLEMA PERSISTE: Verificar outras causas")
            
        # Salvar estado final
        timestamp = datetime.now().strftime("%H:%M:%S")
        os.makedirs("temp/teste_seletores_exatos", exist_ok=True)
        
        with open("temp/teste_seletores_exatos/resultado.txt", "w", encoding="utf-8") as f:
            f.write(f"TESTE SELETORES EXATOS - {timestamp}\n")
            f.write(f"Placa usada: {PLACA_TESTE}\n")
            f.write(f"Radio 'Sim' selecionado: Sim\n")
            f.write(f"Método: CSS selector + JavaScript\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Elementos segurado: {len(elementos_segurado)}\n")
            f.write(f"Tela 4 detectada: {'Sim' if elementos_segurado else 'Não'}\n")
        
        print("\n✅ **TESTE CONCLUÍDO!**")
        print(" Resultado salvo em: temp/teste_seletores_exatos/")
        
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
    testar_seletores_exatos()
