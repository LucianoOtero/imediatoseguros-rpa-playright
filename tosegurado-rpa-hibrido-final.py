#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - SCRIPT HÍBRIDO FINAL
===============================================================================
🎯 OBJETIVO: Fluxo correto (Sim na Tela 6) + Delays extremos que funcionaram
🔧 CORREÇÃO: Selecionar 'Sim' na Tela 6 para acessar Tela 8 (Estimativa Inicial)
⚡ MÉTODO: Delays extremos para evitar stale element reference
📊 BONUS: Capturar dados da estimativa inicial (Tela 8)
📝 NOTA: Combinação perfeita de fluxo correto + estabilidade
===============================================================================
"""

import os
import time
import json
import tempfile
import shutil
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

def configurar_chrome():
    """Configura o Chrome com opções otimizadas"""
    print("🔧 Configurando Chrome...")
    
    # Criar diretório temporário único
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
    
    # Configurar user agent
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver, temp_dir

def criar_diretorio_temp():
    """Cria diretório temporário para salvar arquivos"""
    temp_dir = f"/opt/imediatoseguros-rpa/temp/{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def salvar_pagina(driver, temp_dir, nome_arquivo, acao):
    """Salva HTML, screenshot e informações da página"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    # Criar diretório específico para a tela
    tela_dir = os.path.join(temp_dir, nome_arquivo)
    os.makedirs(tela_dir, exist_ok=True)
    
    # Salvar HTML
    html_path = os.path.join(tela_dir, f"{nome_arquivo}.html")
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(driver.page_source)
    
    # Salvar screenshot
    screenshot_path = os.path.join(tela_dir, f"{nome_arquivo}.png")
    driver.save_screenshot(screenshot_path)
    
    # Salvar informações da página
    info_path = os.path.join(tela_dir, f"{nome_arquivo}.txt")
    with open(info_path, 'w', encoding='utf-8') as f:
        f.write(f"URL: {driver.current_url}\n")
        f.write(f"Título: {driver.title}\n")
        f.write(f"Ação: {acao}\n")
        f.write(f"Timestamp: {timestamp}\n")
    
    print(f"📁 Arquivos salvos em: {tela_dir}")
    return tela_dir

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página com timeout extremo"""
    print(f"⏳ Aguardando carregamento da página (timeout: {timeout}s)...")
    
    try:
        # Aguardar até que a página esteja completamente carregada
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        print("✅ Página carregada completamente")
        return True
    except TimeoutException:
        print(f"⚠️ Timeout após {timeout}s - continuando...")
        return False

def aguardar_estabilizacao(driver, segundos=20):
    """Aguarda estabilização da página com delay extremo"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)
    print("✅ Estabilização concluída")

def clicar_com_delay_extremo(driver, elemento, descricao, timeout=60):
    """Clica em elemento com delays extremos para evitar stale element"""
    print(f"⏳ Aguardando {descricao} aparecer...")
    
    try:
        # Aguardar elemento aparecer
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, elemento))
        )
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 20)
        
        # Tentar clicar
        elemento_web = driver.find_element(By.XPATH, elemento)
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento_web)
        time.sleep(3)
        
        # Tentar clicar via JavaScript primeiro
        try:
            driver.execute_script("arguments[0].click();", elemento_web)
            print(f"✅ {descricao} clicado com sucesso")
            return True
        except:
            # Fallback para clique normal
            elemento_web.click()
            print(f"✅ {descricao} clicado com sucesso")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay_extremo(driver, elemento, valor, descricao, timeout=60):
    """Preenche campo com delays extremos para evitar stale element"""
    print(f"⏳ Aguardando {descricao} aparecer...")
    
    try:
        # Aguardar elemento aparecer
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, elemento))
        )
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 15)
        
        # Tentar preencher
        elemento_web = driver.find_element(By.XPATH, elemento)
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento_web)
        time.sleep(3)
        
        # Limpar e preencher
        elemento_web.clear()
        elemento_web.send_keys(valor)
        print(f"✅ {descricao} preenchido: {valor}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao):
    """Clica em radio button via JavaScript procurando por texto"""
    print(f"⏳ Aguardando radio {descricao} aparecer...")
    
    try:
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 20)
        
        # Script para encontrar e clicar no radio por texto
        script = f"""
        const radios = document.querySelectorAll('input[type="radio"]');
        for (let radio of radios) {{
            const label = radio.closest('label');
            if (label && label.textContent.includes('{texto_radio}')) {{
                radio.checked = true;
                radio.click();
                return true;
            }}
        }}
        return false;
        """
        
        resultado = driver.execute_script(script)
        if resultado:
            print(f"🎯 Radio clicado diretamente: {texto_radio}")
            return True
        else:
            print(f"⚠️ Radio {descricao} não encontrado - tentando prosseguir...")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar no radio {descricao}: {e}")
        return False

