#!/usr/bin/env python3
"""
Investigação Específica da Tela 8 - Estimativa Inicial
Para entender por que está falhando
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

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def aguardar_estabilizacao(driver, segundos=15):
    """Aguarda a estabilização da página"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)

def clicar_com_delay_extremo(driver, by, value, descricao="elemento", timeout=30):
    """Clica em um elemento com delay extremo"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 15)
        
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio"):
    """Clica em um radio button via JavaScript"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        aguardar_estabilizacao(driver, 15)
        
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
            radioEncontrado.click();
            return 'Radio clicado: ' + radioEncontrado.outerHTML.substring(0, 100);
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

def navegar_ate_tela7(driver):
    """Navega o RPA até a Tela 7 usando o método que funcionou"""
    print("🚀 **NAVEGANDO ATÉ TELA 7 - MÉTODO FUNCIONANDO**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    aguardar_estabilizacao(driver, 20)
    
    # Clicar no botão Carro
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    time.sleep(10)
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    aguardar_estabilizacao(driver, 20)
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # Preencher placa
    try:
        placa_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        aguardar_estabilizacao(driver, 10)
        
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("✅ Placa EED3D56 inserida")
        
        aguardar_estabilizacao(driver, 15)
        salvar_estado_tela(driver, 2, "placa_inserida", None)
        
    except Exception as e:
        print(f"❌ Erro ao inserir placa: {e}")
        return False
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    time.sleep(15)
    if not aguardar_carregamento_pagina(driver, 60):
        print("⚠️ Página pode não ter carregado completamente")
    
    aguardar_estabilizacao(driver, 20)
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    # TELA 5: Confirmação do veículo
    print("\n📱 TELA 5: Confirmando veículo...")
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'COROLLA')]"))
        )
        print("✅ Tela 5 carregada - confirmação do veículo detectada!")
        
        salvar_estado_tela(driver, 5, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 5, "confirmacao_carregada", None)
        
        # Selecionar "Sim" para confirmação do veículo
        print("⏳ Selecionando 'Sim' para confirmação do veículo...")
        
        if not clicar_radio_via_javascript(driver, "Sim", "Sim para confirmação"):
            print("⚠️ Radio 'Sim' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 5"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 5")
            return False
        
        time.sleep(15)
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO!**")
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False
    
    # TELA 6: Pergunta se veículo já está segurado
    print("\n📱 TELA 6: Selecionando 'Não' para veículo segurado...")
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 6 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "pergunta_carregada", None)
        
        # Selecionar "Não" para veículo já segurado
        print("⏳ Selecionando 'Não' para veículo já segurado...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        time.sleep(15)
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO!**")
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False
    
    # TELA 7: Confirmação que veículo não está segurado
    print("\n TELA 7: Aguardando confirmação...")
    
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        print("✅ Tela 7 carregada - confirmação detectada!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "confirmacao_carregada", None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        time.sleep(15)
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO!**")
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False
    
    return True

def investigar_tela8(driver):
    """Investiga especificamente a Tela 8"""
    print("\n **INVESTIGANDO TELA 8: Estimativa inicial**")
    
    # Aguardar Tela 8 carregar com timeout muito maior
    print("⏳ Aguardando Tela 8 carregar (timeout: 60s)...")
    
    try:
        # Tentar diferentes elementos da Tela 8
        elementos_detectados = []
        
        # Aguardar muito mais tempo
        time.sleep(30)
        
        # Verificar se a página mudou
        print(f" URL Atual: {driver.current_url}")
        print(f"📄 Título Atual: {driver.title}")
        
        # Salvar estado atual
        salvar_estado_tela(driver, 8, "investigacao", None)
        
        # Procurar por diferentes elementos
        print("\n🔍 **PROCURANDO ELEMENTOS DA TELA 8:**")
        
        # Procurar por estimativa
        try:
            estimativa_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'Estimativa')]")
            print(f"✅ Elementos 'estimativa': {len(estimativa_elements)}")
            if estimativa_elements:
                elementos_detectados.append("estimativa")
        except:
            print("❌ Erro ao procurar 'estimativa'")
        
        # Procurar por inicial
        try:
            inicial_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'inicial') or contains(text(), 'Inicial')]")
            print(f"✅ Elementos 'inicial': {len(inicial_elements)}")
            if inicial_elements:
                elementos_detectados.append("inicial")
        except:
            print("❌ Erro ao procurar 'inicial'")
        
        # Procurar por carrossel
        try:
            carrossel_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'carrossel') or contains(text(), 'Carrossel')]")
            print(f"✅ Elementos 'carrossel': {len(carrossel_elements)}")
            if carrossel_elements:
                elementos_detectados.append("carrossel")
        except:
            print("❌ Erro ao procurar 'carrossel'")
        
        # Procurar por cobertura
        try:
            cobertura_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'cobertura') or contains(text(), 'Cobertura')]")
            print(f"✅ Elementos 'cobertura': {len(cobertura_elements)}")
            if cobertura_elements:
                elementos_detectados.append("cobertura")
        except:
            print("❌ Erro ao procurar 'cobertura'")
        
        # Procurar por loading/carregando
        try:
            loading_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'carregando') or contains(text(), 'Carregando') or contains(text(), 'loading') or contains(text(), 'Loading') or contains(text(), 'aguarde') or contains(text(), 'Aguarde')]")
            print(f"⏳ Elementos de loading: {len(loading_elements)}")
            if loading_elements:
                elementos_detectados.append("loading")
                for i, elem in enumerate(loading_elements):
                    print(f"   Loading {i+1}: {elem.text[:100]}...")
        except:
            print("❌ Erro ao procurar elementos de loading")
        
        # Procurar por botões Continuar
        try:
            continuar_elements = driver.find_elements(By.XPATH, "//button[contains(., 'Continuar')]")
            print(f"✅ Botões 'Continuar': {len(continuar_elements)}")
            if continuar_elements:
                elementos_detectados.append("continuar")
                for i, elem in enumerate(continuar_elements):
                    print(f"   Botão {i+1}: {elem.get_attribute('outerHTML')[:200]}...")
        except:
            print("❌ Erro ao procurar botões 'Continuar'")
        
        print(f"\n **ELEMENTOS DETECTADOS: {', '.join(elementos_detectados) if elementos_detectados else 'Nenhum'}")
        
        if "loading" in elementos_detectados:
            print("⏳ **TELA 8 ESTÁ CARREGANDO - AGUARDANDO MAIS TEMPO...**")
            time.sleep(30)
            
            # Salvar estado após aguardar mais
            salvar_estado_tela(driver, 8, "apos_aguardar_mais", None)
            
            # Verificar novamente
            print("🔍 **VERIFICANDO NOVAMENTE APÓS AGUARDAR MAIS...**")
            
            # Procurar por elementos novamente
            try:
                estimativa_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'Estimativa')]")
                print(f"✅ Elementos 'estimativa' após aguardar: {len(estimativa_elements)}")
                
                carrossel_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'carrossel') or contains(text(), 'Carrossel')]")
                print(f"✅ Elementos 'carrossel' após aguardar: {len(carrossel_elements)}")
                
                if estimativa_elements or carrossel_elements:
                    print("🎉 **TELA 8 CARREGOU APÓS AGUARDAR MAIS TEMPO!**")
                    return True
                else:
                    print("❌ **TELA 8 AINDA NÃO CARREGOU**")
                    return False
                    
            except Exception as e:
                print(f"❌ Erro ao verificar novamente: {e}")
                return False
        
        elif "estimativa" in elementos_detectados or "carrossel" in elementos_detectados:
            print("🎉 **TELA 8 CARREGOU COM SUCESSO!**")
            return True
        else:
            print("❌ **TELA 8 NÃO CARREGOU - ELEMENTOS NÃO ENCONTRADOS**")
            return False
        
    except Exception as e:
        print(f"❌ Erro na investigação da Tela 8: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - INVESTIGAÇÃO TELA 8**")
    print("=" * 60)
    print(" OBJETIVO: Investigar especificamente a Tela 8")
    print("🔧 MÉTODO: Delays extremos + investigação detalhada")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 7
        if not navegar_ate_tela7(driver):
            print("❌ Erro: Falha ao navegar até Tela 7")
            return
        
        # Investigar Tela 8
        if investigar_tela8(driver):
            print("\n **INVESTIGAÇÃO TELA 8 CONCLUÍDA COM SUCESSO!**")
        else:
            print("\n❌ **FALHA NA INVESTIGAÇÃO TELA 8**")
    
    except Exception as e:
        print(f"❌ **ERRO GERAL DURANTE EXECUÇÃO:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")
        
        fim = datetime.now()
        print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
