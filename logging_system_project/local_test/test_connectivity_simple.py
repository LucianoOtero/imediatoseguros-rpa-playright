#!/usr/bin/env python3
"""
Teste Simples de Conectividade - Sistema de Logging PHP
Testa apenas conectividade básica com o servidor
"""

import requests
import time
from datetime import datetime

def test_server_connectivity():
    """Testa conectividade básica com o servidor"""
    print("Testando conectividade com mdmidia.com.br...")
    
    # Teste HTTPS
    try:
        print("1. Testando HTTPS...")
        start_time = time.time()
        response = requests.get("https://mdmidia.com.br", timeout=10)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"   OK HTTPS: {response.status_code} ({duration:.2f}s)")
        else:
            print(f"   ERRO HTTPS: {response.status_code} ({duration:.2f}s)")
            
    except Exception as e:
        print(f"   ERRO HTTPS: {e}")
    
    # Teste HTTP
    try:
        print("2. Testando HTTP...")
        start_time = time.time()
        response = requests.get("http://mdmidia.com.br", timeout=10)
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"   OK HTTP: {response.status_code} ({duration:.2f}s)")
        else:
            print(f"   ERRO HTTP: {response.status_code} ({duration:.2f}s)")
            
    except Exception as e:
        print(f"   ERRO HTTP: {e}")
    
    # Teste API de logging atual
    try:
        print("3. Testando API atual (debug_logger.php)...")
        start_time = time.time()
        
        test_data = {
            'message': 'Teste de conectividade',
            'level': 'INFO',
            'timestamp': datetime.now().isoformat(),
            'sessionId': 'test_connectivity',
            'userAgent': 'TestRunner/1.0'
        }
        
        response = requests.post(
            "https://mdmidia.com.br/debug_logger.php",
            json=test_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"   OK API: {response.status_code} ({duration:.2f}s)")
            try:
                result = response.json()
                print(f"   Resposta: {result.get('success', 'N/A')}")
            except:
                print(f"   Resposta: {response.text[:100]}...")
        else:
            print(f"   ERRO API: {response.status_code} ({duration:.2f}s)")
            
    except Exception as e:
        print(f"   ERRO API: {e}")
    
    # Teste API nova (que criamos)
    try:
        print("4. Testando API nova (debug_logger_db.php)...")
        start_time = time.time()
        
        test_data = {
            'message': 'Teste de conectividade',
            'level': 'INFO',
            'timestamp': datetime.now().isoformat(),
            'sessionId': 'test_connectivity',
            'userAgent': 'TestRunner/1.0'
        }
        
        response = requests.post(
            "https://mdmidia.com.br/debug_logger_db.php",
            json=test_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        duration = time.time() - start_time
        
        if response.status_code == 200:
            print(f"   OK API Nova: {response.status_code} ({duration:.2f}s)")
            try:
                result = response.json()
                print(f"   Resposta: {result.get('success', 'N/A')}")
            except:
                print(f"   Resposta: {response.text[:100]}...")
        else:
            print(f"   ERRO API Nova: {response.status_code} ({duration:.2f}s)")
            
    except Exception as e:
        print(f"   ERRO API Nova: {e}")

def test_database_connection():
    """Testa conectividade com banco de dados"""
    print("\nTestando conectividade com banco de dados...")
    
    try:
        import mysql.connector
        
        print("1. Testando conexão MySQL...")
        start_time = time.time()
        
        connection = mysql.connector.connect(
            host='localhost',
            port=3306,
            user='rpa_logger',
            password='senha_super_segura_123!',
            database='rpa_logs',
            connection_timeout=10
        )
        
        duration = time.time() - start_time
        print(f"   OK MySQL: Conexão estabelecida ({duration:.2f}s)")
        
        # Testar query simples
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM logs")
        count = cursor.fetchone()[0]
        print(f"   Logs no banco: {count}")
        
        cursor.close()
        connection.close()
        
    except Exception as e:
        print(f"   ERRO MySQL: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("TESTE DE CONECTIVIDADE - SISTEMA DE LOGGING PHP")
    print("=" * 60)
    
    test_server_connectivity()
    test_database_connection()
    
    print("\n" + "=" * 60)
    print("TESTE CONCLUIDO")
    print("=" * 60)
