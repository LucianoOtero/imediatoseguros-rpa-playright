#!/usr/bin/env python3
"""
RPA Tô Segurado - COMPLETO COM LOGS DETALHADOS
Executa todo o fluxo com logs, screenshots e HTML de cada tela
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
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    return driver, temp_dir

def criar_diretorio_tela(numero_tela):
    """Cria diretório para salvar arquivos da tela"""
    diretorio = f"/opt/imediatoseguros-rpa/temp/tela_{numero_tela:02d}"
    os.makedirs(diretorio, exist_ok=True)
    return diretorio

def salvar_estado_tela(driver, numero_tela, descricao, sufixo=""):
    """Salva o estado completo da tela"""
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
    """Registra log detalhado da tela"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    url = driver.current_url
    titulo = driver.title
    
    print(f"\n{'='*80}")
    print(f"��️  **TELA {numero_tela:02d}: {descricao}** - {timestamp}")
    print(f"{'='*80}")
    print(f"🌐 URL: {url}")
    print(f"📄 Título: {titulo}")
    
    if acao:
        print(f"🎯 Ação: {acao}")
    
    # Salvar estado da tela
    diretorio = salvar_estado_tela(driver, numero_tela, descricao)
    print(f"�� Arquivos salvos em: {diretorio}")
    
    return diretorio

def tela1_selecionar_carro(driver):
    """Tela 1: Selecionar tipo de seguro (Carro)"""
    print("\n�� **INICIANDO TELA 1: Seleção do tipo de seguro**")
    
    # Navegar para a página
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    time.sleep(5)
    
    # Salvar estado inicial
    log_tela(driver, 1, "inicial", "Página carregada")
    
    # Procurar e clicar no botão Carro
    try:
        carro_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        print("✅ Botão Carro encontrado e clicável")
        
        # Salvar estado antes do clique
        log_tela(driver, 1, "antes_clique", "Antes de clicar no Carro")
        
        # Clicar no botão
        carro_button.click()
        print("✅ Clique no botão Carro realizado")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 1, "apos_clique", "Após clicar no Carro")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 1:** {e}")
        log_tela(driver, 1, "erro", f"Erro: {e}")
        return False

def tela2_inserir_placa(driver):
    """Tela 2: Inserir placa do veículo"""
    print("\n�� **INICIANDO TELA 2: Inserção da placa**")
    
    try:
        # Aguardar campo de placa aparecer
        placa_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "placaTelaPlaca"))
        )
        print("✅ Campo de placa encontrado")
        
        # Salvar estado inicial da Tela 2
        log_tela(driver, 2, "inicial", "Campo de placa encontrado")
        
        # Inserir placa
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        time.sleep(2)
        
        # Salvar estado com placa inserida
        log_tela(driver, 2, "placa_inserida", "Placa EED3D56 inserida")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 2:** {e}")
        log_tela(driver, 2, "erro", f"Erro: {e}")
        return False

def tela3_clicar_continuar(driver):
    """Tela 3: Clicar em Continuar após inserir placa"""
    print("\n�� **INICIANDO TELA 3: Clicar em Continuar**")
    
    try:
        # Procurar botão Continuar
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
        )
        print("✅ Botão Continuar encontrado")
        
        # Salvar estado antes do clique
        log_tela(driver, 3, "antes_clique", "Antes de clicar em Continuar")
        
        # Clicar em Continuar
        continuar_button.click()
        print("✅ Continuar clicado")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 3, "apos_clique", "Após clicar em Continuar")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 3:** {e}")
        log_tela(driver, 3, "erro", f"Erro: {e}")
        return False

def tela5_confirmar_veiculo(driver):
    """Tela 5: Confirmar informações do veículo"""
    print("\n�� **INICIANDO TELA 5: Confirmação do veículo**")
    
    try:
        # Aguardar Tela 5 carregar
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        print("✅ Tela 5 carregada - veículo COROLLA detectado")
        
        # Salvar estado inicial da Tela 5
        log_tela(driver, 5, "inicial", "Tela 5 carregada - veículo COROLLA")
        
        # Procurar e clicar no radio "Sim"
        sim_radio = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@value='Sim']"))
        )
        print("✅ Radio 'Sim' encontrado")
        
        # Salvar estado antes da confirmação
        log_tela(driver, 5, "antes_confirmacao", "Antes de confirmar veículo")
        
        # Clicar via JavaScript
        driver.execute_script("arguments[0].click();", sim_radio)
        print("✅ Veículo confirmado via JavaScript")
        time.sleep(2)
        
        # Salvar estado após confirmação
        log_tela(driver, 5, "apos_confirmacao", "Após confirmar veículo")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 5:** {e}")
        log_tela(driver, 5, "erro", f"Erro: {e}")
        return False

