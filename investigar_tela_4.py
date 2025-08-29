#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import tempfile
import shutil

def investigar_tela_4():
    print("🔍 **INVESTIGANDO TELA 4 - O QUE ACONTECEU?**")
    print("=" * 60)
    
    try:
        # Configurar Chrome headless
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        temp_dir = tempfile.mkdtemp(prefix="investigacao_tela4_")
        chrome_options.add_argument(f"--user-data-dir={temp_dir}")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)
        wait = WebDriverWait(driver, 20)
        
        print("✅ Chrome configurado")
        
        # TELA 1: Navegar para página inicial
        print("\n **Tela 1:** Navegando para página inicial")
        driver.get("https://www.app.tosegurado.com.br/imediatosolucoes")
        time.sleep(3)
        
        if "Qual seguro você deseja cotar?" not in driver.page_source:
            print("   ❌ Página inicial não carregou")
            return False
        print("   ✅ Página inicial carregada")
        
        # TELA 2: Clicar no botão "Carro"
        print("\n **Tela 2:** Clicando no botão 'Carro'")
        carro_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Carro')]"))
        )
        carro_button.click()
        print("   ✅ Botão 'Carro' clicado")
        time.sleep(3)
        
        # TELA 3: Verificar formulário de placa
        print("\n **Tela 3:** Verificando formulário de placa")
        if "Qual é a placa do carro?" not in driver.page_source:
            print("   ❌ Tela de placa não carregou")
            return False
        print("   ✅ Tela de placa carregada")
        
        # Preencher placa
        placa_input = wait.until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ABC-1D34']"))
        )
        placa_input.clear()
        placa_input.send_keys("EED3D56")
        print("   ✅ Placa preenchida: EED3D56")
        
        # TELA 4: INVESTIGAR - Clicar em Continuar e analisar
        print("\n **Tela 4:** INVESTIGANDO - Clicando em Continuar")
        
        # SELETOR CORRETO: <p> com texto "Continuar"
        continuar_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//p[text()='Continuar']"))
        )
        
        # Scroll para o elemento
        driver.execute_script("arguments[0].scrollIntoView(true);", continuar_button)
        time.sleep(1)
        
        # Clicar no elemento
        continuar_button.click()
        print("   ✅ Botão 'Continuar' clicado com sucesso!")
        
        # INVESTIGAÇÃO: Aguardar e analisar o que aconteceu
        print("\n�� **INVESTIGANDO RESULTADO:**")
        
        # Aguardar carregamento
        time.sleep(5)
        
        # Verificar URL atual
        current_url = driver.current_url
        print(f"   🌐 URL atual: {current_url}")
        
        # Verificar título da página
        page_title = driver.title
        print(f"   📄 Título da página: {page_title}")
        
        # Verificar se há texto de erro
        page_source = driver.page_source
        
        # Procurar por diferentes textos que podem indicar o que aconteceu
        textos_procurados = [
            "O veículo COROLLA XEI",
            "Erro",
            "Error",
            "Carregando",
            "Loading",
            "Aguarde",
            "Por favor",
            "Tente novamente",
            "Não foi possível",
            "Problema",
            "Falha"
        ]
        
        print("\n🔍 **PROCURANDO TEXTOS NA PÁGINA:**")
        for texto in textos_procurados:
            if texto in page_source:
                print(f"   ✅ '{texto}' encontrado na página")
            else:
                print(f"   ❌ '{texto}' NÃO encontrado na página")
        
        # Procurar por formulários ou campos
        print("\n🔍 **PROCURANDO ELEMENTOS NA PÁGINA:**")
        
        # Verificar se há campos de input
        inputs = driver.find_elements(By.TAG_NAME, "input")
        print(f"   📝 Campos de input encontrados: {len(inputs)}")
        
        # Verificar se há botões
        buttons = driver.find_elements(By.TAG_NAME, "button")
        print(f"   �� Botões encontrados: {len(buttons)}")
        
        # Verificar se há parágrafos
        paragraphs = driver.find_elements(By.TAG_NAME, "p")
        print(f"   📄 Parágrafos encontrados: {len(paragraphs)}")
        
        # Salvar HTML para análise detalhada
        html_path = "/opt/imediatoseguros-rpa/temp/tela_4_investigacao.html"
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(page_source)
        print(f"\n📄 HTML salvo para análise: {html_path}")
        
        # Salvar screenshot
        screenshot_path = "/opt/imediatoseguros-rpa/temp/tela_4_investigacao.png"
        driver.save_screenshot(screenshot_path)
        print(f"📸 Screenshot salvo: {screenshot_path}")
        
        # Verificar se há JavaScript errors no console
        print("\n🔍 **VERIFICANDO CONSOLE DO NAVEGADOR:**")
        try:
            logs = driver.get_log('browser')
            if logs:
                print("   📋 Logs do navegador encontrados:")
                for log in logs[:5]:  # Mostrar apenas os 5 primeiros
                    print(f"      {log}")
            else:
                print("   ✅ Nenhum erro no console")
        except:
            print("   ⚠️ Não foi possível verificar logs do navegador")
        
        print("\n✅ **INVESTIGAÇÃO CONCLUÍDA**")
        print("Verifique os arquivos salvos para análise detalhada")
        
        return True
        
    except Exception as e:
        print(f"\n❌ **ERRO DURANTE INVESTIGAÇÃO:** {e}")
        return False
        
    finally:
        # Fechar navegador
        if 'driver' in locals():
            driver.quit()
            print("🔒 Navegador fechado")
            
        # Limpar diretório temporário
        if 'temp_dir' in locals():
            shutil.rmtree(temp_dir, ignore_errors=True)
            print(f"🗑️ Diretório temporário removido: {temp_dir}")

if __name__ == "__main__":
    investigar_tela_4()

