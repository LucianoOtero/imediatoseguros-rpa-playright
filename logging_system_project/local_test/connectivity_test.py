#!/usr/bin/env python3
"""
🔍 CONNECTIVITY TEST - SISTEMA DE LOGGING PHP
Testa conectividade com servidor mdmidia e banco de dados
"""

import requests
import mysql.connector
import socket
import ssl
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
            'status': 'UNKNOWN'
        }
    
    def run_all_tests(self):
        """Executa todos os testes de conectividade"""
        print("🔍 Testando conectividade...")
        
        try:
            # 1. Teste de Ping
            self.results['tests']['ping'] = self.test_ping()
            
            # 2. Teste HTTP
            self.results['tests']['http'] = self.test_http()
            
            # 3. Teste HTTPS/SSL
            self.results['tests']['https'] = self.test_https()
            
            # 4. Teste de API Endpoint
            self.results['tests']['api'] = self.test_api_endpoint()
            
            # 5. Teste de Banco de Dados
            self.results['tests']['database'] = self.test_database()
            
            # Determinar status geral
            self.determine_overall_status()
            
        except Exception as e:
            self.results['status'] = 'FAILED'
            self.results['error'] = str(e)
            print(f"❌ Erro crítico: {e}")
        
        self.results['duration'] = (datetime.now() - self.results['start_time']).total_seconds()
        return self.results
    
    def test_ping(self):
        """Testa ping para o servidor"""
        print("  📡 Testando ping...")
        start_time = time.time()
        
        try:
            host = self.config['server']['host']
            port = self.config['server'].get('port', 443)
            
            # Tentar conexão TCP
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            duration = time.time() - start_time
            
            if result == 0:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': f'Conexão TCP bem-sucedida para {host}:{port}'
                }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'message': f'Falha na conexão TCP para {host}:{port}'
                }
                
        except Exception as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro no teste de ping: {str(e)}'
            }
    
    def test_http(self):
        """Testa resposta HTTP"""
        print("  🌐 Testando HTTP...")
        start_time = time.time()
        
        try:
            url = f"http://{self.config['server']['host']}"
            response = requests.get(url, timeout=self.config['server']['timeout'])
            
            duration = time.time() - start_time
            
            return {
                'status': 'PASSED' if response.status_code == 200 else 'WARNING',
                'duration': duration,
                'status_code': response.status_code,
                'message': f'HTTP {response.status_code} - {response.reason}'
            }
            
        except requests.exceptions.RequestException as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro HTTP: {str(e)}'
            }
    
    def test_https(self):
        """Testa HTTPS e SSL"""
        print("  🔒 Testando HTTPS/SSL...")
        start_time = time.time()
        
        try:
            url = f"https://{self.config['server']['host']}"
            response = requests.get(url, timeout=self.config['server']['timeout'], verify=True)
            
            duration = time.time() - start_time
            
            # Verificar certificado SSL
            ssl_info = self.get_ssl_info()
            
            return {
                'status': 'PASSED' if response.status_code == 200 else 'WARNING',
                'duration': duration,
                'status_code': response.status_code,
                'ssl_info': ssl_info,
                'message': f'HTTPS {response.status_code} - SSL válido'
            }
            
        except requests.exceptions.SSLError as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro SSL: {str(e)}'
            }
        except requests.exceptions.RequestException as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro HTTPS: {str(e)}'
            }
    
    def get_ssl_info(self):
        """Obtém informações do certificado SSL"""
        try:
            host = self.config['server']['host']
            port = 443
            
            context = ssl.create_default_context()
            with socket.create_connection((host, port), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'subject': cert.get('subject'),
                        'issuer': cert.get('issuer'),
                        'version': cert.get('version'),
                        'notAfter': cert.get('notAfter'),
                        'notBefore': cert.get('notBefore')
                    }
        except Exception as e:
            return {'error': str(e)}
    
    def test_api_endpoint(self):
        """Testa endpoint da API de logging"""
        print("  📡 Testando API endpoint...")
        start_time = time.time()
        
        try:
            # Testar endpoint de logging
            url = f"https://{self.config['server']['host']}/logging_system/debug_logger_db.php"
            
            # Dados de teste
            test_data = {
                'level': 'INFO',
                'message': 'Teste de conectividade',
                'data': {'test': True},
                'url': 'https://test.local',
                'sessionId': 'test_connectivity_123',
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                url,
                json=test_data,
                timeout=self.config['server']['timeout'],
                headers={'Content-Type': 'application/json'}
            )
            
            duration = time.time() - start_time
            
            if response.status_code == 200:
                try:
                    response_data = response.json()
                    return {
                        'status': 'PASSED',
                        'duration': duration,
                        'status_code': response.status_code,
                        'response': response_data,
                        'message': 'API endpoint funcionando corretamente'
                    }
                except json.JSONDecodeError:
                    return {
                        'status': 'WARNING',
                        'duration': duration,
                        'status_code': response.status_code,
                        'message': 'API respondeu mas não retornou JSON válido'
                    }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'status_code': response.status_code,
                    'message': f'API retornou status {response.status_code}'
                }
                
        except requests.exceptions.RequestException as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro na API: {str(e)}'
            }
    
    def test_database(self):
        """Testa conexão com banco de dados"""
        print("  🗄️ Testando banco de dados...")
        start_time = time.time()
        
        try:
            db_config = self.config['database']
            
            # Tentar conexão
            connection = mysql.connector.connect(
                host=db_config['host'],
                port=db_config['port'],
                database=db_config['database'],
                user=db_config['username'],
                password=db_config['password'],
                connection_timeout=10
            )
            
            # Testar query simples
            cursor = connection.cursor()
            cursor.execute("SELECT 1 as test")
            result = cursor.fetchone()
            cursor.close()
            connection.close()
            
            duration = time.time() - start_time
            
            if result and result[0] == 1:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Conexão com banco de dados bem-sucedida'
                }
            else:
                return {
                    'status': 'FAILED',
                    'duration': duration,
                    'message': 'Query de teste falhou'
                }
                
        except mysql.connector.Error as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro MySQL: {str(e)}'
            }
        except Exception as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro de conexão: {str(e)}'
            }
    
    def determine_overall_status(self):
        """Determina status geral baseado nos testes individuais"""
        test_statuses = [test.get('status', 'UNKNOWN') for test in self.results['tests'].values()]
        
        if all(status == 'PASSED' for status in test_statuses):
            self.results['status'] = 'PASSED'
        elif any(status == 'FAILED' for status in test_statuses):
            self.results['status'] = 'FAILED'
        elif any(status == 'WARNING' for status in test_statuses):
            self.results['status'] = 'WARNING'
        else:
            self.results['status'] = 'UNKNOWN'
        
        # Contar resultados
        self.results['summary'] = {
            'total': len(test_statuses),
            'passed': sum(1 for s in test_statuses if s == 'PASSED'),
            'failed': sum(1 for s in test_statuses if s == 'FAILED'),
            'warning': sum(1 for s in test_statuses if s == 'WARNING')
        }
