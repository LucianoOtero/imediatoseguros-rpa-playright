#!/usr/bin/env python3
"""
🛡️ SECURITY TEST - SISTEMA DE LOGGING PHP
Testa segurança do sistema contra ataques comuns
"""

import requests
import json
import time
from datetime import datetime

class SecurityTest:
    def __init__(self, config):
        """Inicializa teste de segurança"""
        self.config = config
        self.results = {
            'start_time': datetime.now(),
            'tests': {},
            'status': 'UNKNOWN'
        }
        self.base_url = f"https://{config['server']['host']}/logging_system/debug_logger_db.php"
    
    def run_all_tests(self):
        """Executa todos os testes de segurança"""
        print("🛡️ Executando testes de segurança...")
        
        try:
            # 1. Teste de SQL Injection
            self.results['tests']['sql_injection'] = self.test_sql_injection()
            
            # 2. Teste de XSS
            self.results['tests']['xss'] = self.test_xss()
            
            # 3. Teste de Rate Limiting
            self.results['tests']['rate_limiting'] = self.test_rate_limiting()
            
            # 4. Teste de CORS
            self.results['tests']['cors'] = self.test_cors()
            
            # 5. Teste de Validação de Entrada
            self.results['tests']['input_validation'] = self.test_input_validation()
            
            # 6. Teste de Tamanho de Dados
            self.results['tests']['data_size'] = self.test_data_size()
            
            # Determinar status geral
            self.determine_overall_status()
            
        except Exception as e:
            self.results['status'] = 'FAILED'
            self.results['error'] = str(e)
            print(f"❌ Erro crítico: {e}")
        
        self.results['duration'] = (datetime.now() - self.results['start_time']).total_seconds()
        return self.results
    
    def test_sql_injection(self):
        """Testa proteção contra SQL injection"""
        print("  💉 Testando SQL injection...")
        start_time = time.time()
        
        # Payloads de SQL injection comuns
        sql_payloads = [
            "'; DROP TABLE debug_logs; --",
            "' OR '1'='1",
            "' UNION SELECT * FROM users --",
            "'; INSERT INTO debug_logs VALUES (1, 'hack', 'hack'); --",
            "' OR 1=1 --",
            "admin'--",
            "' OR 'x'='x",
            "') OR ('1'='1",
            "1' OR '1'='1' --",
            "'; EXEC xp_cmdshell('dir'); --"
        ]
        
        vulnerable_payloads = []
        protected_payloads = []
        
        for payload in sql_payloads:
            test_data = {
                'level': 'INFO',
                'message': f'Teste SQL injection: {payload}',
                'data': {'payload': payload},
                'url': 'https://test.local',
                'sessionId': f'sql_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                
                # Verificar se a resposta indica vulnerabilidade
                response_text = response.text.lower()
                if any(keyword in response_text for keyword in ['error', 'mysql', 'sql', 'syntax', 'database']):
                    vulnerable_payloads.append(payload)
                else:
                    protected_payloads.append(payload)
                
            except Exception as e:
                # Erro de conexão não indica vulnerabilidade SQL
                protected_payloads.append(payload)
        
        duration = time.time() - start_time
        
        if vulnerable_payloads:
            return {
                'status': 'FAILED',
                'duration': duration,
                'message': f'Vulnerabilidade SQL injection detectada: {len(vulnerable_payloads)} payloads',
                'vulnerable_payloads': vulnerable_payloads,
                'protected_payloads': protected_payloads
            }
        else:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Proteção contra SQL injection adequada',
                'tested_payloads': len(sql_payloads),
                'protected_payloads': protected_payloads
            }
    
    def test_xss(self):
        """Testa proteção contra XSS"""
        print("  🎯 Testando XSS...")
        start_time = time.time()
        
        # Payloads de XSS comuns
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert('XSS')>",
            "javascript:alert('XSS')",
            "<svg onload=alert('XSS')>",
            "<iframe src=javascript:alert('XSS')></iframe>",
            "<body onload=alert('XSS')>",
            "<input onfocus=alert('XSS') autofocus>",
            "<select onfocus=alert('XSS') autofocus>",
            "<textarea onfocus=alert('XSS') autofocus>",
            "<keygen onfocus=alert('XSS') autofocus>"
        ]
        
        vulnerable_payloads = []
        protected_payloads = []
        
        for payload in xss_payloads:
            test_data = {
                'level': 'INFO',
                'message': f'Teste XSS: {payload}',
                'data': {'payload': payload},
                'url': 'https://test.local',
                'sessionId': f'xss_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                
                # Verificar se o payload foi sanitizado
                response_text = response.text
                if payload in response_text:
                    vulnerable_payloads.append(payload)
                else:
                    protected_payloads.append(payload)
                
            except Exception as e:
                protected_payloads.append(payload)
        
        duration = time.time() - start_time
        
        if vulnerable_payloads:
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': f'Possível vulnerabilidade XSS: {len(vulnerable_payloads)} payloads',
                'vulnerable_payloads': vulnerable_payloads,
                'protected_payloads': protected_payloads
            }
        else:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Proteção contra XSS adequada',
                'tested_payloads': len(xss_payloads),
                'protected_payloads': protected_payloads
            }
    
    def test_rate_limiting(self):
        """Testa rate limiting"""
        print("  🚦 Testando rate limiting...")
        start_time = time.time()
        
        # Tentar enviar muitas requisições rapidamente
        num_requests = 20
        successful_requests = 0
        rate_limited_requests = 0
        other_failed_requests = 0
        
        for i in range(num_requests):
            test_data = {
                'level': 'INFO',
                'message': f'Teste rate limiting #{i+1}',
                'data': {'test': 'rate_limiting', 'iteration': i+1},
                'url': 'https://test.local',
                'sessionId': f'rate_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                
                if response.status_code == 200:
                    successful_requests += 1
                elif response.status_code == 429:  # Too Many Requests
                    rate_limited_requests += 1
                else:
                    other_failed_requests += 1
                
                # Pequena pausa entre requisições
                time.sleep(0.1)
                
            except Exception as e:
                other_failed_requests += 1
        
        duration = time.time() - start_time
        
        # Se houve rate limiting, é bom sinal
        if rate_limited_requests > 0:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': f'Rate limiting funcionando: {rate_limited_requests} requisições bloqueadas',
                'metrics': {
                    'total_requests': num_requests,
                    'successful_requests': successful_requests,
                    'rate_limited_requests': rate_limited_requests,
                    'other_failed_requests': other_failed_requests
                }
            }
        elif successful_requests == num_requests:
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': 'Rate limiting não detectado - pode estar desabilitado',
                'metrics': {
                    'total_requests': num_requests,
                    'successful_requests': successful_requests,
                    'rate_limited_requests': rate_limited_requests,
                    'other_failed_requests': other_failed_requests
                }
            }
        else:
            return {
                'status': 'FAILED',
                'duration': duration,
                'message': f'Muitas falhas sem rate limiting: {other_failed_requests}',
                'metrics': {
                    'total_requests': num_requests,
                    'successful_requests': successful_requests,
                    'rate_limited_requests': rate_limited_requests,
                    'other_failed_requests': other_failed_requests
                }
            }
    
    def test_cors(self):
        """Testa política CORS"""
        print("  🌐 Testando CORS...")
        start_time = time.time()
        
        # Testar diferentes origens
        test_origins = [
            'https://www.segurosimediato.com.br',
            'https://segurosimediato.com.br',
            'https://malicious-site.com',
            'http://localhost:3000',
            'https://localhost:3000'
        ]
        
        cors_results = {}
        
        for origin in test_origins:
            headers = {
                'Origin': origin,
                'Content-Type': 'application/json'
            }
            
            test_data = {
                'level': 'INFO',
                'message': f'Teste CORS de {origin}',
                'data': {'origin': origin},
                'url': origin,
                'sessionId': f'cors_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    headers=headers,
                    timeout=self.config['server']['timeout']
                )
                
                # Verificar headers CORS na resposta
                cors_headers = {
                    'Access-Control-Allow-Origin': response.headers.get('Access-Control-Allow-Origin'),
                    'Access-Control-Allow-Methods': response.headers.get('Access-Control-Allow-Methods'),
                    'Access-Control-Allow-Headers': response.headers.get('Access-Control-Allow-Headers')
                }
                
                cors_results[origin] = {
                    'status_code': response.status_code,
                    'cors_headers': cors_headers,
                    'allowed': cors_headers.get('Access-Control-Allow-Origin') == '*' or 
                             cors_headers.get('Access-Control-Allow-Origin') == origin
                }
                
            except Exception as e:
                cors_results[origin] = {
                    'error': str(e),
                    'allowed': False
                }
        
        duration = time.time() - start_time
        
        # Verificar se CORS está configurado corretamente
        malicious_allowed = cors_results.get('https://malicious-site.com', {}).get('allowed', False)
        legitimate_allowed = any(
            cors_results.get(origin, {}).get('allowed', False) 
            for origin in ['https://www.segurosimediato.com.br', 'https://segurosimediato.com.br']
        )
        
        if malicious_allowed:
            return {
                'status': 'FAILED',
                'duration': duration,
                'message': 'CORS muito permissivo - permite origens maliciosas',
                'cors_results': cors_results
            }
        elif not legitimate_allowed:
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': 'CORS muito restritivo - pode bloquear origens legítimas',
                'cors_results': cors_results
            }
        else:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Política CORS adequada',
                'cors_results': cors_results
            }
    
    def test_input_validation(self):
        """Testa validação de entrada"""
        print("  ✅ Testando validação de entrada...")
        start_time = time.time()
        
        # Testes de validação
        validation_tests = [
            {
                'name': 'Campos obrigatórios faltando',
                'data': {'level': 'INFO'},  # Sem message
                'should_fail': True
            },
            {
                'name': 'Level inválido',
                'data': {
                    'level': 'INVALID_LEVEL',
                    'message': 'Teste'
                },
                'should_fail': True
            },
            {
                'name': 'Message vazio',
                'data': {
                    'level': 'INFO',
                    'message': ''
                },
                'should_fail': True
            },
            {
                'name': 'Dados válidos',
                'data': {
                    'level': 'INFO',
                    'message': 'Teste válido',
                    'data': {'test': True},
                    'url': 'https://test.local',
                    'sessionId': 'test_123',
                    'timestamp': datetime.now().isoformat()
                },
                'should_fail': False
            }
        ]
        
        validation_results = []
        
        for test in validation_tests:
            try:
                response = requests.post(
                    self.base_url,
                    json=test['data'],
                    timeout=self.config['server']['timeout']
                )
                
                # Verificar se o comportamento está correto
                if test['should_fail']:
                    # Deveria falhar (status 400)
                    if response.status_code == 400:
                        validation_results.append({
                            'test': test['name'],
                            'status': 'PASSED',
                            'message': 'Validação funcionando corretamente'
                        })
                    else:
                        validation_results.append({
                            'test': test['name'],
                            'status': 'FAILED',
                            'message': f'Deveria falhar mas retornou {response.status_code}'
                        })
                else:
                    # Deveria passar (status 200)
                    if response.status_code == 200:
                        validation_results.append({
                            'test': test['name'],
                            'status': 'PASSED',
                            'message': 'Validação funcionando corretamente'
                        })
                    else:
                        validation_results.append({
                            'test': test['name'],
                            'status': 'FAILED',
                            'message': f'Deveria passar mas retornou {response.status_code}'
                        })
                
            except Exception as e:
                validation_results.append({
                    'test': test['name'],
                    'status': 'FAILED',
                    'message': f'Erro na requisição: {e}'
                })
        
        duration = time.time() - start_time
        
        passed_tests = sum(1 for r in validation_results if r['status'] == 'PASSED')
        total_tests = len(validation_results)
        
        if passed_tests == total_tests:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Validação de entrada funcionando corretamente',
                'validation_results': validation_results
            }
        else:
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': f'Validação de entrada com problemas: {passed_tests}/{total_tests} testes passaram',
                'validation_results': validation_results
            }
    
    def test_data_size(self):
        """Testa limite de tamanho de dados"""
        print("  📏 Testando limite de tamanho...")
        start_time = time.time()
        
        # Testar diferentes tamanhos de dados
        size_tests = [
            {'size': '1KB', 'data': 'x' * 1024},
            {'size': '10KB', 'data': 'x' * 10240},
            {'size': '50KB', 'data': 'x' * 51200},
            {'size': '100KB', 'data': 'x' * 102400}
        ]
        
        size_results = []
        
        for test in size_tests:
            test_data = {
                'level': 'INFO',
                'message': f'Teste de tamanho {test["size"]}',
                'data': {'large_data': test['data']},
                'url': 'https://test.local',
                'sessionId': f'size_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                
                size_results.append({
                    'size': test['size'],
                    'status_code': response.status_code,
                    'success': response.status_code == 200,
                    'response_size': len(response.text)
                })
                
            except Exception as e:
                size_results.append({
                    'size': test['size'],
                    'error': str(e),
                    'success': False
                })
        
        duration = time.time() - start_time
        
        # Verificar se há limite de tamanho implementado
        large_data_failed = any(
            not r.get('success', False) for r in size_results 
            if r['size'] in ['50KB', '100KB']
        )
        
        if large_data_failed:
            return {
                'status': 'PASSED',
                'duration': duration,
                'message': 'Limite de tamanho implementado corretamente',
                'size_results': size_results
            }
        else:
            return {
                'status': 'WARNING',
                'duration': duration,
                'message': 'Limite de tamanho pode não estar implementado',
                'size_results': size_results
            }
    
    def determine_overall_status(self):
        """Determina status geral baseado nos testes"""
        test_statuses = [test.get('status', 'UNKNOWN') for test in self.results['tests'].values()]
        
        if any(status == 'FAILED' for status in test_statuses):
            self.results['status'] = 'FAILED'
        elif any(status == 'WARNING' for status in test_statuses):
            self.results['status'] = 'WARNING'
        elif all(status == 'PASSED' for status in test_statuses):
            self.results['status'] = 'PASSED'
        else:
            self.results['status'] = 'UNKNOWN'
        
        # Contar resultados
        self.results['summary'] = {
            'total_tests': len(test_statuses),
            'passed': sum(1 for s in test_statuses if s == 'PASSED'),
            'failed': sum(1 for s in test_statuses if s == 'FAILED'),
            'warning': sum(1 for s in test_statuses if s == 'WARNING')
        }


