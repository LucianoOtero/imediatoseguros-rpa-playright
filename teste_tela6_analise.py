#!/usr/bin/env python3
"""
Teste para analisar o que está acontecendo na Tela 6
"""

import time
import json
import os
import tempfile
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def configurar_driver():
    """Configura o driver do Chrome"""
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
    
    try:
        chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
        
        if os.path.exists(chromedriver_path):
            print("✅ Usando ChromeDriver local...")
            service = Service(chromedriver_path)
        else:
            print("❌ ChromeDriver local não encontrado")
            return None, None
        
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("✅ Driver configurado com sucesso")
        return driver, temp_dir
        
    except Exception as e:
        print(f"❌ Erro ao configurar driver: {e}")
        return None, None

def aguardar_estabilizacao(driver, segundos=15):
    """Aguarda a estabilização da página"""
    print(f"⏳ Aguardando estabilização da página ({segundos}s)...")
    time.sleep(segundos)

def clicar_com_delay_extremo(driver, by, value, descricao="elemento", timeout=30):
    """Clica em um elemento com delay extremo"""
    try:
        print(f"⏳ Aguardando {descricao} aparecer...")
        
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        
        print(f"✅ {descricao} encontrado, aguardando estabilização...")
        aguardar_estabilizacao(driver, 15)
        
        driver.execute_script("arguments[0].scrollIntoView(true);", elemento)
        time.sleep(2)
        elemento.click()
        print(f"✅ {descricao} clicado com sucesso")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao clicar em {descricao}: {e}")
        return False

def clicar_radio_via_javascript(driver, texto_radio, descricao="radio", timeout=30):
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

def carregar_parametros():
    """Carrega parâmetros do JSON"""
    try:
        with open("parametros.json", "r", encoding="utf-8") as f:
            parametros = json.load(f)
            return parametros
    except:
        return None

def navegar_ate_tela5(driver):
    """Navega até a Tela 5"""
    print("🚀 **NAVEGANDO ATÉ TELA 5**")
    
    try:
        # TELA 1: Seleção do tipo de seguro
        print("\n📱 TELA 1: Selecionando Carro...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        time.sleep(5)
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Carro')]", "botão Carro"):
            return False
        
        time.sleep(10)
        aguardar_estabilizacao(driver, 20)
        
        # TELA 2: Inserção da placa
        print("\n📱 TELA 2: Inserindo placa KVA-1791...")
        aguardar_estabilizacao(driver, 15)
        
        campo_placa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys("KVA-1791")
        print("✅ Placa preenchida: KVA-1791")
        
        aguardar_estabilizacao(driver, 15)
        
        # TELA 3: Clicar em Continuar
        print("\n📱 TELA 3: Clicando Continuar...")
        if not clicar_com_delay_extremo(driver, By.ID, "gtm-telaDadosAutoCotarComPlacaContinuar", "botão Continuar Tela 3"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 20)
        
        # TELA 3: Confirmação do veículo ECOSPORT
        print("\n📱 TELA 3: Confirmando veículo ECOSPORT...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ECOSPORT')]"))
            )
            print("✅ Confirmação do veículo detectada!")
        except:
            print("⚠️ Confirmação do veículo não detectada")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 20)
        
        # TELA 4: Veículo já está segurado?
        print("\n📱 TELA 4: Veículo já está segurado?")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
            )
            print("✅ Tela 4 carregada!")
        except:
            print("❌ Tela 4 não carregou")
            return False
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            print("⚠️ Radio 'Não' não encontrado")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(., 'Continuar')]", "botão Continuar Tela 4"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 20)
        
        # TELA 5: Estimativa inicial
        print("\n📱 TELA 5: Estimativa inicial...")
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel') or contains(text(), 'cobertura')]"))
            )
            print("✅ Tela 5 carregada!")
        except:
            print("⚠️ Tela 5 não detectada")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//button[contains(text(), 'Continuar')]", "botão Continuar Tela 5"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 20)
        
        print("✅ **NAVEGAÇÃO ATÉ TELA 5 CONCLUÍDA!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao navegar até Tela 5: {e}")
        return False

