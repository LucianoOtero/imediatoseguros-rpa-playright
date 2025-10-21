#!/usr/bin/env python3
"""
Conexao Local com Banco de Dados MySQL
Sistema de Logging RPA - Imediato Seguros
Conecta diretamente ao banco sem usar SSH
"""

import mysql.connector
from mysql.connector import Error
import json
from datetime import datetime
import sys

class DatabaseConnector:
    def __init__(self):
        self.connection = None
        self.config = {
            'host': 'bpsegurosimediato.com.br',
            'port': 3306,
            'database': 'rpa_logs',
            'user': 'rpa_user',
            'password': 'RpaLogs2025!',
            'charset': 'utf8mb4',
            'autocommit': True
        }
    
    def connect(self):
        """Conecta ao banco de dados"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                print("OK - Conectado ao banco de dados MySQL")
                return True
        except Error as e:
            print(f"ERRO ao conectar: {e}")
            return False
    
    def disconnect(self):
        """Desconecta do banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Desconectado do banco de dados")
    
    def execute_query(self, query, params=None):
        """Executa uma query e retorna os resultados"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            
            if query.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                return results
            else:
                return cursor.rowcount
                
        except Error as e:
            print(f"ERRO na query: {e}")
            return None
        finally:
            if 'cursor' in locals():
                cursor.close()
    
    def get_recent_logs(self, limit=10):
        """Recupera logs recentes"""
        query = """
        SELECT log_id, timestamp, level, message, session_id, url, data
        FROM debug_logs 
        ORDER BY timestamp DESC 
        LIMIT %s
        """
        return self.execute_query(query, (limit,))
    
    def search_logs_by_message(self, search_term):
        """Busca logs por termo na mensagem"""
        query = """
        SELECT log_id, timestamp, level, message, session_id, url, data
        FROM debug_logs 
        WHERE message LIKE %s
        ORDER BY timestamp DESC
        """
        return self.execute_query(query, (f'%{search_term}%',))
    
    def get_session_logs(self, session_id):
        """Recupera todos os logs de uma sessao"""
        query = """
        SELECT log_id, timestamp, level, message, session_id, url, data
        FROM debug_logs 
        WHERE session_id = %s
        ORDER BY timestamp ASC
        """
        return self.execute_query(query, (session_id,))
    
    def get_session_stats(self):
        """Estatisticas das sessoes"""
        query = """
        SELECT 
            session_id,
            COUNT(*) as log_count,
            MIN(timestamp) as first_log,
            MAX(timestamp) as last_log,
            GROUP_CONCAT(DISTINCT level) as levels
        FROM debug_logs 
        GROUP BY session_id 
        ORDER BY log_count DESC
        """
        return self.execute_query(query)
    
    def get_level_stats(self):
        """Estatisticas por nivel de log"""
        query = """
        SELECT 
            level,
            COUNT(*) as count,
            MIN(timestamp) as first_occurrence,
            MAX(timestamp) as last_occurrence
        FROM debug_logs 
        GROUP BY level 
        ORDER BY count DESC
        """
        return self.execute_query(query)
    
    def get_total_stats(self):
        """Estatisticas gerais"""
        query = """
        SELECT 
            COUNT(*) as total_logs,
            COUNT(DISTINCT session_id) as unique_sessions,
            MIN(timestamp) as oldest_log,
            MAX(timestamp) as newest_log
        FROM debug_logs
        """
        return self.execute_query(query)

def format_log_entry(log):
    """Formata uma entrada de log para exibicao"""
    timestamp = log.get('timestamp', 'N/A')
    level = log.get('level', 'N/A')
    message = log.get('message', 'N/A')
    session_id = log.get('session_id', 'N/A')
    url = log.get('url', 'N/A')
    
    return f"[{level}] {timestamp} | {session_id} | {message} | {url}"

def display_logs(logs, title="LOGS"):
    """Exibe logs formatados"""
    if not logs:
        print(f"ERRO - {title}: Nenhum log encontrado")
        return
    
    print(f"\n{title} ({len(logs)} entradas):")
    print("=" * 80)
    
    for i, log in enumerate(logs, 1):
        print(f"{i:3d}. {format_log_entry(log)}")
        
        # Mostrar dados se existirem
        if log.get('data'):
            try:
                data = json.loads(log['data']) if isinstance(log['data'], str) else log['data']
                if data:
                    print(f"     Dados: {json.dumps(data, indent=6, ensure_ascii=False)}")
            except:
                print(f"     Dados: {log['data']}")

def main():
    print("CONEXAO LOCAL COM BANCO DE DADOS MYSQL")
    print("=" * 50)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Conectar ao banco
    db = DatabaseConnector()
    if not db.connect():
        return
    
    try:
        # Estatisticas gerais
        print("\nESTATISTICAS GERAIS:")
        print("-" * 30)
        stats = db.get_total_stats()
        if stats:
            stat = stats[0]
            print(f"Total de logs: {stat['total_logs']}")
            print(f"Sessoes unicas: {stat['unique_sessions']}")
            print(f"Log mais antigo: {stat['oldest_log']}")
            print(f"Log mais recente: {stat['newest_log']}")
        
        # Estatisticas por nivel
        print("\nESTATISTICAS POR NIVEL:")
        print("-" * 30)
        level_stats = db.get_level_stats()
        if level_stats:
            for stat in level_stats:
                print(f"{stat['level']}: {stat['count']} logs")
        
        # Logs recentes
        print("\nLOGS RECENTES:")
        recent_logs = db.get_recent_logs(10)
        display_logs(recent_logs, "LOGS RECENTES")
        
        # Buscar log especifico do Footer Code
        print("\nBUSCANDO LOG DO FOOTER CODE:")
        footer_logs = db.search_logs_by_message("RPA habilitado")
        display_logs(footer_logs, "LOGS DO FOOTER CODE")
        
        # Estatisticas das sessoes
        print("\nESTATISTICAS DAS SESSOES:")
        print("-" * 30)
        session_stats = db.get_session_stats()
        if session_stats:
            for stat in session_stats[:5]:  # Top 5 sessoes
                print(f"{stat['session_id']}: {stat['log_count']} logs | {stat['levels']}")
        
    except Exception as e:
        print(f"ERRO durante execucao: {e}")
    
    finally:
        db.disconnect()

if __name__ == "__main__":
    main()