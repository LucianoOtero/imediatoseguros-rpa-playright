#!/usr/bin/env python3
"""
Tela 6: Tipo de combustível + checkboxes
"""

import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.helpers import (
    aguardar_estabilizacao, salvar_estado_tela
)

def aguardar_carregamento_pagina(driver, timeout=60):
    """Aguarda o carregamento completo da página (ESTRATÉGIA QUE FUNCIONOU)"""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        return True
    except:
        return False

def clicar_com_delay_extremo(driver, by, value, descricao="elemento", timeout=30):
    """Clica em um elemento com delay extremo (ESTRATÉGIA QUE FUNCIONOU)"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 15)
        
        try:
            elemento = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
        except:
            print(f"⚠️ {descricao} não está mais clicável, tentando JavaScript...")
            if by == By.XPATH:
                driver.execute_script(f"document.evaluate('{value}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click();")
            else:
                driver.execute_script(f"document.querySelector('{by}={value}').click();")
            print(f"✅ {descricao} clicado via JavaScript")
            return True
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(2)
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
    """Clica em um radio button via JavaScript (ESTRATÉGIA QUE FUNCIONOU)"""
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

def clicar_checkbox_via_javascript(driver, texto_checkbox, descricao="checkbox", timeout=30):
    """Clica em um checkbox via JavaScript (ESTRATÉGIA QUE FUNCIONOU)"""
    try:
        print(f"⏳ Aguardando checkbox {descricao} aparecer...")
        aguardar_estabilizacao(driver, 15)
        
        script = f"""
        var elementos = document.querySelectorAll('input[type="checkbox"], label, span, div');
        var checkboxEncontrado = null;
        
        for (var i = 0; i < elementos.length; i++) {{
            var elemento = elementos[i];
            if (elemento.textContent && elemento.textContent.includes('{texto_checkbox}')) {{
                checkboxEncontrado = elemento;
                break;
            }}
        }}
        
        if (checkboxEncontrado) {{
            if (checkboxEncontrado.tagName === 'LABEL') {{
                var inputId = checkboxEncontrado.getAttribute('for');
                if (inputId) {{
                    var input = document.getElementById(inputId);
                    if (input) {{
                        input.click();
                        return 'Checkbox clicado via label: ' + inputId;
                    }}
                }}
            }}
            
            checkboxEncontrado.click();
            return 'Checkbox clicado diretamente: ' + checkboxEncontrado.outerHTML.substring(0, 100);
        }} else {{
            return 'Checkbox não encontrado';
        }}
        """
        
        resultado = driver.execute_script(script)
        print(f"🎯 {resultado}")
        
        if "Checkbox clicado" in resultado:
            print(f"✅ Checkbox {descricao} clicado via JavaScript")
            return True
        else:
            print(f"❌ Checkbox {descricao} não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao clicar checkbox {descricao}: {e}")
        return False

def implementar_tela6(driver, parametros):
    """Implementa a Tela 6: Tipo de combustível + checkboxes (IMPLEMENTAÇÃO EXATA QUE FUNCIONOU)"""
    print(f"\n **INICIANDO TELA 6: Tipo de combustível + checkboxes**")
    
    try:
        # Aguardar elementos da Tela 6 (ESTRATÉGIA QUE FUNCIONOU ONTEM)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível') or contains(text(), 'Flex') or contains(text(), 'Gasolina')]"))
        )
        print("✅ Tela 6 carregada - tipo de combustível detectado!")
        
        salvar_estado_tela(driver, 6, "inicial", None)
        
        # Aguardar carregamento da página (ESTRATÉGIA QUE FUNCIONOU ONTEM)
        if not aguardar_carregamento_pagina(driver, 30):
            print("❌ Erro: Página não carregou completamente")
            return False
        
        salvar_estado_tela(driver, 6, "combustivel_carregado", None)
        
        # Selecionar "Flex" como tipo de combustível (ESTRATÉGIA QUE FUNCIONOU ONTEM)
        print("⏳ Selecionando 'Flex' como tipo de combustível...")
        
        if not clicar_radio_via_javascript(driver, "Flex", "Flex como combustível"):
            print("⚠️ Radio 'Flex' não encontrado - tentando prosseguir...")
        
        # Selecionar checkboxes se disponíveis (ESTRATÉGIA QUE FUNCIONOU ONTEM)
        print("⏳ Verificando checkboxes disponíveis...")
        
        # Kit Gás (se disponível)
        if not clicar_checkbox_via_javascript(driver, "kit gas", "Kit Gás"):
            print("⚠️ Checkbox Kit Gás não encontrado")
        
        # Blindado (se disponível)
        if not clicar_checkbox_via_javascript(driver, "blindado", "Blindado"):
            print("⚠️ Checkbox Blindado não encontrado")
        
        # Financiado (se disponível)
        if not clicar_checkbox_via_javascript(driver, "financiado", "Financiado"):
            print("⚠️ Checkbox Financiado não encontrado")
        
        # Clicar em Continuar (ESTRATÉGIA QUE FUNCIONOU ONTEM)
        print("⏳ Aguardando botão Continuar aparecer...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 6"):
            print("❌ Erro: Falha ao clicar Continuar na Tela 6")
            return False
        
        print("⏳ Aguardando carregamento da página...")
        time.sleep(15)
        
        if not aguardar_carregamento_pagina(driver, 60):
            print("⚠️ Página pode não ter carregado completamente")
        
        aguardar_estabilizacao(driver, 20)
        salvar_estado_tela(driver, 6, "apos_continuar", None)
        print("✅ **TELA 6 IMPLEMENTADA COM SUCESSO!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na Tela 6: {e}")
        return False
