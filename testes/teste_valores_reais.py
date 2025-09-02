#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TESTE DE DETECÇÃO DE VALORES REAIS
Verifica se o problema está na detecção ou no parsing dos valores
"""

import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json

def testar_deteccao_valores():
    """Testa a detecção de valores reais vs valores genéricos"""
    
    print("🔍 **TESTE DE DETECÇÃO DE VALORES REAIS**")
    print("=" * 50)
    
    # Configurar Chrome headless
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        # Carregar parâmetros
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        # Navegar para a página
        driver.get("https://www.app.tosegurado.com.br/imediatoseguros")
        
        print("⏳ Aguardando carregamento...")
        driver.implicitly_wait(10)
        
        # Teste 1: Detecção de valores reais (não R$ 100,00)
        print("\n📊 **TESTE 1: Detecção de valores reais**")
        valores_reais = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$') and not(contains(text(), 'R$ 100,00'))]")
        print(f"Valores reais encontrados: {len(valores_reais)}")
        
        for i, elem in enumerate(valores_reais[:5]):  # Mostrar apenas os primeiros 5
            try:
                texto = elem.text
                if 'R$' in texto:
                    print(f"  {i+1}. {texto}")
            except:
                continue
        
        # Teste 2: Detecção de valores específicos
        print("\n📊 **TESTE 2: Detecção de valores específicos**")
        valores_especificos = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$ 100,00') or contains(text(), 'R$ 2.500,00') or contains(text(), 'R$ 3.584,06')]")
        print(f"Valores específicos encontrados: {len(valores_especificos)}")
        
        for i, elem in enumerate(valores_especificos[:5]):
            try:
                texto = elem.text
                print(f"  {i+1}. {texto}")
            except:
                continue
        
        # Teste 3: Todos os valores monetários
        print("\n📊 **TESTE 3: Todos os valores monetários**")
        todos_valores = driver.find_elements(By.XPATH, "//*[contains(text(), 'R$')]")
        print(f"Total de valores monetários: {len(todos_valores)}")
        
        valores_unicos = set()
        for elem in todos_valores:
            try:
                texto = elem.text
                # Extrair valores R$ do texto
                valores_r = re.findall(r'R\$\s*[0-9.,]+', texto)
                for valor in valores_r:
                    valores_unicos.add(valor)
            except:
                continue
        
        print("Valores únicos encontrados:")
        for valor in sorted(valores_unicos):
            print(f"  - {valor}")
        
        # Teste 4: Verificar se há valores diferentes de R$ 100,00
        print("\n📊 **TESTE 4: Verificar valores diferentes de R$ 100,00**")
        valores_diferentes = [v for v in valores_unicos if v != 'R$ 100,00']
        print(f"Valores diferentes de R$ 100,00: {len(valores_diferentes)}")
        
        if valores_diferentes:
            print("Valores encontrados:")
            for valor in valores_diferentes:
                print(f"  ✅ {valor}")
        else:
            print("  ❌ Nenhum valor diferente de R$ 100,00 encontrado")
        
        # Teste 5: Verificar se a página está carregada corretamente
        print("\n📊 **TESTE 5: Verificação da página**")
        titulo = driver.title
        url = driver.current_url
        print(f"Título: {titulo}")
        print(f"URL: {url}")
        
        # Verificar se há elementos da tela final
        elementos_finais = driver.find_elements(By.XPATH, "//*[contains(text(), 'Parabéns') or contains(text(), 'resultado final') or contains(text(), 'Plano recomendado')]")
        print(f"Elementos da tela final: {len(elementos_finais)}")
        
        if elementos_finais:
            print("✅ Tela final detectada")
        else:
            print("❌ Tela final não detectada")
        
        # Salvar screenshot para análise
        driver.save_screenshot("teste_valores_reais.png")
        print("\n📸 Screenshot salvo: teste_valores_reais.png")
        
        return len(valores_diferentes) > 0
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False
    finally:
        driver.quit()

if __name__ == "__main__":
    sucesso = testar_deteccao_valores()
    print(f"\n{'='*50}")
    print(f"RESULTADO: {'✅ SUCESSO' if sucesso else '❌ FALHA'}")
    print(f"{'='*50}")
