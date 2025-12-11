#!/usr/bin/env python3
"""
Teste Direto do Endpoint de Logging
Investigacao do problema de sensibilizacao
"""

import requests
import json
from datetime import datetime

def test_endpoint_direct():
    """Testa o endpoint diretamente"""
    url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    # Dados de teste exatamente como o Footer Code envia
    test_data = {
        'level': 'INFO',
        'message': '[CONFIG] RPA habilitado via PHP Log',
        'data': {'rpaEnabled': False},
        'timestamp': datetime.now().isoformat(),
        'sessionId': 'test_direct_' + str(int(datetime.now().timestamp())),
        'url': 'https://www.segurosimediato.com.br',
        'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    print("TESTE DIRETO DO ENDPOINT")
    print("=" * 40)
    print(f"URL: {url}")
    print(f"Dados: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
    print()
    
    try:
        response = requests.post(
            url,
            headers={'Content-Type': 'application/json'},
            json=test_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('success'):
                    print("SUCESSO: Log enviado com sucesso!")
                    return True
                else:
                    print(f"ERRO: {result.get('error', 'Erro desconhecido')}")
                    return False
            except:
                print("ERRO: Resposta nao e JSON valido")
                return False
        else:
            print(f"ERRO HTTP: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXAO: {e}")
        return False

def test_cors_preflight():
    """Testa requisicao OPTIONS (preflight)"""
    url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    print("\nTESTE CORS PREFLIGHT")
    print("=" * 40)
    
    try:
        response = requests.options(
            url,
            headers={
                'Origin': 'https://www.segurosimediato.com.br',
                'Access-Control-Request-Method': 'POST',
                'Access-Control-Request-Headers': 'Content-Type'
            },
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
        
        return response.status_code == 200
        
    except requests.exceptions.RequestException as e:
        print(f"ERRO DE CONEXAO: {e}")
        return False

if __name__ == "__main__":
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Teste 1: Requisicao OPTIONS
    cors_ok = test_cors_preflight()
    
    # Teste 2: Requisicao POST
    post_ok = test_endpoint_direct()
    
    print("\nRESUMO DOS TESTES:")
    print("=" * 40)
    print(f"CORS Preflight: {'OK' if cors_ok else 'FALHOU'}")
    print(f"POST Request: {'OK' if post_ok else 'FALHOU'}")
    
    if cors_ok and post_ok:
        print("\nENDPOINT FUNCIONANDO PERFEITAMENTE!")
        print("O problema pode estar no JavaScript do Footer Code.")
    else:
        print("\nPROBLEMA NO ENDPOINT!")
        print("Verificar configuracao do servidor.")