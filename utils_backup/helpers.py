#!/usr/bin/env python3
"""
Funções auxiliares para o RPA
"""

import json
import sys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def carregar_parametros():
    """Carrega parâmetros do JSON passado via linha de comando"""
    if len(sys.argv) != 2:
        print("❌ ERRO: Uso correto: python3 main.py 'JSON_PARAMETROS'")
        sys.exit(1)
    
    try:
        json_str = sys.argv[1]
        parametros = json.loads(json_str)
        print("✅ Parâmetros carregados com sucesso!")
        return parametros
    except Exception as e:
        print(f"❌ ERRO ao carregar parâmetros: {e}")
        sys.exit(1)

def validar_parametros(parametros):
    """Valida se todos os parâmetros obrigatórios estão presentes"""
    obrigatorios = [
        "url", "placa", "marca", "modelo", "ano", "combustivel", 
        "cep", "uso_veiculo", "veiculo_segurado", "nome", "cpf", "email", "celular"
    ]
    
    faltando = []
    for param in obrigatorios:
        if param not in parametros or not parametros[param]:
            faltando.append(param)
    
    if faltando:
        print(f"❌ ERRO: Parâmetros obrigatórios faltando: {', '.join(faltando)}")
        print("📝 Parâmetros obrigatórios:")
        for param in obrigatorios:
            print(f"   - {param}")
        sys.exit(1)
    
    print("✅ Todos os parâmetros obrigatórios estão presentes!")
    return True

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

def salvar_estado_tela(driver, tela_num, acao, temp_dir):
    """Salva o estado atual da tela"""
    from datetime import datetime
    import os
    
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

