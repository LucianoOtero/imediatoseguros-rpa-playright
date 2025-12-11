#!/usr/bin/env python3
"""
Sistema Local de Recuperacao de Logs
Sistema de Logging RPA - Imediato Seguros
Recupera logs do banco de dados usando sessao especifica ou ultima sessao
"""

import requests
import json
import sys
from datetime import datetime
import argparse

class LogRecoverySystem:
    def __init__(self, server_url="https://bpsegurosimediato.com.br"):
        self.server_url = server_url
        self.api_base = f"{server_url}/logging_system"
        
    def get_latest_session(self):
        """Recupera a ultima sessao do banco de dados"""
        try:
            url = f"{self.api_base}/viewer/api/analytics.php?action=stats"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    # Buscar logs recentes para encontrar ultima sessao
                    logs_url = f"{self.api_base}/viewer/api/analytics.php?action=logs&limit=50"
                    logs_response = requests.get(logs_url, timeout=10)
                    
                    if logs_response.status_code == 200:
                        logs_data = logs_response.json()
                        if logs_data.get('success') and logs_data.get('logs'):
                            # Pegar a sessao do log mais recente
                            latest_log = logs_data['logs'][0]
                            return latest_log.get('session_id')
            
            return None
            
        except Exception as e:
            print(f"ERRO ao recuperar ultima sessao: {e}")
            return None
    
    def get_session_logs(self, session_id):
        """Recupera todos os logs de uma sessao especifica"""
        try:
            url = f"{self.api_base}/viewer/api/analytics.php?action=sessions&session_id={session_id}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    return data.get('logs', [])
                else:
                    print(f"ERRO na API: {data.get('error', 'Erro desconhecido')}")
                    return []
            else:
                print(f"ERRO HTTP: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"ERRO ao recuperar logs da sessao: {e}")
            return []
    
    def format_log_entry(self, log):
        """Formata uma entrada de log para exibicao"""
        timestamp = log.get('timestamp', 'N/A')
        level = log.get('level', 'N/A')
        message = log.get('message', 'N/A')
        url = log.get('url', 'N/A')
        
        return f"[{level}] {timestamp} | {message} | {url}"
    
    def display_session_summary(self, session_id, logs):
        """Exibe resumo da sessao"""
        print(f"\nRESUMO DA SESSAO: {session_id}")
        print("=" * 60)
        
        if not logs:
            print("Nenhum log encontrado para esta sessao")
            return
        
        # Contar por nivel
        level_counts = {}
        for log in logs:
            level = log.get('level', 'UNKNOWN')
            level_counts[level] = level_counts.get(level, 0) + 1
        
        print(f"Total de logs: {len(logs)}")
        print("Distribuicao por nivel:")
        for level, count in level_counts.items():
            print(f"   {level}: {count}")
        
        # Timestamp do primeiro e ultimo log
        if logs:
            first_log = logs[0]
            last_log = logs[-1]
            print(f"Primeiro log: {first_log.get('timestamp', 'N/A')}")
            print(f"Ultimo log: {last_log.get('timestamp', 'N/A')}")
    
    def display_logs(self, logs, show_data=False):
        """Exibe os logs formatados"""
        if not logs:
            print("Nenhum log para exibir")
            return
        
        print(f"\nLOGS DA SESSAO ({len(logs)} entradas):")
        print("=" * 80)
        
        for i, log in enumerate(logs, 1):
            print(f"{i:3d}. {self.format_log_entry(log)}")
            
            if show_data and log.get('data'):
                try:
                    data = json.loads(log['data']) if isinstance(log['data'], str) else log['data']
                    if data:
                        print(f"     Dados: {json.dumps(data, indent=6, ensure_ascii=False)}")
                except:
                    print(f"     Dados: {log['data']}")
    
    def export_logs(self, logs, filename=None):
        """Exporta logs para arquivo JSON"""
        if not logs:
            print("Nenhum log para exportar")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"logs_session_{timestamp}.json"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
            print(f"Logs exportados para: {filename}")
        except Exception as e:
            print(f"Erro ao exportar logs: {e}")
    
    def analyze_session(self, session_id):
        """Analisa uma sessao completa"""
        print(f"ANALISANDO SESSAO: {session_id}")
        print("=" * 60)
        
        logs = self.get_session_logs(session_id)
        
        if not logs:
            print("Sessao nao encontrada ou sem logs")
            return
        
        # Exibir resumo
        self.display_session_summary(session_id, logs)
        
        # Exibir logs
        self.display_logs(logs, show_data=True)
        
        # Exportar logs
        self.export_logs(logs)
        
        return logs

def main():
    parser = argparse.ArgumentParser(description='Sistema de Recuperacao de Logs RPA')
    parser.add_argument('--session', '-s', help='ID da sessao especifica')
    parser.add_argument('--latest', '-l', action='store_true', help='Usar ultima sessao')
    parser.add_argument('--server', help='URL do servidor (padrao: https://bpsegurosimediato.com.br)')
    parser.add_argument('--export', '-e', help='Arquivo para exportar logs')
    
    args = parser.parse_args()
    
    # Inicializar sistema
    server_url = args.server or "https://bpsegurosimediato.com.br"
    recovery_system = LogRecoverySystem(server_url)
    
    print("SISTEMA DE RECUPERACAO DE LOGS RPA")
    print("=" * 50)
    print(f"Servidor: {server_url}")
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Determinar sessao
    session_id = None
    
    if args.session:
        session_id = args.session
        print(f"Sessao especificada: {session_id}")
    elif args.latest:
        print("Buscando ultima sessao...")
        session_id = recovery_system.get_latest_session()
        if session_id:
            print(f"Ultima sessao encontrada: {session_id}")
        else:
            print("Nenhuma sessao encontrada")
            return
    else:
        # Modo interativo
        print("Buscando ultima sessao...")
        session_id = recovery_system.get_latest_session()
        if session_id:
            print(f"Ultima sessao encontrada: {session_id}")
            print("Use --latest para sempre usar a ultima sessao")
        else:
            print("Nenhuma sessao encontrada")
            print("Use --session <id> para especificar uma sessao")
            return
    
    # Analisar sessao
    logs = recovery_system.analyze_session(session_id)
    
    if logs and args.export:
        recovery_system.export_logs(logs, args.export)

if __name__ == "__main__":
    main()