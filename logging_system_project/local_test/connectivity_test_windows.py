#!/usr/bin/env python3
"""
Teste de Conectividade - Sistema de Logging PHP (Versão Windows)
Testa conectividade com servidor e banco de dados
"""

import requests
import mysql.connector
import time
from datetime import datetime
import json

class ConnectivityTest:
    def __init__(self, config):
        """Inicializa teste de conectividade"""
        self.config = config
        self.results = {
            'start_time': datetime.now(),
            'tests': {},
            'summary': {}
        }
    
    def run_all_tests(self):
        """Executa todos os testes de conectividade"""
        print("Testando conectividade...")
        
        try:
            # Teste 1: Conectividade HTTP
            self.results['tests']['http_connectivity'] = self.test_http_connectivity()
            
            # Teste 2: Conectividade HTTPS
            self.results['tests']['https_connectivity'] = self.test_https_connectivity()
            
            # Teste 3: Conectividade SSH
            self.results['tests']['ssh_connectivity'] = self.test_ssh_connectivity()
            
            # Teste 4: Conectividade MySQL
            self.results['tests']['mysql_connectivity'] = self.test_mysql_connectivity()
            
            # Teste 5: Conectividade API
            self.results['tests']['api_connectivity'] = self.test_api_connectivity()
            
        except Exception as e:
            self.results['summary']['error'] = str(e)
            print(f"ERRO: {e}")
        
        # Gerar resumo
        self.generate_summary()
        
        return self.results
    
    def test_http_connectivity(self):
        """Testa conectividade HTTP"""
        start_time = time.time()
        try:
            url = f"http://{self.config['server']['host']}"
            response = requests.get(url, timeout=self.config['server']['timeout'])
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'response_time': duration
                }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'error': f'HTTP {response.status_code}'
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
    
    def test_https_connectivity(self):
        """Testa conectividade HTTPS"""
        start_time = time.time()
        try:
            url = f"https://{self.config['server']['host']}"
            response = requests.get(url, timeout=self.config['server']['timeout'])
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'response_time': duration
                }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'error': f'HTTPS {response.status_code}'
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
    
    def test_ssh_connectivity(self):
        """Testa conectividade SSH"""
        start_time = time.time()
        try:
            # Simular teste SSH (sem paramiko para evitar dependências)
            duration = time.time() - start_time
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': 'Teste SSH requer paramiko - pulado'
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
    
    def test_mysql_connectivity(self):
        """Testa conectividade MySQL"""
        start_time = time.time()
        try:
            db_config = self.config['database']
            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                user=db_config['username'],
                password=db_config['password'],
                database=db_config['database'],
                connection_timeout=10
            )
            connection.close()
            duration = time.time() - start_time
            
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Conexão MySQL bem-sucedida'
            }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
    
    def test_api_connectivity(self):
        """Testa conectividade com API de logging"""
        start_time = time.time()
        try:
            url = f"http://{self.config['server']['host']}:{self.config['server']['port']}/debug_logger_db.php"
            test_data = {
                'message': 'Teste de conectividade',
                'level': 'INFO',
                'timestamp': datetime.now().isoformat(),
                'sessionId': 'test_connectivity',
                'userAgent': 'TestRunner/1.0'
            }
            
            response = requests.post(
                url,
                json=test_data,
                timeout=self.config['server']['timeout'],
                headers={'Content-Type': 'application/json'}
            )
            duration = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'response_time': duration
                }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'response_code': response.status_code,
                    'error': f'API retornou {response.status_code}'
                }
        except Exception as e:
            duration = time.time() - start_time
            return {
                'status': 'FAILED',
                'duration': duration,
                'error': str(e)
            }
    
    def generate_summary(self):
        """Gera resumo dos testes"""
        total_tests = len(self.results['tests'])
        passed_tests = sum(1 for test in self.results['tests'].values() 
                          if test.get('status') == 'PASSED')
        failed_tests = sum(1 for test in self.results['tests'].values() 
                          if test.get('status') == 'FAILED')
        warning_tests = sum(1 for test in self.results['tests'].values() 
                           if test.get('status') == 'WARNING')
        
        self.results['summary'] = {
            'total_tests': total_tests,
            'passed_tests': passed_tests,
            'failed_tests': failed_tests,
            'warning_tests': warning_tests,
            'success_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            'end_time': datetime.now(),
            'total_duration': (datetime.now() - self.results['start_time']).total_seconds()
        }
        
        # Status geral
        if failed_tests == 0:
            self.results['status'] = 'PASSED'
        elif passed_tests > 0:
            self.results['status'] = 'WARNING'
        else:
            self.results['status'] = 'FAILED'
        
        self.results['duration'] = self.results['summary']['total_duration']
        
        print(f"Conectividade: {self.results['status']} ({passed_tests}/{total_tests} OK)")

if __name__ == "__main__":
    # Teste standalone
    config = {
        "server": {
            "host": "mdmidia.com.br",
            "port": 443,
            "protocol": "https",
            "timeout": 30
        },
        "database": {
            "host": "localhost",
            "port": 3306,
            "database": "rpa_logs",
            "username": "rpa_logger",
            "password": "senha_super_segura_123!"
        }
    }
    
    test = ConnectivityTest(config)
    results = test.run_all_tests()
    print(f"\nResultado final: {results['status']}")


