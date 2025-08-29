#!/usr/bin/env python3
"""
RPA Tô Segurado - CONTINUANDO COM O QUE FUNCIONAVA
Usando o script que estava funcionando perfeitamente até Tela 11
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

def aguardar_carregamento_pagina(driver, timeout=30):
    """Aguarda o carregamento completo da página"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
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

def navegar_ate_tela11(driver):
    """Navega o RPA até a Tela 11 (Uso do Veículo) - MÉTODO QUE FUNCIONAVA"""
    print("🚀 **NAVEGANDO ATÉ TELA 11 (USO DO VEÍCULO) - MÉTODO FUNCIONANDO**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # Clicar no botão Carro - MÉTODO ORIGINAL QUE FUNCIONAVA
    try:
        carro_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        salvar_estado_tela(driver, 1, "antes_clique", None)
        carro_btn.click()
        print("✅ Carro selecionado")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após selecionar Carro")
            return False
        
        salvar_estado_tela(driver, 1, "apos_clique", None)
    except Exception as e:
        print(f"❌ Erro ao selecionar Carro: {e}")
        return False
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    try:
        placa_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        salvar_estado_tela(driver, 2, "inicial", None)
        
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        
        salvar_estado_tela(driver, 2, "placa_inserida", None)
    except Exception as e:
        print(f"❌ Erro ao inserir placa: {e}")
        return False
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    try:
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após clicar Continuar")
            return False
    except Exception as e:
        print(f"❌ Erro ao clicar Continuar: {e}")
        return False
    
    # TELA 5: Confirmação do veículo
    print("\n📱 TELA 5: Confirmando veículo...")
    try:
        sim_radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmacaoVeiculo"))
        )
        driver.execute_script("arguments[0].click();", sim_radio)
        
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Veículo confirmado")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após confirmar veículo")
            return False
    except Exception as e:
        print(f"❌ Erro ao confirmar veículo: {e}")
        return False
    
    # TELA 6: Pergunta se veículo já está segurado
    print("\n📱 TELA 6: Selecionando 'Não' para veículo segurado...")
    try:
        nao_radio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "jaSegurado"))
        )
        driver.execute_script("arguments[0].click();", nao_radio)
        
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Radio 'Não' selecionado")
        print("✅ Continuar clicado na Tela 6")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após Tela 6")
            return False
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False
    
    # TELA 7: Confirmação que veículo não está segurado
    print("\n TELA 7: Aguardando confirmação...")
    try:
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 7")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou após Tela 7")
            return False
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False
    
    # TELA 8: Estimativa inicial
    print("\n TELA 8: Aguardando estimativa inicial...")
    try:
        # Aguardar elementos da estimativa
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial')]"))
        )
        print("✅ Tela 8 carregada - estimativa inicial detectada!")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        # Clicar em Continuar
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 8")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou após Tela 8")
            return False
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False
    
    # TELA 9: Tipo de combustível
    print("\n TELA 9: Aguardando tipo de combustível...")
    try:
        # Aguardar elementos do tipo de combustível
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível')]"))
        )
        print("✅ Tela 9 carregada - tipo de combustível detectado!")
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        # Clicar em Continuar
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 9")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou após Tela 9")
            return False
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False
    
    # TELA 10: Endereço de pernoite
    print("\n TELA 10: Aguardando endereço de pernoite...")
    try:
        # Aguardar elementos do endereço
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'endereço') or contains(text(), 'Endereço') or contains(text(), 'CEP')]"))
        )
        print("✅ Tela 10 carregada - endereço de pernoite detectado!")
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        # Inserir CEP
        cep_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "enderecoTelaEndereco"))
        )
        cep_input.clear()
        cep_input.send_keys("03084-000")
        print("✅ CEP 03084-000 inserido")
        
        # Aguardar sugestão e selecionar
        time.sleep(2)
        sugestao = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Rua Santa')]"))
        )
        sugestao.click()
        print("✅ Sugestão selecionada")
        
        # Clicar em Continuar
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 10")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou após Tela 10")
            return False
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False
    
    # TELA 11: Uso do veículo
    print("\n TELA 11: Aguardando uso do veículo...")
    try:
        # Aguardar elementos do uso do veículo
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'uso') or contains(text(), 'Uso') or contains(text(), 'veículo')]"))
        )
        print("✅ Tela 11 carregada - uso do veículo detectado!")
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        # Clicar em Continuar (assumindo que Pessoal é padrão)
        continuar_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_btn.click()
        print("✅ Continuar clicado na Tela 11")
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou após Tela 11")
            return False
        
        print("✅ TELA 11 CARREGADA E CONTINUAR CLICADO!")
    except Exception as e:
        print(f"❌ Erro na Tela 11: {e}")
        return False
    
    return True