def clicar_com_delay_otimizado(driver, by, value, descricao="elemento", timeout=20):
    """Clica em um elemento com delay otimizado"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 3)
        
        try:
            elemento = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"arguments[0].click();", elemento)
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(1)
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
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
        aguardar_estabilizacao(driver, 3)
        
        try:
            elemento = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.focus();")
            else:
                driver.execute_script(f"arguments[0].focus();", elemento)
            print(f"✅ {descricao} focado via JavaScript")
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(1)
        elemento.clear()
        time.sleep(0.5)
        elemento.send_keys(texto)
        print(f"✅ {descricao} preenchido com: {texto}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao preencher {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=8):
    """Clica em um radio button via JavaScript"""
    try:
        print(f"⏳ Procurando radio '{texto_radio}'...")
        
        # Tentar diferentes estratégias para encontrar o radio
        estrategias = [
            f"//input[@type='radio' and contains(@value, '{texto_radio}')]",
            f"//input[@type='radio' and contains(@name, '{texto_radio.lower()}')]",
            f"//input[@type='radio' and contains(@id, '{texto_radio.lower()}')]",
            f"//label[contains(text(), '{texto_radio}')]//input[@type='radio']",
            f"//label[contains(text(), '{texto_radio}')]",
            f"//*[contains(text(), '{texto_radio}') and contains(@class, 'radio')]",
            f"//*[contains(text(), '{texto_radio}') and contains(@class, 'Radio')]"
        ]
        
        for estrategia in estrategias:
            try:
                elemento = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, estrategia))
                )
                print(f"✅ Radio '{texto_radio}' encontrado via: {estrategia}")
                
                # Tentar clicar via JavaScript
                driver.execute_script("arguments[0].click();", elemento)
                print(f"✅ Radio '{texto_radio}' clicado via JavaScript")
                return True
                
            except:
                continue
        
        print(f"⚠️ Radio '{texto_radio}' não encontrado")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao clicar radio '{texto_radio}': {e}")
        return False

def clicar_checkbox_via_javascript(driver, texto_checkbox, descricao="checkbox", timeout=8):
    """Clica em um checkbox via JavaScript"""
    try:
        print(f"⏳ Procurando checkbox '{texto_checkbox}'...")
        
        # Tentar diferentes estratégias para encontrar o checkbox
        estrategias = [
            f"//input[@type='checkbox' and contains(@value, '{texto_checkbox}')]",
            f"//input[@type='checkbox' and contains(@name, '{texto_checkbox.lower()}')]",
            f"//input[@type='checkbox' and contains(@id, '{texto_checkbox.lower()}')]",
            f"//label[contains(text(), '{texto_checkbox}')]//input[@type='checkbox']",
            f"//label[contains(text(), '{texto_checkbox}')]",
            f"//*[contains(text(), '{texto_checkbox}') and contains(@class, 'checkbox')]",
            f"//*[contains(text(), '{texto_checkbox}') and contains(@class, 'Checkbox')]"
        ]
        
        for estrategia in estrategias:
            try:
                elemento = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, estrategia))
                )
                print(f"✅ Checkbox '{texto_checkbox}' encontrado via: {estrategia}")
                
                # Verificar se já está marcado
                if elemento.is_selected():
                    print(f"✅ Checkbox '{texto_checkbox}' já está marcado")
                    return True
                
                # Tentar clicar via JavaScript
                driver.execute_script("arguments[0].click();", elemento)
                print(f"✅ Checkbox '{texto_checkbox}' clicado via JavaScript")
                return True
                
            except:
                continue
        
        print(f"⚠️ Checkbox '{texto_checkbox}' não encontrado")
        return False
        
    except Exception as e:
        print(f"❌ Erro ao clicar checkbox '{texto_checkbox}': {e}")
        return False

def clicar_continuar_corrigido(driver, descricao="botão Continuar", timeout=20):
    """Clica no botão Continuar usando seletores corrigidos"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        # Estratégias para encontrar o botão Continuar
        estrategias = [
            # Estratégia 1: Botão com texto "Continuar"
            (By.XPATH, "//button[contains(text(), 'Continuar') or contains(text(), 'continuar')]"),
            (By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'continuar')]"),
            
            # Estratégia 2: Botão com classe específica
            (By.CSS_SELECTOR, "button.btn-continuar"),
            (By.CSS_SELECTOR, "button.btn-primary"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            
            # Estratégia 3: Botão com ID específico
            (By.ID, "continuar"),
            (By.ID, "btn-continuar"),
            (By.ID, "submit"),
            
            # Estratégia 4: Botão com atributo específico
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//input[@type='submit']"),
            
            # Estratégia 5: Botão com texto similar
            (By.XPATH, "//button[contains(text(), 'Próximo') or contains(text(), 'próximo')]"),
            (By.XPATH, "//button[contains(text(), 'Avançar') or contains(text(), 'avançar')]"),
            (By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'next')]")
        ]
        
        elemento = None
        estrategia_usada = None
        
        for estrategia in estrategias:
            try:
                elemento = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located(estrategia)
                )
                estrategia_usada = estrategia
                print(f"✅ {descricao} encontrado via: {estrategia}")
                break
            except:
                continue
        
        if not elemento:
            print(f"❌ {descricao} não encontrado com nenhuma estratégia")
            return False
        
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 3)
        
        try:
            elemento = WebDriverWait(driver, 8).until(
                EC.element_to_be_clickable(estrategia_usada)
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            driver.execute_script("arguments[0].click();", elemento)
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(1)
        
        # Clicar
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def aguardar_carregamento_pagina(driver, timeout=30):
    """Aguarda o carregamento da página"""
    try:
        print(f"⏳ Aguardando carregamento da página (timeout: {timeout}s)...")
        
        # Aguardar página carregar
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Aguardar jQuery (se existir)
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script("return typeof jQuery !== 'undefined' && jQuery.active === 0")
            )
        except:
            print("⚠️ jQuery não detectado ou ainda carregando")
        
        # Aguardar Angular (se existir)
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script("return typeof angular !== 'undefined' && !angular.element(document).injector().get('$http').pendingRequests.length")
            )
        except:
            print("⚠️ Angular não detectado ou ainda carregando")
        
        print("✅ Página carregada com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao aguardar carregamento da página: {e}")
        return False

def aguardar_estabilizacao(driver, segundos):
    """Aguarda estabilização da página"""
    print(f"⏳ Aguardando estabilização ({segundos}s)...")
    time.sleep(segundos)
    print("✅ Estabilização concluída")

def salvar_estado_tela(driver, numero_tela, etapa, dados_adicional):
    """Salva o estado atual da tela"""
    try:
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"tela{numero_tela}_{etapa}_{timestamp}.html"
        
        # Salvar HTML da página
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        
        # Salvar screenshot
        screenshot_nome = f"tela{numero_tela}_{etapa}_{timestamp}.png"
        driver.save_screenshot(screenshot_nome)
        
        print(f"💾 Estado da Tela {numero_tela} salvo: {nome_arquivo}")
        
    except Exception as e:
        print(f"⚠️ Erro ao salvar estado da Tela {numero_tela}: {e}")

