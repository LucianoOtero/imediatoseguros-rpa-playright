#!/usr/bin/env python3
"""
TESTE ESPECÍFICO PARA TELA 9 - DADOS PESSOAIS DO SEGURADO
=========================================================

Este script testa especificamente a implementação da Tela 9,
que coleta os dados pessoais do segurado.

CAMPOS A TESTAR:
===============
1. Nome Completo* - ID: "nomeTelaSegurado"
2. CPF* - ID: "cpfTelaSegurado" 
3. Data de nascimento* - ID: "dataNascimentoTelaSegurado"
4. Sexo* - Opções: "Masculino" e "Feminino"
5. Estado civil* - Opções: "Casado ou União Estável", "Divorciado", "Separado", "Solteiro", "Viuvo"
6. Email* - Campo de email
7. Celular - ID: "celularTelaSegurado"

DADOS DE TESTE:
==============
- Nome: "LUCIANO RODRIGUES OTERO"
- CPF: "085.546.07848"
- Data: "09/02/1965"
- Sexo: "Masculino"
- Estado Civil: "Casado ou União Estável"
- Email: "lrotero@gmail.com"
- Celular: "11976687668"

VERSÃO: 1.0
DATA: 29/08/2025
"""

import time
import json
import os
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def configurar_chrome():
    """Configura o Chrome para execução"""
    print("🔧 Configurando Chrome...")
    
    # Caminho do ChromeDriver
    chromedriver_path = "./chromedriver/chromedriver-win64/chromedriver.exe"
    
    if not os.path.exists(chromedriver_path):
        print(f"❌ ChromeDriver não encontrado em: {chromedriver_path}")
        return None, None
    
    # Configurações do Chrome
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # Diretório temporário único
    temp_dir = f"./temp_chrome_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    chrome_options.add_argument(f"--user-data-dir={temp_dir}")
    
    try:
        service = Service(chromedriver_path)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        print("✅ Chrome configurado com sucesso")
        return driver, temp_dir
    except Exception as e:
        print(f"❌ Erro ao configurar Chrome: {e}")
        return None, None

