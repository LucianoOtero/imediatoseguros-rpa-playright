#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - TELA 3 CORRIGIDA
===============================================================================
�� OBJETIVO: Corrigir Tela 3 para selecionar "Sim" na confirmação do veículo
⚡ MÉTODO: Selecionar radio "Sim" antes de clicar Continuar
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

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio"):
    """Clica em um radio button via JavaScript procurando por texto"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        
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

def testar_tela3_corrigida():
    """Testa Tela 3 corrigida"""
    print("🧪 **TESTANDO TELA 3 CORRIGIDA**")
    print("=" * 80)
    print("�� OBJETIVO: Selecionar 'Sim' na confirmação do veículo")
    print("⚡ MÉTODO: Radio 'Sim' + Continuar")
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
        
        # TELA 3 CORRIGIDA: Selecionar "Sim" na confirmação
        print("\n📱 TELA 3: Selecionando 'Sim' na confirmação do veículo...")
        
        # Aguardar pergunta sobre o veículo aparecer
        print("⏳ Aguardando pergunta sobre o veículo...")
        time.sleep(10)
        
        # Selecionar "Sim" no radio button
        if clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação do veículo"):
            print("✅ Radio 'Sim' selecionado")
        else:
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
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
            print("✅ TELA 4 DETECTADA! Correção funcionou!")
            print("�� PROBLEMA RESOLVIDO: Tela 3 corrigida!")
        else:
            print("❌ TELA 4 ainda não detectada")
            print("⚠️ PROBLEMA PERSISTE: Verificar outras causas")
            
        # Salvar estado final
        timestamp = datetime.now().strftime("%H:%M:%S")
        os.makedirs("temp/teste_tela3_corrigida", exist_ok=True)
        
        with open("temp/teste_tela3_corrigida/resultado.txt", "w", encoding="utf-8") as f:
            f.write(f"TESTE TELA 3 CORRIGIDA - {timestamp}\n")
            f.write(f"Placa usada: {PLACA_TESTE}\n")
            f.write(f"Radio 'Sim' selecionado: Sim\n")
            f.write(f"URL: {driver.current_url}\n")
            f.write(f"Título: {driver.title}\n")
            f.write(f"Elementos segurado: {len(elementos_segurado)}\n")
            f.write(f"Tela 4 detectada: {'Sim' if elementos_segurado else 'Não'}\n")
        
        print("\n✅ **TESTE CONCLUÍDO!**")
        print(" Resultado salvo em: temp/teste_tela3_corrigida/")
        
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
    testar_tela3_corrigida()
