#!/usr/bin/env python3
"""
Teste Direto da API com Banco de Dados
"""

import requests
import json
from datetime import datetime

def test_database_api():
    """Testa a API que usa banco de dados"""
    print("Testando API com banco de dados...")
    
    test_data = {
        'message': 'Teste direto do banco de dados',
        'level': 'INFO',
        'timestamp': datetime.now().isoformat(),
        'sessionId': 'test_db_direct',
        'userAgent': 'TestDB/1.0',
        'url': 'https://test.com',
        'data': {'test': True, 'database': True}
    }
    
    try:
        response = requests.post(
            'https://mdmidia.com.br/debug_logger_db.php',
            json=test_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Method: {result.get('method', 'unknown')}")
            print(f"Success: {result.get('success', False)}")
            return True
        else:
            print(f"Erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return False

def test_file_api():
    """Testa a API que usa arquivos"""
    print("\nTestando API com arquivos...")
    
    test_data = {
        'message': 'Teste direto dos arquivos',
        'level': 'INFO',
        'timestamp': datetime.now().isoformat(),
        'sessionId': 'test_file_direct',
        'userAgent': 'TestFile/1.0',
        'url': 'https://test.com',
        'data': {'test': True, 'file': True}
    }
    
    try:
        response = requests.post(
            'https://mdmidia.com.br/debug_logger.php',
            json=test_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Method: {result.get('method', 'unknown')}")
            print(f"Success: {result.get('success', False)}")
            return True
        else:
            print(f"Erro: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Erro na requisição: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DIRETO DAS APIs")
    print("=" * 60)
    
    # Testar API com banco
    db_success = test_database_api()
    
    # Testar API com arquivos
    file_success = test_file_api()
    
    print("\n" + "=" * 60)
    print("RESULTADOS:")
    print(f"API Banco de Dados: {'OK' if db_success else 'ERRO'}")
    print(f"API Arquivos: {'OK' if file_success else 'ERRO'}")
    print("=" * 60)
