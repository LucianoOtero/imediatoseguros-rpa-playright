#!/usr/bin/env python3
"""
Teste específico para detectar elementos da Tela 7
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
        
        print(" Criando driver do Chrome...")
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
            return json.load(f)
    except Exception as e:
        print(f"❌ Erro ao carregar parâmetros: {e}")
        return None

def navegar_ate_tela6(driver, parametros):
    """Navega até a Tela 6"""
    print("\n🧭 NAVEGANDO ATÉ TELA 6...")
    
    try:
        # TELA 1: Página inicial
        print("\n📱 TELA 1: Selecionando tipo de seguro...")
        driver.get(parametros['url_base'])
        time.sleep(5)
        
        # Clicar em "Carro"
        print("⏳ Clicando no botão Carro...")
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Carro')]", "botão Carro"):
            return False
        
        time.sleep(5)
        
        # TELA 2: Inserir placa
        print("\n📱 TELA 2: Inserindo placa...")
        aguardar_estabilizacao(driver, 3)
        
        campo_placa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "placaTelaDadosPlaca"))
        )
        campo_placa.clear()
        campo_placa.send_keys(parametros['placa'])
        print(f"✅ Placa {parametros['placa']} inserida")
        
        aguardar_estabilizacao(driver, 3)
        
        # TELA 3: Confirmar veículo
        print("\n📱 TELA 3: Confirmando veículo...")
        aguardar_estabilizacao(driver, 5)
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Continuar')]", "botão Continuar"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 10)
        
        # TELA 4: Veículo já segurado
        print("\n📱 TELA 4: Veículo já segurado...")
        aguardar_estabilizacao(driver, 5)
        
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'segurado') or contains(text(), 'Segurado')]"))
            )
            print("✅ Tela 4 carregada!")
        except:
            print("❌ Tela 4 não carregou")
            return False
        
        if not clicar_radio_via_javascript(driver, "Não", "Não para veículo segurado"):
            return False
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Continuar')]", "botão Continuar Tela 4"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 10)
        
        # TELA 5: Estimativa inicial
        print("\n📱 TELA 5: Estimativa inicial...")
        aguardar_estabilizacao(driver, 5)
        
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Continuar') or contains(text(), 'Próximo')]"))
            )
            print("✅ Tela 5 carregada!")
        except:
            print("❌ Tela 5 não carregou")
            return False
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Continuar')]", "botão Continuar"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 10)
        
        # TELA 6: Cobertura/Estimativa
        print("\n📱 TELA 6: Cobertura/Estimativa...")
        aguardar_estabilizacao(driver, 5)
        
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'estimativa') or contains(text(), 'cobertura') or contains(text(), 'Compreensiva') or contains(text(), 'R$')]"))
            )
            print("✅ Tela 6 carregada!")
        except:
            print("❌ Tela 6 não carregou")
            return False
        
        # Selecionar cobertura
        if not clicar_radio_via_javascript(driver, "Compreensiva", "Cobertura Compreensiva"):
            print("⚠️ Cobertura não selecionada - prosseguindo...")
        
        if not clicar_com_delay_extremo(driver, By.XPATH, "//*[contains(text(), 'Continuar')]", "botão Continuar Tela 6"):
            return False
        
        time.sleep(15)
        aguardar_estabilizacao(driver, 10)
        
        print("✅ **NAVEGAÇÃO ATÉ TELA 6 CONCLUÍDA!**")
        return True
        
    except Exception as e:
        print(f"❌ Erro na navegação: {e}")
        return False

def analisar_tela7(driver):
    """Analisa o que está sendo exibido na Tela 7"""
    print("\n🔍 ANALISANDO TELA 7...")
    print("=" * 60)
    
    try:
        # Aguardar estabilização
        aguardar_estabilizacao(driver, 5)
        
        # Verificar URL atual
        print(f"📍 URL atual: {driver.current_url}")
        
        # Verificar título da página
        try:
            titulo = driver.title
            print(f"📄 Título da página: {titulo}")
        except:
            print("❌ Não foi possível obter o título")
        
        # Verificar HTML da página
        print("\n🔍 ANALISANDO HTML DA PÁGINA...")
        html = driver.page_source
        
        # Procurar por palavras-chave específicas
        palavras_chave = [
            "email", "Email", "celular", "Celular", "contato", "Contato",
            "dados", "Dados", "informações", "Informações", "pessoal", "Pessoal",
            "nome", "Nome", "CPF", "cpf", "data", "Data", "nascimento", "Nascimento"
        ]
        
        print("\n🎯 PALAVRAS-CHAVE ENCONTRADAS:")
        for palavra in palavras_chave:
            if palavra.lower() in html.lower():
                print(f"   ✅ '{palavra}' encontrado no HTML")
            else:
                print(f"   ❌ '{palavra}' NÃO encontrado no HTML")
        
        # Listar todos os textos visíveis
        print("\n📝 TEXTOS VISÍVEIS NA PÁGINA:")
        elementos = driver.find_elements(By.XPATH, "//*[text()]")
        textos = [elem.text.strip() for elem in elementos if elem.text.strip()]
        
        print(f"📊 Total de textos encontrados: {len(textos)}")
        
        # Mostrar primeiros 20 textos
        for i, texto in enumerate(textos[:20]):
            print(f"   {i+1:2d}: {texto}")
        
        if len(textos) > 20:
            print(f"   ... e mais {len(textos) - 20} textos")
        
        # Procurar por botões
        print("\n🔘 BOTÕES ENCONTRADOS:")
        botoes = driver.find_elements(By.XPATH, "//button | //input[@type='button'] | //a[contains(@class, 'btn')]")
        for i, botao in enumerate(botoes[:10]):
            texto = botao.text.strip() if botao.text else "Sem texto"
            classe = botao.get_attribute("class") or "Sem classe"
            print(f"   {i+1}: '{texto}' (classe: {classe})")
        
        # Procurar por inputs
        print("\n📝 INPUTS ENCONTRADOS:")
        inputs = driver.find_elements(By.XPATH, "//input")
        for i, inp in enumerate(inputs[:10]):
            tipo = inp.get_attribute("type") or "Sem tipo"
            placeholder = inp.get_attribute("placeholder") or "Sem placeholder"
            id_attr = inp.get_attribute("id") or "Sem ID"
            print(f"   {i+1}: tipo='{tipo}', placeholder='{placeholder}', id='{id_attr}'")
        
        # Salvar HTML para análise
        with open("tela7_analise.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"\n💾 HTML salvo em: tela7_analise.html")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao analisar Tela 7: {e}")
        return False

def main():
    """Função principal"""
    print("🔍 TESTE DE DETECÇÃO DA TELA 7")
    print("=" * 60)
    
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
            return
        
        # Navegar até Tela 6
        if not navegar_ate_tela6(driver, parametros):
            print("❌ Falha ao navegar até Tela 6")
            return
        
        # Analisar Tela 7
        if not analisar_tela7(driver):
            print("❌ Falha ao analisar Tela 7")
            return
        
        print("\n✅ **ANÁLISE DA TELA 7 CONCLUÍDA!**")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        
    finally:
        if driver:
            driver.quit()
        
        if temp_dir and os.path.exists(temp_dir):
            try:
                import shutil
                shutil.rmtree(temp_dir)
            except:
                pass

if __name__ == "__main__":
    main()