def tela6_veiculo_segurado(driver):
    """Tela 6: Informar se veículo já está segurado"""
    print("\n�� **INICIANDO TELA 6: Veículo já segurado**")
    
    try:
        # Aguardar Tela 6 carregar
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'já está segurado')]"))
        )
        print("✅ Tela 6 carregada - pergunta sobre seguro vigente")
        
        # Salvar estado inicial da Tela 6
        log_tela(driver, 6, "inicial", "Tela 6 carregada - seguro vigente")
        
        # Verificar se "Não" já está selecionado
        try:
            nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
            if nao_radio.is_selected():
                print("✅ Radio 'Não' já estava selecionado")
            else:
                print("⚠️ Radio 'Não' não estava selecionado - selecionando...")
                driver.execute_script("arguments[0].click();", nao_radio)
                time.sleep(1)
        except:
            print("⚠️ Radio 'Não' não encontrado - procurando alternativas...")
        
        # Salvar estado antes de continuar
        log_tela(driver, 6, "antes_continuar", "Antes de clicar em Continuar")
        
        # Clicar em Continuar
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 6")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 6, "apos_continuar", "Após clicar em Continuar")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 6:** {e}")
        log_tela(driver, 6, "erro", f"Erro: {e}")
        return False

def tela7_estimativa_inicial(driver):
    """Tela 7: Aguardar carregamento da estimativa inicial"""
    print("\n�� **INICIANDO TELA 7: Estimativa inicial**")
    
    try:
        # Aguardar Tela 7 carregar
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa inicial')]"))
        )
        print("✅ Tela 7 carregada - estimativa inicial detectada")
        
        # Salvar estado da Tela 7
        log_tela(driver, 7, "estimativa_carregada", "Estimativa inicial carregada")
        
        # Aguardar um pouco para garantir que carregou completamente
        time.sleep(5)
        
        # Salvar estado após carregamento completo
        log_tela(driver, 7, "carregamento_completo", "Carregamento completo da estimativa")
        
        # Clicar em Continuar
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 7")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 7, "apos_continuar", "Após clicar em Continuar")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 7:** {e}")
        log_tela(driver, 7, "erro", f"Erro: {e}")
        return False

def tela8_tipo_combustivel(driver):
    """Tela 8: Selecionar tipo de combustível"""
    print("\n�� **INICIANDO TELA 8: Tipo de combustível**")
    
    try:
        # Aguardar Tela 8 carregar
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Tipo de Combustível')]"))
        )
        print("✅ Tela 8 carregada - tipo de combustível")
        
        # Salvar estado inicial da Tela 8
        log_tela(driver, 8, "inicial", "Tela 8 carregada - tipo de combustível")
        
        # Selecionar Flex
        flex_radio = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@value='Flex']"))
        )
        flex_radio.click()
        print("✅ Flex selecionado")
        time.sleep(2)
        
        # Salvar estado com Flex selecionado
        log_tela(driver, 8, "flex_selecionado", "Flex selecionado")
        
        # Clicar em Continuar
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 8")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 8, "apos_continuar", "Após clicar em Continuar")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 8:** {e}")
        log_tela(driver, 8, "erro", f"Erro: {e}")
        return False

