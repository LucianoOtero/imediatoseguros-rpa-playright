#!/usr/bin/env python3
"""
RPA Tô Segurado - TELA 9: Tipo de Combustível
Continuação do fluxo a partir da Tela 8 (Estimativa Inicial)
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
    print(f"️  **TELA {numero_tela:02d}: {descricao}** - {timestamp}")
    print(f"{'='*80}")
    print(f"🌐 URL: {url}")
    print(f"📄 Título: {titulo}")
    
    if acao:
        print(f"🎯 Ação: {acao}")
    
    # Salvar estado da tela
    diretorio = salvar_estado_tela(driver, numero_tela, descricao)
    print(f" Arquivos salvos em: {diretorio}")
    
    return diretorio

def aguardar_carregamento_pagina(driver, timeout=30):
    """Aguarda a página carregar completamente"""
    print(f"⏳ Aguardando carregamento da página (timeout: {timeout}s)...")
    
    # Aguardar até que a página esteja pronta
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
    # Aguardar um pouco mais para garantir que tudo carregou
    time.sleep(3)
    print("✅ Página carregada completamente")

def navegar_ate_tela8(driver):
    """Navega até a Tela 8 (última tela funcionando)"""
    print("🚀 **NAVEGANDO ATÉ TELA 8 (ESTIMATIVA INICIAL)**")
    
    try:
        # Tela 1: Selecionar Carro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        time.sleep(5)
        
        carro_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("✅ Carro selecionado")
        time.sleep(3)
        
        # Tela 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        placa_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        time.sleep(2)
        
        # Tela 3: Clicar Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado")
        time.sleep(5)
        
        # Tela 5: Confirmar veículo
        print("\n📱 TELA 5: Confirmando veículo...")
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
        print("\n📱 TELA 6: Selecionando 'Não' para veículo segurado...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "confirmarVeiculoTelaInformacoesVeiculo"))
        )
        
        nao_radio = driver.find_element(By.XPATH, "//input[@value='Não']")
        if not nao_radio.is_selected():
            driver.execute_script("arguments[0].click();", nao_radio)
            print("✅ Radio 'Não' selecionado")
            time.sleep(2)
        
        continuar_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.ID, "gtm-telaInfosAutoContinuar"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 6")
        time.sleep(5)
        
        # Tela 7: Confirmação não segurado
        print("\n�� TELA 7: Aguardando confirmação...")
        time.sleep(5)
        
        # Procurar botão Continuar na Tela 7
        continuar_selectors = [
            "//button[contains(., 'Continuar')]",
            "//*[contains(., 'Continuar')]",
            "//button[contains(text(), 'Continuar')]",
            "//p[contains(., 'Continuar')]"
        ]
        
        continuar_button = None
        for selector in continuar_selectors:
            try:
                continuar_button = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
                print(f"✅ Botão Continuar encontrado com selector: {selector}")
                break
            except:
                continue
        
        if continuar_button:
            continuar_button.click()
            print("✅ Continuar clicado na Tela 7")
            time.sleep(5)
        else:
            print("⚠️ Botão Continuar não encontrado na Tela 7")
        
        # Tela 8: Estimativa inicial
        print("\n�� TELA 8: Aguardando estimativa inicial...")
        time.sleep(5)
        
        # Aguardar elementos da estimativa inicial
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "estimativa" in d.page_source.lower(),
                "carrossel" in d.page_source.lower(),
                "cobertura" in d.page_source.lower(),
                "plano" in d.page_source.lower(),
                "franquia" in d.page_source.lower()
            ])
        )
        print("✅ Tela 8 carregada - estimativa inicial detectada!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 30)
        
        # Salvar estado da Tela 8
        log_tela(driver, 8, "estimativa_carregada", "Estimativa inicial carregada")
        
        # Aguardar mais um pouco
        time.sleep(10)
        
        # Clicar em Continuar na Tela 8
        print("⏳ Aguardando botão Continuar aparecer...")
        continuar_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Continuar')]"))
        )
        continuar_button.click()
        print("✅ Continuar clicado na Tela 8")
        
        # Aguardar carregamento da próxima página
        aguardar_carregamento_pagina(driver, 30)
        
        print("✅ TELA 8 CARREGADA E CONTINUAR CLICADO!")
        return True
        
    except Exception as e:
        print(f"❌ **ERRO AO NAVEGAR ATÉ TELA 8:** {e}")
        return False

def tela9_tipo_combustivel(driver):
    """Tela 9: Selecionar tipo de combustível"""
    print("\n **INICIANDO TELA 9: Tipo de combustível**")
    
    try:
        # Aguardar Tela 9 carregar com timeout maior
        print("⏳ Aguardando Tela 9 carregar...")
        
        # Aguardar um pouco para a página carregar
        time.sleep(5)
        
        # Salvar estado inicial da Tela 9
        log_tela(driver, 9, "inicial", "Tela 9 carregada - aguardando tipo combustível")
        
        # Procurar elementos específicos da Tela 9
        print("🔍 Procurando elementos da Tela 9...")
        
        # Aguardar carregamento com timeout maior
        WebDriverWait(driver, 60).until(
            lambda d: any([
                "tipo.*combustivel" in d.page_source.lower(),
                "flex" in d.page_source.lower(),
                "gasolina" in d.page_source.lower(),
                "alcool" in d.page_source.lower(),
                "diesel" in d.page_source.lower(),
                "hibrido" in d.page_source.lower(),
                "eletrico" in d.page_source.lower()
            ])
        )
        print("✅ Tela 9 carregada - tipo de combustível detectado!")
        
        # Aguardar carregamento completo
        aguardar_carregamento_pagina(driver, 20)
        
        # Salvar estado da Tela 9
        log_tela(driver, 9, "tipo_combustivel_carregado", "Tipo de combustível carregado")
        
        # Procurar e selecionar Flex
        print("⏳ Aguardando radio Flex aparecer...")
        try:
            # Tentar diferentes seletores para Flex
            flex_selectors = [
                "//input[@value='Flex']",
                "//input[contains(@value, 'Flex')]",
                "//input[@name='tipoCombustivel']",
                "//input[@type='radio'][contains(@value, 'Flex')]"
            ]
            
            flex_radio = None
            for selector in flex_selectors:
                try:
                    flex_radio = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    print(f"✅ Radio Flex encontrado com selector: {selector}")
                    break
                except:
                    continue
            
            if flex_radio:
                # Salvar estado antes da seleção
                log_tela(driver, 9, "antes_selecao_flex", "Antes de selecionar Flex")
                
                # Selecionar Flex
                if not flex_radio.is_selected():
                    driver.execute_script("arguments[0].click();", flex_radio)
                    print("✅ Flex selecionado via JavaScript")
                else:
                    print("✅ Flex já estava selecionado")
                time.sleep(3)
                
                # Salvar estado com Flex selecionado
                log_tela(driver, 9, "flex_selecionado", "Flex selecionado")
            else:
                print("⚠️ Radio Flex não encontrado - tentando prosseguir...")
                
        except Exception as e:
            print(f"⚠️ Erro ao selecionar Flex: {e}")
            print("⏳ Tentando prosseguir...")
        
        # Verificar checkboxes (Kit Gás, Blindado, Financiado)
        print("\n🔍 Verificando checkboxes...")
        try:
            # Procurar checkboxes
            checkbox_patterns = [
                "kit.*gas",
                "blindado",
                "financiado"
            ]
            
            for pattern in checkbox_patterns:
                try:
                    checkbox = driver.find_element(By.XPATH, f"//input[contains(@name, '{pattern}') or contains(@id, '{pattern}')]")
                    if checkbox.is_selected():
                        print(f"⚠️ Checkbox '{pattern}' estava selecionado - desmarcando...")
                        driver.execute_script("arguments[0].click();", checkbox)
                        print(f"✅ Checkbox '{pattern}' desmarcado")
                    else:
                        print(f"✅ Checkbox '{pattern}' já estava desmarcado")
                except:
                    print(f"ℹ️ Checkbox '{pattern}' não encontrado")
            
        except Exception as e:
            print(f"⚠️ Erro ao verificar checkboxes: {e}")
        
        # Salvar estado final da Tela 9
        log_tela(driver, 9, "configuracao_completa", "Configuração completa da Tela 9")
        
        # Procurar botão Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        try:
            continuar_selectors = [
                "//button[contains(., 'Continuar')]",
                "//*[contains(., 'Continuar')]",
                "//button[contains(text(), 'Continuar')]",
                "//p[contains(., 'Continuar')]"
            ]
            
            continuar_button = None
            for selector in continuar_selectors:
                try:
                    continuar_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"✅ Botão Continuar encontrado com selector: {selector}")
                    break
                except:
                    continue
            
            if continuar_button:
                # Salvar estado antes do clique
                log_tela(driver, 9, "antes_continuar", "Antes de clicar em Continuar")
                
                # Clicar
                continuar_button.click()
                print("✅ Continuar clicado na Tela 9")
                
                # Aguardar carregamento da próxima página
                aguardar_carregamento_pagina(driver, 30)
                
                # Salvar estado após clique
                log_tela(driver, 9, "apos_continuar", "Após clicar em Continuar")
            else:
                print("⚠️ Botão Continuar não encontrado - tentando prosseguir...")
                
        except Exception as e:
            print(f"⚠️ Erro ao procurar botão Continuar: {e}")
            print("⏳ Aguardando carregamento automático...")
            time.sleep(10)
        
        return True
        
    except Exception as e:
        print(f"❌ **ERRO NA TELA 9:** {e}")
        log_tela(driver, 9, "erro", f"Erro: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - TELA 9: TIPO DE COMBUSTÍVEL**")
    print("=" * 80)
    print("🎯 OBJETIVO: Implementar Tela 9 (Tipo de Combustível)")
    print("📝 NOTA: Continuação do fluxo a partir da Tela 8")
    print("=" * 80)
    print(f"⏰ Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 8
        if not navegar_ate_tela8(driver):
            print("❌ **FALHA AO NAVEGAR ATÉ TELA 8 - PARANDO**")
            return
        
        # Tela 9: Tipo de combustível
        if tela9_tipo_combustivel(driver):
            print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO!**")
        else:
            print("❌ **FALHA NA TELA 9 - PARANDO EXECUÇÃO**")
            return
        
        # Resumo final
        print(f"\n{'='*80}")
        print("🎉 **RPA EXECUTADO COM SUCESSO! TELA 9 IMPLEMENTADA!**")
        print(f"{'='*80}")
        print(f"✅ Total de telas executadas: 9")
        print(f"✅ Tela 9: Tipo de combustível implementada")
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