def analisar_tela6(driver):
    """Analisa o que está na Tela 6"""
    print("\n🔍 **ANALISANDO TELA 6**")
    
    try:
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 10)
        
        # Verificar URL atual
        print(f"🌐 URL atual: {driver.current_url}")
        print(f"📄 Título da página: {driver.title}")
        
        # Verificar se há elementos de combustível
        print("\n🔍 Procurando elementos relacionados a combustível...")
        
        # Estratégia 1: Procurar por texto "combustível"
        try:
            elementos_combustivel = driver.find_elements(By.XPATH, "//*[contains(text(), 'combustível') or contains(text(), 'Combustível')]")
            print(f"✅ Elementos com 'combustível' encontrados: {len(elementos_combustivel)}")
            for i, elem in enumerate(elementos_combustivel[:3]):
                print(f"   {i+1}: {elem.text[:100]}")
        except:
            print("❌ Nenhum elemento com 'combustível' encontrado")
        
        # Estratégia 2: Procurar por "Flex" ou "Gasolina"
        try:
            elementos_flex = driver.find_elements(By.XPATH, "//*[contains(text(), 'Flex') or contains(text(), 'Gasolina')]")
            print(f"✅ Elementos com 'Flex' ou 'Gasolina' encontrados: {len(elementos_flex)}")
            for i, elem in enumerate(elementos_flex[:3]):
                print(f"   {i+1}: {elem.text[:100]}")
        except:
            print("❌ Nenhum elemento com 'Flex' ou 'Gasolina' encontrado")
        
        # Estratégia 3: Procurar por botões
        try:
            botoes = driver.find_elements(By.TAG_NAME, "button")
            print(f"✅ Botões encontrados: {len(botoes)}")
            for i, botao in enumerate(botoes[:5]):
                print(f"   {i+1}: {botao.text[:50]}")
        except:
            print("❌ Nenhum botão encontrado")
        
        # Estratégia 4: Procurar por inputs
        try:
            inputs = driver.find_elements(By.TAG_NAME, "input")
            print(f"✅ Inputs encontrados: {len(inputs)}")
            for i, inp in enumerate(inputs[:5]):
                print(f"   {i+1}: type={inp.get_attribute('type')}, placeholder={inp.get_attribute('placeholder')}, id={inp.get_attribute('id')}")
        except:
            print("❌ Nenhum input encontrado")
        
        # Estratégia 5: Verificar se há elementos de estimativa
        try:
            elementos_estimativa = driver.find_elements(By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'inicial') or contains(text(), 'carrossel')]")
            print(f"✅ Elementos de estimativa ainda presentes: {len(elementos_estimativa)}")
            for i, elem in enumerate(elementos_estimativa[:3]):
                print(f"   {i+1}: {elem.text[:100]}")
        except:
            print("❌ Nenhum elemento de estimativa encontrado")
        
        # Salvar HTML da página para análise
        with open("tela6_analise_detalhada.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        print("💾 HTML da página salvo em 'tela6_analise_detalhada.html'")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao analisar Tela 6: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 **ANÁLISE DETALHADA DA TELA 6**")
    
    driver = None
    temp_dir = None
    
    try:
        # Configurar driver
        driver, temp_dir = configurar_driver()
        if not driver:
            return
        
        # Carregar parâmetros
        parametros = carregar_parametros()
        if not parametros:
            print("❌ Falha ao carregar parâmetros")
            return
        
        # Navegar até Tela 5
        if not navegar_ate_tela5(driver):
            print("❌ Falha ao navegar até Tela 5")
            return
        
        # Analisar Tela 6
        analisar_tela6(driver)
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            import shutil
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    main()
