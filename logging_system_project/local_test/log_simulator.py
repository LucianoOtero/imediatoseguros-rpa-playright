#!/usr/bin/env python3
"""
📝 LOG SIMULATOR - SISTEMA DE LOGGING PHP
Simula logs do Footer Code e Injection para teste do sistema
"""

import requests
import json
import time
import random
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

class LogSimulator:
    def __init__(self, config):
        """Inicializa simulador de logs"""
        self.config = config
        self.results = {
            'start_time': datetime.now(),
            'simulations': {},
            'status': 'UNKNOWN'
        }
        self.base_url = f"https://{config['server']['host']}/logging_system/debug_logger_db.php"
    
    def run_all_simulations(self):
        """Executa todas as simulações de log"""
        print("📝 Executando simulações de log...")
        
        try:
            # 1. Simulação Footer Code
            self.results['simulations']['footer_code'] = self.simulate_footer_code_logs()
            
            # 2. Simulação Injection
            self.results['simulations']['injection'] = self.simulate_injection_logs()
            
            # 3. Simulação Cenários de Erro
            self.results['simulations']['error_scenarios'] = self.simulate_error_scenarios()
            
            # 4. Simulação Concorrente
            self.results['simulations']['concurrent'] = self.simulate_concurrent_logs()
            
            # 5. Simulação Volume Alto
            self.results['simulations']['high_volume'] = self.simulate_high_volume()
            
            # Determinar status geral
            self.determine_overall_status()
            
        except Exception as e:
            self.results['status'] = 'FAILED'
            self.results['error'] = str(e)
            print(f"❌ Erro crítico: {e}")
        
        self.results['duration'] = (datetime.now() - self.results['start_time']).total_seconds()
        return self.results
    
    def simulate_footer_code_logs(self):
        """Simula logs do Footer Code"""
        print("  📄 Simulando logs do Footer Code...")
        start_time = time.time()
        
        session_id = f"footer_test_{int(time.time())}"
        logs = [
            {
                'level': 'INFO',
                'message': 'Footer Code Site Definitivo.js carregado',
                'data': {
                    'timestamp': datetime.now().isoformat(),
                    'domReady': 'complete',
                    'url': 'https://www.segurosimediato.com.br'
                }
            },
            {
                'level': 'INFO',
                'message': 'Configuração RPA definida',
                'data': {
                    'rpaEnabled': True,
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'level': 'DEBUG',
                'message': 'Botão CALCULE AGORA! clicado',
                'data': {
                    'target': 'submit_button_auto',
                    'currentTarget': 'submit_button_auto',
                    'timestamp': datetime.now().isoformat()
                }
            },
            {
                'level': 'DEBUG',
                'message': 'Formulário encontrado via botão',
                'data': {
                    'formFound': True,
                    'formId': 'rpa-form'
                }
            },
            {
                'level': 'DEBUG',
                'message': 'Submit do formulário interceptado',
                'data': {
                    'validatedOk': False,
                    'skipValidate': False,
                    'formId': 'rpa-form'
                }
            },
            {
                'level': 'DEBUG',
                'message': 'Iniciando validação de dados',
                'data': {}
            },
            {
                'level': 'DEBUG',
                'message': 'Resultados das validações recebidos',
                'data': {
                    'cpf': {'ok': True, 'reason': 'Válido'},
                    'cep': {'ok': True, 'reason': 'Válido'},
                    'placa': {'ok': True, 'reason': 'Válido'},
                    'telefone': {'ok': True, 'reason': 'Válido'},
                    'email': {'ok': True, 'reason': 'Válido'}
                }
            },
            {
                'level': 'INFO',
                'message': 'Dados válidos - verificando RPA',
                'data': {
                    'rpaEnabled': True,
                    'rpaEnabledType': 'boolean',
                    'strictComparison': True
                }
            },
            {
                'level': 'INFO',
                'message': 'RPA habilitado - iniciando processo RPA',
                'data': {
                    'loadRPAScriptExists': 'function',
                    'loadRPAScriptType': 'function'
                }
            },
            {
                'level': 'INFO',
                'message': 'Script RPA carregado - verificando classes',
                'data': {
                    'MainPageExists': 'function',
                    'MainPageType': 'function',
                    'handleFormSubmitExists': 'function',
                    'handleFormSubmitType': 'function'
                }
            }
        ]
        
        return self.send_logs(session_id, logs, 'Footer Code')
    
    def simulate_injection_logs(self):
        """Simula logs do Injection"""
        print("  💉 Simulando logs do Injection...")
        start_time = time.time()
        
        session_id = f"injection_test_{int(time.time())}"
        logs = [
            {
                'level': 'INFO',
                'message': 'Webflow Injection Limpo carregado',
                'data': {
                    'timestamp': datetime.now().isoformat(),
                    'MainPageWillBeDefined': 'undefined',
                    'MainPageValue': None
                }
            },
            {
                'level': 'DEBUG',
                'message': 'MainPage constructor chamado',
                'data': {
                    'timestamp': datetime.now().isoformat(),
                    'sessionId': session_id
                }
            },
            {
                'level': 'DEBUG',
                'message': 'MainPage inicializada',
                'data': {
                    'sessionId': session_id,
                    'modalProgress': None
                }
            },
            {
                'level': 'INFO',
                'message': 'handleFormSubmit chamado',
                'data': {
                    'form': 'FORM',
                    'formId': 'rpa-form',
                    'formType': 'object',
                    'formInstance': True
                }
            },
            {
                'level': 'INFO',
                'message': 'Iniciando processo RPA',
                'data': {}
            },
            {
                'level': 'DEBUG',
                'message': 'Dados coletados',
                'data': {
                    'cpf': '12345678901',
                    'cep': '01234567',
                    'placa': 'ABC1234',
                    'telefone': '11999999999',
                    'email': 'teste@teste.com'
                }
            },
            {
                'level': 'INFO',
                'message': 'API RPA chamada',
                'data': {
                    'sessionId': session_id,
                    'endpoint': 'https://rpaimediatoseguros.com.br/api/rpa/start'
                }
            },
            {
                'level': 'DEBUG',
                'message': 'Expondo classes globalmente',
                'data': {
                    'MainPage': 'function',
                    'ProgressModalRPA': 'function',
                    'SpinnerTimer': 'function'
                }
            },
            {
                'level': 'INFO',
                'message': 'Classes expostas globalmente',
                'data': {
                    'windowMainPage': 'function',
                    'windowProgressModalRPA': 'function',
                    'windowSpinnerTimer': 'function'
                }
            }
        ]
        
        return self.send_logs(session_id, logs, 'Injection')
    
    def simulate_error_scenarios(self):
        """Simula cenários de erro"""
        print("  ❌ Simulando cenários de erro...")
        start_time = time.time()
        
        error_scenarios = [
            {
                'name': 'RPA Desabilitado',
                'session_id': f"error_rpa_disabled_{int(time.time())}",
                'logs': [
                    {
                        'level': 'INFO',
                        'message': 'Dados válidos - verificando RPA',
                        'data': {'rpaEnabled': False}
                    },
                    {
                        'level': 'INFO',
                        'message': 'RPA desabilitado - processando apenas com Webflow',
                        'data': {}
                    }
                ]
            },
            {
                'name': 'Script RPA Não Carregado',
                'session_id': f"error_script_not_loaded_{int(time.time())}",
                'logs': [
                    {
                        'level': 'ERROR',
                        'message': 'Erro ao carregar script RPA',
                        'data': {
                            'error': 'Failed to load webflow_injection_limpo.js',
                            'stack': 'Error: Network request failed',
                            'name': 'NetworkError'
                        }
                    },
                    {
                        'level': 'INFO',
                        'message': 'Fallback para processamento Webflow',
                        'data': {}
                    }
                ]
            },
            {
                'name': 'Classe MainPage Não Encontrada',
                'session_id': f"error_mainpage_not_found_{int(time.time())}",
                'logs': [
                    {
                        'level': 'ERROR',
                        'message': 'window.MainPage não definido',
                        'data': {}
                    },
                    {
                        'level': 'INFO',
                        'message': 'Fallback para processamento Webflow',
                        'data': {}
                    }
                ]
            }
        ]
        
        results = []
        for scenario in error_scenarios:
            result = self.send_logs(
                scenario['session_id'], 
                scenario['logs'], 
                f"Erro: {scenario['name']}"
            )
            results.append(result)
        
        duration = time.time() - start_time
        return {
            'status': 'PASSED' if all(r.get('status') == 'PASSED' for r in results) else 'FAILED',
            'duration': duration,
            'scenarios': results,
            'message': f'Executados {len(scenarios)} cenários de erro'
        }
    
    def simulate_concurrent_logs(self):
        """Simula logs concorrentes"""
        print("  🔄 Simulando logs concorrentes...")
        start_time = time.time()
        
        concurrent_users = self.config['test_data']['concurrent_users']
        
        def send_concurrent_logs(user_id):
            session_id = f"concurrent_user_{user_id}_{int(time.time())}"
            logs = [
                {
                    'level': 'INFO',
                    'message': f'Usuário {user_id} - Footer Code carregado',
                    'data': {'user_id': user_id}
                },
                {
                    'level': 'DEBUG',
                    'message': f'Usuário {user_id} - Botão clicado',
                    'data': {'user_id': user_id}
                },
                {
                    'level': 'INFO',
                    'message': f'Usuário {user_id} - RPA executado',
                    'data': {'user_id': user_id}
                }
            ]
            return self.send_logs(session_id, logs, f"Usuário Concorrente {user_id}")
        
        # Executar logs concorrentes
        results = []
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(send_concurrent_logs, i) for i in range(concurrent_users)]
            for future in as_completed(futures):
                results.append(future.result())
        
        duration = time.time() - start_time
        return {
            'status': 'PASSED' if all(r.get('status') == 'PASSED' for r in results) else 'FAILED',
            'duration': duration,
            'concurrent_users': concurrent_users,
            'results': results,
            'message': f'Executados logs para {concurrent_users} usuários concorrentes'
        }
    
    def simulate_high_volume(self):
        """Simula volume alto de logs"""
        print("  📊 Simulando volume alto...")
        start_time = time.time()
        
        logs_per_session = self.config['test_data']['logs_per_session']
        session_id = f"high_volume_{int(time.time())}"
        
        # Gerar logs com volume alto
        logs = []
        for i in range(logs_per_session):
            logs.append({
                'level': random.choice(['DEBUG', 'INFO', 'WARNING']),
                'message': f'Log de volume alto #{i+1}',
                'data': {
                    'log_number': i+1,
                    'timestamp': datetime.now().isoformat(),
                    'random_data': f'data_{random.randint(1000, 9999)}'
                }
            })
        
        return self.send_logs(session_id, logs, 'Volume Alto')
    
    def send_logs(self, session_id, logs, simulation_name):
        """Envia logs para o servidor"""
        start_time = time.time()
        successful_logs = 0
        failed_logs = 0
        errors = []
        
        for log in logs:
            try:
                # Adicionar informações padrão
                log_data = {
                    'level': log['level'],
                    'message': log['message'],
                    'data': log.get('data', {}),
                    'url': 'https://www.segurosimediato.com.br',
                    'sessionId': session_id,
                    'timestamp': datetime.now().isoformat(),
                    'userAgent': 'Test Simulator/1.0'
                }
                
                response = requests.post(
                    self.base_url,
                    json=log_data,
                    timeout=self.config['server']['timeout'],
                    headers={'Content-Type': 'application/json'}
                )
                
                if response.status_code == 200:
                    successful_logs += 1
                else:
                    failed_logs += 1
                    errors.append(f'HTTP {response.status_code}: {response.text}')
                
                # Pequena pausa entre logs para simular comportamento real
                time.sleep(0.1)
                
            except Exception as e:
                failed_logs += 1
                errors.append(str(e))
        
        duration = time.time() - start_time
        
        return {
            'status': 'PASSED' if failed_logs == 0 else 'FAILED',
            'duration': duration,
            'simulation_name': simulation_name,
            'session_id': session_id,
            'total_logs': len(logs),
            'successful_logs': successful_logs,
            'failed_logs': failed_logs,
            'errors': errors,
            'message': f'{simulation_name}: {successful_logs}/{len(logs)} logs enviados com sucesso'
        }
    
    def determine_overall_status(self):
        """Determina status geral baseado nas simulações"""
        simulation_statuses = [sim.get('status', 'UNKNOWN') for sim in self.results['simulations'].values()]
        
        if all(status == 'PASSED' for status in simulation_statuses):
            self.results['status'] = 'PASSED'
        elif any(status == 'FAILED' for status in simulation_statuses):
            self.results['status'] = 'FAILED'
        else:
            self.results['status'] = 'WARNING'
        
        # Contar resultados
        self.results['summary'] = {
            'total_simulations': len(simulation_statuses),
            'passed': sum(1 for s in simulation_statuses if s == 'PASSED'),
            'failed': sum(1 for s in simulation_statuses if s == 'FAILED'),
            'warning': sum(1 for s in simulation_statuses if s == 'WARNING')
        }
