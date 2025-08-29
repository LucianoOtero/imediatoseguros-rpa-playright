#!/usr/bin/env python3
"""
RPA Tô Segurado - Continuando da Tela 8 (COMPLETO)
Continua o fluxo a partir da Tela 8 com todas as opções documentadas
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

def navegar_ate_tela8(driver):
    """Navega até a Tela 8 (tipo de combustível)"""
    print("🚀 **NAVEGANDO ATÉ TELA 8...**")
    
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
    
    return True

def preencher_tela8(driver):
    """Preenche a Tela 8 (tipo de combustível e checkboxes)"""
    print("\n⛽ **PREENCHENDO TELA 8...**")
    
    try:
        # ========================================
        # TIPO DE COMBUSTÍVEL - OPÇÕES DISPONÍVEIS:
        # ========================================
        # ✅ Flex (SELECIONADO ATUALMENTE)
        # 🔄 Gasolina (OPÇÃO FUTURA)
        # 🔄 Álcool (OPÇÃO FUTURA)
        # 🔄 Diesel (OPÇÃO FUTURA)
        # �� Híbrido (OPÇÃO FUTURA)
        # 🔄 Elétrico (OPÇÃO FUTURA)
        # ========================================
        
        # Selecionar Flex (combustível)
        flex_radio = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Flex')]"))
        )
        driver.execute_script("arguments[0].click();", flex_radio)
        print("✅ Flex selecionado")
        
        # ========================================
        # CHECKBOXES - OPÇÕES DISPONÍVEIS:
        # ========================================
        # �� Kit Gás (OPÇÃO FUTURA - não selecionado)
        # 🔄 Blindado (OPÇÃO FUTURA - não selecionado)
        # 🔄 Financiado (OPÇÃO FUTURA - não selecionado)
        # ========================================
        
        # Deixar checkboxes em branco (Kit Gás, Blindado, Financiado)
        print("✅ Checkboxes deixados em branco")
        
        # Clicar em Continuar
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 8")
        
        # Aguardar carregamento da próxima tela
        time.sleep(5)
        
        # Verificar se carregou a Tela 9 (endereço onde o carro passa a noite)
        if "CEP" in driver.page_source or "endereço" in driver.page_source.lower():
            print("✅ Tela 9 carregada - endereço onde o carro passa a noite")
            return True
        else:
            print("❌ Tela 9 não carregou como esperado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao preencher Tela 8: {e}")
        return False

def extrair_dados_tela8(driver):
    """Extrai os dados da Tela 8 com todas as opções documentadas"""
    print("\n📊 **EXTRAINDO DADOS DA TELA 8...**")
    
    try:
        # Salvar HTML da Tela 8
        with open("/opt/imediatoseguros-rpa/temp/tela8_combustivel_completo.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print(" HTML da Tela 8 salvo")
        
        # Salvar dados da Tela 8 com todas as opções
        with open("/opt/imediatoseguros-rpa/temp/dados_tela8_completo.txt", "w", encoding="utf-8") as f:
            f.write("=== DADOS DA TELA 8 (TIPO DE COMBUSTÍVEL) ===\n\n")
            
            f.write("⛽ TIPOS DE COMBUSTÍVEL DISPONÍVEIS:\n")
            f.write("✅ Flex (SELECIONADO ATUALMENTE)\n")
            f.write("🔄 Gasolina (OPÇÃO FUTURA)\n")
            f.write("🔄 Álcool (OPÇÃO FUTURA)\n")
            f.write("🔄 Diesel (OPÇÃO FUTURA)\n")
            f.write("�� Híbrido (OPÇÃO FUTURA)\n")
            f.write("🔄 Elétrico (OPÇÃO FUTURA)\n\n")
            
            f.write("�� CHECKBOXES DISPONÍVEIS:\n")
            f.write("�� Kit Gás (OPÇÃO FUTURA - não selecionado)\n")
            f.write("🔄 Blindado (OPÇÃO FUTURA - não selecionado)\n")
            f.write("🔄 Financiado (OPÇÃO FUTURA - não selecionado)\n\n")
            
            f.write("�� CONFIGURAÇÃO ATUAL:\n")
            f.write("- Combustível: Flex\n")
            f.write("- Kit Gás: Não selecionado\n")
            f.write("- Blindado: Não selecionado\n")
            f.write("- Financiado: Não selecionado\n\n")
            
            f.write("💡 NOTAS PARA FUTURO:\n")
            f.write("- Estes campos podem ser modificados para aprimorar o cálculo\n")
            f.write("- Diferentes combustíveis podem alterar o valor do seguro\n")
            f.write("- Checkboxes adicionais podem modificar a cobertura\n")
        
        print("📝 Dados da Tela 8 salvos com todas as opções")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao extrair dados da Tela 8: {e}")
        return False

def main():
    """Função principal"""
    driver = None
    temp_dir = None
    
    try:
        print("🚀 **RPA TÔ SEGURADO - CONTINUANDO DA TELA 8 (COMPLETO)**")
        print("=" * 70)
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 8
        if not navegar_ate_tela8(driver):
            print("❌ Falha ao navegar até Tela 8")
            return
        
        # Extrair dados da Tela 8
        extrair_dados_tela8(driver)
        
        # Preencher e continuar da Tela 8
        if preencher_tela8(driver):
            print("\n **TELA 8 CONCLUÍDA COM SUCESSO!**")
            print("✅ Flex selecionado")
            print("✅ Checkboxes deixados em branco")
            print("✅ Navegou para Tela 9")
            print("📋 Todas as opções futuras documentadas")
        else:
            print("\n❌ **FALHA AO CONTINUAR PARA TELA 9**")
        
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
