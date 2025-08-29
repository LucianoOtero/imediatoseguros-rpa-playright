#!/usr/bin/env python3
"""
Teste forçado da Tela 4 com navegação forçada
"""

import time
import json
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    """Configura o driver do Chrome"""
    print("🔧 Configurando Chrome...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    
    try:
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            print("✅ Usando ChromeDriver local...")
            service = Service(chromedriver_path)
        else:
            print("❌ ChromeDriver local não encontrado")
            return None
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver configurado com sucesso")
        return driver
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        return None

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return None

def navegar_ate_tela4(driver, parametros):
    """Navega até a Tela 4"""
    print("\n🧭 NAVEGANDO ATÉ TELA 4")
    print("=" * 50)
    
    try:
        # TELA 1: Página inicial
        print("\n📱 TELA 1: Página inicial...")
        driver.get(parametros['url_base'])
        time.sleep(5)
        
        # Clicar em "Carro"
        print("⏳ Clicando em 'Carro'...")
        botao_carro = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Carro')]"))
        )
        botao_carro.click()
        print("✅ Botão Carro clicado")
        time.sleep(5)
        
        # TELA 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        campo_placa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys(parametros['placa'])
        print(f"✅ Placa {parametros['placa']} inserida")
        time.sleep(3)
        
        # TELA 3: Confirmar veículo
        print("\n📱 TELA 3: Confirmando veículo...")
        time.sleep(5)
        
        botao_continuar = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Continuar')]"))
        )
        botao_continuar.click()
        print("✅ Botão Continuar clicado na Tela 3")
        time.sleep(10)
        
        print("✅ Chegamos na Tela 4!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao navegar até Tela 4: {e}")
        return False

