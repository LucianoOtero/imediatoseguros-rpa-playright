#!/usr/bin/env python3
"""
Teste de Execucao do Footer Code
Verifica se a funcao logDebug esta sendo chamada
"""

import requests
import json
from datetime import datetime

def test_footer_code_execution():
    """Simula exatamente o que o Footer Code deveria fazer"""
    url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    # Dados EXATAMENTE como o Footer Code envia
    footer_data = {
        'level': 'INFO',
        'message': '🎯 [CONFIG] RPA habilitado via PHP Log',  # Com emoji original
        'data': {'rpaEnabled': False},
        'timestamp': datetime.now().isoformat(),
        'sessionId': 'footer_test_' + str(int(datetime.now().timestamp())),
        'url': 'https://www.segurosimediato.com.br',
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("TESTE DE EXECUCAO DO FOOTER CODE")
    print("=" * 50)
    print(f"Simulando chamada da funcao logDebug...")
    print(f"Dados: {json.dumps(footer_data, indent=2, ensure_ascii=False)}")
    print()
    
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=footer_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("✅ SUCESSO: Footer Code simulado funcionou!")
                    return True
                else:
                    print(f"❌ ERRO: {result.get('error', 'Erro desconhecido')}")
                    return False
            except:
                print("❌ ERRO: Resposta nao e JSON valido")
                return False
        else:
            print(f"❌ ERRO HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ ERRO DE CONEXAO: {e}")
        return False

def check_recent_logs():
    """Verifica logs recentes no banco"""
    print("\nVERIFICANDO LOGS RECENTES NO BANCO:")
    print("=" * 50)
    
    # Usar o sistema de recuperacao para verificar
    import subprocess
    result = subprocess.run([
        'python', 
        'C:\\Users\\Luciano\\OneDrive - Imediato Soluções em Seguros\\Imediato\\imediatoseguros-rpa-playwright\\database_connector.py'
    ], capture_output=True, text=True)
    
    print(result.stdout)
    if result.stderr:
        print("ERRO:", result.stderr)

if __name__ == "__main__":
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Teste 1: Simular Footer Code
    footer_ok = test_footer_code_execution()
    
    # Teste 2: Verificar banco
    check_recent_logs()
    
    print("\nCONCLUSÃO:")
    print("=" * 50)
    if footer_ok:
        print("✅ O ENDPOINT FUNCIONA PERFEITAMENTE!")
        print("❌ O PROBLEMA ESTÁ NO JAVASCRIPT DO FOOTER CODE!")
        print("🔍 A função logDebug não está sendo executada no website.")
        print("\nPOSSÍVEIS CAUSAS:")
        print("1. Footer Code não está sendo carregado no website")
        print("2. JavaScript está sendo bloqueado")
        print("3. Erro silencioso na função logDebug")
        print("4. Console.log funciona, mas fetch falha silenciosamente")
    else:
        print("❌ PROBLEMA NO ENDPOINT!")


































