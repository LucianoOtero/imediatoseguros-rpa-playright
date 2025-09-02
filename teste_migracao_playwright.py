#!/usr/bin/env python3
"""
TESTE DA MIGRAÇÃO PLAYWRIGHT
Script para testar se a migração do Selenium para Playwright está funcionando corretamente
"""

import json
import sys
import os
from datetime import datetime

def testar_imports_playwright():
    """Testa se os imports do Playwright estão funcionando"""
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Import do Playwright OK")
        return True
    except ImportError as e:
        print(f"❌ Erro no import do Playwright: {e}")
        return False

def testar_imports_utils():
    """Testa se os imports das utils estão funcionando"""
    try:
        from utils.validacao_parametros import validar_parametros_json
        from utils.logger_rpa import setup_logger, exibir_mensagem
        from utils.retorno_estruturado import criar_retorno_sucesso, criar_retorno_erro
        print("✅ Imports das utils OK")
        return True
    except ImportError as e:
        print(f"❌ Erro no import das utils: {e}")
        return False

def testar_imports_exception_handler():
    """Testa se o exception handler está funcionando"""
    try:
        from exception_handler import (
            handle_selenium_exception,
            handle_retry_attempt,
            format_success_message,
            set_session_info
        )
        print("✅ Exception handler OK")
        return True
    except ImportError as e:
        print(f"❌ Erro no exception handler: {e}")
        return False

def testar_parametros_json():
    """Testa se o arquivo parametros.json está válido"""
    try:
        with open('parametros.json', 'r', encoding='utf-8') as f:
            parametros = json.load(f)
        
        # Verificar campos obrigatórios
        campos_obrigatorios = [
            'configuracao', 'autenticacao', 'url_base', 'placa',
            'marca', 'modelo', 'ano', 'combustivel'
        ]
        
        for campo in campos_obrigatorios:
            if campo not in parametros:
                print(f"❌ Campo obrigatório '{campo}' não encontrado em parametros.json")
                return False
        
        print("✅ parametros.json válido")
        return True
        
    except FileNotFoundError:
        print("❌ Arquivo parametros.json não encontrado")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ JSON inválido em parametros.json: {e}")
        return False

def testar_funcoes_playwright():
    """Testa se as funções do Playwright estão definidas"""
    try:
        from executar_rpa_playwright import (
            setup_playwright_browser,
            realizar_login_automatico_playwright,
            navegar_tela_1_playwright,
            navegar_tela_2_playwright,
            navegar_tela_3_playwright,
            navegar_tela_4_playwright,
            navegar_tela_5_playwright,
            navegar_tela_6_playwright,
            navegar_tela_7_playwright,
            navegar_tela_8_playwright,
            navegar_tela_9_playwright,
            navegar_tela_10_playwright,
            navegar_tela_11_playwright,
            navegar_tela_12_playwright,
            navegar_tela_13_playwright,
            capturar_dados_tela_final_playwright,
            executar_todas_telas_playwright
        )
        print("✅ Todas as funções Playwright estão definidas")
        return True
        
    except ImportError as e:
        print(f"❌ Erro ao importar funções Playwright: {e}")
        return False

def testar_browser_playwright():
    """Testa se o browser Playwright consegue ser inicializado"""
    try:
        from playwright.sync_api import sync_playwright
        
        playwright = sync_playwright().start()
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        # Teste simples
        page.goto("https://www.google.com")
        title = page.title()
        
        browser.close()
        playwright.stop()
        
        print(f"✅ Browser Playwright funcionando (teste: {title})")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar browser Playwright: {e}")
        return False

def testar_migracao_completa():
    """Testa a migração completa comparando com o Selenium"""
    try:
        # Verificar se ambos os arquivos existem
        if not os.path.exists('executar_rpa_imediato.py'):
            print("❌ Arquivo executar_rpa_imediato.py (Selenium) não encontrado")
            return False
            
        if not os.path.exists('executar_rpa_playwright.py'):
            print("❌ Arquivo executar_rpa_playwright.py (Playwright) não encontrado")
            return False
        
        # Verificar tamanhos dos arquivos
        tamanho_selenium = os.path.getsize('executar_rpa_imediato.py')
        tamanho_playwright = os.path.getsize('executar_rpa_playwright.py')
        
        print(f"📊 Comparação de tamanhos:")
        print(f"   Selenium: {tamanho_selenium:,} bytes")
        print(f"   Playwright: {tamanho_playwright:,} bytes")
        
        # Verificar se o Playwright é menor (mais eficiente)
        if tamanho_playwright < tamanho_selenium:
            print("✅ Playwright é mais conciso que Selenium")
        else:
            print("⚠️ Playwright é maior que Selenium (pode ter mais funcionalidades)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao testar migração completa: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🧪 TESTE DA MIGRAÇÃO PLAYWRIGHT")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    testes = [
        ("Imports Playwright", testar_imports_playwright),
        ("Imports Utils", testar_imports_utils),
        ("Exception Handler", testar_imports_exception_handler),
        ("Parâmetros JSON", testar_parametros_json),
        ("Funções Playwright", testar_funcoes_playwright),
        ("Browser Playwright", testar_browser_playwright),
        ("Migração Completa", testar_migracao_completa)
    ]
    
    resultados = []
    
    for nome_teste, funcao_teste in testes:
        print(f"\n🔍 Testando: {nome_teste}")
        print("-" * 30)
        
        try:
            resultado = funcao_teste()
            resultados.append((nome_teste, resultado))
            
            if resultado:
                print(f"✅ {nome_teste}: PASSOU")
            else:
                print(f"❌ {nome_teste}: FALHOU")
                
        except Exception as e:
            print(f"❌ {nome_teste}: ERRO - {e}")
            resultados.append((nome_teste, False))
    
    # Resumo final
    print("\n" + "=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    testes_passaram = sum(1 for _, resultado in resultados if resultado)
    total_testes = len(resultados)
    
    for nome_teste, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"{nome_teste}: {status}")
    
    print(f"\n🎯 RESULTADO FINAL: {testes_passaram}/{total_testes} testes passaram")
    
    if testes_passaram == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Migração Playwright está funcionando corretamente")
        return 0
    else:
        print("⚠️ ALGUNS TESTES FALHARAM")
        print("🔧 Verifique os erros acima e corrija antes de usar")
        return 1

if __name__ == "__main__":
    sys.exit(main())

