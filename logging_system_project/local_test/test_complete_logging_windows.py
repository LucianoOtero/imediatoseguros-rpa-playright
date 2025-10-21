#!/usr/bin/env python3
"""
Teste Completo do Sistema de Logging - Versão Windows
Simula logs do Footer Code e Injection para validar o sistema
"""

import requests
import time
import json
from datetime import datetime
import random

def send_log(api_url, log_data):
    """Envia log para a API"""
    try:
        response = requests.post(
            api_url,
            json=log_data,
            timeout=10,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"OK Log enviado: {log_data['level']} - {log_data['message'][:50]}...")
            return True, result
        else:
            print(f"ERRO {response.status_code}: {response.text}")
            return False, None
            
    except Exception as e:
        print(f"ERRO na requisicao: {e}")
        return False, None

def simulate_footer_code_logs():
    """Simula logs do Footer Code"""
    print("\n=== SIMULANDO FOOTER CODE ===")
    
    logs = [
        {
            'message': 'Footer Code carregado - Iniciando monitoramento do formulario',
            'level': 'INFO',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'data': {'component': 'footer_code', 'version': '1.0.0'}
        },
        {
            'message': 'Formulario detectado - ID: #form-cotacao',
            'level': 'DEBUG',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'form_id': 'form-cotacao', 'form_elements': 15}
        },
        {
            'message': 'Event listener adicionado ao submit',
            'level': 'INFO',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'event': 'submit', 'preventDefault': True}
        },
        {
            'message': 'Validacao de campos iniciada',
            'level': 'DEBUG',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'fields_validated': ['nome', 'email', 'telefone', 'ddd']}
        },
        {
            'message': 'Campos validados com sucesso',
            'level': 'INFO',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'validation_result': 'success', 'errors': []}
        },
        {
            'message': 'Iniciando carregamento do Injection Script',
            'level': 'INFO',
            'sessionId': 'footer_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'injection_url': 'https://mdmidia.com.br/webflow_injection_limpo.js'}
        }
    ]
    
    api_url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    for log in logs:
        log['timestamp'] = datetime.now().isoformat()
        success, result = send_log(api_url, log)
        if not success:
            return False
        time.sleep(0.5)  # Pequeno delay entre logs
    
    return True

def simulate_injection_logs():
    """Simula logs do Injection Script"""
    print("\n=== SIMULANDO INJECTION SCRIPT ===")
    
    logs = [
        {
            'message': 'Injection Script carregado - Iniciando processo RPA',
            'level': 'INFO',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'data': {'component': 'injection', 'version': '1.0.0', 'rpa_enabled': True}
        },
        {
            'message': 'Modal de progresso criado',
            'level': 'DEBUG',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'modal_id': 'rpa-progress-modal', 'spinner_active': True}
        },
        {
            'message': 'Dados do formulario coletados',
            'level': 'INFO',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {
                'form_data': {
                    'nome': 'Joao Silva',
                    'email': 'joao@email.com',
                    'telefone': '99999-9999',
                    'ddd': '11'
                }
            }
        },
        {
            'message': 'Chamada para API RPA iniciada',
            'level': 'INFO',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'api_url': 'https://rpaimediatoseguros.com.br/api/rpa/start', 'method': 'POST'}
        },
        {
            'message': 'ERRO: Falha na chamada da API RPA',
            'level': 'ERROR',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {
                'error': 'Network Error',
                'status_code': 0,
                'response': 'Failed to fetch'
            }
        },
        {
            'message': 'Tentativa de fallback - Redirecionamento manual',
            'level': 'WARNING',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'fallback_method': 'window.location.href', 'target_url': 'https://www.segurosimediato.com.br/sucesso'}
        },
        {
            'message': 'Processo RPA finalizado com erro',
            'level': 'ERROR',
            'sessionId': 'injection_session_001',
            'url': 'https://www.segurosimediato.com.br',
            'data': {'final_status': 'failed', 'error_count': 1, 'success': False}
        }
    ]
    
    api_url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    for log in logs:
        log['timestamp'] = datetime.now().isoformat()
        success, result = send_log(api_url, log)
        if not success:
            return False
        time.sleep(0.5)  # Pequeno delay entre logs
    
    return True

def simulate_multiple_sessions():
    """Simula múltiplas sessões simultâneas"""
    print("\n=== SIMULANDO MULTIPLAS SESSOES ===")
    
    sessions = ['session_001', 'session_002', 'session_003']
    api_url = 'https://bpsegurosimediato.com.br/logging_system/debug_logger_db.php'
    
    for session in sessions:
        log = {
            'message': f'Usuario iniciou cotacao - Sessao {session}',
            'level': 'INFO',
            'sessionId': session,
            'url': 'https://www.segurosimediato.com.br',
            'timestamp': datetime.now().isoformat(),
            'data': {'user_session': session, 'timestamp': datetime.now().isoformat()}
        }
        
        success, result = send_log(api_url, log)
        if not success:
            return False
        time.sleep(0.2)
    
    return True

def check_logs_on_server():
    """Verifica logs no servidor"""
    print("\n=== VERIFICANDO LOGS NO SERVIDOR ===")
    
    try:
        # Usar SSH para verificar logs
        import subprocess
        
        # Verificar logs no banco de dados do Hetzner
        result = subprocess.run([
            'ssh', 'root@bpsegurosimediato.com.br', 
            'mysql -u rpa_user -pRpaLogs2025! -e "USE rpa_logs; SELECT COUNT(*) as total_logs FROM debug_logs; SELECT log_id, timestamp, level, message FROM debug_logs ORDER BY timestamp DESC LIMIT 5;"'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("OK Logs verificados no servidor:")
            print(result.stdout)
            return True
        else:
            print(f"ERRO ao verificar logs: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"ERRO ao verificar logs: {e}")
        return False

def main():
    """Função principal"""
    print("=" * 60)
    print("TESTE COMPLETO DO SISTEMA DE LOGGING")
    print("=" * 60)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success_count = 0
    total_tests = 4
    
    # Teste 1: Footer Code
    if simulate_footer_code_logs():
        success_count += 1
        print("OK Footer Code: SUCESSO")
    else:
        print("ERRO Footer Code: FALHOU")
    
    # Teste 2: Injection Script
    if simulate_injection_logs():
        success_count += 1
        print("OK Injection Script: SUCESSO")
    else:
        print("ERRO Injection Script: FALHOU")
    
    # Teste 3: Múltiplas Sessões
    if simulate_multiple_sessions():
        success_count += 1
        print("OK Multiplas Sessoes: SUCESSO")
    else:
        print("ERRO Multiplas Sessoes: FALHOU")
    
    # Teste 4: Verificar Logs no Servidor
    if check_logs_on_server():
        success_count += 1
        print("OK Verificacao de Logs: SUCESSO")
    else:
        print("ERRO Verificacao de Logs: FALHOU")
    
    # Resumo
    print("\n" + "=" * 60)
    print("RESUMO DOS TESTES")
    print("=" * 60)
    print(f"Testes Executados: {total_tests}")
    print(f"Sucessos: {success_count}")
    print(f"Falhas: {total_tests - success_count}")
    print(f"Taxa de Sucesso: {(success_count/total_tests)*100:.1f}%")
    
    if success_count == total_tests:
        print("\nTODOS OS TESTES PASSARAM!")
        print("Sistema de logging esta funcionando perfeitamente!")
    else:
        print(f"\n{total_tests - success_count} teste(s) falharam")
        print("Verifique os erros acima para correcao")
    
    print("=" * 60)

if __name__ == "__main__":
    main()


