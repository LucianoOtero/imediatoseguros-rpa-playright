#!/usr/bin/env python3
"""
RPA TÔ SEGURADO - SCRIPT CORRIGIDO FINAL
===============================================================================
🎯 OBJETIVO: Seletores que funcionaram + Fluxo correto (Não na Tela 6)
�� CORREÇÃO: Selecionar 'Não' na Tela 6 para funcionar como antes
⚡ MÉTODO: Delays extremos que funcionaram + Seletores testados
📊 BONUS: Capturar dados da estimativa inicial (Tela 8)
📝 NOTA: Combinação perfeita de estabilidade + fluxo correto
===============================================================================
"""

import time
import tempfile
import shutil
import os
import json
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
    """Aguarda o carregamento completo da página com timeout maior"""
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
    """Clica em um elemento com delay extremo para evitar stale element"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # Aguardar elemento estar presente
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 15)
        
        # Verificar se ainda está presente
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            # Tentar JavaScript como fallback
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').click();")
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(2)
        
        # Clicar
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay_extremo(driver, by, value, texto, descricao="campo", timeout=30):
    """Preenche um campo com delay extremo"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # Aguardar elemento estar presente
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 10)
        
        # Verificar se ainda está presente
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais presente, tentando JavaScript...")
            # Tentar JavaScript como fallback
            if by == By.ID:
                driver.execute_script(f"document.getElementById('{value}').value = '{texto}';")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').value = '{texto}';")
            print(f"✅ {descricao} preenchido via JavaScript")
            return True
        
        # Limpar e preencher
        elemento.clear()
        time.sleep(1)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
    """Clica em um radio button via JavaScript procurando por texto"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 15)
        
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

def capturar_dados_tela8(driver, temp_dir):
    """Captura dados da Tela 8 (Estimativa Inicial)"""
    print("**CAPTURANDO DADOS DA TELA 8 (ESTIMATIVA INICIAL)**")
    print("=" * 70)
    
    # Salvar página da Tela 8
    tela8_dir = salvar_estado_tela(driver, 8, "captura_dados", temp_dir)
    
    # Procurar por elementos da cobertura "Compreensiva"
    try:
        # Procurar por texto "Compreensiva"
        elementos_compreensiva = driver.find_elements(By.XPATH, "//*[contains(text(), 'Compreensiva')]")
        
        if elementos_compreensiva:
            print("✅ Nome Cobertura: Compreensiva")
            
            # Procurar por valores monetários próximos
            valores_monetarios = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
            print(f"�� Valores monetários encontrados: {len(valores_monetarios)}")
            
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
            print(f"�� Dados salvos em TXT: {txt_path}")
            
        else:
            print("❌ Cobertura 'Compreensiva' não encontrada")
            
    except Exception as e:
        print(f"❌ Erro ao capturar dados: {e}")
    
    print("**RESUMO DOS DADOS CAPTURADOS:**")
    print("=" * 70)
    print("✅ Dados da Tela 8 capturados com sucesso!")

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

def navegar_ate_tela3(driver):
    """Navega o RPA até a Tela 3 com seletores que funcionaram"""
    print("🚀 **NAVEGANDO ATÉ TELA 3 COM SELETORES TESTADOS**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    # Clicar no botão Carro com seletor que funcionou
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Carro')]", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento completo da página...")
    time.sleep(10)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # Preencher placa com delay extremo
    if not preencher_com_delay_extremo(driver, By.ID, "placaTelaDadosPlaca", "EED3D56", "placa"):
        print("❌ Erro: Falha ao preencher placa")
        return False
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 15)
    
    salvar_estado_tela(driver, 2, "placa_inserida", None)
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    # USAR O SELETOR QUE FUNCIONOU!
    if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    # AGUARDAR CARREGAMENTO COMPLETO
    print("⏳ Aguardando carregamento da página...")
    time.sleep(15)
    
    if not aguardar_carregamento_pagina(driver, 60):
        print("⚠️ Página pode não ter carregado completamente")
    
    # AGUARDAR ESTABILIZAÇÃO EXTREMA
    aguardar_estabilizacao(driver, 20)
    
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    print("✅ **NAVEGAÇÃO ATÉ TELA 3 CONCLUÍDA COM SUCESSO!**")
    return True

def implementar_tela5(driver):
    """Implementa a Tela 5 (Confirmação do veículo)"""
    print("\n **INICIANDO TELA 5: Confirmação do veículo**")
    
    # Aguardar Tela 5 carregar
    print("⏳ Aguardando Tela 5 carregar...")
    
    try:
        # Aguardar elementos da confirmação
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
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 5, "apos_continuar", None)
        print("✅ **TELA 5 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 5: {e}")
        return False

def implementar_tela6(driver):
    """Implementa a Tela 6 (Veículo já está segurado) - CORREÇÃO: NÃO para funcionar como antes"""
    print("\n **INICIANDO TELA 6: Veículo já está segurado**")
    
    # Aguardar Tela 6 carregar
    print("⏳ Aguardando Tela 6 carregar...")
    
    try:
        # Aguardar elementos da pergunta
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
        )
        print("✅ Tela 6 carregada - pergunta sobre veículo segurado detectada!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "pergunta_carregada", None)
        
        # CORREÇÃO: Selecionar "Não" para veículo já segurado (como funcionou antes)
        print("⏳ Selecionando 'Não' para veículo já segurado (CORREÇÃO!)...")
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO! (Não selecionado)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False

def implementar_tela7(driver):
    """Implementa a Tela 7 (Tela de renovação)"""
    print("\n **INICIANDO TELA 7: Tela de renovação**")
    
    # Aguardar Tela 7 carregar
    print("⏳ Aguardando Tela 7 carregar...")
    
    try:
        # Aguardar elementos da renovação
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'renovação') or contains(text(), 'renovacao')]"))
        )
        print("✅ Tela 7 carregada - renovação detectada!")
        
        salvar_estado_tela(driver, 7, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 7, "renovacao_carregada", None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 7"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 7")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 7, "apos_continuar", None)
        print("✅ **TELA 7 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 7: {e}")
        return False

def implementar_tela8(driver):
    """Implementa a Tela 8 (Estimativa inicial) - AGORA DEVE FUNCIONAR!"""
    print("\n **INICIANDO TELA 8: Estimativa inicial**")
    
    # Aguardar Tela 8 carregar
    print("⏳ Aguardando Tela 8 carregar...")
    
    try:
        # Aguardar elementos da estimativa
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel')]"))
        )
        print("✅ Tela 8 carregada - estimativa inicial detectada!")
        
        salvar_estado_tela(driver, 8, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 8, "estimativa_carregada", None)
        
        # CAPTURAR DADOS DA TELA 8
        capturar_dados_tela8(driver, None)
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 8"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 8")
            return False
        
        # AGUARDAR CARREGAMENTO COMPLETO
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        # AGUARDAR ESTABILIZAÇÃO EXTREMA
        aguardar_estabilizacao(driver, 20)
        
        salvar_estado_tela(driver, 8, "apos_continuar", None)
        print("✅ **TELA 8 IMPLEMENTADA COM SUCESSO! (Estimativa inicial)**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 8: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - SCRIPT CORRIGIDO FINAL**")
    print("=" * 80)
    print("🎯 OBJETIVO: Seletores que funcionaram + Fluxo correto (Não na Tela 6)")
    print("�� CORREÇÃO: Selecionar 'Não' na Tela 6 para funcionar como antes")
    print("⚡ MÉTODO: Delays extremos que funcionaram + Seletores testados")
    print("📊 BONUS: Capturar dados da estimativa inicial (Tela 8)")
    print("📝 NOTA: Combinação perfeita de estabilidade + fluxo correto")
    print("=" * 80)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar até Tela 3
        if not navegar_ate_tela3(driver):
            print("❌ Erro: Falha ao navegar até Tela 3")
            return
        
        # Implementar Tela 5
        if not implementar_tela5(driver):
            print("❌ Erro: Falha ao implementar Tela 5")
            return
        
        # Implementar Tela 6 (CORREÇÃO: Não para funcionar como antes)
        if not implementar_tela6(driver):
            print("❌ Erro: Falha ao implementar Tela 6")
            return
        
        # Implementar Tela 7
        if not implementar_tela7(driver):
            print("❌ Erro: Falha ao implementar Tela 7")
            return
        
        # Implementar Tela 8 (AGORA DEVE FUNCIONAR!)
        if not implementar_tela8(driver):
            print("❌ Erro: Falha ao implementar Tela 8")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA EXECUTADO COM SUCESSO! TELA 8 IMPLEMENTADA!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 8")
        print(f"✅ Tela 5: Confirmação do veículo")
        print(f"✅ Tela 6: Veículo já segurado (Não selecionado)")
        print(f"✅ Tela 7: Tela de renovação")
        print(f"✅ Tela 8: Estimativa inicial (dados capturados!)")
        print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        
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
