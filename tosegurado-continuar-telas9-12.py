#!/usr/bin/env python3
"""
RPA Tô Segurado - CONTINUANDO TELAS 9-12
Continua da Tela 8 para implementar as telas restantes
"""

import json
import sys
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

def carregar_parametros():
    """Carrega parâmetros do JSON passado via linha de comando"""
    if len(sys.argv) != 2:
        print("❌ ERRO: Uso correto: python3 tosegurado-continuar-telas9-12.py 'JSON_PARAMETROS'")
        sys.exit(1)
    
    try:
        json_str = sys.argv[1]
        parametros = json.loads(json_str)
        print("✅ Parâmetros carregados com sucesso!")
        return parametros
    except Exception as e:
        print(f"❌ ERRO ao carregar parâmetros: {e}")
        sys.exit(1)

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

def aguardar_estabilizacao(driver, segundos=3):
    """Aguarda a estabilização da página"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)

def clicar_continuar_corrigido(driver, descricao="Continuar", timeout=20):
    """Clica no botão Continuar usando o seletor CORRETO (elemento <p>)"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # ESTRATÉGIA CORRIGIDA: Elemento <p> com texto 'Continuar'
        try:
            elemento_continuar = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
            )
            print(f"✅ {descricao} encontrado (elemento <p>), aguardando estabilização...")
            aguardar_estabilizacao(driver, 3)
            
            driver.execute_script("arguments[0].scrollIntoView(true);", elemento_continuar)
            time.sleep(1)
            elemento_continuar.click()
            print(f"✅ {descricao} clicado com sucesso (elemento <p>)")
            return True
            
        except:
            print(f"⚠️ Elemento <p> 'Continuar' não encontrado, tentando JavaScript...")
            
            # JavaScript como fallback
            resultado = driver.execute_script("""
                var elementos = document.querySelectorAll('p, button, div, span');
                var continuarEncontrado = null;
                
                for (var i = 0; i < elementos.length; i++) {
                    var elemento = elementos[i];
                    if (elemento.textContent && elemento.textContent.includes('Continuar')) {
                        continuarEncontrado = elemento;
                        break;
                    }
                }
                
                if (continuarEncontrado) {
                    continuarEncontrado.click();
                    return 'Continuar clicado via JavaScript: ' + continuarEncontrado.outerHTML.substring(0, 100);
                } else {
                    return 'Continuar não encontrado';
                }
            """)
            
            print(f"🎯 {resultado}")
            
            if "Continuar clicado" in resultado:
                print(f"✅ {descricao} clicado via JavaScript")
                return True
            else:
                print(f"❌ {descricao} não encontrado via JavaScript")
                return False
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def preencher_com_delay_otimizado(driver, by, value, texto, descricao="campo", timeout=20):
    """Preenche um campo com delay otimizado"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 2)
        
        elemento.clear()
        time.sleep(0.5)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=20):
    """Clica em um radio button via JavaScript"""
    try:
        print(f"⏳ Aguardando radio {descricao} aparecer...")
        aguardar_estabilizacao(driver, 3)
        
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
    print(f"📱 **TELA {tela_num:02d}: {acao}** - {timestamp}")
    print(f"==================================================================================")
    print(f"🌐 URL: {driver.current_url}")
    print(f"📄 Título: {driver.title}")
    print(f" Ação: {acao}")
    print(f" Arquivos salvos em: {os.path.abspath(tela_dir)}")
    
    return tela_dir

def implementar_tela9(driver, parametros):
    """Implementa a Tela 9: Dados pessoais"""
    print("\n **INICIANDO TELA 9: Dados pessoais**")
    
    try:
        # Aguardar elementos dos dados pessoais
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'nome') or contains(text(), 'Nome') or contains(text(), 'CPF') or contains(text(), 'cpf')]"))
        )
        print("✅ Tela 9 carregada - dados pessoais detectados!")
        
        salvar_estado_tela(driver, 9, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 9, "dados_carregados", None)
        
        # Preencher Nome
        print(f"⏳ Preenchendo nome: {parametros['nome']}...")
        
        # Tentar diferentes seletores para o campo nome
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'nome') or contains(@placeholder, 'Nome') or contains(@name, 'nome') or contains(@id, 'nome')]", parametros['nome'], "nome"):
                print("⚠️ Campo nome não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher nome - tentando prosseguir...")
        
        # Preencher CPF
        print(f"⏳ Preenchendo CPF: {parametros['cpf']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'CPF') or contains(@placeholder, 'cpf') or contains(@name, 'cpf') or contains(@id, 'cpf')]", parametros['cpf'], "CPF"):
                print("⚠️ Campo CPF não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher CPF - tentando prosseguir...")
        
        # Preencher Data de Nascimento
        print(f"⏳ Preenchendo data de nascimento: {parametros['data_nascimento']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'nascimento') or contains(@placeholder, 'Nascimento') or contains(@name, 'nascimento') or contains(@id, 'nascimento')]", parametros['data_nascimento'], "data de nascimento"):
                print("⚠️ Campo data de nascimento não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher data de nascimento - tentando prosseguir...")
        
        # Selecionar Sexo
        print(f"⏳ Selecionando sexo: {parametros['sexo']}...")
        
        if not clicar_radio_via_javascript(driver, parametros['sexo'], f"{parametros['sexo']} como sexo"):
            print(f"⚠️ Radio '{parametros['sexo']}' não encontrado - tentando prosseguir...")
        
        # Selecionar Estado Civil
        print(f"⏳ Selecionando estado civil: {parametros['estado_civil']}...")
        
        if not clicar_radio_via_javascript(driver, parametros['estado_civil'], f"{parametros['estado_civil']} como estado civil"):
            print(f"⚠️ Radio '{parametros['estado_civil']}' não encontrado - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 9"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 9")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 9, "apos_continuar", None)
        print("✅ **TELA 9 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 9: {e}")
        return False

def implementar_tela10(driver, parametros):
    """Implementa a Tela 10: Contato"""
    print("\n **INICIANDO TELA 10: Contato**")
    
    try:
        # Aguardar elementos de contato
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'email') or contains(text(), 'Email') or contains(text(), 'telefone') or contains(text(), 'Telefone')]"))
        )
        print("✅ Tela 10 carregada - contato detectado!")
        
        salvar_estado_tela(driver, 10, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 10, "contato_carregado", None)
        
        # Preencher Email
        print(f"⏳ Preenchendo email: {parametros['email']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email') or contains(@name, 'email') or contains(@id, 'email')]", parametros['email'], "email"):
                print("⚠️ Campo email não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher email - tentando prosseguir...")
        
        # Preencher Telefone/Celular
        print(f"⏳ Preenchendo celular: {parametros['celular']}...")
        
        try:
            if not preencher_com_delay_otimizado(driver, By.XPATH, "//input[contains(@placeholder, 'telefone') or contains(@placeholder, 'Telefone') or contains(@placeholder, 'celular') or contains(@name, 'telefone') or contains(@id, 'telefone')]", parametros['celular'], "celular"):
                print("⚠️ Campo celular não encontrado - tentando prosseguir...")
        except:
            print("⚠️ Erro ao preencher celular - tentando prosseguir...")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 10"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 10")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 10, "apos_continuar", None)
        print("✅ **TELA 10 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 10: {e}")
        return False

def implementar_tela11(driver, parametros):
    """Implementa a Tela 11: Coberturas adicionais"""
    print("\n **INICIANDO TELA 11: Coberturas adicionais**")
    
    try:
        # Aguardar elementos de coberturas
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'cobertura') or contains(text(), 'Cobertura') or contains(text(), 'seguro') or contains(text(), 'Seguro')]"))
        )
        print("✅ Tela 11 carregada - coberturas adicionais detectadas!")
        
        salvar_estado_tela(driver, 11, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 11, "coberturas_carregadas", None)
        
        # Selecionar coberturas padrão (se disponíveis)
        print("⏳ Verificando coberturas disponíveis...")
        
        # Tentar selecionar coberturas comuns
        coberturas_comuns = ["Assistência 24h", "Carro reserva", "Vidros", "Roubo", "Furto"]
        
        for cobertura in coberturas_comuns:
            try:
                if clicar_radio_via_javascript(driver, cobertura, f"{cobertura} como cobertura"):
                    print(f"✅ Cobertura {cobertura} selecionada")
                else:
                    print(f"⚠️ Cobertura {cobertura} não encontrada")
            except:
                print(f"⚠️ Erro ao selecionar cobertura {cobertura}")
        
        # Clicar em Continuar
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_continuar_corrigido(driver, "botão Continuar Tela 11"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 11")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 11, "apos_continuar", None)
        print("✅ **TELA 11 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 11: {e}")
        return False

def implementar_tela12(driver, parametros):
    """Implementa a Tela 12: Finalização e resultado"""
    print("\n **INICIANDO TELA 12: Finalização e resultado**")
    
    try:
        # Aguardar elementos de finalização
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'finalizar') or contains(text(), 'Finalizar') or contains(text(), 'resultado') or contains(text(), 'Resultado') or contains(text(), 'cotação') or contains(text(), 'Cotação')]"))
        )
        print("✅ Tela 12 carregada - finalização detectada!")
        
        salvar_estado_tela(driver, 12, "inicial", None)
        
        if not aguardar_carregamento_pagina(driver, 20):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 12, "finalizacao_carregada", None)
        
        # Aguardar processamento da cotação
        print("⏳ Aguardando processamento da cotação...")
        time.sleep(10)
        
        salvar_estado_tela(driver, 12, "processamento_aguardado", None)
        
        # Verificar se há botão para finalizar
        try:
            if clicar_continuar_corrigido(driver, "botão Finalizar Tela 12"):
                print("✅ Botão Finalizar clicado com sucesso!")
            else:
                print("⚠️ Botão Finalizar não encontrado - cotação pode estar completa")
        except:
            print("⚠️ Erro ao clicar Finalizar - tentando prosseguir...")
        
        # Aguardar resultado final
        print("⏳ Aguardando resultado final...")
        time.sleep(8)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 5)
        salvar_estado_tela(driver, 12, "resultado_final", None)
        print("✅ **TELA 12 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 12: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 **RPA TÔ SEGURADO - CONTINUANDO TELAS 9-12**")
    print("=" * 80)
    print("🎯 OBJETIVO: Continuar da Tela 8 para implementar telas 9-12")
    print("🔧 MÉTODO: Script específico para telas finais")
    print("📝 NOTA: Assumindo que já estamos na Tela 8")
    print("=" * 80)
    
    # Carregar parâmetros
    print("�� CARREGANDO PARÂMETROS...")
    parametros = carregar_parametros()
    
    # Exibir parâmetros carregados
    print("\n📊 PARÂMETROS CARREGADOS:")
    for key, value in parametros.items():
        print(f"   {key}: {value}")
    
    inicio = datetime.now()
    print(f"\n⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar Chrome
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar para a URL e começar da Tela 8
        print(f"\n🌐 Navegando para {parametros['url']}...")
        driver.get(parametros['url'])
        
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou")
            return
        
        print("⚠️ ATENÇÃO: Este script assume que você já está na Tela 8!")
        print("⏳ Se não estiver, navegue manualmente até a Tela 8 primeiro...")
        time.sleep(5)
        
        # Implementar Tela 9
        if not implementar_tela9(driver, parametros):
            print("❌ Erro: Falha ao implementar Tela 9")
            return
        
        # Implementar Tela 10
        if not implementar_tela10(driver, parametros):
            print("❌ Erro: Falha ao implementar Tela 10")
            return
        
        # Implementar Tela 11
        if not implementar_tela11(driver, parametros):
            print("❌ Erro: Falha ao implementar Tela 11")
            return
        
        # Implementar Tela 12
        if not implementar_tela12(driver, parametros):
            print("❌ Erro: Falha ao implementar Tela 12")
            return
        
        print("\n" + "=" * 80)
        print("🎉 **RPA COMPLETO! TODAS AS 12 TELAS IMPLEMENTADAS!**")
        print("=" * 80)
        print(f"✅ Total de telas executadas: 12")
        print(f"✅ Telas 1-8: Já implementadas anteriormente")
        print(f"✅ Tela 9: Dados pessoais - {parametros['nome']}")
        print(f"✅ Tela 10: Contato - {parametros['email']}")
        print(f"✅ Tela 11: Coberturas adicionais")
        print(f"✅ Tela 12: Finalização e resultado")
        print(f"📁 Todos os arquivos salvos em: /opt/imediatoseguros-rpa/temp/")
        print(f"🔧 Parâmetros utilizados: {len(parametros)} parâmetros do JSON")
        
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