def tela9_endereco_pernoite(driver):
    """Tela 9: Endereço onde o carro passa a noite"""
    print("\n�� **INICIANDO TELA 9: Endereço onde o carro passa a noite**")
    
    try:
        # Aguardar Tela 9 carregar
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Onde o carro passa a noite')]"))
        )
        print("✅ Tela 9 carregada - endereço onde o carro passa a noite")
        
        # Salvar estado inicial da Tela 9
        log_tela(driver, 9, "inicial", "Tela 9 carregada - endereço pernoite")
        
        # Encontrar campo CEP
        cep_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.ID, "enderecoTelaEndereco"))
        )
        print("✅ Campo CEP encontrado")
        
        # Salvar estado com campo CEP encontrado
        log_tela(driver, 9, "campo_cep_encontrado", "Campo CEP encontrado")
        
        # Inserir CEP
        cep_input.clear()
        cep_input.send_keys("03084-000")
        print("✅ CEP 03084-000 inserido")
        time.sleep(3)
        
        # Salvar estado com CEP inserido
        log_tela(driver, 9, "cep_inserido", "CEP inserido - aguardando autocomplete")
        
        # Tentar selecionar sugestão automática
        try:
            sugestao = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'São Paulo')]"))
            )
            print("✅ Sugestão de endereço detectada")
            sugestao.click()
            print("✅ Sugestão selecionada")
            time.sleep(2)
            
            # Salvar estado com sugestão selecionada
            log_tela(driver, 9, "sugestao_selecionada", "Sugestão de endereço selecionada")
            
        except:
            print("⚠️ Não foi possível selecionar sugestão - preenchendo manualmente")
            cep_input.clear()
            cep_input.send_keys("Rua Serra de Botucatu, Tatuapé - São Paulo/SP")
            print("✅ Endereço preenchido manualmente")
            time.sleep(2)
            
            # Salvar estado com endereço manual
            log_tela(driver, 9, "endereco_manual", "Endereço preenchido manualmente")
        
        # Verificar endereço preenchido
        endereco_preenchido = cep_input.get_attribute("value")
        print(f"📝 Endereço preenchido: {endereco_preenchido}")
        
        # Salvar estado final da Tela 9
        log_tela(driver, 9, "endereco_completo", f"Endereço completo: {endereco_preenchido}")
        
        # Clicar em Continuar
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaPernoiteVeiculoContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 9")
        time.sleep(3)
        
        # Salvar estado após clique
        log_tela(driver, 9, "apos_continuar", "Após clicar em Continuar")
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 9:** {e}")
        log_tela(driver, 9, "erro", f"Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - COMPLETO COM LOGS DETALHADOS**")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Executar fluxo completo
        telas_executadas = []
        
        # Tela 1: Selecionar Carro
        if tela1_selecionar_carro(driver):
            telas_executadas.append("Tela 1: Carro selecionado")
        else:
            print("❌ **FALHA NA TELA 1 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 2: Inserir placa
        if tela2_inserir_placa(driver):
            telas_executadas.append("Tela 2: Placa inserida")
        else:
            print("❌ **FALHA NA TELA 2 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 3: Clicar Continuar
        if tela3_clicar_continuar(driver):
            telas_executadas.append("Tela 3: Continuar clicado")
        else:
            print("❌ **FALHA NA TELA 3 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 5: Confirmar veículo
        if tela5_confirmar_veiculo(driver):
            telas_executadas.append("Tela 5: Veículo confirmado")
        else:
            print("❌ **FALHA NA TELA 5 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 6: Veículo segurado
        if tela6_veiculo_segurado(driver):
            telas_executadas.append("Tela 6: Seguro vigente informado")
        else:
            print("❌ **FALHA NA TELA 6 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 7: Estimativa inicial
        if tela7_estimativa_inicial(driver):
            telas_executadas.append("Tela 7: Estimativa inicial carregada")
        else:
            print("❌ **FALHA NA TELA 7 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 8: Tipo de combustível
        if tela8_tipo_combustivel(driver):
            telas_executadas.append("Tela 8: Tipo de combustível selecionado")
        else:
            print("❌ **FALHA NA TELA 8 - PARANDO EXECUÇÃO**")
            return
        
        # Tela 9: Endereço pernoite
        if tela9_endereco_pernoite(driver):
            telas_executadas.append("Tela 9: Endereço preenchido")
        else:
            print("❌ **FALHA NA TELA 9 - PARANDO EXECUÇÃO**")
            return
        
        # Resumo final
        print(f"\n{'='*80}")
        print("🎉 **RPA EXECUTADO COM SUCESSO!**")
        print(f"{'='*80}")
        print(f"✅ Total de telas executadas: {len(telas_executadas)}")
        for tela in telas_executadas:
            print(f"   ✅ {tela}")
        print(f"\n📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"⏰ Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
        if driver:
            driver.save_screenshot("/opt/imediatoseguros-rpa/temp/erro-geral.png")
            print(" Screenshot do erro geral salvo")
    
    finally:
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    main()
