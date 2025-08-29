#!/usr/bin/env python3
"""
RPA Tô Segurado - JAVASCRIPT PURO
Solução radical: JavaScript direto sem Selenium para localização
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

def clicar_via_javascript_puro(driver, texto_elemento, descricao="elemento", timeout=10):
    """Clica em um elemento via JavaScript puro, procurando por texto"""
    for tentativa in range(5):
        try:
            # Aguardar um pouco para estabilizar
            time.sleep(1)
            
            # JavaScript para encontrar e clicar no elemento
            script = f"""
            // Procurar por botões que contenham o texto
            var elementos = document.querySelectorAll('button, a, div, p, span');
            var elementoEncontrado = null;
            
            for (var i = 0; i < elementos.length; i++) {{
                var elemento = elementos[i];
                if (elemento.textContent && elemento.textContent.includes('{texto_elemento}')) {{
                    elementoEncontrado = elemento;
                    break;
                }}
            }}
            
            if (elementoEncontrado) {{
                // Scroll para o elemento
                elementoEncontrado.scrollIntoView({{behavior: 'smooth', block: 'center'}});
                
                // Aguardar um pouco
                setTimeout(function() {{
                    // Clicar no elemento
                    elementoEncontrado.click();
                }}, 500);
                
                return 'Elemento encontrado e clicado: ' + elementoEncontrado.outerHTML.substring(0, 200);
            }} else {{
                return 'Elemento não encontrado';
            }}
            """
            
            resultado = driver.execute_script(script)
            print(f"🎯 Tentativa {tentativa + 1}: {resultado}")
            
            if "Elemento encontrado e clicado" in resultado:
                print(f"✅ {descricao} clicado via JavaScript puro")
                return True
            
            # Aguardar um pouco mais
            time.sleep(2)
            
        except Exception as e:
            print(f"⚠️ Tentativa {tentativa + 1}: Erro - {e}")
            time.sleep(1)
            continue
    
    print(f"❌ Falha ao clicar em {descricao} após 5 tentativas")
    return False

def preencher_via_javascript_puro(driver, id_campo, valor, descricao="campo", timeout=10):
    """Preenche um campo via JavaScript puro usando ID"""
    try:
        # Aguardar um pouco para estabilizar
        time.sleep(1)
        
        # JavaScript para preencher o campo
        script = f"""
        var campo = document.getElementById('{id_campo}');
        if (campo) {{
            // Limpar o campo
            campo.value = '';
            
            // Preencher com o valor
            campo.value = '{valor}';
            
            // Trigger de eventos
            campo.dispatchEvent(new Event('input', {{ bubbles: true }}));
            campo.dispatchEvent(new Event('change', {{ bubbles: true }}));
            campo.dispatchEvent(new Event('blur', {{ bubbles: true }}));
            
            return 'Campo preenchido: ' + campo.value;
        }} else {{
            return 'Campo não encontrado';
        }}
        """
        
        resultado = driver.execute_script(script)
        print(f"🎯 {resultado}")
        
        if "Campo preenchido" in resultado:
            print(f"✅ {descricao} preenchido via JavaScript puro: {valor}")
            return True
        else:
            print(f"❌ {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
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

def navegar_ate_tela5(driver):
    """Navega o RPA até a Tela 5 usando JavaScript puro"""
    print("🚀 **NAVEGANDO ATÉ TELA 5 USANDO JAVASCRIPT PURO**")
    
    # TELA 1: Seleção do tipo de seguro
    print("\n📱 TELA 1: Selecionando Carro...")
    driver.get("https://www.app.tosegurado.com.br/cotacao")
    
    if not aguardar_carregamento_pagina(driver):
        print("❌ Erro: Página não carregou")
        return False
    
    salvar_estado_tela(driver, 1, "inicial", None)
    
    # Clicar no botão Carro via JavaScript puro
    salvar_estado_tela(driver, 1, "antes_clique", None)
    
    if not clicar_via_javascript_puro(driver, "Carro", "botão Carro"):
        print("❌ Erro: Falha ao clicar no botão Carro")
        return False
    
    # Aguardar carregamento
    print("⏳ Aguardando carregamento da página...")
    time.sleep(3)
    
    if not aguardar_carregamento_pagina(driver):
        print("❌ Erro: Página não carregou após selecionar Carro")
        return False
    
    salvar_estado_tela(driver, 1, "apos_clique", None)
    
    # TELA 2: Inserção da placa
    print("\n📱 TELA 2: Inserindo placa...")
    
    # Aguardar um pouco para a página estabilizar
    time.sleep(2)
    
    salvar_estado_tela(driver, 2, "inicial", None)
    
    # Preencher placa via JavaScript puro
    if not preencher_via_javascript_puro(driver, "placaTelaDadosPlaca", "EED3D56", "placa"):
        print("❌ Erro: Falha ao preencher placa")
        return False
    
    salvar_estado_tela(driver, 2, "placa_inserida", None)
    
    # TELA 3: Clicar em Continuar
    print("\n📱 TELA 3: Clicando Continuar...")
    
    if not clicar_via_javascript_puro(driver, "Continuar", "botão Continuar Tela 3"):
        print("❌ Erro: Falha ao clicar Continuar na Tela 3")
        return False
    
    # Aguardar carregamento e investigar
    print("⏳ Aguardando carregamento da página...")
    time.sleep(5)
    
    if not aguardar_carregamento_pagina(driver, 30):
        print("⚠️ Página pode não ter carregado completamente")
    
    # INVESTIGAR O QUE CARREGOU
    print("\n🔍 **INVESTIGANDO O QUE CARREGOU APÓS TELA 3:**")
    print("=" * 60)
    
    # Salvar estado atual
    salvar_estado_tela(driver, 3, "apos_clique", None)
    
    # Verificar URL e título
    print(f" URL Atual: {driver.current_url}")
    print(f"📄 Título Atual: {driver.title}")
    
    # Procurar por elementos específicos via JavaScript
    print("\n🔍 **PROCURANDO ELEMENTOS ESPECÍFICOS VIA JAVASCRIPT:**")
    
    # Script para procurar elementos
    script_busca = """
    var resultados = {};
    
    // Procurar por confirmação de veículo
    var confirmacao = document.querySelectorAll('[name="confirmacaoVeiculo"]');
    resultados.confirmacao = confirmacao.length;
    
    // Procurar por texto COROLLA
    var corolla = document.querySelectorAll('*');
    var corollaCount = 0;
    for (var i = 0; i < corolla.length; i++) {
        if (corolla[i].textContent && corolla[i].textContent.includes('COROLLA')) {
            corollaCount++;
        }
    }
    resultados.corolla = corollaCount;
    
    // Procurar por botões Continuar
    var continuar = document.querySelectorAll('button, a, div, p, span');
    var continuarCount = 0;
    for (var i = 0; i < continuar.length; i++) {
        if (continuar[i].textContent && continuar[i].textContent.includes('Continuar')) {
            continuarCount++;
        }
    }
    resultados.continuar = continuarCount;
    
    // Procurar por erros
    var erros = document.querySelectorAll('*');
    var erroCount = 0;
    for (var i = 0; i < erros.length; i++) {
        if (erros[i].textContent && (erros[i].textContent.includes('erro') || erros[i].textContent.includes('Erro') || erros[i].textContent.includes('error') || erros[i].textContent.includes('Error'))) {
            erroCount++;
        }
    }
    resultados.erros = erroCount;
    
    return resultados;
    """
    
    try:
        resultados = driver.execute_script(script_busca)
        print(f"✅ Elementos 'confirmacaoVeiculo': {resultados.get('confirmacao', 0)}")
        print(f"✅ Elementos 'COROLLA': {resultados.get('corolla', 0)}")
        print(f"✅ Botões 'Continuar': {resultados.get('continuar', 0)}")
        print(f"⚠️ Elementos de erro: {resultados.get('erros', 0)}")
    except Exception as e:
        print(f"❌ Erro ao executar busca via JavaScript: {e}")
    
    print("\n **INVESTIGAÇÃO CONCLUÍDA!**")
    print("📁 Verifique os arquivos salvos para análise detalhada")
    
    return True

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - JAVASCRIPT PURO**")
    print("=" * 60)
    print(" OBJETIVO: Investigar Tela 5 usando JavaScript puro")
    print("🔧 SOLUÇÃO: JavaScript direto sem Selenium para localização")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        if navegar_ate_tela5(driver):
            print("\n **INVESTIGAÇÃO CONCLUÍDA COM SUCESSO!**")
        else:
            print("\n❌ **FALHA NA INVESTIGAÇÃO**")
    
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
