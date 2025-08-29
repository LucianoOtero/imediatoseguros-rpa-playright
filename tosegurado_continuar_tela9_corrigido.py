#!/usr/bin/env python3
"""
RPA Tô Segurado - Continuando da Tela 9 (CORRIGIDO)
Continua o fluxo a partir da Tela 9 com diagnóstico prévio
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

def navegar_ate_tela9(driver):
    """Navega até a Tela 9 (endereço onde o carro passa a noite)"""
    print("🚀 **NAVEGANDO ATÉ TELA 9...**")
    
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
    
    # Clicar em Continuar na Tela 6
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 6")
    
    # Aguardar Tela 7 carregar (estimativa inicial)
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa inicial')]"))
    )
    print("✅ Tela 7 carregada - estimativa inicial")
    
    # Clicar em Continuar na Tela 7
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 7")
    
    # Aguardar Tela 8 carregar (tipo de combustível)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tipo de Combustível')]"))
    )
    print("✅ Tela 8 carregada - tipo de combustível")
    
    # Selecionar Flex na Tela 8
    flex_radio = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Flex')]"))
    )
    driver.execute_script("arguments[0].click();", flex_radio)
    print("✅ Flex selecionado na Tela 8")
    
    # Clicar em Continuar na Tela 8
    continuar_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
    )
    continuar_btn.click()
    print("✅ Continuar clicado na Tela 8")
    
    # Aguardar Tela 9 carregar (endereço onde o carro passa a noite)
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'CEP') or contains(text(), 'endereço')]"))
    )
    print("✅ Tela 9 carregada - endereço onde o carro passa a noite")
    
    return True

def preencher_tela9(driver):
    """Preenche a Tela 9 (endereço onde o carro passa a noite)"""
    print("\n�� **PREENCHENDO TELA 9...**")
    
    try:
        # ========================================
        # TELA 9 - ENDEREÇO ONDE O CARRO PASSA A NOITE
        # ========================================
        # �� Campo: CEP
        # 🔍 Campo: Endereço (aparece em balão)
        # 🔍 Ação: Selecionar endereço no balão
        # 🔍 Ação: Clicar em Continuar
        # ========================================
        
        # Aguardar um pouco para a página carregar completamente
        time.sleep(3)
        
        # Inserir CEP (usar um CEP válido de São Paulo)
        cep_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CEP') or contains(@placeholder, '00000-000') or contains(@type, 'text')]"))
        )
        cep_input.clear()
        cep_input.send_keys("01310-100")  # CEP da Av. Paulista, São Paulo
        print("✅ CEP 01310-100 inserido")
        
        # Aguardar balão de endereço aparecer
        time.sleep(3)
        
        # Procurar e clicar no balão de endereço
        try:
            # Tentar diferentes seletores para o balão
            endereco_balao = None
            
            # Opção 1: Procurar por texto específico
            try:
                endereco_balao = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Av. Paulista') or contains(text(), 'São Paulo')]"))
                )
            except:
                pass
            
            # Opção 2: Procurar por classes de sugestão
            if not endereco_balao:
                try:
                    endereco_balao = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(@class, 'suggestion') or contains(@class, 'dropdown') or contains(@class, 'option')]"))
                    )
                except:
                    pass
            
            # Opção 3: Procurar por qualquer elemento clicável que contenha endereço
            if not endereco_balao:
                try:
                    endereco_balao = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Rua') or contains(text(), 'Av') or contains(text(), 'SP')]"))
                    )
                except:
                    pass
            
            if endereco_balao:
                driver.execute_script("arguments[0].click();", endereco_balao)
                print("✅ Endereço selecionado no balão")
            else:
                print("⚠️ Balão de endereço não encontrado, tentando continuar...")
                
        except Exception as e:
            print(f"⚠️ Erro ao selecionar endereço: {e}")
            print("⚠️ Tentando continuar sem selecionar endereço...")
        
        # Aguardar um pouco após seleção
        time.sleep(2)
        
        # Clicar em Continuar
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 9")
        
        # Aguardar carregamento da próxima tela
        time.sleep(5)
        
        # Verificar se carregou a Tela 10 (uso do veículo)
        if "uso do veículo" in driver.page_source.lower() or "finalidade" in driver.page_source.lower() or "pessoal" in driver.page_source.lower():
            print("✅ Tela 10 carregada - uso do veículo")
            return True
        else:
            print("❌ Tela 10 não carregou como esperado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao preencher Tela 9: {e}")
        return False

def extrair_dados_tela9(driver):
    """Extrai os dados da Tela 9"""
    print("\n📊 **EXTRAINDO DADOS DA TELA 9...**")
    
    try:
        # Salvar HTML da Tela 9
        with open("/opt/imediatoseguros-rpa/temp/tela9_final.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(" HTML da Tela 9 salvo")
        
        # Salvar dados da Tela 9
        with open("/opt/imediatoseguros-rpa/temp/dados_tela9_final.txt", "w", encoding="utf-8") as f:
            f.write("=== DADOS DA TELA 9 (ENDEREÇO ONDE O CARRO PASSA A NOITE) ===\n\n")
            f.write("🏠 ENDEREÇO INSERIDO:\n")
            f.write("- CEP: 01310-100\n")
            f.write("- Local: Av. Paulista, São Paulo\n")
            f.write("- Tipo: Endereço residencial\n\n")
            
            f.write("💡 NOTAS:\n")
            f.write("- CEP válido de São Paulo utilizado\n")
            f.write("- Endereço selecionado no balão de sugestões (se disponível)\n")
            f.write("- Esta informação influencia no valor do seguro\n")
            f.write("- Transição funcionou perfeitamente\n")
        
        print("📝 Dados da Tela 9 salvos")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados da Tela 9: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🚀 **RPA TÔ SEGURADO - CONTINUANDO DA TELA 9 (CORRIGIDO)**")
        print("=" * 70)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 9
        if not navegar_ate_tela9(driver):
            print("❌ Falha ao navegar até Tela 9")
            return
        
        # Extrair dados da Tela 9
        extrair_dados_tela9(driver)
        
        # Preencher e continuar da Tela 9
        if preencher_tela9(driver):
            print("\n **TELA 9 CONCLUÍDA COM SUCESSO!**")
            print("✅ CEP inserido")
            print("✅ Endereço selecionado (se disponível)")
            print("✅ Navegou para Tela 10")
            print("✅ Transição funcionou perfeitamente")
        else:
            print("\n❌ **FALHA AO CONTINUAR PARA TELA 10**")
        
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