def forcar_navegacao_tela4(driver):
    """Força a navegação da Tela 4"""
    print("\n🚀 FORÇANDO NAVEGAÇÃO DA TELA 4")
    print("=" * 50)
    
    try:
        # Aguardar carregamento
        print("⏳ Aguardando carregamento da Tela 4...")
        time.sleep(5)
        
        # ESTRATÉGIA 1: Selecionar radio "Não"
        print("🔍 Estratégia 1: Selecionando radio 'Não'...")
        
        script_radio = """
        var radios = document.querySelectorAll('input[type="radio"]');
        var radioNao = null;
        
        for (var i = 0; i < radios.length; i++) {
            var radio = radios[i];
            var label = document.querySelector('label[for="' + radio.id + '"]');
            
            if (label && label.textContent.includes('Não')) {
                radioNao = radio;
                break;
            }
            
            if (radio.value && radio.value.includes('Não')) {
                radioNao = radio;
                break;
            }
        }
        
        if (radioNao) {
            radioNao.checked = true;
            radioNao.click();
            return 'Radio Não encontrado e selecionado: ' + radioNao.id;
        } else {
            return 'Radio Não não encontrado';
        }
        """
        
        resultado = driver.execute_script(script_radio)
        print(f"🎯 Resultado: {resultado}")
        
        if "Radio Não encontrado" in resultado:
            print("✅ Radio 'Não' selecionado com sucesso!")
            
            # ESTRATÉGIA 2: Forçar navegação via JavaScript
            print("🔍 Estratégia 2: Forçando navegação via JavaScript...")
            
            # Aguardar um pouco mais
            time.sleep(3)
            
            # Tentar múltiplas estratégias para o botão Continuar
            estrategias = [
                # Estratégia 1: Procurar por botão com texto "Continuar"
                """
                var botoes = document.querySelectorAll('button, input[type="button"], a, div[role="button"]');
                var botaoContinuar = null;
                
                for (var i = 0; i < botoes.length; i++) {
                    var botao = botoes[i];
                    if (botao.textContent && botao.textContent.toLowerCase().includes('continuar')) {
                        botaoContinuar = botao;
                        break;
                    }
                }
                
                if (botaoContinuar) {
                    botaoContinuar.click();
                    return 'Botão Continuar clicado via texto: ' + botaoContinuar.textContent;
                } else {
                    return 'Botão Continuar não encontrado via texto';
                }
                """,
                
                # Estratégia 2: Procurar por botão com classe específica
                """
                var botaoContinuar = document.querySelector('.btn-continuar, .btn-primary, .btn-success, [class*="continuar"], [class*="btn"]');
                if (botaoContinuar) {
                    botaoContinuar.click();
                    return 'Botão Continuar clicado via classe: ' + botaoContinuar.className;
                } else {
                    return 'Botão Continuar não encontrado via classe';
                }
                """,
                
                # Estratégia 3: Procurar por qualquer elemento clicável
                """
                var elementos = document.querySelectorAll('*');
                var botaoContinuar = null;
                
                for (var i = 0; i < elementos.length; i++) {
                    var elemento = elementos[i];
                    if (elemento.textContent && elemento.textContent.toLowerCase().includes('continuar') && 
                        (elemento.tagName === 'BUTTON' || elemento.tagName === 'A' || elemento.tagName === 'INPUT' || 
                         elemento.onclick || elemento.getAttribute('onclick'))) {
                        botaoContinuar = elemento;
                        break;
                    }
                }
                
                if (botaoContinuar) {
                    botaoContinuar.click();
                    return 'Botão Continuar clicado via elemento clicável: ' + botaoContinuar.tagName;
                } else {
                    return 'Botão Continuar não encontrado via elemento clicável';
                }
                """
            ]
            
            for i, estrategia in enumerate(estrategias, 1):
                print(f"⏳ Tentando Estratégia {i}...")
                resultado_continuar = driver.execute_script(estrategia)
                print(f"🎯 Resultado Estratégia {i}: {resultado_continuar}")
                
                if "clicado" in resultado_continuar.lower():
                    print(f"✅ Navegação forçada com sucesso via Estratégia {i}!")
                    break
                else:
                    print(f"⚠️ Estratégia {i} falhou, tentando próxima...")
            
            # Aguardar carregamento da próxima página
            print("⏳ Aguardando carregamento da próxima página (30s)...")
            time.sleep(30)
            
            # Verificar se chegamos na Tela 5
            html = driver.page_source
            if "estimativa" in html.lower() or "próximo" in html.lower() or "combustível" in html.lower():
                print("✅ TELA 5 ALCANÇADA! Texto encontrado!")
                return True
            else:
                print("❌ TELA 5 NÃO ALCANÇADA!")
                print("📝 Últimos textos encontrados:")
                elementos = driver.find_elements(By.XPATH, "//*[text()]")
                textos = [elem.text.strip() for elem in elementos if elem.text.strip()]
                for i, texto in enumerate(textos[-15:]):
                    print(f"   {i+1}: {texto}")
                return False
        else:
            print("❌ Radio 'Não' não encontrado")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao forçar navegação da Tela 4: {e}")
        return False

def main():
    """Função principal"""
    print("🚀 TESTE DE NAVEGAÇÃO FORÇADA DA TELA 4")
    print("=" * 50)
    
    # Configurar driver
    driver = configurar_driver()
    if not driver:
        return
    
    try:
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            return
        
        # Navegar até Tela 4
        if navegar_ate_tela4(driver, parametros):
            # Forçar navegação da Tela 4
            sucesso = forcar_navegacao_tela4(driver)
            
            if sucesso:
                print("\n🎉 TELA 4 NAVEGOU COM SUCESSO PARA TELA 5!")
            else:
                print("\n❌ TELA 4 NÃO NAVEGOU PARA TELA 5!")
        else:
            print("\n❌ NÃO FOI POSSÍVEL CHEGAR NA TELA 4!")
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        if driver:
            driver.quit()
            print("✅ Driver fechado")

if __name__ == "__main__":
    main()
