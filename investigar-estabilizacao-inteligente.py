#!/usr/bin/env python3
"""
Investigação de Métodos Inteligentes para Detectar Estabilização da Página
Alternativas aos delays fixos de 20 segundos
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
    
    # Usar ChromeDriver local que já baixamos
    chromedriver_path = os.path.join(os.getcwd(), "chromedriver", "chromedriver-win64", "chromedriver.exe")
    
    if os.path.exists(chromedriver_path):
        print("✅ Usando ChromeDriver local...")
        service = Service(chromedriver_path)
    else:
        print("❌ ChromeDriver local não encontrado")
        return None, None
    
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

def detectar_estabilizacao_por_dom(driver, timeout=10, intervalo=0.5):
    """
    Detecta estabilização da página monitorando mudanças no DOM
    Retorna True quando o DOM para de mudar
    """
    print("�� **DETECTANDO ESTABILIZACAO POR DOM**")
    
    try:
        # Capturar estado inicial do DOM
        dom_inicial = driver.execute_script("return document.documentElement.outerHTML")
        mudancas = 0
        max_mudancas = 3  # Máximo de mudanças permitidas
        
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            # Capturar estado atual do DOM
            dom_atual = driver.execute_script("return document.documentElement.outerHTML")
            
            if dom_atual != dom_inicial:
                mudancas += 1
                print(f"   ⚠️ Mudança {mudancas} detectada no DOM")
                dom_inicial = dom_atual
                
                if mudancas >= max_mudancas:
                    print(f"   ❌ Muitas mudanças no DOM ({mudancas})")
                    return False
            
            # Se não houve mudanças por alguns intervalos, considerar estável
            if mudancas == 0 and i >= 2:
                print(f"   ✅ DOM estável após {i * intervalo:.1f}s")
                return True
        
        print(f"   ⏰ Timeout atingido ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao detectar estabilização por DOM: {e}")
        return False

def detectar_estabilizacao_por_network(driver, timeout=10, intervalo=0.5):
    """
    Detecta estabilização da página monitorando requisições de rede
    Retorna True quando não há mais requisições ativas
    """
    print("�� **DETECTANDO ESTABILIZACAO POR NETWORK**")
    
    try:
        # Verificar se há requisições de rede ativas
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            # Verificar se há requisições pendentes
            requests_pendentes = driver.execute_script("""
                return window.performance.getEntriesByType('resource').filter(
                    resource => resource.responseEnd === 0
                ).length;
            """)
            
            if requests_pendentes == 0:
                print(f"   ✅ Sem requisições pendentes após {i * intervalo:.1f}s")
                return True
            else:
                print(f"   ⏳ {requests_pendentes} requisições pendentes...")
        
        print(f"   ⏰ Timeout atingido ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao detectar estabilização por network: {e}")
        return False

def detectar_estabilizacao_por_elementos(driver, xpath_alvo, timeout=10, intervalo=0.5):
    """
    Detecta estabilização da página monitorando elementos específicos
    Retorna True quando o elemento alvo para de mudar
    """
    print(f"�� **DETECTANDO ESTABILIZACAO POR ELEMENTO: {xpath_alvo}**")
    
    try:
        # Aguardar elemento aparecer
        elemento = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath_alvo))
        )
        
        # Capturar estado inicial do elemento
        estado_inicial = elemento.get_attribute('outerHTML')
        mudancas = 0
        max_mudancas = 2
        
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            try:
                elemento = driver.find_element(By.XPATH, xpath_alvo)
                estado_atual = elemento.get_attribute('outerHTML')
                
                if estado_atual != estado_inicial:
                    mudancas += 1
                    print(f"   ⚠️ Mudança {mudancas} no elemento alvo")
                    estado_inicial = estado_atual
                    
                    if mudancas >= max_mudancas:
                        print(f"   ❌ Muitas mudanças no elemento ({mudancas})")
                        return False
                
                # Se não houve mudanças por alguns intervalos, considerar estável
                if mudancas == 0 and i >= 2:
                    print(f"   ✅ Elemento estável após {i * intervalo:.1f}s")
                    return True
                    
            except:
                print(f"   ⚠️ Elemento não encontrado na iteração {i}")
                continue
        
        print(f"   ⏰ Timeout atingido ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao detectar estabilização por elemento: {e}")
        return False

def detectar_estabilizacao_por_javascript(driver, timeout=10, intervalo=0.5):
    """
    Detecta estabilização da página usando JavaScript avançado
    Retorna True quando a página está realmente estável
    """
    print("⚡ **DETECTANDO ESTABILIZACAO POR JAVASCRIPT**")
    
    try:
        script = """
        // Verificar múltiplos indicadores de estabilização
        var indicadores = {
            readyState: document.readyState,
            loading: document.querySelectorAll('[class*="loading"], [class*="Loading"]').length,
            spinner: document.querySelectorAll('[class*="spinner"], [class*="Spinner"]').length,
            progress: document.querySelectorAll('[class*="progress"], [class*="Progress"]').length,
            overlay: document.querySelectorAll('[class*="overlay"], [class*="Overlay"]').length,
            requests: window.performance.getEntriesByType('resource').filter(r => r.responseEnd === 0).length,
            mutations: 0
        };
        
        // Verificar se há mutações no DOM
        if (window.mutationObserver) {
            var observer = new MutationObserver(function(mutations) {
                indicadores.mutations += mutations.length;
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true,
                attributes: true
            });
        }
        
        return indicadores;
        """
        
        indicadores_iniciais = driver.execute_script(script)
        print(f"   �� Indicadores iniciais: {indicadores_iniciais}")
        
        for i in range(int(timeout / intervalo)):
            time.sleep(intervalo)
            
            indicadores_atual = driver.execute_script(script)
            
            # Verificar se os indicadores mudaram
            mudancas = 0
            for key in indicadores_iniciais:
                if indicadores_iniciais[key] != indicadores_atual[key]:
                    mudancas += 1
            
            if mudancas == 0 and i >= 2:
                print(f"   ✅ Página estável após {i * intervalo:.1f}s")
                print(f"   �� Indicadores finais: {indicadores_atual}")
                return True
            else:
                print(f"   ⏳ {mudancas} indicadores mudaram...")
        
        print(f"   ⏰ Timeout atingido ({timeout}s)")
        return False
        
    except Exception as e:
        print(f"   ❌ Erro ao detectar estabilização por JavaScript: {e}")
        return False

def aguardar_estabilizacao_inteligente(driver, metodo="javascript", timeout=10):
    """
    Aguarda estabilização da página usando método inteligente
    """
    print(f"�� **AGUARDANDO ESTABILIZACAO INTELLIGENTE - MÉTODO: {metodo.upper()}**")
    
    inicio = time.time()
    
    if metodo == "dom":
        resultado = detectar_estabilizacao_por_dom(driver, timeout)
    elif metodo == "network":
        resultado = detectar_estabilizacao_por_network(driver, timeout)
    elif metodo == "javascript":
        resultado = detectar_estabilizacao_por_javascript(driver, timeout)
    else:
        print(f"   ❌ Método '{metodo}' não reconhecido")
        return False
    
    duracao = time.time() - inicio
    print(f"   ⏱️ Tempo total: {duracao:.1f}s")
    
    return resultado

def testar_metodos_estabilizacao():
    """Testa todos os métodos de estabilização"""
    print("�� **TESTANDO MÉTODOS DE ESTABILIZACAO INTELLIGENTE**")
    print("=" * 70)
    
    driver = None
    temp_dir = None
    
    try:
        driver, temp_dir = configurar_chrome()
        print("✅ Chrome configurado")
        
        # Navegar para uma página de teste
        print("\n🌐 Navegando para página de teste...")
        driver.get("https://www.app.tosegurado.com.br/cotacao")
        
        if not aguardar_carregamento_pagina(driver):
            print("❌ Erro: Página não carregou")
            return
        
        print("✅ Página carregada")
        
        # Testar método DOM
        print("\n" + "=" * 50)
        aguardar_estabilizacao_inteligente(driver, "dom", 15)
        
        # Testar método Network
        print("\n" + "=" * 50)
        aguardar_estabilizacao_inteligente(driver, "network", 15)
        
        # Testar método JavaScript
        print("\n" + "=" * 50)
        aguardar_estabilizacao_inteligente(driver, "javascript", 15)
        
        # Testar com elemento específico
        print("\n" + "=" * 50)
        detectar_estabilizacao_por_elementos(driver, "//button[contains(., 'Carro')]", 15)
        
        print("\n" + "=" * 70)
        print("🎯 **TESTES CONCLUÍDOS!**")
        print("📊 Compare os resultados para escolher o melhor método")
        
    except Exception as e:
        print(f"❌ **ERRO DURANTE TESTES:** {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if driver:
            driver.quit()
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

def main():
    """Função principal"""
    print("🧠 **INVESTIGAÇÃO DE ESTABILIZACAO INTELLIGENTE**")
    print("=" * 60)
    print("�� OBJETIVO: Substituir delays fixos por detecção inteligente")
    print("🔧 MÉTODOS: DOM, Network, JavaScript, Elementos específicos")
    print("=" * 60)
    
    inicio = datetime.now()
    print(f"⏰ Início: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    
    testar_metodos_estabilizacao()
    
    fim = datetime.now()
    print(f"⏰ Fim: {fim.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()