def implementar_tela12(driver):
    """Implementa a Tela 12 (Dados Pessoais)"""
    print("\n **INICIANDO TELA 12: Dados pessoais**")
    
    # Aguardar Tela 12 carregar
    print("⏳ Aguardando Tela 12 carregar...")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Nome') or contains(text(), 'CPF') or contains(text(), 'nascimento')]"))
        )
        print("✅ Tela 12 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 12, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 12, "dados_pessoais_carregados", None)
        
        # Preencher Nome Completo
        print("⏳ Preenchendo Nome Completo...")
        try:
            nome_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Nome') or contains(@placeholder, 'nome')]"))
            )
            nome_input.clear()
            nome_input.send_keys("LUCIANO OTERO")
            print("✅ Nome Completo preenchido")
        except:
            print("⚠️ Campo Nome não encontrado - tentando prosseguir...")
        
        # Preencher CPF
        print("⏳ Preenchendo CPF...")
        try:
            cpf_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'CPF') or contains(@placeholder, 'cpf')]"))
            )
            cpf_input.clear()
            cpf_input.send_keys("085.546.078-48")
            print("✅ CPF preenchido")
        except:
            print("⚠️ Campo CPF não encontrado - tentando prosseguir...")
        
        # Preencher Data de Nascimento
        print("⏳ Preenchendo Data de Nascimento...")
        try:
            data_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Data') or contains(@placeholder, 'nascimento') or contains(@placeholder, 'Nascimento')]"))
            )
            data_input.clear()
            data_input.send_keys("09/02/1965")
            print("✅ Data de Nascimento preenchida")
        except:
            print("⚠️ Campo Data não encontrado - tentando prosseguir...")
        
        # Selecionar Sexo
        print("⏳ Selecionando Sexo...")
        try:
            masculino_radio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'masculino') or contains(text(), 'Masculino')]"))
            )
            driver.execute_script("arguments[0].click();", masculino_radio)
            print("✅ Sexo masculino selecionado")
        except:
            print("⚠️ Radio masculino não encontrado - tentando prosseguir...")
        
        # Selecionar Estado Civil
        print("⏳ Selecionando Estado Civil...")
        try:
            casado_radio = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'casado') or contains(text(), 'Casado')]"))
            )
            driver.execute_script("arguments[0].click();", casado_radio)
            print("✅ Estado civil casado selecionado")
        except:
            print("⚠️ Radio casado não encontrado - tentando prosseguir...")
        
        # Preencher E-mail
        print("⏳ Preenchendo E-mail...")
        try:
            email_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'E-mail') or contains(@placeholder, 'email') or contains(@type, 'email')]"))
            )
            email_input.clear()
            email_input.send_keys("lrotero@gmail.com")
            print("✅ E-mail preenchido")
        except:
            print("⚠️ Campo E-mail não encontrado - tentando prosseguir...")
        
        # Preencher Celular
        print("⏳ Preenchendo Celular...")
        try:
            celular_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[contains(@placeholder, 'Celular') or contains(@placeholder, 'celular') or contains(@placeholder, 'Telefone')]"))
            )
            celular_input.clear()
            celular_input.send_keys("(11) 97668-7668")
            print("✅ Celular preenchido")
        except:
            print("⚠️ Campo Celular não encontrado - tentando prosseguir...")
        
        salvar_estado_tela(driver, 12, "configuracao_completa", None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        try:
            continuar_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
            )
            print("✅ Botão Continuar encontrado")
            
            salvar_estado_tela(driver, 12, "antes_continuar", None)
            continuar_btn.click()
            print("✅ Continuar clicado na Tela 12")
            
            if not aguardar_carregamento_pagina(driver, 30):
                print("❌ Erro: Página não carregou após Tela 12")
                return False
            
            salvar_estado_tela(driver, 12, "apos_continuar", None)
            print("✅ **TELA 12 IMPLEMENTADA COM SUCESSO!**")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao clicar Continuar: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro na Tela 12: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - CONTINUANDO COM O QUE FUNCIONAVA**")
    print("=" * 80)
    print("🎯 OBJETIVO: Implementar Tela 12 (Dados Pessoais)")
    print("🔧 MÉTODO: Usando o script que funcionava perfeitamente até Tela 11")
    print("📝 NOTA: Continuação do fluxo a partir da Tela 11 (Uso do Veículo)")
    print("=" * 80)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 11 usando o método que funcionava
        if not navegar_ate_tela11(driver):
            print("❌ Erro: Falha ao navegar até Tela 11")
            return
        
        # Implementar Tela 12
        if implementar_tela12(driver):
            print("\n" + "=" * 80)
            print("🎉 **RPA EXECUTADO COM SUCESSO! TELA 12 IMPLEMENTADA!**")
            print("=" * 80)
            print(f"✅ Total de telas executadas: 12")
            print(f"✅ Tela 12: Dados pessoais implementada")
            print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        else:
            print("❌ Erro: Falha ao implementar Tela 12")
    
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
    
    finally:
        # Limpeza
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