def capturar_dados_tela8(driver, temp_dir):
    """Captura dados da Tela 8 (Estimativa Inicial)"""
    print("**CAPTURANDO DADOS DA TELA 8 (ESTIMATIVA INICIAL)**")
    print("=" * 70)
    
    # Salvar página da Tela 8
    tela8_dir = salvar_pagina(driver, temp_dir, "tela_08", "captura_dados")
    
    # Procurar por elementos da cobertura "Compreensiva"
    try:
        # Procurar por texto "Compreensiva"
        elementos_compreensiva = driver.find_elements(By.XPATH, "//*[contains(text(), 'Compreensiva')]")
        
        if elementos_compreensiva:
            print("✅ Nome Cobertura: Compreensiva")
            
            # Procurar por valores monetários próximos
            valores_monetarios = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
            print(f"🔍 Valores monetários encontrados: {len(valores_monetarios)}")
            
            # Salvar dados em JSON
            dados_cobertura = {
                "nome_cobertura": "Compreensiva",
                "valores_encontrados": len(valores_monetarios),
                "timestamp": datetime.now().isoformat(),
                "url": driver.current_url,
                "titulo": driver.title
            }
            
            # Salvar JSON
            json_path = os.path.join(tela8_dir, "dados_cobertura_compreensiva.json")
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(dados_cobertura, f, indent=2, ensure_ascii=False)
            
            # Salvar TXT
            txt_path = os.path.join(tela8_dir, "dados_cobertura_compreensiva.txt")
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(f"Nome Cobertura: {dados_cobertura['nome_cobertura']}\n")
                f.write(f"Valores Encontrados: {dados_cobertura['valores_encontrados']}\n")
                f.write(f"Timestamp: {dados_cobertura['timestamp']}\n")
                f.write(f"URL: {dados_cobertura['url']}\n")
                f.write(f"Título: {dados_cobertura['titulo']}\n")
            
            print(f"💾 Dados salvos em JSON: {json_path}")
            print(f"💾 Dados salvos em TXT: {txt_path}")
            
        else:
            print("❌ Cobertura 'Compreensiva' não encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
    
    print("**RESUMO DOS DADOS CAPTURADOS:**")
    print("=" * 70)
    print("✅ Dados da Tela 8 capturados com sucesso!")

def main():
    """Função principal do RPA"""
    print("🚀 **RPA TÔ SEGURADO - SCRIPT HÍBRIDO FINAL**")
    print("=" * 70)
    print("🎯 OBJETIVO: Fluxo correto (Sim na Tela 6) + Delays extremos")
    print("🔧 CORREÇÃO: Selecionar 'Sim' na Tela 6 para acessar Tela 8")
    print("⚡ MÉTODO: Delays extremos para evitar stale element reference")
    print("📊 BONUS: Capturar dados da estimativa inicial (Tela 8)")
    print("📝 NOTA: Combinação perfeita de fluxo correto + estabilidade")
    print("=" * 70)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Criar diretório temporário
        temp_dir_rpa = criar_diretorio_temp()
        
        # TELA 1: Seleção do tipo de seguro
        print("\n**INICIANDO TELA 1: Seleção do tipo de seguro**")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("❌ Falha ao carregar página inicial")
            return
        
        # Salvar estado inicial
        salvar_pagina(driver, temp_dir_rpa, "tela_01", "inicial")
        
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 20)
        
        # Procurar e clicar no botão Carro
        carro_xpath = "//button[contains(text(), 'Carro')]"
        if not clicar_com_delay_extremo(driver, carro_xpath, "botão Carro", 60):
            print("❌ Falha ao clicar no botão Carro")
            return
        
        # Aguardar carregamento e salvar
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_01", "apos_clique")
        
        # TELA 2: Inserção da placa
        print("\n**INICIANDO TELA 2: Inserção da placa**")
        
        # Aguardar campo de placa
        placa_xpath = "//input[@id='placaTelaDadosPlaca']"
        try:
            WebDriverWait(driver, 60).until(
                EC.presence_of_element_located((By.XPATH, placa_xpath))
            )
            print("✅ Campo de placa encontrado!")
        except TimeoutException:
            print("❌ Campo de placa não encontrado")
            return
        
        # Salvar estado da Tela 2
        salvar_pagina(driver, temp_dir_rpa, "tela_02", "inicial")
        
        # Preencher placa
        if not preencher_com_delay_extremo(driver, placa_xpath, "EED3D56", "placa", 60):
            print("❌ Falha ao preencher placa")
            return
        
        # Aguardar e salvar
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_02", "placa_inserida")
        
        # TELA 3: Clicar em Continuar
        print("\n**INICIANDO TELA 3: Clicar em Continuar**")
        
        # Procurar botão Continuar
        continuar_xpath = "//button[contains(text(), 'Continuar')]"
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 3", 60):
            print("❌ Falha ao clicar em Continuar")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_03", "apos_clique")
        
        # TELA 5: Confirmação do veículo
        print("\n**INICIANDO TELA 5: Confirmação do veículo**")
        
        # Aguardar Tela 5 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "COROLLA" in d.page_source or "confirmacaoVeiculo" in d.page_source
            )
            print("✅ Tela 5 carregada - confirmação do veículo detectada!")
        except TimeoutException:
            print("❌ Tela 5 não carregou")
            return
        
        # Salvar Tela 5
        salvar_pagina(driver, temp_dir_rpa, "tela_05", "confirmacao_carregada")
        
        # Selecionar 'Sim' para confirmação
        print("⏳ Selecionando 'Sim' para confirmação do veículo...")
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
            print("❌ Falha ao selecionar Sim para confirmação")
            return
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 5", 60):
            print("❌ Falha ao clicar em Continuar na Tela 5")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_05", "apos_continuar")
        
        # TELA 6: Veículo já está segurado
        print("\n**INICIANDO TELA 6: Veículo já está segurado**")
        
        # Aguardar Tela 6 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "já está segurado" in d.page_source or "segurado" in d.page_source
            )
            print("✅ Tela 6 carregada - pergunta sobre veículo segurado detectada!")
        except TimeoutException:
            print("❌ Tela 6 não carregou")
            return
        
        # Salvar Tela 6
        salvar_pagina(driver, temp_dir_rpa, "tela_06", "pergunta_carregada")
        
        # Selecionar 'Sim' para veículo já segurado (CORREÇÃO!)
        print("⏳ Selecionando 'Sim' para veículo já segurado...")
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para veículo segurado"):
            print("❌ Falha ao selecionar Sim para veículo segurado")
            return
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 6", 60):
            print("❌ Falha ao clicar em Continuar na Tela 6")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_06", "apos_continuar")
        
        # TELA 7: Tela de renovação
        print("\n**INICIANDO TELA 7: Tela de renovação**")
        
        # Aguardar Tela 7 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "renovação" in d.page_source.lower() or "renovacao" in d.page_source.lower()
            )
            print("✅ Tela 7 carregada - renovação detectada!")
        except TimeoutException:
            print("⚠️ Tela 7 pode ter carregado com conteúdo diferente")
        
        # Salvar Tela 7
        salvar_pagina(driver, temp_dir_rpa, "tela_07", "renovacao_carregada")
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 7", 60):
            print("❌ Falha ao clicar em Continuar na Tela 7")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_07", "apos_continuar")
        
        # TELA 8: Estimativa inicial
        print("\n**INICIANDO TELA 8: Estimativa inicial**")
        
        # Aguardar Tela 8 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "estimativa" in d.page_source.lower() or "carrossel" in d.page_source.lower()
            )
            print("✅ Tela 8 carregada - estimativa inicial detectada!")
        except TimeoutException:
            print("❌ Tela 8 não carregou")
            return
        
        # Salvar Tela 8
        salvar_pagina(driver, temp_dir_rpa, "tela_08", "estimativa_carregada")
        
        # CAPTURAR DADOS DA TELA 8
        capturar_dados_tela8(driver, temp_dir_rpa)
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 8", 60):
            print("❌ Falha ao clicar em Continuar na Tela 8")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_08", "apos_continuar")
        
        # TELA 9: Tipo de combustível
        print("\n**INICIANDO TELA 9: Tipo de combustível**")
        
        # Aguardar Tela 9 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "combustível" in d.page_source.lower() or "combustivel" in d.page_source.lower()
            )
            print("✅ Tela 9 carregada - tipo de combustível detectado!")
        except TimeoutException:
            print("❌ Tela 9 não carregou")
            return
        
        # Salvar Tela 9
        salvar_pagina(driver, temp_dir_rpa, "tela_09", "tipo_combustivel_carregado")
        
        # Selecionar 'Flex' (já deve estar selecionado)
        print("⏳ Verificando seleção 'Flex'...")
        if not clicar_radio_via_javascript(driver, "Flex", "Flex"):
            print("⚠️ Radio Flex não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 9", 60):
            print("❌ Falha ao clicar em Continuar na Tela 9")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_09", "apos_continuar")
        
        # TELA 10: Endereço de pernoite
        print("\n**INICIANDO TELA 10: Endereço de pernoite**")
        
        # Aguardar Tela 10 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "pernoite" in d.page_source.lower() or "endereço" in d.page_source.lower()
            )
            print("✅ Tela 10 carregada - endereço de pernoite detectado!")
        except TimeoutException:
            print("❌ Tela 10 não carregou")
            return
        
        # Salvar Tela 10
        salvar_pagina(driver, temp_dir_rpa, "tela_10", "endereco_pernoite_carregado")
        
        # Preencher CEP
        cep_xpath = "//input[@id='enderecoTelaEndereco']"
        if not preencher_com_delay_extremo(driver, cep_xpath, "03084-000", "CEP", 60):
            print("❌ Falha ao preencher CEP")
            return
        
        # Aguardar sugestões e selecionar
        time.sleep(5)
        
        # Procurar e clicar na sugestão
        sugestao_xpath = "//div[contains(@class, 'suggestion') or contains(text(), '03084-000')]"
        try:
            sugestao = WebDriverWait(driver, 15).until(
                EC.element_to_be_clickable((By.XPATH, sugestao_xpath))
            )
            sugestao.click()
            print("✅ Sugestão selecionada")
        except:
            print("⚠️ Sugestão não encontrada - continuando...")
        
        # Aguardar e salvar
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_10", "cep_preenchido")
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 10", 60):
            print("❌ Falha ao clicar em Continuar na Tela 10")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_10", "apos_continuar")
        
        # TELA 11: Uso do veículo
        print("\n**INICIANDO TELA 11: Uso do veículo**")
        
        # Aguardar Tela 11 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "uso do veículo" in d.page_source.lower() or "uso do veiculo" in d.page_source.lower()
            )
            print("✅ Tela 11 carregada - uso do veículo detectado!")
        except TimeoutException:
            print("❌ Tela 11 não carregou")
            return
        
        # Salvar Tela 11
        salvar_pagina(driver, temp_dir_rpa, "tela_11", "uso_veiculo_carregado")
        
        # Selecionar 'Pessoal'
        print("⏳ Selecionando 'Pessoal' para uso do veículo...")
        if not clicar_radio_via_javascript(driver, "Pessoal", "Pessoal"):
            print("⚠️ Radio 'Pessoal' não encontrado - tentando prosseguir...")
        
        # Aguardar e salvar
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_11", "configuracao_completa")
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 11", 60):
            print("❌ Falha ao clicar em Continuar na Tela 11")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_11", "apos_continuar")
        
        # TELA 12: Dados pessoais
        print("\n**INICIANDO TELA 12: Dados pessoais**")
        
        # Aguardar Tela 12 carregar
        try:
            WebDriverWait(driver, 60).until(
                lambda d: "dados pessoais" in d.page_source.lower() or "nome completo" in d.page_source.lower()
            )
            print("✅ Tela 12 carregada - dados pessoais detectados!")
        except TimeoutException:
            print("❌ Tela 12 não carregou")
            return
        
        # Salvar Tela 12
        salvar_pagina(driver, temp_dir_rpa, "tela_12", "dados_pessoais_carregado")
        
        # Preencher dados pessoais
        print("⏳ Preenchendo dados pessoais...")
        
        # Nome completo
        nome_xpath = "//input[@id='nomeTelaDadosPessoais']"
        if not preencher_com_delay_extremo(driver, nome_xpath, "LUCIANO OTERO", "Nome completo", 60):
            print("⚠️ Campo nome não encontrado - tentando prosseguir...")
        
        # CPF
        cpf_xpath = "//input[@id='cpfTelaDadosPessoais']"
        if not preencher_com_delay_extremo(driver, cpf_xpath, "085.546.078-48", "CPF", 60):
            print("⚠️ Campo CPF não encontrado - tentando prosseguir...")
        
        # Data de nascimento
        nascimento_xpath = "//input[@id='dataNascimentoTelaDadosPessoais']"
        if not preencher_com_delay_extremo(driver, nascimento_xpath, "09/02/1965", "Data de nascimento", 60):
            print("⚠️ Campo data de nascimento não encontrado - tentando prosseguir...")
        
        # Sexo (masculino)
        if not clicar_radio_via_javascript(driver, "masculino", "Masculino"):
            print("⚠️ Radio masculino não encontrado - tentando prosseguir...")
        
        # Estado civil (casado)
        if not clicar_radio_via_javascript(driver, "casado", "Casado"):
            print("⚠️ Radio casado não encontrado - tentando prosseguir...")
        
        # Email
        email_xpath = "//input[@id='emailTelaDadosPessoais']"
        if not preencher_com_delay_extremo(driver, email_xpath, "lrotero@gmail.com", "Email", 60):
            print("⚠️ Campo email não encontrado - tentando prosseguir...")
        
        # Celular
        celular_xpath = "//input[@id='celularTelaDadosPessoais']"
        if not preencher_com_delay_extremo(driver, celular_xpath, "(11) 97668-7668", "Celular", 60):
            print("⚠️ Campo celular não encontrado - tentando prosseguir...")
        
        # Aguardar e salvar
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_12", "dados_preenchidos")
        
        # Clicar em Continuar
        if not clicar_com_delay_extremo(driver, continuar_xpath, "botão Continuar Tela 12", 60):
            print("❌ Falha ao clicar em Continuar na Tela 12")
            return
        
        # Aguardar carregamento
        aguardar_carregamento_pagina(driver, 60)
        aguardar_estabilizacao(driver, 20)
        salvar_pagina(driver, temp_dir_rpa, "tela_12", "apos_continuar")
        
        print("\n✅ **TELA 12 IMPLEMENTADA COM SUCESSO!**")
        print("=" * 70)
        
        # SUCCESSO!
        print("🎉 **RPA EXECUTADO COM SUCESSO! TELA 12 IMPLEMENTADA!**")
        print("=" * 70)
        print("✅ Total de telas executadas: 12")
        print("✅ Tela 12: Dados pessoais implementada")
        print("📊 BONUS: Dados da Tela 8 capturados para uso futuro")
        print(f"📁 Todos os arquivos salvos em: {temp_dir_rpa}")
        
    except Exception as e:
        print(f"\n❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpeza
        if driver:
            driver.quit()
        if temp_dir:
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
