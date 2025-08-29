#!/usr/bin/env python3
"""
Teste Específico da Tela 7 - Verifica Redirecionamentos
RPA Tô Segurado
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

def navegar_ate_tela6(driver):
    """Navega até a Tela 6"""
    print("🚀 **NAVEGANDO ATÉ TELA 6**")
    
    try:
        # Tela 1: Selecionar Carro
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        time.sleep(5)
        
        carro_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("✅ Carro selecionado")
        time.sleep(3)
        
        # Tela 2: Inserir placa
        placa_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        time.sleep(2)
        
        # Tela 3: Clicar Continuar
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado")
        time.sleep(5)
        
        # Tela 5: Confirmar veículo
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        
        sim_radio = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
        )
        driver.execute_script("arguments[0].click();", sim_radio)
        print("✅ Veículo confirmado")
        time.sleep(3)
        
        # Tela 6: Veículo segurado
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmarVeiculoTelaInformacoesVeiculo"))
        )
        
        nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
        if not nao_radio.is_selected():
            driver.execute_script("arguments[0].click();", nao_radio)
            print("✅ Radio 'Não' selecionado")
            time.sleep(2)
        
        print("✅ TELA 6 CARREGADA!")
        return True
        
    except Exception as e:
        print(f"❌ **ERRO AO NAVEGAR ATÉ TELA 6:** {e}")
        return False

def testar_clique_continuar_tela6(driver):
    """Testa o clique em Continuar na Tela 6 com monitoramento detalhado"""
    print("\n🔍 **TESTANDO CLIQUE CONTINUAR TELA 6**")
    
    try:
        # Salvar estado inicial
        print("📸 Salvando estado inicial da Tela 6...")
        with open("/opt/imediatoseguros-rpa/temp/tela_06_estado_inicial.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_06_estado_inicial.png")
        
        # Verificar elementos antes do clique
        print("\n🔍 **ELEMENTOS ANTES DO CLIQUE:**")
        page_source = driver.page_source
        
        # Verificar se estamos realmente na Tela 6
        if "EED3D56" in page_source and "COROLLA" in page_source:
            print("✅ Confirmação: Estamos na Tela 6 (placa e veículo detectados)")
        else:
            print("❌ PROBLEMA: Não estamos na Tela 6 esperada!")
            return False
        
        # Verificar radio buttons
        radio_nao = driver.find_element(By.XPATH, "//input[@value='Não']")
        if radio_nao.is_selected():
            print("✅ Radio 'Não' está selecionado")
        else:
            print("❌ Radio 'Não' NÃO está selecionado!")
            return False
        
        # Verificar botão Continuar
        continuar_button = driver.find_element(By.ID, "gtm-telaInfosAutoContinuar")
        if continuar_button.is_enabled():
            print("✅ Botão Continuar está habilitado")
        else:
            print("❌ Botão Continuar NÃO está habilitado!")
            return False
        
        # Clicar em Continuar e monitorar
        print("\n🖱️ **CLICANDO EM CONTINUAR E MONITORANDO...**")
        
        # Salvar estado antes do clique
        with open("/opt/imediatoseguros-rpa/temp/tela_06_antes_clique_final.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_06_antes_clique_final.png")
        
        # Clicar
        continuar_button.click()
        print("✅ Continuar clicado")
        
        # Monitorar mudanças por 45 segundos (mais tempo)
        print("\n⏳ **MONITORANDO MUDANÇAS POR 45 SEGUNDOS...**")
        mudancas_detectadas = False
        
        for i in range(45):
            time.sleep(1)
            current_url = driver.current_url
            current_title = driver.title
            
            # Verificar se houve mudança na URL
            if i == 0:
                url_inicial = current_url
                title_inicial = current_title
                print(f"⏱️ {i+1:02d}s - URL INICIAL: {url_inicial}")
                print(f"     Título INICIAL: {title_inicial}")
            else:
                if current_url != url_inicial or current_title != title_inicial:
                    print(f"🔄 MUDANÇA DETECTADA aos {i+1}s!")
                    print(f"   URL: {url_inicial} → {current_url}")
                    print(f"   Título: {title_inicial} → {current_title}")
                    mudancas_detectadas = True
                    break
                else:
                    print(f"⏱️ {i+1:02d}s - Sem mudanças")
            
            # Verificar se apareceu algum elemento específico
            page_text = driver.page_source.lower()
            
            if "estimativa" in page_text:
                print("🎯 'ESTIMATIVA' DETECTADO!")
                mudancas_detectadas = True
                break
            elif "carrossel" in page_text:
                print(" 'CARROSSEL' DETECTADO!")
                mudancas_detectadas = True
                break
            elif "cobertura" in page_text:
                print("🛡️ 'COBERTURA' DETECTADO!")
                mudancas_detectadas = True
                break
            elif "loading" in page_text and "lazy" not in page_text:
                print("⏳ ELEMENTO DE CARREGAMENTO REAL DETECTADO!")
                mudancas_detectadas = True
                break
        
        # Salvar estado final
        print("\n📸 Salvando estado final...")
        with open("/opt/imediatoseguros-rpa/temp/tela_07_estado_final.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("/opt/imediatoseguros-rpa/temp/tela_07_estado_final.png")
        
        # Análise final
        print(f"\n **ANÁLISE FINAL:**")
        print(f"URL Final: {driver.current_url}")
        print(f"Título Final: {driver.title}")
        
        if mudancas_detectadas:
            print("✅ MUDANÇAS DETECTADAS - Tela 7 pode ter carregado!")
        else:
            print("❌ NENHUMA MUDANÇA DETECTADA - Página travou!")
        
        # Verificar se voltamos para Tela 6
        page_source_final = driver.page_source
        if "EED3D56" in page_source_final and "COROLLA" in page_source_final:
            print("⚠️ POSSÍVEL PROBLEMA: Voltamos para Tela 6!")
        else:
            print("✅ Não voltamos para Tela 6")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NO TESTE:** {e}")
        return False

def main():
    """Função principal"""
    print("�� **TESTE ESPECÍFICO DA TELA 7 - REDIRECIONAMENTOS**")
    print("=" * 70)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 6
        if not navegar_ate_tela6(driver):
            print("❌ **FALHA AO NAVEGAR ATÉ TELA 6 - PARANDO**")
            return
        
        # Testar clique Continuar
        if not testar_clique_continuar_tela6(driver):
            print("❌ **FALHA NO TESTE - PARANDO**")
            return
        
        print(f"\n **TESTE CONCLUÍDO COM SUCESSO!**")
        print(f"�� Arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"🔍 Verifique os resultados para entender o problema")
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL DURANTE TESTE:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-teste.png")
            print(" Screenshot do erro salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