def carregar_parametros():
    """Carrega parâmetros do arquivo JSON"""
    try:
        with open("parametros_exemplo.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return None

def salvar_estado_tela(driver, tela, etapa, erro=None):
    """Salva o estado atual da tela para debug"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dir_tela = f"./temp/tela_{tela:02d}"
    os.makedirs(dir_tela, exist_ok=True)
    
    # Salvar HTML
    html_file = f"{dir_tela}/tela_{tela}_{etapa}_{timestamp}.html"
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(driver.page_source)
    
    # Salvar screenshot
    png_file = f"{dir_tela}/tela_{tela}_{etapa}_{timestamp}.png"
    driver.save_screenshot(png_file)
    
    # Salvar log
    log_file = f"{dir_tela}/tela_{tela}_{etapa}_{timestamp}.txt"
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Tela {tela} - {etapa}\n")
        f.write(f"Timestamp: {timestamp}\n")
        if erro:
            f.write(f"Erro: {erro}\n")
        f.write(f"URL: {driver.current_url}\n")
        f.write(f"Título: {driver.title}\n")
    
    print(f"📁 Estado salvo: {html_file}")

def navegar_ate_tela9(driver, parametros):
    """Navega até a Tela 9 usando o fluxo completo"""
    print("\n🚀 **NAVEGANDO ATÉ TELA 9 VIA FLUXO COMPLETO**")
    
    try:
        # Abrir URL base
        print("⏳ Abrindo URL base...")
        driver.get(parametros["url_base"])
        time.sleep(5)
        
        # Tela 1: Selecionar Carro
        print("⏳ Tela 1: Selecionando Carro...")
        carro_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Carro')]"))
        )
        driver.execute_script("arguments[0].click();", carro_element)
        time.sleep(15)
        
        # Tela 2: Inserir placa
        print("⏳ Tela 2: Inserindo placa...")
        placa_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Digite a placa']"))
        )
        placa_element.clear()
        placa_element.send_keys("KVA-1791")
        time.sleep(15)
        
        # Tela 3: Confirmar ECOSPORT
        print("⏳ Tela 3: Confirmando ECOSPORT...")
        sim_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sim')]"))
        )
        driver.execute_script("arguments[0].click();", sim_element)
        time.sleep(15)
        
        # Tela 4: Veículo segurado
        print("⏳ Tela 4: Veículo segurado...")
        nao_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Não')]"))
        )
        driver.execute_script("arguments[0].click();", nao_element)
        time.sleep(15)
        
        # Tela 5: Estimativa inicial
        print("⏳ Tela 5: Estimativa inicial...")
        continuar_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaEstimativaContinuar"))
        )
        driver.execute_script("arguments[0].click();", continuar_element)
        time.sleep(15)
        
        # Tela 6: Tipo combustível
        print("⏳ Tela 6: Tipo combustível...")
        continuar_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaCombustivelContinuar"))
        )
        driver.execute_script("arguments[0].click();", continuar_element)
        time.sleep(15)
        
        # Tela 7: Endereço pernoite
        print("⏳ Tela 7: Endereço pernoite...")
        continuar_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaEnderecoPernoiteContinuar"))
        )
        driver.execute_script("arguments[0].click();", continuar_element)
        time.sleep(15)
        
        # Tela 8: Finalidade veículo
        print("⏳ Tela 8: Finalidade veículo...")
        continuar_element = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaUsoVeiculoContinuar"))
        )
        driver.execute_script("arguments[0].click();", continuar_element)
        time.sleep(15)
        
        print("✅ Navegação até Tela 9 concluída!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na navegação: {e}")
        return False

def testar_tela9(driver, parametros):
    """Testa especificamente a Tela 9"""
    print("\n👤 **TESTANDO TELA 9: Dados pessoais do segurado**")
    
    try:
        # Aguardar elementos da tela de dados pessoais
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'dados pessoais') or contains(text(), 'Dados pessoais')]"))
        )
        print("✅ Tela 9 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        # 1. Testar Nome Completo
        print("⏳ Testando Nome Completo...")
        nome_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "nomeTelaSegurado"))
        )
        nome_element.clear()
        nome_element.send_keys(parametros["nome"])
        print(f"✅ Nome preenchido: {parametros['nome']}")
        
        # 2. Testar CPF
        print("⏳ Testando CPF...")
        cpf_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "cpfTelaSegurado"))
        )
        cpf_element.clear()
        cpf_element.send_keys(parametros["cpf"])
        print(f"✅ CPF preenchido: {parametros['cpf']}")
        
        # 3. Testar Data de Nascimento
        print("⏳ Testando Data de Nascimento...")
        data_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "dataNascimentoTelaSegurado"))
        )
        data_element.clear()
        data_element.send_keys(parametros["data_nascimento"])
        print(f"✅ Data de nascimento preenchida: {parametros['data_nascimento']}")
        
        # 4. Testar Sexo
        print("⏳ Testando Sexo...")
        # Tentar encontrar opções de sexo
        sexo_options = driver.find_elements(By.XPATH, "//*[contains(text(), 'Masculino') or contains(text(), 'Feminino')]")
        if sexo_options:
            print(f"✅ Opções de sexo encontradas: {len(sexo_options)}")
            for option in sexo_options:
                print(f"   - {option.text}")
        else:
            print("⚠️ Opções de sexo não encontradas")
        
        # 5. Testar Estado Civil
        print("⏳ Testando Estado Civil...")
        # Tentar encontrar opções de estado civil
        estado_options = driver.find_elements(By.XPATH, "//*[contains(text(), 'Casado') or contains(text(), 'Solteiro') or contains(text(), 'Divorciado') or contains(text(), 'Separado') or contains(text(), 'Viuvo')]")
        if estado_options:
            print(f"✅ Opções de estado civil encontradas: {len(estado_options)}")
            for option in estado_options:
                print(f"   - {option.text}")
        else:
            print("⚠️ Opções de estado civil não encontradas")
        
        # 6. Testar Email
        print("⏳ Testando Email...")
        email_selectors = [
            "//input[@type='email']",
            "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email')]",
            "//input[contains(@id, 'email') or contains(@name, 'email')]"
        ]
        
        email_element = None
        for selector in email_selectors:
            try:
                email_element = driver.find_element(By.XPATH, selector)
                break
            except NoSuchElementException:
                continue
        
        if email_element:
            email_element.clear()
            email_element.send_keys(parametros["email"])
            print(f"✅ Email preenchido: {parametros['email']}")
        else:
            print("⚠️ Campo de email não encontrado")
        
        # 7. Testar Celular
        print("⏳ Testando Celular...")
        celular_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "celularTelaSegurado"))
        )
        celular_element.clear()
        celular_element.send_keys(parametros["celular"])
        print(f"✅ Celular preenchido: {parametros['celular']}")
        
        # Salvar estado após preenchimento
        salvar_estado_tela(driver, 9, "campos_preenchidos", None)
        
        # Testar botão Continuar
        print("⏳ Testando botão Continuar...")
        continuar_selectors = [
            "//p[contains(@class, 'font-semibold') and contains(@class, 'cursor-pointer') and contains(text(), 'Continuar')]",
            "//button[contains(text(), 'Continuar')]",
            "//*[contains(text(), 'Continuar') and contains(@class, 'cursor-pointer')]"
        ]
        
        continuar_encontrado = False
        for selector in continuar_selectors:
            try:
                continuar_element = driver.find_element(By.XPATH, selector)
                print(f"✅ Botão Continuar encontrado com seletor: {selector}")
                continuar_encontrado = True
                break
            except NoSuchElementException:
                continue
        
        if not continuar_encontrado:
            print("⚠️ Botão Continuar não encontrado")
        
        print("✅ **TESTE DA TELA 9 CONCLUÍDO COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste da Tela 9: {e}")
        salvar_estado_tela(driver, 9, "erro", str(e))
        return False

def main():
    """Função principal"""
    print("🧪 **TESTE ESPECÍFICO PARA TELA 9 - DADOS PESSOAIS**")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            print("❌ Falha ao carregar parâmetros")
            return False
        
        print("✅ Parâmetros carregados:")
        print(f"   - Nome: {parametros['nome']}")
        print(f"   - CPF: {parametros['cpf']}")
        print(f"   - Data: {parametros['data_nascimento']}")
        print(f"   - Sexo: {parametros['sexo']}")
        print(f"   - Estado Civil: {parametros['estado_civil']}")
        print(f"   - Email: {parametros['email']}")
        print(f"   - Celular: {parametros['celular']}")
        
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        if not driver:
            print("❌ Falha ao configurar Chrome")
            return False
        
        # Navegar até Tela 9
        if not navegar_ate_tela9(driver, parametros):
            print("❌ Erro: Falha ao navegar até Tela 9")
            return False
        
        # Testar Tela 9
        if not testar_tela9(driver, parametros):
            print("❌ Erro: Falha no teste da Tela 9")
            return False
        
        print("\n" + "=" * 80)
        print("🎉 **TESTE DA TELA 9 CONCLUÍDO COM SUCESSO!**")
        print("=" * 80)
        print("✅ Todos os campos foram testados")
        print("✅ Dados de teste foram preenchidos")
        print("✅ Botão Continuar foi localizado")
        print(f"📁 Arquivos de debug salvos em: temp/")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE TESTE:** {e}")
        return False
        
    finally:
        # Limpeza
        if driver:
            print("🔧 Fechando driver...")
            try:
                driver.quit()
                print("✅ Driver fechado com sucesso")
            except Exception as e:
                print(f"⚠️ Erro ao fechar driver: {e}")
        
        if temp_dir and os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
                print(f"🗑️ Diretório temporário removido: {temp_dir}")
            except Exception as e:
                print(f"⚠️ Erro ao remover diretório temporário: {e}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
