#!/usr/bin/env python3
"""
🧪 TEST RUNNER - SISTEMA DE LOGGING PHP
Executor principal de testes para validação do sistema de logging
"""

import json
import time
import requests
import mysql.connector
from datetime import datetime
from pathlib import Path
import sys
import os

# Adicionar diretório atual ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from connectivity_test import ConnectivityTest
from log_simulator import LogSimulator
from integrity_validator import IntegrityValidator
from performance_test import PerformanceTest
from security_test import SecurityTest
from report_generator import ReportGenerator

class TestRunner:
    def __init__(self):
        """Inicializa o executor de testes"""
        self.config = self.load_config()
        self.results = {
            'start_time': datetime.now(),
            'tests': {},
            'summary': {},
            'errors': []
        }
        
    def load_config(self):
        """Carrega configurações de teste"""
        config_path = Path(__file__).parent / 'config' / 'test_config.json'
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ Arquivo de configuração não encontrado!")
            return self.get_default_config()
    
    def get_default_config(self):
        """Configuração padrão para testes"""
        return {
            "server": {
                "host": "bpsegurosimediato.com.br",
                "port": 8080,
                "protocol": "http",
                "timeout": 30
            },
            "database": {
                "host": "localhost",
                "port": 3306,
                "database": "rpa_logs",
                "username": "rpa_user",
                "password": "RpaLogs2025!"
            },
            "test_data": {
                "sample_sessions": 5,
                "logs_per_session": 10,
                "concurrent_users": 2
            }
        }
    
    def run_all_tests(self):
        """Executa todos os testes do sistema"""
        print("🚀 Iniciando testes do sistema de logging...")
        print(f"📅 Data/Hora: {self.results['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # 1. Teste de Conectividade
            print("\n🔍 1. TESTE DE CONECTIVIDADE")
            self.results['tests']['connectivity'] = self.run_connectivity_test()
            
            # 2. Teste de Funcionalidade (Simulação de Logs)
            print("\n📝 2. TESTE DE FUNCIONALIDADE")
            self.results['tests']['functionality'] = self.run_functionality_test()
            
            # 3. Teste de Integridade
            print("\n🔒 3. TESTE DE INTEGRIDADE")
            self.results['tests']['integrity'] = self.run_integrity_test()
            
            # 4. Teste de Performance
            print("\n⚡ 4. TESTE DE PERFORMANCE")
            self.results['tests']['performance'] = self.run_performance_test()
            
            # 5. Teste de Segurança
            print("\n🛡️ 5. TESTE DE SEGURANÇA")
            self.results['tests']['security'] = self.run_security_test()
            
        except Exception as e:
            self.results['errors'].append(f"Erro durante execução dos testes: {str(e)}")
            print(f"❌ Erro crítico: {e}")
        
        # Gerar resumo e relatório
        self.generate_summary()
        self.generate_report()
        
        return self.results
    
    def run_connectivity_test(self):
        """Executa teste de conectividade"""
        try:
            test = ConnectivityTest(self.config)
            result = test.run_all_tests()
            self.print_test_result("Conectividade", result)
            return result
        except Exception as e:
            error_msg = f"Erro no teste de conectividade: {str(e)}"
            self.results['errors'].append(error_msg)
            return {'status': 'FAILED', 'error': error_msg}
    
    def run_functionality_test(self):
        """Executa teste de funcionalidade"""
        try:
            simulator = LogSimulator(self.config)
            result = simulator.run_all_simulations()
            self.print_test_result("Funcionalidade", result)
            return result
        except Exception as e:
            error_msg = f"Erro no teste de funcionalidade: {str(e)}"
            self.results['errors'].append(error_msg)
            return {'status': 'FAILED', 'error': error_msg}
    
    def run_integrity_test(self):
        """Executa teste de integridade"""
        try:
            validator = IntegrityValidator(self.config)
            result = validator.run_all_checks()
            self.print_test_result("Integridade", result)
            return result
        except Exception as e:
            error_msg = f"Erro no teste de integridade: {str(e)}"
            self.results['errors'].append(error_msg)
            return {'status': 'FAILED', 'error': error_msg}
    
    def run_performance_test(self):
        """Executa teste de performance"""
        try:
            test = PerformanceTest(self.config)
            result = test.run_all_tests()
            self.print_test_result("Performance", result)
            return result
        except Exception as e:
            error_msg = f"Erro no teste de performance: {str(e)}"
            self.results['errors'].append(error_msg)
            return {'status': 'FAILED', 'error': error_msg}
    
    def run_security_test(self):
        """Executa teste de segurança"""
        try:
            test = SecurityTest(self.config)
            result = test.run_all_tests()
            self.print_test_result("Segurança", result)
            return result
        except Exception as e:
            error_msg = f"Erro no teste de segurança: {str(e)}"
            self.results['errors'].append(error_msg)
            return {'status': 'FAILED', 'error': error_msg}
    
    def print_test_result(self, test_name, result):
        """Imprime resultado do teste"""
        status = result.get('status', 'UNKNOWN')
        duration = result.get('duration', 0)
        
        if status == 'PASSED':
            print(f"✅ {test_name}: PASSOU ({duration:.1f}s)")
        elif status == 'FAILED':
            print(f"❌ {test_name}: FALHOU ({duration:.1f}s)")
            if 'error' in result:
                print(f"   Erro: {result['error']}")
        elif status == 'WARNING':
            print(f"⚠️  {test_name}: AVISO ({duration:.1f}s)")
        else:
            print(f"❓ {test_name}: DESCONHECIDO ({duration:.1f}s)")
    
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
        
        # Imprimir resumo
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        print(f"Total de Testes: {total_tests}")
        print(f"✅ Passou: {passed_tests}")
        print(f"❌ Falhou: {failed_tests}")
        print(f"⚠️  Avisos: {warning_tests}")
        print(f"📈 Taxa de Sucesso: {self.results['summary']['success_rate']:.1f}%")
        print(f"⏱️  Duração Total: {self.results['summary']['total_duration']:.1f}s")
        
        if self.results['errors']:
            print(f"\n❌ Erros Encontrados: {len(self.results['errors'])}")
            for error in self.results['errors']:
                print(f"   - {error}")
    
    def generate_report(self):
        """Gera relatório detalhado"""
        try:
            generator = ReportGenerator(self.results)
            report_path = generator.generate_html_report()
            print(f"\n📄 Relatório gerado: {report_path}")
            
            # Também salvar JSON
            json_path = Path(__file__).parent / 'results' / f'test_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
            json_path.parent.mkdir(exist_ok=True)
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2, default=str, ensure_ascii=False)
            print(f"📄 Dados JSON: {json_path}")
            
        except Exception as e:
            print(f"❌ Erro ao gerar relatório: {e}")
    
    def run_specific_test(self, test_name):
        """Executa teste específico"""
        test_methods = {
            'connectivity': self.run_connectivity_test,
            'functionality': self.run_functionality_test,
            'integrity': self.run_integrity_test,
            'performance': self.run_performance_test,
            'security': self.run_security_test
        }
        
        if test_name in test_methods:
            print(f"🔍 Executando teste: {test_name}")
            result = test_methods[test_name]()
            self.results['tests'][test_name] = result
            return result
        else:
            print(f"❌ Teste '{test_name}' não encontrado!")
            return None

def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Test Runner - Sistema de Logging PHP')
    parser.add_argument('--all', action='store_true', help='Executar todos os testes')
    parser.add_argument('--test', type=str, help='Executar teste específico')
    parser.add_argument('--verbose', action='store_true', help='Modo verbose')
    parser.add_argument('--report-only', action='store_true', help='Gerar apenas relatório')
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.report_only:
        # Gerar relatório dos últimos resultados
        results_path = Path(__file__).parent / 'results'
        if results_path.exists():
            latest_json = max(results_path.glob('test_results_*.json'), key=os.path.getctime)
            with open(latest_json, 'r', encoding='utf-8') as f:
                runner.results = json.load(f)
            runner.generate_report()
        else:
            print("❌ Nenhum resultado de teste encontrado!")
    elif args.test:
        # Executar teste específico
        runner.run_specific_test(args.test)
    elif args.all or len(sys.argv) == 1:
        # Executar todos os testes
        runner.run_all_tests()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()


