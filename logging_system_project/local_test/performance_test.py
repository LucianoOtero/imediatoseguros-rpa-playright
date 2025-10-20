#!/usr/bin/env python3
"""
⚡ PERFORMANCE TEST - SISTEMA DE LOGGING PHP
Testa performance e throughput do sistema de logging
"""

import requests
import time
import statistics
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

class PerformanceTest:
    def __init__(self, config):
        """Inicializa teste de performance"""
        self.config = config
        self.results = {
            'start_time': datetime.now(),
            'tests': {},
            'status': 'UNKNOWN'
        }
        self.base_url = f"https://{config['server']['host']}/logging_system/debug_logger_db.php"
    
    def run_all_tests(self):
        """Executa todos os testes de performance"""
        print("⚡ Executando testes de performance...")
        
        try:
            # 1. Teste de Latência
            self.results['tests']['latency'] = self.test_latency()
            
            # 2. Teste de Throughput
            self.results['tests']['throughput'] = self.test_throughput()
            
            # 3. Teste de Concorrência
            self.results['tests']['concurrency'] = self.test_concurrency()
            
            # 4. Teste de Volume
            self.results['tests']['volume'] = self.test_volume()
            
            # 5. Teste de Stress
            self.results['tests']['stress'] = self.test_stress()
            
            # Determinar status geral
            self.determine_overall_status()
            
        except Exception as e:
            self.results['status'] = 'FAILED'
            self.results['error'] = str(e)
            print(f"❌ Erro crítico: {e}")
        
        self.results['duration'] = (datetime.now() - self.results['start_time']).total_seconds()
        return self.results
    
    def test_latency(self):
        """Testa latência de resposta"""
        print("  ⏱️ Testando latência...")
        start_time = time.time()
        
        test_data = {
            'level': 'INFO',
            'message': 'Teste de latência',
            'data': {'test': 'latency'},
            'url': 'https://test.local',
            'sessionId': f'latency_test_{int(time.time())}',
            'timestamp': datetime.now().isoformat()
        }
        
        latencies = []
        successful_requests = 0
        failed_requests = 0
        
        # Executar 10 requisições para calcular latência média
        for i in range(10):
            try:
                request_start = time.time()
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                request_end = time.time()
                
                latency = request_end - request_start
                latencies.append(latency)
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                    print(f"    ⚠️ Requisição {i+1} falhou: HTTP {response.status_code}")
                
                # Pequena pausa entre requisições
                time.sleep(0.1)
                
            except Exception as e:
                failed_requests += 1
                print(f"    ❌ Requisição {i+1} erro: {e}")
        
        duration = time.time() - start_time
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            min_latency = min(latencies)
            max_latency = max(latencies)
            median_latency = statistics.median(latencies)
            
            # Definir limites de latência aceitável
            max_acceptable_latency = 2.0  # 2 segundos
            
            if avg_latency > max_acceptable_latency:
                status = 'WARNING'
                message = f'Latência média alta: {avg_latency:.3f}s'
            else:
                status = 'PASSED'
                message = f'Latência adequada: {avg_latency:.3f}s'
            
            return {
                'status': status,
                'duration': duration,
                'message': message,
                'metrics': {
                    'avg_latency': avg_latency,
                    'min_latency': min_latency,
                    'max_latency': max_latency,
                    'median_latency': median_latency,
                    'successful_requests': successful_requests,
                    'failed_requests': failed_requests,
                    'success_rate': (successful_requests / (successful_requests + failed_requests)) * 100
                }
            }
        else:
            return {
                'status': 'FAILED',
                'duration': duration,
                'message': 'Nenhuma requisição bem-sucedida',
                'metrics': {
                    'successful_requests': 0,
                    'failed_requests': failed_requests
                }
            }
    
    def test_throughput(self):
        """Testa throughput (requisições por minuto)"""
        print("  📊 Testando throughput...")
        start_time = time.time()
        
        test_data = {
            'level': 'INFO',
            'message': 'Teste de throughput',
            'data': {'test': 'throughput'},
            'url': 'https://test.local',
            'sessionId': f'throughput_test_{int(time.time())}',
            'timestamp': datetime.now().isoformat()
        }
        
        successful_requests = 0
        failed_requests = 0
        start_time_throughput = time.time()
        
        # Executar requisições por 30 segundos
        test_duration = 30
        end_time = start_time_throughput + test_duration
        
        while time.time() < end_time:
            try:
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                
                # Pequena pausa para não sobrecarregar
                time.sleep(0.05)
                
            except Exception as e:
                failed_requests += 1
        
        actual_duration = time.time() - start_time_throughput
        throughput_rpm = (successful_requests / actual_duration) * 60
        
        # Definir throughput mínimo esperado
        min_throughput = 50  # 50 requisições por minuto
        
        if throughput_rpm < min_throughput:
            status = 'WARNING'
            message = f'Throughput baixo: {throughput_rpm:.1f} req/min'
        else:
            status = 'PASSED'
            message = f'Throughput adequado: {throughput_rpm:.1f} req/min'
        
        duration = time.time() - start_time
        
        return {
            'status': status,
            'duration': duration,
            'message': message,
            'metrics': {
                'throughput_rpm': throughput_rpm,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'test_duration': actual_duration,
                'success_rate': (successful_requests / (successful_requests + failed_requests)) * 100,
                'min_acceptable_throughput': min_throughput
            }
        }
    
    def test_concurrency(self):
        """Testa requisições concorrentes"""
        print("  🔄 Testando concorrência...")
        start_time = time.time()
        
        concurrent_users = self.config['test_data']['concurrent_users']
        
        def send_concurrent_request(user_id):
            test_data = {
                'level': 'INFO',
                'message': f'Teste concorrente usuário {user_id}',
                'data': {'user_id': user_id, 'test': 'concurrency'},
                'url': 'https://test.local',
                'sessionId': f'concurrency_test_{user_id}_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                request_start = time.time()
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                request_end = time.time()
                
                return {
                    'user_id': user_id,
                    'status_code': response.status_code,
                    'latency': request_end - request_start,
                    'success': response.status_code == 200
                }
            except Exception as e:
                return {
                    'user_id': user_id,
                    'error': str(e),
                    'success': False
                }
        
        # Executar requisições concorrentes
        results = []
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(send_concurrent_request, i) for i in range(concurrent_users)]
            for future in as_completed(futures):
                results.append(future.result())
        
        successful_requests = sum(1 for r in results if r.get('success', False))
        failed_requests = len(results) - successful_requests
        
        if results:
            latencies = [r.get('latency', 0) for r in results if 'latency' in r]
            avg_latency = statistics.mean(latencies) if latencies else 0
        else:
            avg_latency = 0
        
        duration = time.time() - start_time
        
        success_rate = (successful_requests / len(results)) * 100 if results else 0
        
        if success_rate < 90:  # Menos de 90% de sucesso
            status = 'WARNING'
            message = f'Taxa de sucesso baixa em concorrência: {success_rate:.1f}%'
        else:
            status = 'PASSED'
            message = f'Concorrência adequada: {success_rate:.1f}% de sucesso'
        
        return {
            'status': status,
            'duration': duration,
            'message': message,
            'metrics': {
                'concurrent_users': concurrent_users,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'success_rate': success_rate,
                'avg_latency': avg_latency,
                'results': results
            }
        }
    
    def test_volume(self):
        """Testa volume alto de dados"""
        print("  📈 Testando volume alto...")
        start_time = time.time()
        
        # Criar dados grandes para testar limite de tamanho
        large_data = {
            'level': 'INFO',
            'message': 'Teste de volume alto',
            'data': {
                'large_string': 'x' * 5000,  # 5KB de dados
                'array': list(range(1000)),
                'nested_object': {
                    'level1': {
                        'level2': {
                            'level3': 'deep_value'
                        }
                    }
                }
            },
            'url': 'https://test.local',
            'sessionId': f'volume_test_{int(time.time())}',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            request_start = time.time()
            response = requests.post(
                self.base_url,
                json=large_data,
                timeout=self.config['server']['timeout']
            )
            request_end = time.time()
            
            duration = time.time() - start_time
            latency = request_end - request_start
            
            if response.status_code == 200:
                return {
                    'status': 'PASSED',
                    'duration': duration,
                    'message': 'Volume alto processado com sucesso',
                    'metrics': {
                        'latency': latency,
                        'data_size': len(json.dumps(large_data)),
                        'status_code': response.status_code
                    }
                }
            else:
                return {
                    'status': 'WARNING',
                    'duration': duration,
                    'message': f'Volume alto retornou status {response.status_code}',
                    'metrics': {
                        'latency': latency,
                        'data_size': len(json.dumps(large_data)),
                        'status_code': response.status_code,
                        'response': response.text[:200]
                    }
                }
                
        except Exception as e:
            return {
                'status': 'FAILED',
                'duration': time.time() - start_time,
                'message': f'Erro no teste de volume: {e}',
                'metrics': {
                    'error': str(e)
                }
            }
    
    def test_stress(self):
        """Teste de stress (requisições intensivas)"""
        print("  💪 Testando stress...")
        start_time = time.time()
        
        # Executar muitas requisições rapidamente
        num_requests = 50
        successful_requests = 0
        failed_requests = 0
        latencies = []
        
        for i in range(num_requests):
            test_data = {
                'level': 'INFO',
                'message': f'Teste de stress #{i+1}',
                'data': {'test': 'stress', 'iteration': i+1},
                'url': 'https://test.local',
                'sessionId': f'stress_test_{int(time.time())}',
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                request_start = time.time()
                response = requests.post(
                    self.base_url,
                    json=test_data,
                    timeout=self.config['server']['timeout']
                )
                request_end = time.time()
                
                latency = request_end - request_start
                latencies.append(latency)
                
                if response.status_code == 200:
                    successful_requests += 1
                else:
                    failed_requests += 1
                
            except Exception as e:
                failed_requests += 1
        
        duration = time.time() - start_time
        
        if latencies:
            avg_latency = statistics.mean(latencies)
            max_latency = max(latencies)
        else:
            avg_latency = 0
            max_latency = 0
        
        success_rate = (successful_requests / num_requests) * 100
        
        # Critérios de stress test
        if success_rate < 80:  # Menos de 80% de sucesso
            status = 'FAILED'
            message = f'Stress test falhou: {success_rate:.1f}% de sucesso'
        elif avg_latency > 5.0:  # Latência média > 5s
            status = 'WARNING'
            message = f'Stress test com latência alta: {avg_latency:.3f}s'
        else:
            status = 'PASSED'
            message = f'Stress test passou: {success_rate:.1f}% sucesso, {avg_latency:.3f}s latência'
        
        return {
            'status': status,
            'duration': duration,
            'message': message,
            'metrics': {
                'total_requests': num_requests,
                'successful_requests': successful_requests,
                'failed_requests': failed_requests,
                'success_rate': success_rate,
                'avg_latency': avg_latency,
                'max_latency': max_latency,
                'requests_per_second': num_requests / duration
            }
        }
    
    def determine_overall_status(self):
        """Determina status geral baseado nos testes"""
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
            'total_tests': len(test_statuses),
            'passed': sum(1 for s in test_statuses if s == 'PASSED'),
            'failed': sum(1 for s in test_statuses if s == 'FAILED'),
            'warning': sum(1 for s in test_statuses if s == 'WARNING')
        }
