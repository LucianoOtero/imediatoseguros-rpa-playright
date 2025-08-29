#!/usr/bin/env python3
"""
RPA SIMPLES - TÔ SEGURADO - TESTE INICIAL
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_chrome_basic():
    """Teste básico do Chrome"""
    print("🚀 **TESTE BÁSICO DO CHROME**")
    print("=" * 50)
    
    try:
        # Configurações básicas
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--headless")  # Executar sem interface gráfica
        
        print("🔧 Configurando Chrome...")
        
        # Instalar ChromeDriver
        service = Service(ChromeDriverManager().install())
        
        # Criar driver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        print("✅ Chrome configurado com sucesso!")
        
        # Teste simples
        print("🌐 Navegando para Google...")
        driver.get("https://www.google.com")
        
        print(f"📄 Título da página: {driver.title}")
        
        # Aguardar um pouco
        time.sleep(3)
        
        print("✅ Teste básico concluído com sucesso!")
        
        # Fechar
        driver.quit()
        print("🔒 Navegador fechado")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = test_chrome_basic()
    
    if success:
        print("\n🎉 **CHROME FUNCIONANDO!**")
        print("Próximo passo: Criar RPA completo")
    else:
        print("\n❌ **PROBLEMA NO CHROME**")
        print("Precisamos resolver antes de continuar")
